import logging
from sqlalchemy import select
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from . base import router_factory
from app.app_ctx import get_ctx_session
from app.auth.base import create_access_token
from app.data_layer.schemas import UserSignupRequest
from app.data_layer.tables import User, Vote
from app.auth.password import get_password_hash, verify_password
from app.api.vote_v2 import attach_votes

rt = router_factory(__name__)
logger = logging.getLogger(__name__)


@rt.post("/user/signup", status_code=status.HTTP_201_CREATED)
async def user_signup(request: UserSignupRequest) -> dict:
    async with get_ctx_session() as session:
        query = await session.execute(select(User).where(User.email == request.email))
        user = query.fetchone()
        if user:
            logging.info(f'Email address {request.email} already registered')
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f'Email address {request.email} already registered')

        request.password = get_password_hash(request.password)
        user = User(**request.dict())
        session.add(user)

    await attach_votes(user_id=user.id)

    return {'id': user.id}


@rt.post('/token', status_code=status.HTTP_201_CREATED)
async def create_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    email = form_data.username
    password = form_data.password
    async with get_ctx_session() as session:
        query = await session.execute(select(User).where(User.email == email))
        user = query.fetchone()
        if user:
            user = user[0]
            if verify_password(password, user.password):
                access_token = create_access_token(user.email)
                return {"access_token": access_token, "token_type": "bearer"}
            else:
                error_msg = f'Invalid password for {email}'
                logging.info(f'Invalid password for {email}')
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_msg)
        else:
            error_msg = f'User not found for {email}'
            logging.info(error_msg)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)


@rt.get('/what_is_lunch')
async def menu_ranks() -> dict:
    from collections import defaultdict
    result = defaultdict(lambda: 0)

    async with get_ctx_session() as session:
        votes = await session.execute(select(Vote))
        for vote in votes:
            if vote[0].menu_id:
                result[vote[0].menu_id] += 1

    return {'message': 'success', 'result': result}
