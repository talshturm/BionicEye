import pytest
from database import engine, SessionLocal


@pytest.fixture(scope='session')
def db_engine():
    return engine


@pytest.fixture(scope='function')
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    session = SessionLocal(bind=connection)

    yield session

    session.rollback()
    connection.close()
