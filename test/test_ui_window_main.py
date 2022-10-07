from ctypes import windll
import pytest

from PyQt5.QtWidgets import QApplication
from ui import MainWindow


@pytest.fixture(scope="module")
def main_window():
    app = QApplication([])
    window = MainWindow(user="test")
    # window.show()
    yield window
    window.close()


def test_main_window(main_window):
    window = main_window
    assert window, "window does not exist"
    title = window.windowTitle()
    assert title == "Expensieve - test", "title did not match required value"


def test_default_summary_values(main_window):
    window = main_window
    value = int(window.labelTotalExpensesValue.text())
    assert value == 0, f"expected 0, got {value}"
    value = int(window.labelOwedToOthersValue.text())
    assert value == 0, f"expected 0, got {value}"
    value = int(window.labelOwedToMeValue.text())
    assert value == 0, f"expected 0, got {value}"
