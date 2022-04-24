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


async def attach_votes(user_id: id):
    async with get_ctx_session() as session:
        for rank in range(1, MAX_VOTE_RANKS+1):
            vote = Vote(user_id=user_id, rank=rank)
            session.add(vote)
    return


async def validate_votes(votes: [VoteData]):
    async def _rank(votes: [VoteData]):
        rank_ids: [int] = []
        for vote in votes:
            if vote.rank in rank_ids or vote.rank > MAX_VOTE_RANKS:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Rank')
            rank_ids.append(vote.rank)
        return

    async def _menu(votes: [VoteData]):
        menu_ids: [int] = []
        async with get_ctx_session() as session:
            for vote in votes:
                query = await session.execute(select(Menu).where(Menu.id == vote.menu_id))
                menu = query.fetchone()
                if vote.menu_id in menu_ids or not menu:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Menu')
                menu_ids.append(vote.menu_id)

    await _rank(votes)
    await _menu(votes)
    return


@rt.post('/vote')
async def vote_v2(request: VoteRequest, current_user: UserDb = Depends(get_current_user)) -> dict:
    await validate_votes(request.votes)

    async with get_ctx_session() as session:
        for vote in request.votes:
            await session.execute(
                update(Vote).where(Vote.user_id == current_user.id)
                .where(Vote.rank == vote.rank)
                .values(vote.dict()))

    return {'message': 'success'}
