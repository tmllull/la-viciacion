import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    invitation_key: str


class User(UserBase):
    id: int
    name: Union[str, None] = None
    # telegram_id: Union[int, None] = None
    is_admin: Union[int, None] = 0
    email: Union[str, None] = None
    is_active: Union[int, None] = 0
    # played_time: Union[int, None] = 0
    clockify_id: Union[str, None] = None
    # current_ranking_hours: Union[int, None] = None
    # current_streak: Union[int, None] = 0
    # best_streak: Union[int, None] = 0
    # best_streak_date: Union[datetime.date, None] = None
    # played_days: Union[int, None] = 0
    # unplayed_streak: Union[int, None] = None

    class Config:
        from_attributes = True


class UserStatistics(BaseModel):
    user_id: int
    played_time: Union[int, None] = 0
    current_ranking_hours: Union[int, None] = None
    current_streak: Union[int, None] = 0
    best_streak: Union[int, None] = 0
    best_streak_date: Union[datetime.date, None] = None
    played_days: Union[int, None] = 0
    unplayed_streak: Union[int, None] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Union[str, None] = None
    username: str
    password: Union[str, None] = None
    email: Union[str, None] = None
    # telegram_id: Union[int, None] = None
    is_admin: Union[int, None] = None
    is_active: Union[int, None] = None
    clockify_id: Union[str, None] = None

    class Config:
        from_attributes = True


# class TelegramUser(BaseModel):
#     telegram_name: str
#     telegram_id: int


# class GamesInfoBase(BaseModel):
#     id: int

#     class Config:
#         from_attributes = True


class Game(BaseModel):
    id: int
    name: str
    dev: Union[str, None] = None
    release_date: Union[datetime.date, str, None] = None
    steam_id: Union[str, None] = None
    image_url: Union[str, None] = None
    genres: Union[str, None] = None
    # played_time: Union[int, None] = 0
    avg_time: Union[int, None] = 0
    # current_ranking: Optional[Union[int, None]] = 10000000
    clockify_id: Union[str, None] = None

    class Config:
        from_attributes = True


class GameStatistics(BaseModel):
    game_id: int
    played_time: Union[int, None] = 0
    avg_time: Union[int, None] = 0
    current_ranking: Optional[Union[int, None]] = 10000000

    class Config:
        from_attributes = True


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


class UpdateGame(BaseModel):
    name: str
    dev: Optional[Union[str, None]] = None
    release_date: Optional[Union[datetime.date, None]] = None
    steam_id: Optional[Union[str, None]] = None
    image_url: Optional[Union[str, None]] = None
    genres: Optional[Union[str, None]] = None
    avg_time: Optional[Union[int, None]] = None
    clockify_id: Optional[Union[str, None]] = None


class NewGameUser(BaseModel):
    project_clockify_id: str
    platform: Union[str, None] = None


class UsersGamesBase(BaseModel):
    id: int

    class Config:
        from_attributes = True


class UserGame(UsersGamesBase):
    id: Union[int, None] = None
    # user: Union[str, None] = None
    user_id: Union[int, None] = None
    # game_name: Union[str, None] = None
    game_id: Union[int, None] = None
    project_clockify_id: Union[str, None] = None
    started_date: Union[datetime.date, None] = None
    platform: Union[str, None] = None
    completed: Union[int, None] = None
    completed_date: Union[datetime.date, None] = None
    score: Union[float, None] = None
    played_time: Union[int, None] = None
    completion_time: Union[int, None] = None
    last_update: Union[str, None] = None

    # class Config:
    #     from_attributes = True


class Achievement(BaseModel):
    id: Union[int, None] = None
    key: Union[str, None] = None
    title: Union[str, None] = None
    message: Union[str, None] = None

    class Config:
        from_attributes = True


class UserAchievement(BaseModel):
    id: Union[int, None] = None
    user: Union[str, None] = None
    user_id: Union[int, None] = None
    achievement_id: Union[int, None] = None
    date: Union[datetime.date, None] = None

    class Config:
        from_attributes = True


class TimeEntrie(BaseModel):
    id: Union[int, None] = None
    # user: Union[str, None] = None
    user_id: Union[str, None] = None
    user_clockify_id: Union[str, None] = None
    # project: Union[str, None] = None
    project_clockify_id: Union[str, None] = None
    start: Union[datetime.date, None] = None
    end: Union[datetime.date, None] = None
    duration: Union[int, None] = None

    class Config:
        from_attributes = True


class CompletedGame(BaseModel):
    completed_games: Union[int, None]
    completion_time: Union[int, None]
    avg_time: Union[int, None]


# class RankingsResponse(BaseModel):
#     type: str
#     data: List[Union[str, int, None]]
