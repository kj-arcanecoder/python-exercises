

class Contact:
    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        
    def to_dict(self):
        return {self.name : {
            "phone" : self.phone,
            "email" : self.email,
            "address" : self.address
        }}