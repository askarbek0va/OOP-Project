import sqlite3
from donors import Donors

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

