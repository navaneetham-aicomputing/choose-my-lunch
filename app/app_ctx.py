from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from app.connections import create_db_engine


class AppCtx:
    db_engine = None

    @classmethod
    async def start(cls) -> None:
        cls.db_engine = await create_db_engine()


@asynccontextmanager
async def get_application_ctx():
    await AppCtx.start()
    yield AppCtx


async def get_db_session() -> AsyncSession:
    session = AsyncSession(AppCtx.db_engine, expire_on_commit=False)
    try:
        yield session
        await session.commit()
    except Exception as exc:
        await session.rollback()
        raise exc
    finally:
        await session.close()

get_ctx_session = asynccontextmanager(get_db_session)
