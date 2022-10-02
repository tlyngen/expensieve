import pytest

from PyQt5.QtWidgets import QApplication
from ui import LoginDialog


@pytest.fixture(scope="function")
def setup_application():
    app = QApplication([])
    yield app


def test_user_login(setup_application):
    _username = "test_user"
    _password = "test_password"
    dialog = LoginDialog(test=True, username=_username, password=_password)
    result = dialog.exec()
    assert result
    user, password = dialog.get_inputs()
    assert user == _username
    assert password == _password
