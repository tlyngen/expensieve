from ast import For
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (Column, Integer, Float, String, Boolean, ForeignKey)
from sqlalchemy.dialects.sqlite import DATETIME


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    expense = relationship("Expense")
    user_expense = relationship("UserExpense")

    def __repr__(self):
        return f"{self.id}, {self.username}, {self.password}"


class Expense(Base):
    __tablename__ = 'expense'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    amount = Column(Float)
    split_type = Column(String)
    open = Column(Boolean)
    date = Column(DATETIME)

    user = relationship("User", viewonly=True)

    def __repr__(self):
        return f"""
            {self.id},
            {self.user_id},
            {self.amount},
            {self.split_type},
            {self.open},
            {self.date}"""


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
        return f"""
            {self.user_id},
            {self.user_id},
            {self.expense_id},
            {self.amount},
            {self.amount_paid}"""
