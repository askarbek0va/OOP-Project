from PyQt6 import QtWidgets, uic,QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton,QMainWindow
import sqlite3
from datetime import datetime
from PyQt6.QtGui import QMovie
from form_window import FormWindow


class RequestForm(FormWindow):
    def __init__(self):
        super().__init__("request_blood.ui", "patient.gif")

        self.label = self.findChild(QtWidgets.QLabel, "label")
        self.label.setScaledContents(True)

        self.movie = QMovie("patient.gif")
        self.label.setMovie(self.movie)
        self.movie.start()

        self.submit_button = self.findChild(QtWidgets.QPushButton, "submitButton")
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
            conn = sqlite3.connect("blood_donation_db")
            cursor = conn.cursor()

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                INSERT INTO Requests (Hospital, City, "Blood type", status,timestamp)
                VALUES (?, ?, ?, 'pending',?)
            """, (hospital, city, blood_type,now))
            conn.commit()

            cursor.execute("""
                SELECT * FROM Donors
                WHERE "Blood type" = ?
            """, (blood_type,))
            all_donors = cursor.fetchall()

            if not all_donors:
                self.show_warning( "No Donor Found", "No donor with this blood type available.")
                conn.close()
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

            for donor in all_donors:
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

            conn.close()

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
                conn = sqlite3.connect("blood_donation_db")
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT rowid FROM Requests 
                    WHERE Hospital = ? AND "Blood type" = ? AND status = 'pending' 
                    ORDER BY rowid DESC LIMIT 1
                """, (hospital, blood_type))
                latest_request_id = cursor.fetchone()[0]


                cursor.execute("""
                    UPDATE Requests
                    SET status = 'fulfilled'
                    WHERE rowid = ?
                """, (latest_request_id,))
                conn.commit()

                cursor.execute("DELETE FROM Donors WHERE ID = ?", (donor_id,))

                cursor.execute("""
                    UPDATE [Blood Inventory]
                    SET Quantity = Quantity - 1
                    WHERE "Blood type" = ? AND Quantity > 0
                """, (blood_type,))

                conn.commit()
                conn.close()

                self.show_information( "Done", "Donor has been successfully requested.")

                self.matching_window.close()
                self.close()

            except Exception as e:
                self.show_critical( "Error", str(e))

