from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..Chat_Section.Chat import OllamaSupabaseChat

class ChatRequest(BaseModel):
    user_id: str
    user_input: str
    model: str = "llama3"

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/stream")
def stream_chat(req: ChatRequest):
    """Streams chat response for given user and input"""
    try:
        chat = OllamaSupabaseChat(req.model, user_id=req.user_id)
        response = chat.invoke(req.user_input)
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
