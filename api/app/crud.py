from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_tg_username(db: Session, telegram_username: str = None):
    return (
        db.query(models.User)
        .filter(models.User.telegram_username == telegram_username)
        .first()
    )
    if telegram_id is not None:
        user = (
            db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
        )
        if user is not None:
            return user
        if user is None and telegram_username is not None:
            stmt = (
                update(models.User)
                .where(models.User.telegram_username == telegram_username)
                .values(telegram_id=telegram_id)
            )
            db.execute(stmt)
            stmt = select(models.User).where(
                models.User.telegram_username == telegram_username
            )
            user = db.execute(stmt).first()
            db.commit()
            # db.close()
            return user
        else:
            return None
    elif telegram_username is not None:
        user = user = (
            db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
        )
        if user is not None:
            return user
        if user is None and telegram_id is not None:
            stmt = (
                update(models.User)
                .where(models.User.telegram_id == telegram_id)
                .values(telegram_username=telegram_username)
            )
            db.execute(stmt)
            stmt = select(models.User).where(
                models.User.telegram_username == telegram_username
            )
            user = db.execute(stmt).first()
            db.commit()
            # db.close()
            return user
        else:
            return None
    # elif name is not None:
    #     stmt = select(User).where(User.name == name)
    #     user = session.execute(stmt).first()
    #     session.commit()
    #     session.close()
    else:
        return None
        return user
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
