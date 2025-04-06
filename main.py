from blood_inventory import BloodInventory,BloodInventoryDAO
from donors_dao import DonorsDAO
from donors import Donors
from requests import Requests
from requests_dao import RequestsDAO
import sys
from PyQt6.QtWidgets import QApplication
from first_page import MainWindow



if __name__=='__main__':
    donors_dao=DonorsDAO('blood_donation_db')

    donors = donors_dao.get_all()
    for donor in donors:
        print(donor)

    print()


    requests_dao=RequestsDAO('blood_donation_db')

    requests=requests_dao.get_all()
    for request in requests:
        print(request)

    print()

    blood_inventory_dao=BloodInventoryDAO('blood_donation_db')

    bloods=blood_inventory_dao.get_all()
    for blood in bloods:
        print(blood)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Blood Donation Management")
    window.show()
    sys.exit(app.exec())