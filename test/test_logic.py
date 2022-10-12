from expense_list import ExpenseList
from dataclass import ExpenseData


def test_empty_insantiation():
    ex_list = ExpenseList()
    assert len(ex_list) == 0


def test_list_instatiation():
    ex1 = ExpenseData(name="foo", amount=0)
    ex2 = ExpenseData(name="bar", amount=0)
    ex_list = ExpenseList([ex1, ex2])
    assert len(ex_list) == 2


def test_list_append():
    ex_list = ExpenseList()
    assert len(ex_list) == 0
    ex = ExpenseData(name="foo", amount=0)
    ex_list.append(ex)
    assert len(ex_list) == 1


def test_expense_total():
    expenses = ExpenseList()
    expenses.append(ExpenseData(name="foo", amount=123))
    expenses.append(ExpenseData(name="bar", amount=321))
    total = expenses.get_expense_total()
    assert total == 444.0
