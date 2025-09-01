import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from app.restconf import router as restconf_router

# Грузим переменные окружения из .env
load_dotenv()

# Экземпляр FastAPI приложения
app = FastAPI(title="RESTCONF Server")

# Маршруты для RESTCONF API
app.include_router(restconf_router, prefix="/restconf")


if __name__ == "__main__":
    """
    Запуск сервера FastAPI с использованием Uvicorn.

    Переменные окружения:
        - HOST: хост для сервера (по умолчанию 0.0.0.0)
        - PORT: порт для сервера (по умолчанию 8000)
    """

    # Настройки хоста и порта из переменных окружения
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    # Запуск Uvicorn сервера с заданными параметрами
    uvicorn.run("app.server:app", host=host, port=port, reload=True)
