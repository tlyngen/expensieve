from ast import For
from email.policy import default
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (Column, Integer, Float, String, Boolean, ForeignKey)
from sqlalchemy.dialects.sqlite import DATETIME
from datetime import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    expense = relationship("Expense")
    user_expense = relationship("UserExpense")

    def __repr__(self):
        return \
            f"id={self.id}, "\
            f"username={self.username}, "\
            f"password={self.password}"


class Expense(Base):
    __tablename__ = 'expense'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    name = Column(String)
    amount = Column(Float)
    split_type = Column(String)
    open = Column(Boolean, default=True)
    date = Column(DATETIME, default=datetime.now())

    user = relationship("User", viewonly=True)

    def __repr__(self):
        return \
            f"id={self.id}, "\
            f"user_id={self.user_id}, "\
            f"name={self.name}, "\
            f"amount={self.amount}, "\
            f"split_type={self.split_type}, "\
            f"open={self.open}, "\
            f"date={self.date}"


class UserExpense(Base):
    __tablename__ = 'user_expense'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    expense_id = Column(Integer, ForeignKey("expense.id"))
    amount = Column(Float)
    amount_paid = Column(Integer)

    user = relationship("User", viewonly=True)
    expense = relationship("Expense", viewonly=True)

    def __repr__(self):
        return \
            f"user_id={self.user_id}, "\
            f"expense_id={self.expense_id}, "\
            f"amount={self.amount}, "\
            f"amount_paid={self.amount_paid}"
