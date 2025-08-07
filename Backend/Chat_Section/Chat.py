from typing import Iterator, Optional
from langchain.chat_models import init_chat_model
from langchain.schema import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from ..supabase_client import insert_turn, fetch_last_n_turns
from ..Usage.monitor import log_usage
import uuid


class OllamaSupabaseChat:
    """
    Same streaming behaviour as before, but:
      - persists every (user, AI) turn to Supabase
      - pre-loads the last 5 turns for the given user_id at start
    """

    def __init__(
        self,
        model: str,
        user_id: str,
        base_url: str = "http://localhost:11434",
        system_prompt: Optional[str] = None,
        history_size: int = 5,
    ):
        self.llm = init_chat_model(
            model,
            model_provider="ollama",
            base_url=base_url,
            streaming=True,
        )
        self.user_id = user_id
        self.model = model
        self.history_size = history_size

        # Supabase gives us (user_text, ai_text) pairs -> convert to LangChain messages
        self.history_messages = self._load_history()

        _system = system_prompt or "You are a helpful AI assistant."
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", _system),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )
        self.chain = self.prompt | self.llm

    # ------------- internal helpers -------------
    def _load_history(self) -> list:
        turns = fetch_last_n_turns(self.user_id, self.history_size)
        messages = []
        for user_txt, ai_txt in turns:
            messages.append(HumanMessage(content=user_txt))
            messages.append(AIMessage(content=ai_txt))
        return messages

    def _save_turn(self, user_txt: str, ai_txt: str) -> None:
        insert_turn(self.user_id, user_txt, ai_txt)

    # ------------- public API -------------
    def stream(self, user_input: str) -> Iterator[str]:
        """
        Streams response, stores turn, and updates local history.
        """
        inputs = {"history": self.history_messages, "input": user_input}

        reply_chunks = []
        for chunk in self.chain.stream(inputs):
            reply_chunks.append(chunk.content)
            yield chunk.content

        reply = "".join(reply_chunks)

        # --- persist & keep local history in sync ---
        self._save_turn(user_input, reply)
        self.history_messages.append(HumanMessage(content=user_input))
        self.history_messages.append(AIMessage(content=reply))

        # Trim local history to history_size * 2 (pairs of messages)
        keep = self.history_size * 2
        self.history_messages = self.history_messages[-keep:]

        # monitor usage
        tokens = len(reply.split())
        cost = tokens * 0.0001
        log_usage(self.user_id, self.model, tokens, cost)

    # blocking wrapper if you need it
    def invoke(self, user_input: str) -> str:
        return "".join(self.stream(user_input))


if __name__ == "__main__":
    import os, uuid

    # For demo purposes we use a random user id; in real app fetch from auth.
    DEMO_USER_ID = str(uuid.uuid4())

    chat = OllamaSupabaseChat("llama3", user_id=DEMO_USER_ID)

    while True:
        try:
            q = input("\nYou: ")
            if q.lower() in {"quit", "exit"}:
                break
            print("AI: ", end="")
            for tok in chat.stream(q):
                print(tok, end="", flush=True)
        except KeyboardInterrupt:
            break