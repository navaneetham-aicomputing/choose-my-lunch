import enum
from urllib.parse import urlparse

from pydantic import BaseSettings, validator


class Env(str, enum.Enum):
    LOCAL = 'local'
    TEST = 'test'
    DEV = 'dev'
    STAGE = 'stage'
    QA = 'qa'
    UAT = 'uat'
    PROD = 'prod'


class Settings(BaseSettings):

    DEBUG: bool = True
    APP_PORT: int = 8000
    APP_HOST: str = '127.0.0.1'
    ENV: Env = Env.DEV
    JWK4JWT: str


    DATABASE_URL: str
    DATABASE_POOL_MAX_CONN: int = 3

    class Config:
        env_prefix = "SDC_"


settings = Settings()
