import pytest
from httpx import AsyncClient

from app.app_ctx import AppCtx
from app.main import app
from app.data_layer.tables import BaseModel


@pytest.mark.asyncio
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def app_ctx():
    await AppCtx.start()

    yield AppCtx

    async with AppCtx.db_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

