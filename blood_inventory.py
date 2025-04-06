import  sqlite3
class BloodInventory():
    def __init__(self,blood_type,quantity,matching):
        self.blood_type=blood_type
        self.quantity=quantity
        self.matching=matching

    def __str__(self):
        return f'Blood type:{self.blood_type}  Quantity Available:{self.quantity}   Matching Blood Type:{self.matching}'


class BloodInventoryDAO():
    def __init__(self,db_file='blood_donation_db'):
        self.conn=sqlite3.connect(db_file)
        self.cursor=self.conn.cursor()


    def get_all(self):
        sql='SELECT * FROM "Blood Inventory"'
        self.cursor.execute(sql)

        rows=self.cursor.fetchall()
        bloods=[]
        for row in rows:
            b = BloodInventory(blood_type=row[0], quantity=row[1], matching=row[2])
            bloods.append(b)

        return bloods