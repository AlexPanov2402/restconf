from fastapi import APIRouter

router = APIRouter()


@router.get("/data/{path:path}")
async def get_data(path: str = ""):
    # TODO: достаём данные из yang_manager
    return {"message": f"GET data for path: {path}"}


@router.patch("/data/{path:path}")
async def patch_data(path: str, body: dict):
    # TODO: применяем изменения в datastore
    return {"message": f"PATCH data at path: {path}", "data": body}


@router.post("/operations/{rpc_name}")
async def call_rpc(rpc_name: str, body: dict):
    # TODO: вызвать метод из rpc_handler
    return {"rpc": rpc_name, "input": body, "output": {"status": "ok"}}
