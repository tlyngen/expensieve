import pytest

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker
from database.models import Base, Expense

from database.dao import Database


@pytest.fixture(scope="session")
def app_database():
    database = Database.instance()
    yield database


@pytest.fixture(scope="session")
def db_engine():
    conn_str = "sqlite:///./database/expensieve.db"
    engine = create_engine(conn_str)
    Base.metadata.create_all(engine)  # not working with GitHub CI workflow
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

    def test_drop_tables(db_session, app_database, db_engine):
        app_database.drop_tables()
        user_exists = inspect(db_engine).has_table("user")
        expense_exists = inspect(db_engine).has_table("expense")
        user_expense_exists = inspect(db_engine).has_table("user_expense")
        assert not user_exists
        assert not expense_exists
        assert not user_expense_exists

    def test_create_tables(db_session, app_database, db_engine):
        app_database.create_tables()
        user_exists = inspect(db_engine).has_table("user")
        expense_exists = inspect(db_engine).has_table("expense")
        user_expense_exists = inspect(db_engine).has_table("user_expense")
        assert user_exists
        assert expense_exists
        assert user_expense_exists

    def test_create_user(db_session, app_database):
        app_database.create_user(
            username=TestDatabase.USERNAME,
            password=TestDatabase.PASSWORD
        )
        user_id = app_database.get_user_id(TestDatabase.USERNAME)
        assert user_id > 0, f"user={user_id}"
        print(f"user_id={user_id}")

    def test_get_user_password(db_session, app_database):
        password = app_database.get_user_password(TestDatabase.USERNAME)
        assert password == TestDatabase.PASSWORD
        print(f"password: {password}")

    def test_save_expense(db_session, app_database):
        user_id = app_database.get_user_id(username=TestDatabase.USERNAME)
        _name = "expense 1"
        _amount = 100.00
        app_database.save_expense(
            user_id,
            expense_name=_name,
            expense_amount=_amount)
        expenses = app_database.get_user_expenses(user_id)
        expense = expenses[0]
        assert expense.name == _name
        assert expense.amount == _amount
