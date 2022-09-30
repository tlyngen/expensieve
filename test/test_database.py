import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database.models import Base, User

from database.dao import Database


@pytest.fixture(scope="session")
def app_database():
    database = Database(echo=True)
    yield database


@pytest.fixture(scope="session")
def db_engine():
    conn_str = "sqlite:///./database/expensieve.db"
    engine = create_engine(conn_str)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def db_session_factory(db_engine):
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope="function")
def db_session(db_session_factory):
    session = db_session_factory()
    yield session
    session.rollback()
    session.close()


class TestDatabase:
    USERNAME = "test_user"
    PASSWORD = "test_password"

    def assert_passed(message="None"):
        print(message)
        return True

    def test_create_user(db_session, app_database):
        app_database.create_user(
            username=TestDatabase.USERNAME,
            password=TestDatabase.PASSWORD
        )
        user_id = app_database.get_user_id(TestDatabase.USERNAME)
        # user = User(
        #     username=TestDatabase.USERNAME,
        #     password=TestDatabase.PASSWORD)
        # db_session.add(user)
        # db_session.commit()
        assert user_id > 0, f"user={user_id}"
        print(f"user_id={user_id}")

    def test_get_user_password(db_session, app_database):
        password = app_database.get_user_password(TestDatabase.USERNAME)
        assert password == TestDatabase.PASSWORD
        print(f"password: {password}")
