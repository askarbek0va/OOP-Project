import sqlite3
from requests import Requests
from datetime import datetime,date

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


    def add_request(self,hospital, city, blood_type):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute("""
                        INSERT INTO Requests (Hospital, City, "Blood type", status,timestamp)
                        VALUES (?, ?, ?, 'pending',?)
                    """, (hospital, city, blood_type, now))
        self.conn.commit()

    def get_donors_by_blood_type(self, blood_type):
        self.cursor.execute("""
            SELECT * FROM Donors
            WHERE "Blood type" = ?
        """, (blood_type,))
        return self.cursor.fetchall()

    def fulfill_latest_pending_request(self, hospital, blood_type):
        self.cursor.execute("""
            SELECT rowid FROM Requests 
            WHERE Hospital = ? AND "Blood type" = ? AND status = 'pending' 
            ORDER BY rowid DESC LIMIT 1
        """, (hospital, blood_type))
        result = self.cursor.fetchone()

        if result:
            latest_request_id = result[0]
            self.cursor.execute("""
                UPDATE Requests
                SET status = 'fulfilled'
                WHERE rowid = ?
            """, (latest_request_id,))
            self.conn.commit()


    def close(self):
        self.conn.close()