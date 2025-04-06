
class Requests():
    def __init__(self,hospital,city,blood_type):
        self.hospital=hospital
        self.city=city
        self.blood_type=blood_type

    def __str__(self):
        return f'Hospital\'s name:{self.hospital}  City:{self.city}  Requested blood type:{self.blood_type}'


