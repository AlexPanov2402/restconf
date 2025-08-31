from fastapi import APIRouter, Body, HTTPException

from app.rpc_handler import Rpc_Handler
from app.yang_manager import YangManager

router = APIRouter()

yang_manager = YangManager()
yang_manager.load_model()
rpc_handler = Rpc_Handler()


@router.get("/data/{path:path}")
async def get_data(path: str = ""):
    try:
        return yang_manager.get_data(path)
    except KeyError:
        raise HTTPException(status_code=404, detail="Path not found")


@router.patch("/data/{path:path}")
async def patch_data(path: str, body: dict = Body(...)):
    try:
        return yang_manager.patch_data(path, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/operations/{rpc_name}")
async def call_rpc(rpc_name: str, body: dict = Body(...)):
    if not hasattr(rpc_handler, rpc_name):
        raise HTTPException(status_code=404, detail=f"RPC {rpc_name} not found")
    method = getattr(rpc_handler, rpc_name)
    return method(body)
