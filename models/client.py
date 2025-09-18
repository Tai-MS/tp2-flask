from . import db
from werkzeug.security import check_password_hash, generate_password_hash

class Client(db.Model):
    __tablename__ = "clients"
    id_client = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, nullable=False, default=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    tel = db.Column(db.Integer, nullable=False)
    address = db.Column(db.Integer, nullable=False)

    tickets = db.relationship("Ticket", backref="client")

    def __repr__(self):
        return f"<Client {self.id_client}: {self.name} {self.lastname} ({self.email}) - Tel {self.tel} - Dirección {self.address}>"

    def set_status(self, status):
        self.status = status

    def set_name(self, name):
        self.name = name

    def set_lastname(self, lastname):
        self.lastname = lastname

    def set_email(self, email):
        self.email = email

    def set_tel(self, tel):
        self.tel = tel

    def set_address(self, address):
        self.address = address

    def get_name(self, name):
        return self.name

    def get_lastname(self, lastname):
        return self.lastname

    def get_email(self, email):
        return self.email

    def get_tel(self, tel):
        return self.tel

    def get_address(self, address):
        return self.address
    
    def get_status(self, status):
        self.status = status