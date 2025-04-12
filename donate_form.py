from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QMainWindow,QPushButton
import sqlite3
from datetime import datetime,date
from PyQt6.QtGui import QMovie


class DonateForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("donateform.ui", self)

        self.label = self.findChild(QtWidgets.QLabel, "label")
        self.label.setScaledContents(True)

        self.movie = QMovie("blood-donation.gif")
        self.label.setMovie(self.movie)
        self.movie.start()


        self.name_input = self.findChild(QtWidgets.QLineEdit, "nameLineEdit")
        self.birthdate_input = self.findChild(QtWidgets.QDateEdit, "birthDateEdit")
        self.bloodtype_input = self.findChild(QtWidgets.QComboBox, "bloodTypeComboBox")
        self.last_donation_input = self.findChild(QtWidgets.QDateEdit, "lastDonationDateEdit")
        self.location_input = self.findChild(QtWidgets.QLineEdit, "locationLineEdit")
        self.contacts_input = self.findChild(QtWidgets.QLineEdit, "ContactsLineEdit")
        self.checkbox = self.findChild(QtWidgets.QCheckBox, "checkBox")
        self.submit_button = self.findChild(QtWidgets.QPushButton, "submitBtn")

        self.ok_button = self.findChild(QtWidgets.QPushButton, "okButton")

        self.submit_button.clicked.connect(self.handle_submit)

    def handle_submit(self):

        name = self.name_input.text()
        birth_qdate = self.birthdate_input.date()
        birthdate_str = birth_qdate.toString("yyyy-MM-dd")
        birthdate_obj = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - birthdate_obj.year - ((today.month, today.day) < (birthdate_obj.month, birthdate_obj.day))

        blood_type = self.bloodtype_input.currentText()
        last_donation = self.last_donation_input.date().toString("yyyy-MM-dd")
        location = self.location_input.text()
        contacts = self.contacts_input.text()

        if not name or not location or not contacts:
            QMessageBox.warning(self, "Error", "All fields must be filled.")
            return

        try:
            age = int(age)
            if age < 18 or age > 60:
                QMessageBox.warning(self, "Error", "Age should be from 18 to 60")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "Age should be a number")
            return

        if not self.checkbox.isChecked():
            QMessageBox.warning(self, "Error", "Please confirm the checkbox before submitting.")
            return


        try:
            conn = sqlite3.connect("blood_donation_db")
            cursor = conn.cursor()


            cursor.execute('''
                INSERT INTO Donors ('Name','Age' , 'Blood type', 'Last donation date', 'Location', 'Contacts')
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, age, blood_type, last_donation, location, contacts))

            cursor.execute('''
                            INSERT INTO AllDonors ('Name','Age' , 'Blood type', 'Last donation date', 'Location', 'Contacts')
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (name, age, blood_type, last_donation, location, contacts))

            cursor.execute('''
                UPDATE "Blood Inventory"
                SET Quantity = Quantity + 1
                WHERE "Blood type" = ?
            ''', (blood_type,))

            conn.commit()
            conn.close()


            self.name_input.clear()
            self.birthdate_input.clear()
            self.bloodtype_input.clear()
            self.last_donation_input.clear()
            self.location_input.clear()
            self.contacts_input.clear()
            self.checkbox.setChecked(False)


            self.open_thank_you_window()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")

    def open_thank_you_window(self):
        self.donate_window = self

        self.thank_window = QMainWindow()
        uic.loadUi("thank.ui", self.thank_window)

        self.ok_button = self.thank_window.findChild(QPushButton, "okButton")

        self.ok_button.clicked.connect(self.close_window)

        self.thank_window.show()

    def close_window(self):
        self.thank_window.close()
        self.donate_window.close()
