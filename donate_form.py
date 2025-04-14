from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QMainWindow,QPushButton
import sqlite3
from datetime import datetime,date
from PyQt6.QtGui import QMovie

from blood_inventory import BloodInventoryDAO
from form_window import FormWindow
from donors_dao import DonorsDAO


class DonateForm(FormWindow):
    def __init__(self):
        super().__init__("donateform.ui", "blood-donation.gif")

        self.dao_donors=DonorsDAO()
        self.dao_inventory=BloodInventoryDAO()

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
        self.__contacts_input = self.findChild(QtWidgets.QLineEdit, "ContactsLineEdit")
        self.checkbox = self.findChild(QtWidgets.QCheckBox, "checkBox")
        self.submit_button = self.findChild(QtWidgets.QPushButton, "submitBtn")

        self.ok_button = self.findChild(QtWidgets.QPushButton, "okButton")

        self.submit_button.clicked.connect(self.handle_submit)

    def set_contacts_input(self,contacts):
        self.__contacts_input=contacts

    def get_contacts_input(self):
        return self.__contacts_input


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
        contacts = self.__contacts_input.text()

        standardized_name = name.strip().lower()


        if not name or not location or not contacts:
            self.show_warning("Error", "Please fill all fields.")

        try:
            age = int(age)
            if age < 18 or age > 60:
                self.show_warning("Error", "Age should be from 18 to 60")
        except ValueError:
            self.show_warning( "Error", "Age should be a number")


        if not self.checkbox.isChecked():
            self.show_warning( "Error", "Please confirm the checkbox before submitting.")



        name_parts = standardized_name.split()
        if len(name_parts) != 2:
            self.show_warning( "Error", "Please enter both first name and last name.")
            return

        first_name, last_name = name_parts
        first_name = first_name.strip()
        last_name = last_name.strip()

        name_variant_1 = f"{first_name} {last_name}"
        name_variant_2 = f"{last_name} {first_name}"

        try:

            if  self.dao_donors.donor_exists(name_variant_1, name_variant_2, contacts, blood_type):
                self.show_warning( "Error", "This donor is already registered.")

            else:
                 self.dao_donors.add_donor(name,age,blood_type, last_donation,location,contacts)
                 self.dao_inventory.update_blood_inventory(blood_type)

            self.dao_donors.close()


            self.name_input.clear()
            self.birthdate_input.clear()
            self.bloodtype_input.clear()
            self.last_donation_input.clear()
            self.location_input.clear()
            self.__contacts_input.clear()
            self.checkbox.setChecked(False)


            self.open_thank_you_window()

        except Exception as e:
            self.show_critical("Error", f"Database error: {str(e)}")

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
