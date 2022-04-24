import json
import pytest

from sqlalchemy import select
from fastapi import status

from app.app_ctx import get_ctx_session
from app.data_layer.tables import Menu


@pytest.mark.asyncio
async def test_new_restaurant(async_client, app_ctx):
    restaurant_data: dict = {'name': 'Dosa Dosa', 'cousin': 'Indian'}
    response = await async_client.post('/restaurant/new', json=restaurant_data)
    resp_dict = response.json()
    restaurant_id = resp_dict.get('id')
    assert response.status_code == status.HTTP_201_CREATED
    assert restaurant_id

    async with get_ctx_session() as session:
        menus = await session.execute(select(Menu).where(Menu.restaurant_id == restaurant_id))
        for menu in menus:
            m = menu[0]
            assert m.restaurant_id == restaurant_id

    response = await async_client.post('/restaurant/new', json=restaurant_data)
    assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.asyncio
async def test_restaurant_update_menu(async_client, app_ctx):

    restaurant_data: dict = {'name': 'ZenXi', 'cousin': 'Chines'}

    restaurant_res = await async_client.post('/restaurant/new', json=restaurant_data)
    restaurant_id = restaurant_res.json().get('id')

    menu_data: dict = {'name': 'Tuesday', 'items': json.dumps({'mains': 'dinner'}),
                       'restaurant_id': restaurant_id}
    response = await async_client.post('/restaurant/update_menu', json=menu_data)
    assert response.status_code == status.HTTP_201_CREATED

    async with get_ctx_session() as session:
        menus = await session.execute(select(Menu).where(Menu.restaurant_id == restaurant_id))
        for menu in menus:
            m = menu[0]
            assert m.restaurant_id == 1
            assert m.name == menu_data['name']
            assert m.items == json.loads(menu_data['items'])


@pytest.mark.asyncio
async def test_restaurant_update_menu(async_client, app_ctx):

    restaurant_data: dict = {'name': 'ZenXi', 'cousin': 'Chines'}

    restaurant_res = await async_client.post('/restaurant/new', json=restaurant_data)
    restaurant_id = restaurant_res.json().get('id')

    menu_item: dict = {'mains': 'dinner'}
    menu_data: dict = {'name': 'Tuesday', 'items': json.dumps(menu_item),
                       'restaurant_id': restaurant_id}
    await async_client.post('/restaurant/update_menu', json=menu_data)

    today_menu_res = await async_client.get('/restaurant/today_menu')
    result = today_menu_res.json()['result'][0]

    assert result['items'] == menu_item
    assert result['restaurant_id'] == restaurant_id

