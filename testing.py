import unittest
from unittest.mock import patch, MagicMock
from donate_form import DonateForm
from PyQt6.QtWidgets import QApplication
import sys
import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import QApplication
from main_page import MainWindow

app = QApplication(sys.argv)

class TestMainWindow(unittest.TestCase):
    def setUp(self):

        self.window = MainWindow()
        self.window.show()


        self.conn = sqlite3.connect("blood_donation_db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            INSERT OR REPLACE INTO [Blood Inventory] ("Blood type", Quantity, "Matching Donor Blood Type")
            VALUES ('A+', 5, 'A+, AB+')
        """)
        self.conn.commit()

    def test_load_blood_inventory(self):
        self.window.load_blood_inventory()
        table = self.window.findChild(type(self.window.table), "tableWidget")
        self.assertIsNotNone(table, "Таблица не найдена")
        self.assertGreaterEqual(table.rowCount(), 1, "Нет строк в таблице после загрузки")

        found = False
        for row in range(table.rowCount()):
            blood_type_item = table.item(row, 0)
            quantity_item = table.item(row, 1)
            if blood_type_item and blood_type_item.text() == 'A+':
                self.assertEqual(quantity_item.text(), '5', "Количество должно быть '5'")
                found = True
                break

        self.assertTrue(found, "Не найдена строка с группой крови 'A+'")

    def tearDown(self):
        self.cursor.execute("DELETE FROM [Blood Inventory] WHERE [Blood type] = 'A+'")
        self.conn.commit()
        self.conn.close()
        self.window.close()

class TestDonateForm(unittest.TestCase):

    def setUp(self):
        self.form = DonateForm()
        self.form.name_input.setText("John Doe")
        self.form.birthdate_input.setDate(self.form.birthdate_input.minimumDate().addYears(25))  # Пример возраста 25 лет
        self.form.bloodtype_input.setCurrentText("A+")
        self.form.last_donation_input.setDate(self.form.last_donation_input.minimumDate())
        self.form.location_input.setText("City")
        self.form.contacts_input.setText("123456789")
        self.form.checkbox.setChecked(True)

    @patch("donate_form.QMessageBox.warning")
    @patch("donate_form.sqlite3.connect")
    def test_successful_submission(self, mock_connect, mock_warning):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        self.form.handle_submit()

        self.assertTrue(mock_cursor.execute.called)
        self.assertTrue(mock_conn.commit.called)
        self.assertFalse(mock_warning.called)

    @patch("donate_form.QMessageBox.warning")
    def test_missing_fields(self, mock_warning):
        self.form.name_input.setText("")  # Нет имени
        self.form.handle_submit()
        mock_warning.assert_called_with(self.form, "Error", "All fields must be filled.")

    @patch("donate_form.QMessageBox.warning")
    def test_invalid_age(self, mock_warning):
        self.form.birthdate_input.setDate(self.form.birthdate_input.maximumDate().addYears(-10))  # Возраст < 18
        self.form.handle_submit()
        mock_warning.assert_called_with(self.form, "Error", "Age should be from 18 to 60")

    @patch("donate_form.QMessageBox.warning")
    def test_checkbox_not_checked(self, mock_warning):
        self.form.checkbox.setChecked(False)
        self.form.handle_submit()
        mock_warning.assert_called_with(self.form, "Error", "Please confirm the checkbox before submitting.")

    @patch("donate_form.QMessageBox.warning")
    def test_name_format_invalid(self, mock_warning):
        self.form.name_input.setText("John")  # Только имя
        self.form.handle_submit()
        mock_warning.assert_called_with(self.form, "Error", "Please enter both first name and last name.")

    @patch("donate_form.QMessageBox.warning")
    @patch("donate_form.sqlite3.connect")
    def test_duplicate_donor(self, mock_connect, mock_warning):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("John Doe",)

        self.form.handle_submit()

        mock_warning.assert_called_with(self.form, "Error", "This donor is already registered.")

DB_PATH = "blood_donation_db"

class TestRequestsForm(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            INSERT INTO Donors (Name, Age, "Blood type", "Last donation date", Location, Contacts)
            VALUES ('Test Donor', 30, 'A+', '2024-12-01', 'TestCity', '123456789')
        """)
        self.donor_id = self.cursor.lastrowid

        self.cursor.execute("""
            INSERT OR IGNORE INTO [Blood Inventory] ("Blood type", Quantity)
            VALUES ('A+', 5)
        """)
        self.conn.commit()

    def test_add_and_fulfill_request(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            INSERT INTO Requests (Hospital, City, "Blood type", status, timestamp)
            VALUES (?, ?, ?, 'pending', ?)
        """, ("Test Hospital", "TestCity", "A+", timestamp))
        request_id = self.cursor.lastrowid
        self.conn.commit()

        self.cursor.execute("SELECT status FROM Requests WHERE rowid = ?", (request_id,))
        status = self.cursor.fetchone()[0]
        self.assertEqual(status, "pending")

        self.cursor.execute("UPDATE Requests SET status = 'fulfilled' WHERE rowid = ?", (request_id,))
        self.conn.commit()

        self.cursor.execute("SELECT status FROM Requests WHERE rowid = ?", (request_id,))
        updated_status = self.cursor.fetchone()[0]
        self.assertEqual(updated_status, "fulfilled")

    def tearDown(self):
        self.cursor.execute("DELETE FROM Donors WHERE ID = ?", (self.donor_id,))
        self.cursor.execute("DELETE FROM Requests WHERE Hospital = 'Test Hospital'")
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    unittest.main()
