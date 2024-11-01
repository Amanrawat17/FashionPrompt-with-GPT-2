# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Import the db object from database.py
from database import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
