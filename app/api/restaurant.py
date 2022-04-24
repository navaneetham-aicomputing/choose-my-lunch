import logging
from sqlalchemy import select, update
from fastapi import status, HTTPException

from . base import router_factory
from app.app_ctx import get_ctx_session
from app.data_layer.schemas import RestaurantRequest, MenuRequest, MenuResponse, MenusResponse
from app.data_layer.tables import Restaurant, Menu

rt = router_factory(__name__)
logger = logging.getLogger(__name__)


async def attach_default_menu(restaurant_id: int):
    async with get_ctx_session() as session:
        menu = Menu(**MenuRequest(restaurant_id=restaurant_id).dict())
        session.add(menu)
    return


@rt.post("/restaurant/new", status_code=status.HTTP_201_CREATED)
async def new(request: RestaurantRequest) -> dict:
    async with get_ctx_session() as session:
        query = await session.execute(select(Restaurant).where(Restaurant.name == request.name))
        restaurant = query.fetchone()
        if restaurant:
            error_msg = f'Restaurant {request.name} already registered'
            logging.info(error_msg)
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail=error_msg)

        restaurant = Restaurant(**request.dict())
        session.add(restaurant)

    await attach_default_menu(restaurant_id=restaurant.id)
    return {'id': restaurant.id}


@rt.post("/restaurant/update_menu", status_code=status.HTTP_201_CREATED)
async def update_menu(request: MenuRequest) -> dict:

    async with get_ctx_session() as session:
        query = await session.execute(select(Menu).where(Menu.restaurant_id == request.restaurant_id))
        menu = query.first()
        if not menu:
            error_msg = f'No menu found for restaurant id {request.restaurant_id}'
            logging.info(error_msg)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)

        await session.execute(
            update(Menu).where(Menu.restaurant_id == request.restaurant_id).\
            values(**request.dict())
        )

    return {'message': 'success'}


@rt.get("/restaurant/today_menu")
async def today_menu() -> [MenuResponse]:
    menus_list = []

    async with get_ctx_session() as session:
        menus = await session.execute(select(Menu))
        for menu in menus:
            menu = menu[0]
            menus_list.append(MenuResponse(id=menu.id, name=menu.name,
                                           restaurant_id=menu.restaurant_id, items=menu.items))

    return {'message': 'success', 'result': menus_list}

