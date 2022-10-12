from PyQt5.QtWidgets import QApplication
from ui import ExpenseDialog


def test_user_expense():
    app = QApplication([])
    dialog = ExpenseDialog()
    dialog.show()
    assert dialog
