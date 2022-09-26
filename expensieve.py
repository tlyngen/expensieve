from dataclasses import dataclass
import logging

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog, QMessageBox
)

from database.dao import Database
from ui import Ui_MainWindow, Ui_DialogExpense, Ui_DialogLogin
from exceptions import LoginException, AuthenticationFailureException


class ExpensieveApp(object):
    VERSION = "0.1"

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.logger.info(f"Expensieve {self.VERSION}")
        self.logger.info(f"config {self.config['version']}")
        self.db = Database(self.config["database"])
        self.app = QApplication([])

    def run(self):
        self.logger.info("Expensieve app running")
        if self.user_login():
            self.load_main_form()
        self.logger.info("Expensieve app exiting")

    def user_login(self):
        dialog = LoginDialog()
        result = dialog.exec()
        self.logger.debug(result)
        if result:
            user, password = dialog.get_inputs()
            self.logger.debug(f"{user} {password}")
        try:
            if dialog.is_create_user():
                return self.create_user(user, password)
            else:
                return self.authenticate_user(user, password)
        except LoginException as le:
            self.error_message(str(le))

    def error_message(self, message):
        error = QMessageBox()
        error.setWindowTitle("Error")
        error.setText(message)
        error.exec()

    def authenticate_user(self, user, password):
        self.logger.info("authenticating user")
        pw = self.db.get_user_password(user)
        if pw == password:
            self.logger.info("authentication successful")
            return True
        else:
            raise AuthenticationFailureException(
                "Incorrect username or password"
            )

    def create_user(self, user, password):
        self.logger.info("creating new user")
        self.db.create_user(username=user, password=password)
        return True

    def load_main_form(self):
        self.logger.info("loading main form")
        window = Window(self.db)
        window.show()
        self.app.exec()

    def db_test(self):
        self.db.drop_tables()
        self.db.create_tables()
        self.db.create_user(username="tlyngen", password="hello123")
        password = self.db.get_user_password("tlyngen")
        self.logger.info(f"user password: {password}")
        self.db.create_user(username="tlyngen", password="hello123")


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, database, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.database = database
        self.setupUi(self)
        self.pushButtonNewExpense.clicked.connect(self.new_expense)

    def new_expense(self):
        dialog = ExpenseDialog(self)
        dialog.exec()


class ExpenseDialog(QDialog, Ui_DialogExpense):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButtonCancel.clicked.connect(self.close)


class LoginDialog(QDialog, Ui_DialogLogin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.create_user = False
        self.pushButtonCreate.clicked.connect(self.set_create_user)

    def set_create_user(self):
        self.create_user = True

    def is_create_user(self):
        return self.create_user

    def get_inputs(self):
        user = self.lineEditUserName.text()
        password = self.lineEditPassword.text()
        return user, password
