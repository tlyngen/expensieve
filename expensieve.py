import sys
import logging

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog, QMessageBox
)

from database.dao import Database
from ui import Ui_MainWindow, Ui_DialogExpense, Ui_DialogLogin
from exceptions import LoginException, AuthenticationFailureException


class ExpensieveApp(object):

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.db = Database(self.config["database"])
        self.db.create_tables()
        self.app = QApplication([])

    def run(self):
        self.logger.info("Expensieve app running")
        # self.db_test()
        user = self.user_login()
        if user:
            self.load_main_form(user)
        else:
            self.app.quit()
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
            return user
        else:
            raise AuthenticationFailureException(
                "Incorrect username or password"
            )

    def create_user(self, user, password):
        self.logger.info("creating new user")
        self.db.create_user(username=user, password=password)
        return user

    def load_main_form(self, user):
        self.logger.info("loading main form")
        window = Window(self.db, user)
        window.show()
        self.app.exec()

    def db_test(self):
        self.db.drop_tables()
        self.db.create_tables()
        self.db.create_user(username="tlyngen", password="hello")
        password = self.db.get_user_password("tlyngen")
        self.logger.info(f"user password: {password}")
        self.db.create_user(username="tlyngen", password="hello")


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, database, user, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.database = database
        self.active_user = user
        self.setupUi(self)
        self.setWindowTitle(f"{self.windowTitle()} - {self.active_user}")
        self.pushButtonNewExpense.clicked.connect(self.new_expense)

    def new_expense(self):
        dialog = ExpenseDialog(self)
        if dialog.exec():
            name, amount = dialog.get_inputs()
            self.logger.debug(f"name: {name} amount: {amount}")
            self.database.save_expense(
                username=self.active_user,
                expense_name=name,
                expense_amount=amount)


class ExpenseDialog(QDialog, Ui_DialogExpense):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButtonCancel.clicked.connect(self.close)

    def get_inputs(self):
        name = self.lineEditExpenseName.text()
        amount = float(self.lineEditExpenseAmount.text())
        return name, amount


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
