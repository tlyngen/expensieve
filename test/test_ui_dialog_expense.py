from PyQt5.QtWidgets import QApplication
from ui import ExpenseDialog


def test_user_login():
    app = QApplication([])
    dialog = ExpenseDialog()
    dialog.show()
    assert dialog
