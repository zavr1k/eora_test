from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from bot_api import database, models, schemas, services

models.Base.metadata.create_all(database.engine)


app = FastAPI(title='CatOrBread')


@app.post('/user', response_model=schemas.User)
def create_user(db: Session = Depends(services.get_db)):
    user = services.create_user(db)
    return user


@app.post('/send_message', response_model=schemas.BotMessage)
def send_message(
    message: schemas.UserMessage, db: Session = Depends(services.get_db)
):
    response = services.send_bot_message(db=db, message=message)
    return schemas.BotMessage(text=response)
