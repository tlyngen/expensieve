import pytest

from PyQt5.QtWidgets import QApplication
from ui import MainWindow


@pytest.fixture(scope="function")
def setup_application():
    app = QApplication([])
    yield app


def test_user_login(setup_application):
    dialog = MainWindow()
    result = dialog.exec()
    assert result
    user, password = dialog.get_inputs()
    assert user == _username
    assert password == _password
