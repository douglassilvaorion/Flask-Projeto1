from database import db

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

	def __repr__(self):
		return "Contas: {}".format(self.code)
	
class messages(db.Model):

	__tablename__ = "messages"

	id = db.Column(db.Integer, primary_key=True)
	accountnumber = db.Column(db.Integer)
	vehicleaddress = db.Column(db.Integer)
	priority = db.Column(db.Integer)
	grmn = db.Column(db.Integer)
	ignition = db.Column(db.Integer)
	macronumber = db.Column(db.Integer)
	macrodescri = db.Column(db.String())
	macroversion = db.Column(db.Integer)
	binarydatatype = db.Column(db.Integer)
	msgsubtype = db.Column(db.Integer)
	messagetime = db.Column(db.String(200))
	messagetext = db.Column(db.String(200))
	latitude = db.Column(db.Integer)
	longitude = db.Column(db.Integer)
	positiontime = db.Column(db.String(200))
	landmark = db.Column(db.String(200))
	transmissionchannel = db.Column(db.Integer)

	def __init__(self, id, accountnumber, vehicleaddress, priority, grmn, ignition, macronumber, macrodescri, macroversion, binarydatatype, msgsubtype, messagetime, messagetext, latitude, longitude, positiontime, landmark, transmissionchannel):
		self.id = id
		self.accountnumber = accountnumber
		self.vehicleaddress = vehicleaddress
		self.priority = priority
		self.grmn = grmn
		self.ignition = ignition
		self.macronumber = macronumber
		self.macrodescri = macrodescri
		self.macroversion = macroversion
		self.binarydatatype = binarydatatype
		self.msgsubtype = msgsubtype
		self.messagetime = messagetime
		self.messagetext = messagetext
		self.latitude = latitude
		self.longitude = longitude
		self.positiontime = positiontime
		self.landmark = landmark
		self.transmissionchannel = transmissionchannel			
		
class vehicles(db.Model):

	__tablename__ = "vehicles"
	code = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	address = db.Column(db.String)
	tripname = db.Column(db.String)
	authorization = db.Column(db.Boolean)

	def __init__(self, code, name, address, tripname,authorization):
		self.code = code
		self.name = name
		self.address = address
		self.tripname = tripname
		self.authorization = authorization		

	def __repr__(self):
			return "Vehicles: {}".format(self.code)	
	
class macros(db.Model):
	
	__tablename__ = "macros"
	code = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	
	def __init__(self, code, name):
		self.code = code
		self.name = name	

class vehiclespositions(db.Model):

	__tablename__ = "vehiclespositions"

	id = db.Column(db.Integer, index=True, unique=True, autoincrement=True, primary_key=True)
	accountnumber = db.Column(db.Integer)
	vehiclename = db.Column(db.String)
	vehicleaddress = db.Column(db.String)
	vehicleignition = db.Column(db.Integer)
	velocity = db.Column(db.Integer)
	odometer = db.Column(db.Integer)
	hourmeter = db.Column(db.Integer)
	latitude = db.Column(db.Integer)
	longitude = db.Column(db.Integer)
	landmark = db.Column(db.String)
	uf = db.Column(db.String)
	countrydescription = db.Column(db.String)
	positiontime  = db.Column(db.String)
	direction = db.Column(db.Integer)
	directiongps = db.Column(db.Integer)
	distance = db.Column(db.Integer)
	receivedtime = db.Column(db.String)
	transmissionchannel = db.Column(db.Integer)
	county = db.Column(db.String)

	def __init__(self, accountnumber, vehiclename, vehicleaddress, vehicleignition, velocity, odometer, 
			  hourmeter, latitude, longitude, landmark, uf, countrydescription, positiontime, 
			  direction, directiongps, distance, receivedtime, transmissionchannel, county  ):
		
		self.accountnumber = accountnumber
		self.vehiclename = vehiclename
		self.vehicleaddress = vehicleaddress
		self.vehicleignition = vehicleignition
		self.velocity = velocity
		self.odometer = odometer
		self.hourmeter = hourmeter
		self.latitude = latitude
		self.longitude = longitude
		self.landmark = landmark
		self.uf = uf
		self.countrydescription = countrydescription
		self.positiontime = positiontime
		self.direction = direction
		self.directiongps = directiongps
		self.distance = distance
		self.receivedtime = receivedtime
		self.transmissionchannel = transmissionchannel
		self.county = county
	