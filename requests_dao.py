import sqlite3
from requests import Requests

class RequestsDAO():
    def __init__(self,db_file='blood_donation_db'):
        self.conn=sqlite3.connect(db_file)
        self.cursor=self.conn.cursor()


    def get_all(self):
        sql='SELECT * FROM Requests'
        self.cursor.execute(sql)

        rows=self.cursor.fetchall()
        requests=[]
        for row in rows:
            r = Requests(hospital=row[0], city=row[1], blood_type=row[2])
            requests.append(r)

        return requests