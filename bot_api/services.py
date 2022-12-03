from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from bot_api import models, schemas
from catbreadbot.bot import CatBreadBot, State

from . import database


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(db: Session):
    new_user = models.User(state=State.NONE)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def write_history(
    db: Session, bot: CatBreadBot, message: schemas.UserMessage
) -> None:
    """Writes the chat history to the database"""
    record = models.ChatHistory(
        user=message.user_id,
        state=str(bot.state),
        message=message.text,
        time=datetime.utcnow()
    )
    db.add(record)
    db.commit()
    db.refresh(record)


def get_users(db: Session):
    """Gets all users from the database"""
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: str) -> models.User:
    """Gets user by them id"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found. Please check user_id or register'
        )
    return user


def get_bot_with_state(state: str) -> CatBreadBot:
    """Returns the CatBreadBot instance in the specific state"""
    bot = CatBreadBot()
    bot._state = State.__dict__['_member_map_'][state.upper()]
    return bot


def send_bot_message(db: Session, message: schemas.UserMessage) -> str:
    """Sends user message to the bot, return the bot's response,
    change the bot's state for current user,
    writes the history to the database"""
    user = get_user_by_id(db=db, user_id=message.user_id)
    bot = get_bot_with_state(str(user.state))
    bot_response = bot.send(message.text)
    user.state = bot.state.value
    db.commit()
    write_history(db=db, bot=bot, message=message)
    return bot_response
