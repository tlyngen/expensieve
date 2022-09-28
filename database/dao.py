import logging

from .models import Base, User, Expense, UserExpense

from sqlalchemy import create_engine, select, insert, update
from database.session import Session
from exceptions import BlankUsernameOrPasswordException, BlankExpenseException


class Database:

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)

        # duplicate db logger debug statements
        # loggers = [logging.getLogger(name)
        #   for name in logging.root.manager.loggerDict]
        # self.logger.debug("*** loggers ***")
        # for logger in loggers:
        #    self.logger.debug(logger)

        self.config = config
        self.connection_string = self._create_conn_string()
        self.engine = create_engine(self.connection_string,
                                    echo=self.config["sql_echo"])

    def _create_conn_string(self):
        conn_str = "sqlite:///./database/expensieve.db"
        return conn_str

    def create_tables(self):
        self.logger.info("creating tables")
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        self.logger.info("dropping tables")
        Base.metadata.drop_all(self.engine)

    def get_user_password(self, username):
        self.logger.info(f"get_user_password: {username}")
        with Session(self.engine) as session:
            stmt = select(User.password).where(User.username == username)
            result = session.execute(stmt)
            password = result.scalar_one_or_none()
            self.logger.info(f"password: {password}")
            return password

    def get_user_id(self, username):
        self.logger.info(f"get_user_id: {username}")
        with Session(self.engine) as session:
            stmt = select(User.id).where(User.username == username)
            result = session.execute(stmt)
            id = result.scalar_one_or_none()
            self.logger.info(f"id: {id}")
            return id

    def create_user(self, username, password):
        if not username or not password:
            raise BlankUsernameOrPasswordException(
                "blanks not permitted for username or password")
        self.logger.info(f"create_user: {username} {password}")
        with Session(self.engine) as session:
            stmt = select(User.password).where(User.username == username)
            result = session.execute(stmt)
            _username = result.scalar_one_or_none()
            if _username:
                self.logger.info(f"user exists: {username}")
            else:
                new_user = User(username=username, password=password)
                session.add(new_user)
                self.logger.info(f"created user: {username}")

    def save_expense(self, username, expense_name, expense_amount):
        if not username or not expense_name or not expense_amount:
            raise BlankExpenseException(
                "blanks not permitted for expense name or amount")
        self.logger.info(f"""save_expense:
            {username} {expense_name} {expense_amount}""")
        user_id = self.get_user_id(username)
        expense = Expense()
        expense.user_id = user_id
        expense.name = expense_name
        expense.amount = expense_amount
        self.logger.debug(f"saving expense: {expense}")
        with Session(self.engine) as session:
            session.add(expense)
