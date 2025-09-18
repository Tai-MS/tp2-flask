from . import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id_user = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<User {self.id_user}: {self.name} {self.lastname} ({self.email}) - Rol {self.role}>"

    def set_and_hash_pass(self, password):
        self.password = generate_password_hash(password)

    def verify_pass(self, password):
        return check_password_hash(self.password, password)

    def set_name(self, name):
        self.name = name

    def set_lastname(self, lastname):
        self.lastname = lastname

    def set_email(self, email):
        self.email = email

    def set_role(self, role):
        self.role = role

    def set_lastname(self, lastname):
        self.lastname = lastname

    def get_id(self):
        return str(self.id_user)

    def get_name(self, name):
        return self.name

    def get_lastname(self, lastname):
        return self.lastname

    def get_email(self, email):
        return self.email

    def get_role(self, role):
        return self.role

    def get_lastname(self, lastname):
        return self.lastname