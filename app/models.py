from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    def __init__(self, login, password, email, first_name, last_name):
        self.login = login
        self.password_hash = generate_password_hash(password=password)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# flask db init
# flask db migrate -m "create table User"
# flask db upgrade