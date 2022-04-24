import logging
from sqlalchemy import select, update
from fastapi import status, HTTPException, Depends

from .base import router_factory
from app.app_ctx import get_ctx_session
from app.auth.base import get_current_user
from app.data_layer.schemas import VoteRequest, VoteData, UserDb
from app.data_layer.tables import Vote, Menu

rt = router_factory(__name__)
logger = logging.getLogger(__name__)

MAX_VOTE_RANKS = 3


@rt.post('/vote/{menu_id}')
async def vote_v1(menu_id: int, current_user: UserDb = Depends(get_current_user)) -> dict:
    async with get_ctx_session() as session:
        await session.execute(
            update(Vote)
            .where(Vote.user_id == current_user.id)
            .where(Vote.rank == 1)
            .values({'menu_id': menu_id}))

    return {'message': 'success'}

