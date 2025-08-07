from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client, Client
from typing import List, Tuple

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Chat functions
def insert_turn(user_id: str, user_text: str, ai_text: str) -> None:
    supabase.table("user_conversations").insert({
        "user_id": user_id,
        "user_text": user_text,
        "ai_text": ai_text
    }).execute()

def fetch_last_n_turns(user_id: str, n: int = 5) -> List[Tuple[str, str]]:
    """Returns [(user_text, ai_text), ...] newest first, max `n` pairs."""
    resp = (
        supabase.table("user_conversations")
        .select("user_text, ai_text")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(n)
        .execute()
    )
    data = resp.data or []
    return [(row["user_text"], row["ai_text"]) for row in reversed(data)]
