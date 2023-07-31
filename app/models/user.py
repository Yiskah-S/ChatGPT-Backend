from app import db
from flask_security import UserMixin
from flask_security import check_password_hash, generate_password_hash, login_required
from flask_login import LoginManager, current_user, login_user, logout_user
from flask import Blueprint, jsonify, request

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    

    def to_dict(self):
        user_dict = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
        }
        return user_dict
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)


    @classmethod
    def from_dict(cls, request_body):
        return cls(
            username=request_body["username"],
            email=request_body["email"],
            password=request_body["password"],
        )
