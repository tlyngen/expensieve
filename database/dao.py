import logging

from .models import Base, User, Expense, UserExpense

from sqlalchemy import create_engine, select, insert, update
from database.session import Session
from exceptions import BlankUsernameOrPasswordException, BlankExpenseException
from dataclass import ExpenseData


class Database:
    def __init__(self, echo=False):
        self.logger = logging.getLogger(__name__)
        self.connection_string = self._create_conn_string()
        self.engine = create_engine(self.connection_string, echo=echo)

    def _create_conn_string(self):
        conn_str = "sqlite:///./database/expensieve.db"
        return conn_str

    def create_tables(self):
        self.logger.info("creating tables")
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        self.logger.info("dropping tables")
        Base.metadata.drop_all(self.engine)

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

    def get_user_id(self, username):
        self.logger.info(f"get_user_id: {username}")
        with Session(self.engine) as session:
            stmt = select(User.id).where(User.username == username)
            result = session.execute(stmt)
            id = result.scalar_one_or_none()
            self.logger.info(f"id: {id}")
            return id

    def get_user_password(self, username):
        self.logger.info(f"get_user_password: {username}")
        with Session(self.engine) as session:
            stmt = select(User.password).where(User.username == username)
            result = session.execute(stmt)
            password = result.scalar_one_or_none()
            self.logger.info(f"password: {password}")
            return password

    def save_expense(self, user_id, expense_name, expense_amount):
        if not user_id or not expense_name or not expense_amount:
            raise BlankExpenseException(
                "blanks not permitted for expense name or amount")
        expense = Expense()
        expense.user_id = user_id
        expense.name = expense_name
        expense.amount = expense_amount
        self.logger.debug(f"saving expense: {expense}")
        with Session(self.engine) as session:
            session.add(expense)

    def get_user_expenses(self, user_id):
        self.logger.info(f"get_user_expenses for user_id: {user_id}")
        with Session(self.engine) as session:
            stmt = select(Expense).where(Expense.user_id == user_id)
            result = session.execute(stmt)
            expenses = result.scalars().all()
            self.logger.info(f"expenses for user_id: {user_id}")
            expense_data = []
            for ex in expenses:
                self.logger.info(ex)
                expense_data.append(self.expense_model_to_data(ex))
            return expense_data

    def expense_model_to_data(self, expense):
        ex = ExpenseData()
        ex.id = expense.id
        ex.user_id = expense.user_id
        ex.name = expense.name
        ex.amount = expense.amount
        ex.split_type = expense.split_type
        ex.open = expense.open
        ex.date = expense.date
        return ex
