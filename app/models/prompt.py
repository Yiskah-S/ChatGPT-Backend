from app import db

class Prompt(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	category = db.Column(db.String(50), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	responses = db.relationship('Response', backref='prompt', lazy=True)

	def to_dict(self):
		prompt_dict = {
			"id": self.id,
			"title": self.title,
			"category": self.category,
			"user_id": self.user_id,
			"responses": [response.to_dict() for response in self.responses]
		}
		return prompt_dict

	@classmethod
	def from_dict(cls, request_body):
		return cls(
			title=request_body["title"],
			category=request_body["category"],
			user_id=request_body["user_id"],
		)

	def update(self, data):
		for key, item in data.items():
			setattr(self, key, item)