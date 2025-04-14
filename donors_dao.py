import sqlite3
from datetime import datetime,date
from donors import Donors
from PyQt6.QtWidgets import QMessageBox

class DonorsDAO():

    def __init__(self,db_file='blood_donation_db'):
        self.conn=sqlite3.connect(db_file)
        self.cursor=self.conn.cursor()




    def get_all(self):
        sql='SELECT * FROM Donors'
        self.cursor.execute(sql)

        rows=self.cursor.fetchall()
        donors=[]
        for row in rows:
             d = Donors(id=row[0], name=row[1], age=row[2], blood_type=row[3],last_donation=row[4],location=row[5],contacts=row[6])
             donors.append(d)

        return donors

    def add_donor(self, name,age,blood_type, last_donation,location,contacts):

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute('''
                        INSERT INTO Donors ('Name','Age' , 'Blood type', 'Last donation date', 'Location', 'Contacts',timestamp)
                        VALUES (?, ?, ?, ?, ?, ?,?)
                    ''', (name, age, blood_type, last_donation, location, contacts, now))

        self.cursor.execute('''
                                INSERT INTO AllDonors ('Name','Age' , 'Blood type', 'Last donation date', 'Location', 'Contacts',timestamp)
                                VALUES (?, ?, ?, ?, ?, ?,?)
                            ''', (name, age, blood_type, last_donation, location, contacts, now))

        self.conn.commit()

    def donor_exists(self,name_variant_1, name_variant_2, contacts, blood_type):

        self.cursor.execute('''
                            SELECT * FROM Donors WHERE (LOWER(Name) = ? OR LOWER(Name) = ?) AND Contacts = ? AND "Blood type" = ?
                        ''', (name_variant_1, name_variant_2, contacts, blood_type))
        return self.cursor.fetchone() is not None


    def delete_by_id(self, donor_id):
        self.cursor.execute("DELETE FROM Donors WHERE ID = ?", (donor_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()


