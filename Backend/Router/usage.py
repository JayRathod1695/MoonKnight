from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..Usage.monitor import log_usage
from ..DataBase.Usage_Database.CRUD_Usage import fetch_usage

class LogUsageRequest(BaseModel):
    user_id: str
    model: str
    tokens: int
    cost: float

router = APIRouter(prefix="/usage", tags=["usage"])

@router.post("/log")
def log_usage_endpoint(req: LogUsageRequest):
    """Logs usage data into usage_logs table"""
    try:
        log_usage(req.user_id, req.model, req.tokens, req.cost)
        return {"status": "success", "message": "Usage logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
def get_usage(user_id: str):
    """Fetches usage logs for a user"""
    try:
        data = fetch_usage(user_id)
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
