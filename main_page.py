from PyQt6 import QtWidgets, uic, QtCore, QtGui
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import  FigureCanvasQTAgg as FigureCanvas
import sqlite3
from PyQt6.QtWidgets import QTableWidgetItem
from donate_form import DonateForm
from requests_form import RequestForm


class SubWindow(QtWidgets.QMainWindow):
    def __init__(self, ui_file):
        super().__init__()
        uic.loadUi(ui_file, self)
        self.setWindowTitle("Blood C+")

        self.ok_button = self.findChild(QtWidgets.QPushButton, "okButton")
        if self.ok_button:
            self.ok_button.clicked.connect(self.close)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("blood.ui", self)

        self.chart_layout = self.findChild(QtWidgets.QVBoxLayout, "bargraph")

        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setMinimumSize(335, 330)
        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        if self.chart_layout:
            self.chart_layout.addWidget(self.canvas)

        self.load_blood_inventory()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.load_blood_inventory)
        self.timer.start(10000)


        self.about_us_button = self.findChild(QtWidgets.QPushButton, "aboutUsBtn")
        self.preparation_button = self.findChild(QtWidgets.QPushButton, "preperationBtn")
        self.important_button = self.findChild(QtWidgets.QPushButton, "whyImportantBtn")
        self.who_button = self.findChild(QtWidgets.QPushButton, "whoCanDonateBtn")

        self.donate_button = self.findChild(QtWidgets.QPushButton, "donateBtn")
        self.request_button = self.findChild(QtWidgets.QPushButton, "requestBtn")

        if self.about_us_button:
            self.about_us_button.clicked.connect(lambda: self.open_subwindow("about.ui"))
        if self.preparation_button:
            self.preparation_button.clicked.connect(lambda: self.open_subwindow("preparation.ui"))
        if self.important_button:
            self.important_button.clicked.connect(lambda: self.open_subwindow("why_donate.ui"))
        if self.who_button:
            self.who_button.clicked.connect(lambda: self.open_subwindow("who_can.ui"))
        if self.donate_button:
            self.donate_button.clicked.connect(lambda: self.open_subwindow("donateform.ui"))
        if self.request_button:
            self.request_button.clicked.connect(lambda: self.open_subwindow("request_blood.ui"))

    def open_subwindow(self, ui_file):
        if ui_file == "donateform.ui":
            self.window = DonateForm()
        elif ui_file == "request_blood.ui":
            self.window = RequestForm()
        else:
            self.window = SubWindow(ui_file)
        self.window.show()

    def load_blood_inventory(self):
        conn = sqlite3.connect("blood_donation_db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "Blood Inventory" ORDER BY "Blood type"')
        rows = cursor.fetchall()
        conn.close()

        self.table = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        if self.table:
            self.table.clearContents()
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(["Blood Type", "Quantity", "Matching Bloods"])

            blood_types = []
            quantities = []
            for row_idx, row_data in enumerate(rows):
                blood_types.append(row_data[0])
                quantities.append(row_data[1])
                for col_idx, value in enumerate(row_data):
                   item = QTableWidgetItem(str(value))
                   item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                   item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                   self.table.setItem(row_idx, col_idx, item)


            self.ax.clear()
            x_pos = range(len(blood_types))
            self.ax.bar(x_pos, quantities, color='#000080')
            self.ax.set_title("Blood Type Inventory")
            self.ax.set_xlabel("Blood Type")
            self.ax.set_ylabel("Quantity")
            self.ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
            self.ax.set_xticks(x_pos)
            self.ax.set_xticklabels(blood_types, rotation=45, ha="right")
            self.canvas.draw()



            self.table.setColumnWidth(0, 80)
            self.table.setColumnWidth(1, 65)
            self.table.setColumnWidth(2, 180)

            self.table.setMinimumHeight(310)

            self.table.setFixedWidth(330)

            self.table.verticalHeader().setDefaultSectionSize(30)
            self.table.horizontalHeader().setFixedHeight(40)

            self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

            self.table.verticalHeader().setVisible(False)

            header_font = QtGui.QFont("Arial", 11, QtGui.QFont.Weight.Bold)
            self.table.horizontalHeader().setFont(header_font)

            cell_font = QtGui.QFont("Arial", 10)
            self.table.setFont(cell_font)

            self.table.horizontalHeader().setStretchLastSection(True)


            self.table.setStyleSheet("""
                QTableWidget {
                    background-color: white;
                    font-size: 12px;
                    font-family: 'Arial';
                    color: #000040;
                    gridline-color: #ccc;
                    border: none;
                }
                QHeaderView::section {
                    background-color: #b30000;
                    color: white;
                    font-weight: bold;
                    font-size: 11px;
                    padding: 6px;
                    border: none;
                }
            """)


