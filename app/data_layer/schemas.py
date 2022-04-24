from typing import Optional, List

from pydantic import BaseModel, Json


class BaseResponse(BaseModel):
    success: bool = True
    message: Optional[str]


class ErrorResponse(BaseResponse):
    success: bool = False


class AppInfo(BaseModel):
    name: str
    api_version: str

    class Config:
        schema_extra = {
            "example": {
                "name": "base description",
                "version": "0.0.1",
            }
        }


class RestaurantRequest(BaseModel):
    name: str
    cousin: str

    class Config:
        schema_extra = {
            'example': {
                'name': 'Ping Pong',
                'cousin': 'Chines'
            }
        }


class RestaurantResponse(BaseModel):
    id: int
    name: str
    cousin: str

    class Config:
        schema_extra = {
            'example': {
                'success': True,
                'result': {
                    'id': 1,
                    'name': 'Ping Pong',
                    'cousin': 'Chines'
                }
            }
        }


class MenuRequest(BaseModel):
    name: str = 'default menu'
    items: Json = {'sorry': 'yet to add our menu, please wait'}
    restaurant_id: int

    class Config:
        schema_extra = {
            'example': {
                'name': 'Monday',
                'items': '{"starter": ["Soup", "Chicken Tikka"]}',
                'restaurant_id': 1
            }
        }


class MenuResponse(BaseModel):
    id: int
    name: str
    items: dict
    restaurant_id: int

    class Config:
        schema_extra = {
            'example': {
                'success': True,
                'result': {
                    'id': 1,
                    'name': 'Monday',
                    'items': '{"starter": ["Soup", "Chicken Tikka"]}',
                    'restaurant_id': 1
                }
            }
        }


class MenusResponse(BaseResponse):
    menus: Optional[MenuResponse]

    class Config:
        schema_extra = {
            'example': {
                'success': True,
                'result': [
                    {
                        'id': 1,
                        'name': 'Menu 1',
                        'items': '{"starter": ["Soup", "Chicken Tikka"]}',
                        'restaurant_id': 1
                    },
                    {
                        'id': 2,
                        'name': 'Menu 2',
                        'items': '{"mains": ["rice", "chicken"]}',
                        'restaurant_id': 2
                    },
                ]
            }
        }


class UserLoginRequest(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            'example': {
                'email': 'email@email.com',
                'password': 'hard to guess'
            }
        }


class UserSignupRequest(UserLoginRequest):
    name: str

    class Config:
        schema_extra = {
            'example': {
                'name': 'My Name',
                'email': 'email@email.com',
                'password': 'hard to guess'
            }
        }


class UserDb(UserSignupRequest):
    id: int


class VoteData(BaseModel):
    menu_id: int
    rank: int


class VoteRequest(BaseModel):
    votes: List[VoteData]

    class Config:
        schema_extra = {
            'example': {
                'votes': [
                    {'menu_id': 1, 'rank': 1},
                    {'menu_id': 2, 'rank': 2},
                    {'menu_id': 3, 'rank': 3},
                ]
            }
        }
