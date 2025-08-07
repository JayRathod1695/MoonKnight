from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..Auth.crud import signup, login, refresh

class AuthRequest(BaseModel):
    email: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
def signup_user(req: AuthRequest):
    """Creates a new user with email and password"""
    try:
        resp = signup(req.email, req.password)
        if hasattr(resp, 'error') and resp.error:
            raise HTTPException(status_code=400, detail=resp.error.message)
        return {"message": "User created successfully", "data": resp.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login_user(req: AuthRequest):
    """Authenticates user and returns session tokens"""
    try:
        resp = login(req.email, req.password)
        if hasattr(resp, 'error') and resp.error:
            raise HTTPException(status_code=401, detail=resp.error.message)
        return {"message": "Login successful", "data": resp}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/refresh")
def refresh_token(req: RefreshRequest):
    """Refreshes access and refresh tokens"""
    try:
        resp = refresh(req.refresh_token)
        if hasattr(resp, 'error') and resp.error:
            raise HTTPException(status_code=400, detail=resp.error.message)
        return {"message": "Token refreshed", "data": resp}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
