import enum
import os

from fastapi import FastAPI


APP_ROOT_PATH: str = os.path.dirname(os.path.abspath(__file__))
APP_NAME: str = "my_lunch"
APP_DESCRIPTION: str = "voting for my lunch"


def application_factory() -> FastAPI:

    app = FastAPI(
        title=APP_NAME,
        description=APP_DESCRIPTION
    )
    return app
