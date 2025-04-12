from main_page import MainWindow,SubWindow
from PyQt6 import QtWidgets, uic
import sys


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Blood Donation")
    window.show()
    sys.exit(app.exec())

