from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Interval,
    LargeBinary,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import relationship

from .database import Base

# from sqlalchemy.orm import relationship


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)

#     items = relationship("Item", back_populates="owner")


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(255), index=True)
#     description = Column(String(255), index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("Users", back_populates="items")


#############################
#### LA VICIACION TABLES ####
#############################


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    username = Column(String(255))
    password = Column(String(255))
    telegram_id = Column(BigInteger)
    clockify_id = Column(String(255))
    email = Column(String(255))
    is_admin = Column(Integer)
    is_active = Column(Integer)
    avatar = Column(LargeBinary)
    # played_time = Column(Integer)
    # current_ranking_hours = Column(Integer)
    # current_streak = Column(Integer)
    # best_streak = Column(Integer)
    # best_streak_date = Column(Date)
    # played_days = Column(Integer)
    # unplayed_streak = Column(Integer)

    # games = relationship("UsersGames", back_populates="user")
    # ranking = relationship("RankingUsers", back_populates="user")
    # time_entries = relationship("RankingUsers", back_populates="user")

    __table_args__ = (UniqueConstraint("username"),)


class UserStatistics(Base):
    __tablename__ = "users_statistics"

    user_id = Column(Integer, primary_key=True)
    played_time = Column(Integer)
    current_ranking_hours = Column(Integer)
    current_streak = Column(Integer)
    best_streak = Column(Integer)
    best_streak_date = Column(Date)
    played_days = Column(Integer)
    unplayed_streak = Column(Integer)

    # games = relationship("UsersGames", back_populates="user")
    # ranking = relationship("RankingUsers", back_populates="user")
    # time_entries = relationship("RankingUsers", back_populates="user")

    __table_args__ = (UniqueConstraint("user_id"),)


# class RankingUsers(Base):
#     __tablename__ = "ranking_users"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer)
#     # name = Column(String(255))
#     played_hours_current = Column(Integer)
#     played_hours_last = Column(Integer)
#     played_games_current = Column(Integer)
#     played_games_last = Column(Integer)
#     played_days_total = Column(Integer)
#     completed_games_current = Column(Integer)
#     completed_games_last = Column(Integer)
#     streak_current = Column(Integer)
#     streak_last = Column(Integer)
#     streak_best = Column(Integer)
#     streak_best_date = Column(Date)
#     unplayed_streak = Column(Integer)

#     # user = relationship("Users", back_populates="ranking")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    dev = Column(String(255))
    release_date = Column(Date)
    steam_id = Column(String(255))
    image_url = Column(String(255))
    genres = Column(String(255))
    # played_time = Column(Integer)
    avg_time = Column(Integer)
    # current_ranking = Column(Integer)
    clockify_id = Column(String(255))

    # users = relationship("UsersGames", back_populates="game")
    # time_entries = relationship("TimeEntries", back_populates="game")

    __table_args__ = (UniqueConstraint("name"),)


class GameStatistics(Base):
    __tablename__ = "games_statistics"

    game_id = Column(Integer, primary_key=True, autoincrement=True)
    played_time = Column(Integer)
    avg_time = Column(Integer)
    current_ranking = Column(Integer)

    # users = relationship("UsersGames", back_populates="game")
    # time_entries = relationship("TimeEntries", back_populates="game")

    __table_args__ = (UniqueConstraint("game_id"),)


class UserGame(Base):
    __tablename__ = "users_games"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    game_id = Column(Integer)
    project_clockify_id = Column(String(255))
    started_date = Column(Date)
    platform = Column(String(255))
    completed = Column(Integer)
    completed_date = Column(Date)
    score = Column(Float)
    played_time = Column(Integer)
    completion_time = Column(Integer)

    # user = relationship("Users", back_populates="games")
    # game = relationship("GamesInfo", back_populates="users")

    __table_args__ = (UniqueConstraint("user_id", "game_id", "platform"),)


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(255))
    title = Column(String(255))
    message = Column(String(255))
    __table_args__ = (UniqueConstraint("key"),)


class UserAchievement(Base):
    __tablename__ = "users_achievements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(255))
    user_id = Column(Integer)
    achievement_id = Column(Integer)
    date = Column(Date)
    __table_args__ = (UniqueConstraint("user_id", "achievement_id"),)


class TimeEntry(Base):
    __tablename__ = "time_entries"

    id = Column(String(255), primary_key=True)
    # user = Column(String(255))
    user_id = Column(Integer)
    user_clockify_id = Column(String(255))
    # project = Column(String(255))
    project_clockify_id = Column(String(255))
    start = Column(DateTime)
    end = Column(DateTime)
    duration = Column(Integer)

    # user = relationship("Users", back_populates="time_entries")
    # game = relationship("GamesInfo", back_populates="time_entries")

    __table_args__ = (UniqueConstraint("id"),)


class ClockifyTag(Base):
    __tablename__ = "clockify_tags"

    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    __table_args__ = (UniqueConstraint("id"),)


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    player = Column(String(255))
    action = Column(String(255))
    date = Column(DateTime)
