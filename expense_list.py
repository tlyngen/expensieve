from typing import Type
from dataclass import ExpenseData
from collections import UserList


class ExpenseList(UserList):

    def __init__(self, expense_list=None):
        super().__init__(self._validate_list(expense_list))

    def append(self, expense: ExpenseData):
        return self.data.append(self._validate_type(expense))

    def get_expense_total(self):
        sum = 0.0
        for ex in self.data:
            sum += ex.amount
        return sum

    def _validate_type(self, item):
        if not item:
            return item

        if not isinstance(item, ExpenseData):
            raise TypeError(
                f"Expected: ExpenseData. Got: {type(item).__name__}")
        return item

    def _validate_list(self, item_list):
        if not item_list:
            return item_list

        if not isinstance(item_list, list):
            return TypeError(f"Expected list. Got {type(item_list).__name__}")

        for item in item_list:
            self._validate_type(item)

        return item_list
