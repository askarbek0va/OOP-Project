from PyQt6 import QtWidgets,uic
from PyQt6.QtWidgets import QMessageBox, QMainWindow
from PyQt6.QtGui import QMovie
from datetime import datetime

class FormWindow(QMainWindow):
    def __init__(self, ui_file, gif_file):
        super().__init__()
        uic.loadUi(ui_file, self)

        # Общие элементы
        self.label = self.findChild(QtWidgets.QLabel, "label")
        self.label.setScaledContents(True)

        self.movie = QMovie(gif_file)
        self.label.setMovie(self.movie)
        self.movie.start()

        self.submit_button = self.findChild(QtWidgets.QPushButton, "submitBtn")
        self.submit_button.clicked.connect(self.handle_submit)

    def handle_submit(self):
        raise NotImplementedError("This method should be overridden in child classes")

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)

    def show_critical(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_information(self, title, message):
        QMessageBox.information(self, title, message)
