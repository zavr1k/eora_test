import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from bot_api import schemas
from bot_api.services import get_user_by_id, get_users
from catbreadbot.bot import BotPhrase, State


def test_craate_user(client: TestClient, db_session: Session) -> None:
    _ = client.post('/user')
    response = client.post('/user')
    users = get_users(db_session)
    data = response.json()
    assert response.status_code == 200
    assert len(users) == 2
    assert data['id'] == '2'
    assert data['state'] == 'none'


def test_no_user_id_db(
        client: TestClient,
        db_session: Session,
) -> None:
    user_message = {'user_id': '1', 'text': '/start'}
    response = client.post('/send_message', json=user_message)
    user = get_users(db=db_session)
    assert response.status_code == 404
    assert len(user) == 0


start_cases = (
    ({'user_id': '1', 'text': 'asdf'}, BotPhrase.START, State.NONE.value),
    ({'user_id': '1', 'text': '/start'},
        f'{BotPhrase.GREETING} {BotPhrase.IS_SQUARE}', State.START.value),
)


@pytest.mark.parametrize("user_message, bot_message, state", start_cases)
def test_start_handler(
        client: TestClient,
        db_session: Session,
        state: State,
        user_message: schemas.UserMessage,
        bot_message: schemas.BotMessage,
) -> None:
    client.post('/user')
    response = client.post('/send_message', json=user_message)
    data = response.json()
    user = get_user_by_id(db=db_session, user_id='1')
    assert response.status_code == 200
    assert data['text'] == bot_message
    assert user.state == state


square_cases = (
    ({'user_id': '1', 'text': 'asdf'}, BotPhrase.IS_SQUARE, State.START.value),
    ({'user_id': '1', 'text': 'no'}, BotPhrase.CAT, State.NONE.value),
    ({'user_id': '1', 'text': 'yes'}, BotPhrase.HAS_EARS, State.SQUARE.value),
)


@pytest.mark.parametrize("user_message, bot_message, state", square_cases)
def test_square_handler(
        client: TestClient,
        db_session: Session,
        state: State,
        user_message: schemas.UserMessage,
        bot_message: schemas.BotMessage,
) -> None:
    client.post('/user')
    client.post('/send_message', json={'user_id': '1', 'text': '/start'})
    response = client.post('/send_message', json=user_message)
    data = response.json()
    user = get_user_by_id(db=db_session, user_id='1')
    assert response.status_code == 200
    assert data['text'] == bot_message
    assert user.state == state


ear_cases = (
    ({'user_id': '1', 'text': 'asdf'}, BotPhrase.HAS_EARS, State.SQUARE.value),
    ({'user_id': '1', 'text': 'no'}, BotPhrase.BREAD, State.NONE.value),
    ({'user_id': '1', 'text': 'yes'}, BotPhrase.CAT, State.NONE.value),
)


@pytest.mark.parametrize("user_message, bot_message, state", ear_cases)
def test_ear_handler(
        client: TestClient,
        db_session: Session,
        state: State,
        user_message: schemas.UserMessage,
        bot_message: schemas.BotMessage,
 ) -> None:
    client.post('/user')
    client.post('/send_message', json={'user_id': '1', 'text': '/start'})
    client.post('/send_message', json={'user_id': '1', 'text': 'yes'})
    response = client.post('/send_message', json=user_message)
    data = response.json()
    user = get_user_by_id(db=db_session, user_id='1')
    assert response.status_code == 200
    assert data['text'] == bot_message
    assert user.state == state
