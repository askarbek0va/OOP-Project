

class Donors:
    def __init__(self,id:int,name:str,age:int,blood_type:str,last_donation:str,location:str,contacts:str):
        self.id=id
        self.name=name
        self.age=age
        self.blood_type=blood_type
        self.last_donation=last_donation
        self.location=location
        self.contacts=contacts


    def __str__(self):
        return f'Donor\'s ID:{self.id}  Name:{self.name}  Age:{self.age}   Blood type:{self.blood_type}   Location:{self.location}   Contacts:{self.contacts}'
