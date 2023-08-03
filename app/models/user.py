# user.py

from app import db
from flask_security import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import CheckConstraint

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(120), nullable=False)
	active = db.Column(db.Boolean, default=True, nullable=False)
	__table_args__ = (CheckConstraint('length(username) > 1'), )

	def to_dict(self):
		user_dict = {
			"id": self.id,
			"username": self.username,
			"email": self.email,
		}
		return user_dict

	def verify_password(self, password):
		return check_password_hash(self.password, password)

	def set_password(self, password):
		try:
			self.password = generate_password_hash(password)
		except Exception as e:
			print("Error setting password: ", str(e))

	@classmethod
	def from_dict(cls, request_body):
		return cls(
			username=request_body["username"],
			email=request_body["email"],
			password=generate_password_hash(request_body["password"]),
		)
