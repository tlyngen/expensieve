import logging

from .models import Base, User, Expense, UserExpense

from sqlalchemy import create_engine, select, insert, update
from database.session import Session


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
            password = result.scalar_one()
            if password:
                self.logger.info(f"password: {password}")
                return password
            else:
                return None

    def create_user(self, username, password):
        self.logger.info(f"create_user: {username} {password}")
        with Session(self.engine) as session:
            stmt = select(User.username)
            result = session.execute(stmt)
            _username = result.scalar_one_or_none()
            if _username:
                self.logger.info(f"user exists: {username}")
                return
            else:
                new_user = User(username=username, password=password)
                session.add(new_user)
                self.logger.info(f"created user: {username}")
                return
