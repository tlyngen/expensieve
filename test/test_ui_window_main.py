import pytest

from PyQt5.QtWidgets import QApplication
from ui import MainWindow


def test_user_login():
    app = QApplication([])
    window = MainWindow(user="test")
    window.show()
    assert window
    title = window.windowTitle()
    assert title == "Expensieve - test"
