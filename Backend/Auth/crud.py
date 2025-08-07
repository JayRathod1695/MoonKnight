from ..supabase_client import supabase


def signup(email: str, password: str):
    return supabase.auth.sign_up({"email": email, "password": password})


def login(email: str, password: str):
    return supabase.auth.sign_in_with_password({"email": email, "password": password})


def refresh(token: str):
    return supabase.auth.refresh_session({"refresh_token": token})
