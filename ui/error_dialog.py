from PyQt5.QtWidgets import QMessageBox


class ErrorDialog:

    @staticmethod
    def show_error_message(message):
        error = QMessageBox()
        error.setWindowTitle("Error")
        error.setText(message)
        error.exec()
