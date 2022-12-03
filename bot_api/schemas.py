from datetime import datetime

from pydantic import BaseModel

from catbreadbot.bot import State


class User(BaseModel):
    id: str
    state: State

    class Config:
        orm_mode = True


class ChatHistory(BaseModel):
    user: str
    state: str
    message: str | None
    time: datetime

    class Config:
        orm_mode = True


class BotMessage(BaseModel):
    text: str | None


class UserMessage(BaseModel):
    user_id: str
    text: str
