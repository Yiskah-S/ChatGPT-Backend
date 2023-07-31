from app import db

class Response(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(500), nullable=False)
	prompt_id = db.Column(db.Integer, db.ForeignKey('prompt.id'), nullable=False)

	def to_dict(self):
		response_dict = {
			"id": self.id,
			"body": self.body,
			"prompt_id": self.prompt_id,
			"prompt": self.prompt.to_dict()
		}
		return response_dict

	@classmethod
	def from_dict(cls, request_body):
		return cls(
			body=request_body["body"],
			prompt_id=request_body["prompt_id"],
		)

	def update(self, data):
		for key, item in data.items():
			setattr(self, key, item)
