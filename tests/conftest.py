from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from bot_api import database
from bot_api.services import get_db
from main import app as _app

TEST_DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='session', autouse=True)
def app() -> Generator[FastAPI, Any, None]:
    database.Base.metadata.create_all(engine)
    yield _app
    database.Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def db_session(app):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestSession(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(app: FastAPI, db_session: Session):

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
