from app import db

class accounts(db.Model):

	__tablename__ = "accounts"

	code = db.Column(db.Integer, primary_key=True)  
	name = db.Column(db.String(200))
	family_number = db.Column(db.Integer)
	family_description = db.Column(db.String(200))
	number = db.Column(db.Integer)
	administrative_unit_code = db.Column(db.Integer)
		
	def __init__(self, code, name, family_number, family_description, number, administrative_unit_code):
		self.code = code
		self.name = name
		self.family_number = family_number
		self.family_description = family_description
		self.number = number
		self.administrative_unit_code = administrative_unit_code