import logging

from database.dao import Database
from ui import MainWindow, LoginDialog, ErrorDialog
from exceptions import LoginException, AuthenticationFailureException
from PyQt5.QtWidgets import QApplication


class ExpensieveApp(object):

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.db = Database.instance()
        self.logger.debug(f"database instance: {self.db}")
        self.db.create_tables()
        self.app = QApplication([])

    def run(self):
        self.logger.info("Expensieve app running")
        user = self.user_login()
        if user:
            self.load_main_form(user)
        else:
            self.app.quit()
        self.logger.info("Expensieve app exiting")

    def user_login(self):
        dialog = LoginDialog()
        result = dialog.exec()
        user = None
        password = None
        if result:
            user, password = dialog.get_inputs()
            self.logger.debug(f"{user} {password}")
            try:
                if dialog.is_create_user():
                    return self.create_user(user, password)
                else:
                    return self.authenticate_user(user, password)
            except LoginException as le:
                ErrorDialog.show_error_message(str(le))
        else:
            self.logger.info("no result from user login")

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
        window = MainWindow(user)
        window.show()
        self.app.exec()
