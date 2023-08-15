# api_key.py

from app import db
from typing import Dict

class APIKey(db.Model):
	# Columns definition
	id = db.Column(db.Integer, primary_key=True)
	api_type = db.Column(db.String(120), nullable=False)
	api_key = db.Column(db.String(120), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	# Convert the object into a dictionary
	def to_dict(self) -> Dict[str, any]:
		api_key_dict = {
			"id": self.id,
			"api_type": self.api_type,
			"api_key": self.api_key,
			"user_id": self.user_id,
		}
		return api_key_dict

	# Create an object from a dictionary
	@classmethod
	def from_dict(cls, request_body: Dict[str, any]) -> 'APIKey':
		return cls(
			api_type=request_body["api_type"],
			api_key=request_body["api_key"],
			user_id=request_body["user_id"],
		)
	
	# Update the object with new data
	def update(self, data: Dict[str, any]) -> None:
		for key, item in data.items():
			setattr(self, key, item)