import logging

from PyQt5.QtWidgets import QMainWindow
from ui.qt.ui_main_window import Ui_MainWindow
from ui.expense_dialog import ExpenseDialog
from database import Database


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.database = Database.instance()
        self.logger.debug(f"database instance: {self.database}")
        self.user = user
        self.setupUi(self)
        self.setWindowTitle(f"{self.windowTitle()} - {self.user}")
        self.pushButtonNewExpense.clicked.connect(self.new_expense)
        self.update_expense_list()

    def new_expense(self):
        dialog = ExpenseDialog(self)
        if dialog.exec():
            name, amount = dialog.get_inputs()
            self.logger.debug(f"name: {name} amount: {amount}")
            user_id = self.database.get_user_id(self.user)
            self.database.save_expense(
                user_id=user_id,
                expense_name=name,
                expense_amount=amount)
            self.update_expense_list()

    def update_expense_list(self):
        user_id = self.database.get_user_id(self.user)
        expenses = self.database.get_user_expenses(user_id)
        self.listWidgetExpenses.clear()
        exp = [ex.__repr__() for ex in expenses]
        self.listWidgetExpenses.addItems(exp)
        self.labelTotalExpensesValue.setText(str(expenses.get_expense_total()))
