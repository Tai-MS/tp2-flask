from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = "users"
    id_user = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<User {self.id_user}: {self.name} {self.lastname} ({self.email})>"

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
