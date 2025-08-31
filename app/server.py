import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from app.restconf import router as restconf_router

load_dotenv()

app = FastAPI(title="RESTCONF Server")

app.include_router(restconf_router, prefix="/restconf")


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.server:app", host=host, port=port, reload=True)
