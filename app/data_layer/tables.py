from datetime import datetime

from sqlalchemy import Integer, Column, DateTime, String, ForeignKey, JSON
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)


class CreatedUpdatedModelMixin(Base):

    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Restaurant(BaseModel, CreatedUpdatedModelMixin):
    __tablename__ = 'restaurants'

    name = Column(String, nullable=False, unique=True)
    cousin = Column(String, nullable=False)


class User(BaseModel, CreatedUpdatedModelMixin):
    __tablename__ = 'users'

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Menu(BaseModel):
    __tablename__ = 'menus'

    name = Column(String, nullable=False)
    items = Column(JSON, nullable=False)
    restaurant_id = Column(ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)


class Vote(BaseModel):
    __tablename__ = 'votes'

    rank = Column(Integer, nullable=False, default=1)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    menu_id = Column(ForeignKey("menus.id", ondelete="CASCADE"))
