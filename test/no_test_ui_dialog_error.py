import pytest

from PyQt5.QtWidgets import QApplication
from ui import ErrorDialog


@pytest.fixture(scope="function")
def setup_application():
    app = QApplication([])
    yield app


# modal dialog difficult to test. consider refactor for better testing
def test_error_dialog(setup_application):
    message = "error message"
    dialog = ErrorDialog.show_error_message(message)
    assert not dialog, "dialog exists when it should be out of scope"
