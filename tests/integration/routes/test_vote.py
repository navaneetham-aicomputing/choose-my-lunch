import json
import pytest
from sqlalchemy import select
from fastapi import status

from app.app_ctx import get_ctx_session
from app.data_layer.tables import Vote


@pytest.mark.asyncio
async def test_vote_v1(async_client, app_ctx):
    user_data: dict = {'name': 'name', 'email': 'email@email.com', 'password': 'secret'}
    response = await async_client.post('/user/signup', json=user_data)
    resp_dict = response.json()
    user_id = resp_dict.get('id')

    response = await async_client.post('/token', data={'username': 'email@email.com', 'password': 'secret'})
    auth_token = response.json()['access_token']
    header = {'Authorization': 'Bearer ' + auth_token}

    response = await async_client.post('/v1/vote/1', headers=header)

    assert response.status_code == status.HTTP_200_OK

    async with get_ctx_session() as session:
        votes = await session.execute(select(Vote).where(Vote.user_id == user_id).where(Vote.rank == 1))
        for vote in votes:
            v = vote[0]
            assert v.user_id == user_id
            assert v.rank == 1


@pytest.mark.asyncio
async def test_vote_v2(async_client, app_ctx):
    user_data: dict = {'name': 'name', 'email': 'email@email.com', 'password': 'secret'}
    response = await async_client.post('/user/signup', json=user_data)
    resp_dict = response.json()
    user_id = resp_dict.get('id')

    response = await async_client.post('/token', data={'username': 'email@email.com', 'password': 'secret'})
    auth_token = response.json()['access_token']
    header = {'Authorization': 'Bearer ' + auth_token}

    restaurants_data: list = [
        {'name': 'Restaurant-1', 'cousin': 'taste-1'},
        {'name': 'Restaurant-2', 'cousin': 'taste-2'},
        {'name': 'Restaurant-3', 'cousin': 'taste-3'},
    ]

    restaurant_ids = []
    for restaurant_data in restaurants_data:
        restaurant_res = await async_client.post('/restaurant/new', json=restaurant_data)
        restaurant_id = restaurant_res.json().get('id')
        restaurant_ids.append(restaurant_id)

        menu_item: dict = {'mains': 'dinner'}
        menu_data: dict = {'name': 'Tuesday', 'items': json.dumps(menu_item),
                           'restaurant_id': restaurant_id}
        await async_client.post('/restaurant/update_menu', json=menu_data)

    vote_data = {'votes': [
                    {'menu_id': 1, 'rank': 1},
                    {'menu_id': 2, 'rank': 2},
                    {'menu_id': 3, 'rank': 3},
                ]}

    response = await async_client.post('/v2/vote', json=vote_data, headers=header)

    assert response.status_code == status.HTTP_200_OK

    async with get_ctx_session() as session:
        votes = await session.execute(select(Vote).where(Vote.user_id == user_id))
        for vote in votes:
            v = vote[0]
            assert v.user_id == user_id
            assert v.rank in [1, 2, 3]
            assert v.rank == v.menu_id

