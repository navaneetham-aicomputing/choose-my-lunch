import pytest
from sqlalchemy import select
from fastapi import status

from app.app_ctx import get_ctx_session
from app.data_layer.tables import Vote


@pytest.mark.asyncio
async def test_user_signup(async_client, app_ctx):
    user_data: dict = {'name': 'name', 'email': 'email@email.com', 'password': 'secret'}
    response = await async_client.post('/user/signup', json=user_data)
    resp_dict = response.json()
    user_id = resp_dict.get('id')
    assert response.status_code == status.HTTP_201_CREATED
    assert user_id

    async with get_ctx_session() as session:
        votes = await session.execute(select(Vote).where(Vote.user_id == user_id))
        for vote in votes:
            v = vote[0]
            assert v.user_id == user_id
            assert v.rank in [1, 2, 3]

    response = await async_client.post('/user/signup', json=user_data)
    assert response.status_code == status.HTTP_302_FOUND

    response = await async_client.post('/token', data={'username': 'email@email.com', 'password': 'secret'})
    auth_token = response.json()['access_token']
    header = {'Authorization': 'Bearer ' + auth_token}

    vote_data = {'votes': [
                    {'menu_id': 1, 'rank': 1},
                    {'menu_id': 2, 'rank': 2},
                    {'menu_id': 3, 'rank': 3},
                ]}

    response = await async_client.post('/v1/vote', json=vote_data, headers=header)


@pytest.mark.asyncio
async def test_token(async_client, app_ctx):
    user_data: dict = {'name': 'name', 'email': 'email@email.com', 'password': 'secret'}
    response = await async_client.post('/user/signup', json=user_data)
    resp_dict = response.json()
    user_id = resp_dict.get('id')
    assert response.status_code == status.HTTP_201_CREATED
    assert user_id

    response = await async_client.post('/token', data={'username': 'email@email.com', 'password': 'secret'})
    auth_token = response.json()['access_token']
    assert auth_token
