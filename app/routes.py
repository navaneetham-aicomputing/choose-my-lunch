from fastapi import APIRouter

from app.data_layer.schemas import BaseResponse

rt = APIRouter()


@rt.post("/ping", response_model=BaseResponse, tags=["Ping"])
async def ping(msg: str):
    return {"success": True, "message": msg}
