from ...supabase_client import supabase
from typing import Dict

def insert_usage(user_id: str, model: str, tokens: int, cost: float):
    supabase.table("usage_logs").insert({
        "user_id": user_id,
        "model": model,
        "tokens": tokens,
        "cost": cost,
    }).execute()

def fetch_usage(user_id: str):
    resp = supabase.table("usage_logs").select("model, tokens, cost, created_at").eq("user_id", user_id).execute()
    return resp.data or []
