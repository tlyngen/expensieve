from PyQt5.QtWidgets import QDialog
from ui.qt.ui_expense_dialog import Ui_DialogExpense


class ExpenseDialog(QDialog, Ui_DialogExpense):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.lineEditExpenseName.setFocus()
        self.pushButtonCancel.clicked.connect(self.close)

    def get_inputs(self):
        name = self.lineEditExpenseName.text()
        amount = float(self.lineEditExpenseAmount.text())
        return name, amount
