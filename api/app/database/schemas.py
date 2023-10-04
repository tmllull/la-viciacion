import datetime
from typing import Optional, Union

from pydantic import BaseModel

# class ItemBase(BaseModel):
#     title: str
#     description: Union[str, None] = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         from_attributes = True


class UserBase(BaseModel):
    id: int


# class UserCreate(UserBase):
#     password: str


class User(UserBase):
    id: int
    name: str
    telegram_username: str
    telegram_id: Union[str, None] = None
    is_admin: Union[int, None] = None
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


class GamesInfoBase(BaseModel):
    id: int

    class Config:
        from_attributes = True


class GamesInfo(GamesInfoBase):
    name: str
    dev: Union[str, None] = None
    release_date: Union[datetime.date, str, None] = None
    steam_id: Union[str, None] = None
    image_url: Union[str, None] = None
    genres: Union[str, None] = None
    played_time: Union[int, None] = None
    avg_time: Union[int, None] = None
    last_ranking: Optional[Union[int, None]] = 100000000
    current_ranking: Optional[Union[int, None]] = 10000000
    clockify_id: Union[str, None] = None

    # class Config:
    #     from_attributes = True


class NewGame(BaseModel):
    name: str
    dev: Optional[Union[str, None]] = None
    release_date: Optional[Union[datetime.date, None]] = None
    steam_id: Optional[Union[str, None]] = None
    image_url: Optional[Union[str, None]] = None
    genres: Optional[Union[str, None]] = None
    avg_time: Optional[Union[int, None]] = None
    clockify_id: Optional[Union[str, None]] = None

    # class Config:
    #     from_attributes = True


class StartGame(BaseModel):
    game: str
    platform: Union[str, None] = None


class UsersGamesBase(BaseModel):
    id: int

    class Config:
        from_attributes = True


class UsersGames(UsersGamesBase):
    id: Union[int, None] = None
    user: Union[str, None] = None
    user_id: Union[int, None] = None
    game: Union[str, None] = None
    started_date: Union[datetime.date, None] = None
    platform: Union[str, None] = None
    completed: Union[int, None] = None
    completed_date: Union[datetime.date, None] = None
    score: Union[float, None] = None
    played_time: Union[int, None] = None
    completion_time: Union[str, None] = None
    last_update: Union[str, None] = None

    class Config:
        from_attributes = True


class UserAchievements(BaseModel):
    id: Union[int, None] = None
    player: Union[str, None] = None
    achievement: Union[str, None] = None
    date: Union[datetime.date, None] = None

    class Config:
        from_attributes = True


class TimeEntries(BaseModel):
    id: Union[int, None] = None
    user: Union[str, None] = None
    user_id: Union[str, None] = None
    user_clockify_id: Union[str, None] = None
    project: Union[str, None] = None
    project_id: Union[str, None] = None
    start: Union[str, None] = None
    end: Union[str, None] = None
    duration: Union[int, None] = None

    class Config:
        from_attributes = True