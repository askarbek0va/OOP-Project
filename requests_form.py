from PyQt6 import QtWidgets, uic,QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton,QMainWindow
import sqlite3
from datetime import datetime
from PyQt6.QtGui import QMovie
from form_window import FormWindow
from requests_dao import RequestsDAO
from blood_inventory import BloodInventoryDAO
from donors_dao import DonorsDAO


class RequestForm(FormWindow):
    def __init__(self):
        super().__init__("request_blood.ui", "patient.gif")

        self.dao_request=RequestsDAO()
        self.dao_inventory = BloodInventoryDAO()
        self.dao_donor=DonorsDAO()

        self.label = self.findChild(QtWidgets.QLabel, "label")
        self.label.setScaledContents(True)

        self.movie = QMovie("patient.gif")
        self.label.setMovie(self.movie)
        self.movie.start()

        self.submit_button = self.findChild(QtWidgets.QPushButton, "submitBtn")
        self.hospital_input = self.findChild(QtWidgets.QLineEdit, "hospitalNameInput")
        self.city_input = self.findChild(QtWidgets.QLineEdit, "cityInput")
        self.bloodtype_input = self.findChild(QtWidgets.QComboBox, "requestedBloodCombo")

        self.submit_button.clicked.connect(self.handle_submit)

    def handle_submit(self):
        hospital = self.hospital_input.text()
        city = self.city_input.text()
        blood_type = self.bloodtype_input.currentText()

        if not hospital or not city:
            self.show_warning("Error", "Please fill all fields.")
            return

        try:
            self.dao_request.add_request(hospital, city, blood_type)

            matching_donors = self.dao_request.get_donors_by_blood_type(blood_type)

            if not matching_donors:
                self.show_warning( "No Donor Found", "No donor with this blood type available.")

                return

            self.matching_window = QtWidgets.QMainWindow()
            self.matching_window.setWindowTitle("Matching Donors")

            table = QtWidgets.QTableWidget()
            table.setColumnCount(7)
            table.setHorizontalHeaderLabels(
                ["Name", "Age", "Blood Type", "Last Donation", "Location", "Contacts", "Request"])

            table.setStyleSheet("""
                QTableWidget {
                    background-color: white;
                    color: rgb(0,0,128);
                    font-size: 14px;
                    font-family:'Arial';
                    gridline-color: #dddddd;
                }
                QHeaderView::section {
                    background-color: #b30000;
                    color: white;
                    font-weight: bold;
                    padding: 8px;
                    border: none;
                    font-family: 'Arial';
                    font-size: 15px;
                }

                QHeaderView::section:vertical {
                    background-color: white;
                    color: black;
                    border: none;
                    font-size: 14px;
                    font-family: 'Arial';
                }

                QTableWidget::item {
                    padding: 6px;
                }
            """)

            table.setRowCount(0)

            for donor in matching_donors:
                last_date = datetime.strptime(donor[4], "%Y-%m-%d").date()
                days_since = (datetime.today().date() - last_date).days

                if days_since >= 90:
                    row = table.rowCount()
                    table.insertRow(row)

                    table.setItem(row, 0, QTableWidgetItem(donor[1]))  # Name
                    table.setItem(row, 1, QTableWidgetItem(str(donor[2])))  # Age
                    table.setItem(row, 2, QTableWidgetItem(donor[3]))  # Blood type
                    table.setItem(row, 3, QTableWidgetItem(donor[4]))  # Last donation
                    table.setItem(row, 4, QTableWidgetItem(donor[5]))  # Location
                    table.setItem(row, 5, QTableWidgetItem(donor[6]))  # Contacts

                    for col, value in enumerate([donor[1], str(donor[2]), donor[3], donor[4], donor[5], donor[6]]):
                        item = QTableWidgetItem(value)
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                        table.setItem(row, col, item)


                    request_btn = QPushButton("Request")
                    request_btn.setStyleSheet("""
                            QPushButton {
                                background-color: rgb(0,0,128);
                                color: white;
                                font-weight: bold;
                                font-size: 14px;
                                font-family: 'Arial';
                            }
                            QPushButton:hover {
                                background-color: #ffcccc;
                                color: #800000;
                            }
                            QPushButton:pressed {
                                background-color: #ffe6e6;
                            }
                    """)
                    request_btn.setFixedWidth(110)
                    request_btn.setFixedHeight(34)

                    request_btn.clicked.connect(
                        lambda _, donor_id=donor[0]: self.confirm_request(donor_id, hospital, blood_type, table))
                    table.setCellWidget(row, 6, request_btn)

            table.resizeColumnsToContents()
            table.resizeRowsToContents()
            table.horizontalHeader().setStretchLastSection(True)
            table.adjustSize()
            self.matching_window.adjustSize()

            self.matching_window.setCentralWidget(table)
            self.matching_window.resize(850, 350)
            self.matching_window.show()


            self.hospital_input.clear()
            self.city_input.clear()
            self.bloodtype_input.setCurrentIndex(0)

        except Exception as e:
            self.show_critical( "Database Error", str(e))

    def confirm_request(self, donor_id, hospital, blood_type, table):
        reply = QMessageBox.question(self, "Confirm", "Are you sure you want to select this donor?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.dao_request.fulfill_latest_pending_request(hospital, blood_type)

                self.dao_donor.delete_by_id(donor_id)

                self.dao_inventory.update_blood_inventory_minus(blood_type)


                self.show_information( "Done", "Donor has been successfully requested.")

                self.matching_window.close()
                self.close()

            except Exception as e:
                self.show_critical( "Error", str(e))

