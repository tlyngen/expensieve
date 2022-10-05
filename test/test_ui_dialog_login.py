import pytest

from PyQt5.QtWidgets import QApplication
from ui import LoginDialog


def test_user_login():
    app = QApplication([])
    dialog = LoginDialog()
    dialog.show()
    assert dialog
