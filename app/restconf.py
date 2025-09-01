from fastapi import APIRouter, Body, HTTPException

from app.rpc_handler import Rpc_Handler
from app.yang_manager import YangManager

# Маршрутизатор для работы с RESTCONF API
router = APIRouter()

# Инициализация менеджера YANG и загрузка модели
yang_manager = YangManager()
yang_manager.load_model()

# Обработчик RPC
rpc_handler = Rpc_Handler()


@router.get("/data/{path:path}")
async def get_data(path: str = ""):
    """
    Получение данных из хранилища по указанному пути.

    :param path: Путь в формате строки (например, "jukebox/library").
    :return: данные в формате json.
    :raises HTTPException: если путь не найден, возвращаем ошибку 404.
    """
    try:
        return yang_manager.get_data(path)
    except KeyError:
        raise HTTPException(status_code=404, detail="Path not found")


@router.patch("/data/{path:path}")
async def patch_data(path: str, body: dict = Body(...)):
    """
    Обновление данных по указанному пути.

    :param path: Путь для обновления данных (например, "jukebox/library").
    :param body: Данные для обновления в формате json.
    :return: Обновлённые данные.
    :raises HTTPException: если данные не проходят валидацию, возвращаем ошибку 400.
    """
    try:
        return yang_manager.patch_data(path, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/operations/{rpc_name}")
async def call_rpc(rpc_name: str, body: dict = Body(...)):
    """
    Вызов удалённой процедуры (RPC) по имени.

    :param rpc_name: Имя RPC-процедуры, которую нужно вызвать.
    :param body: Параметры для вызова RPC в формате json.
    :return: Результат выполнения RPC.
    :raises HTTPException: если RPC не существует, возвращаем ошибку 404.
    """
    if not hasattr(rpc_handler, rpc_name):
        raise HTTPException(status_code=404, detail=f"RPC {rpc_name} not found")

    method = getattr(rpc_handler, rpc_name)
    return method(body)
