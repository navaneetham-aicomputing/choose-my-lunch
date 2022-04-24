from sqlalchemy.ext.asyncio import create_async_engine

from app.settings import settings


async def create_db_engine(address: str = settings.DATABASE_URL):
    return create_async_engine(address, connect_args={"check_same_thread": False})


