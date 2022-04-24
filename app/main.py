import os
import signal
import logging
import uvicorn
from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse

from app import application_factory
from app.app_ctx import AppCtx
from app.api import REGISTERED_ROUTES
from app.data_layer.schemas import AppInfo, ErrorResponse
from app.settings import settings

logger = logging.getLogger(__name__)

responses = {
    status.HTTP_401_UNAUTHORIZED: {'description': 'Unauthorized', 'model': ErrorResponse},
    status.HTTP_404_NOT_FOUND: {'description': 'Not found', 'model': ErrorResponse},
}

app: FastAPI = application_factory()
for rt in REGISTERED_ROUTES:
    app.include_router(rt, responses=responses)


@app.get("/", response_model=AppInfo)
async def root() -> dict:
    return {'name': app.title, 'api_version': app.version}


@app.on_event("startup")
async def on_startup() -> None:
    await AppCtx.start()


def worker_exit(server, worker):
    os.kill(server.pid, signal.SIGTERM)


if __name__ == "__main__":
    uvicorn.run(app=app, host=settings.APP_HOST, port=settings.APP_PORT)
