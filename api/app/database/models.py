from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Interval,
    String,
    UniqueConstraint,
    text,
)

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

#     owner = relationship("User", back_populates="items")


#############################
#### LA VICIACION TABLES ####
#############################


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    telegram_username = Column(String(255))
    telegram_id = Column(String(255))
    clockify_id = Column(String(255))
    is_admin = Column(Integer)
    last_ranking_hours = Column(Integer)
    current_ranking_hours = Column(Integer)
    last_streak = Column(Integer)
    last_streak_date = Column(Date)
    current_streak = Column(Integer)
    best_streak = Column(Integer)
    best_streak_date = Column(Date)
    played_days = Column(Integer)
    unplayed_streak = Column(Integer)
    __table_args__ = (UniqueConstraint("id"),)


class GamesInfo(Base):
    __tablename__ = "games_info"

    id = Column(Integer, primary_key=True)
    game = Column(String(255))
    dev = Column(String(255))
    release_date = Column(Date)
    steam_id = Column(String(255))
    image_url = Column(String(255))
    genres = Column(String(255))
    played_time = Column(Integer)
    mean_time = Column(String(255))
    last_ranking = Column(Integer)
    current_ranking = Column(Integer)
    clockify_id = Column(String(255))
    __table_args__ = (UniqueConstraint("game"),)


class UsersGames(Base):
    __tablename__ = "users_games"

    id = Column(Integer, primary_key=True)
    player = Column(String(255))
    game = Column(String(255))
    started_date = Column(Date)
    platform = Column(String(255))
    completed = Column(Integer)
    completed_date = Column(Date)
    score = Column(Float)
    row = Column(Integer)
    played_time = Column(Integer)
    completion_time = Column(String(255))
    last_update = Column(String(255))
    __table_args__ = (UniqueConstraint("player", "platform", "row"),)


class UserAchievements(Base):
    __tablename__ = "users_achievements"

    id = Column(Integer, primary_key=True)
    player = Column(String(255))
    achievement = Column(String(255))
    date = Column(Date)
    __table_args__ = (UniqueConstraint("player", "achievement"),)


class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True)
    achievement = Column(String(255))
    message = Column(String(255))
    __table_args__ = (UniqueConstraint("achievement"),)


class TimeEntries(Base):
    __tablename__ = "time_entries"
    id = Column(String(255), primary_key=True)
    user = Column(String(255))
    user_id = Column(String(255))
    user_clockify_id = Column(String(255))
    project = Column(String(255))
    project_id = Column(String(255))
    start = Column(String(255))
    end = Column(String(255))
    duration = Column(Integer)
    __table_args__ = (UniqueConstraint("id"),)


class Logs(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    player = Column(String(255))
    action = Column(String(255))
    date = Column(DateTime)
