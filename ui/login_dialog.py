from PyQt5.QtWidgets import QDialog
from ui.qt.ui_login_dialog import Ui_DialogLogin


class LoginDialog(QDialog, Ui_DialogLogin):
    def __init__(self, parent=None, test=False, username=None, password=None):
        super().__init__(parent)
        self.setupUi(self)
        self.lineEditUserName.setFocus()
        self.create_user = False
        self.pushButtonCreate.clicked.connect(self.set_create_user)
        if test:
            self.test_dialog(username, password)

    def set_create_user(self):
        self.create_user = True

    def is_create_user(self):
        return self.create_user

    def get_inputs(self):
        user = self.lineEditUserName.text()
        password = self.lineEditPassword.text()
        return user, password

    def test_dialog(self, username, password):
        self.lineEditUserName.setText(username)
        self.lineEditPassword.setText(password)
        self.pushButtonLogin.click()
