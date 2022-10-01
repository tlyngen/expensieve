import logging

from PyQt5.QtWidgets import QMainWindow, QDialog
from ui.qt.ui_main_window import Ui_MainWindow
from ui.expense_dialog import ExpenseDialog


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, database, user, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.database = database
        self.active_user = user
        self.active_user_id = self.database.get_user_id(self.active_user)
        self.setupUi(self)
        self.setWindowTitle(f"{self.windowTitle()} - {self.active_user}")
        self.pushButtonNewExpense.clicked.connect(self.new_expense)
        self.update_expense_list()

    def new_expense(self):
        dialog = ExpenseDialog(self)
        if dialog.exec():
            name, amount = dialog.get_inputs()
            self.logger.debug(f"name: {name} amount: {amount}")
            self.database.save_expense(
                user_id=self.active_user_id,
                expense_name=name,
                expense_amount=amount)
            self.update_expense_list()

    def update_expense_list(self):
        expenses = self.database.get_user_expenses(self.active_user_id)
        self.listWidgetExpenses.clear()
        exp = [ex.__repr__() for ex in expenses]
        self.listWidgetExpenses.addItems(exp)
        total = 0
        for ex in expenses:
            total += ex.amount
        self.labelTotalExpensesValue.setText(str(total))
