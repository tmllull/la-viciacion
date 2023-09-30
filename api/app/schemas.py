import datetime
from typing import Union

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    id: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    name: str
    telegram_username: str
    telegram_id: Union[str, None] = None
    clockify_id: Union[str, None] = None
    last_ranking_hours: Union[int, None] = None
    current_ranking_hours: Union[int, None] = None
    last_streak: Union[int, None] = None
    last_streak_date: Union[datetime.date, None] = None
    current_streak: Union[int, None] = None
    best_streak: Union[int, None] = None
    best_streak_date: Union[datetime.date, None] = None
    played_days: Union[int, None] = None
    unplayed_streak: Union[int, None] = None

    class Config:
        from_attributes = True
