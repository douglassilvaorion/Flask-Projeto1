import requests, json
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from urllib.parse import urlparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Inicia comunicação com o Banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///autotrac.db"

app.app_context().push()
db = SQLAlchemy(app)

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

##Montagem da tabela Accounts
class messages(db.Model):

	__tablename__ = "messages"

	id = db.Column(db.Integer, primary_key=True)
	accountnumber = db.Column(db.Integer)
	vehicleaddress = db.Column(db.Integer)
	priority = db.Column(db.Integer)
	grmn = db.Column(db.Integer)
	ignition = db.Column(db.Integer)
	macronumber = db.Column(db.Integer)
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

	def __init__(self, id, accountnumber, vehicleaddress, priority, grmn, ignition, macronumber, macroversion, binarydatatype, msgsubtype, messagetime, messagetext, latitude, longitude, positiontime, landmark, transmissionchannel):
		self.id = id
		self.accountnumber = accountnumber
		self.vehicleaddress = vehicleaddress
		self.priority = priority
		self.grmn = grmn
		self.ignition = ignition
		self.macronumber = macronumber
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

class vehiclespositions(db.Model):

	__tablename__ = "vehiclespositions"
	
	id = db.Column(db.Integer, primary_key=True)
	accountnumber = db.Column(db.Integer)
	vehiclename = db.Column(db.String(200))
	vehicleaddress = db.Column(db.String(200))
	vehicleignition = db.Column(db.Integer)
	velocity = db.Column(db.Integer)
	odometer = db.Column(db.Integer)
	hourmeter = db.Column(db.Integer)
	latitude = db.Column(db.Integer)
	longitude = db.Column(db.Integer)
	landmark = db.Column(db.String(250))
	uf = db.Column(db.String(2))
	countrydescription = db.Column(db.String(150))
	positionTime = db.Column(db.String(150))
	direction = db.Column(db.Integer)
	directionGPS = db.Column(db.Integer)
	distance = db.Column(db.Integer)
	receivedtime = db.Column(db.String(150))
	transmissionchannel = db.Column(db.Integer)
	county = db.Column(db.String(150))

	def __init__(self, accountnumber, vehiclename, vehicleaddress, vehicleignition, velocity, 
			  odometer, hourmeter, latitude, longitude, landmark, uf, countrydescription, positionTime, 
			  direction, directionGPS, distance, receivedtime, transmissionchannel, county ):
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
		self.positionTime = positionTime
		self.direction = direction
		self.directionGPS = directionGPS
		self.distance = distance
		self.receivedtime = receivedtime
		self.transmissionchannel = transmissionchannel
		self.county = county

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
		
#Fim da Montagem de Dados do Banco
  
@app.route('/contas', methods=["GET", "POST"])
def contas():	
	
	#Inicia Busca de Dados API
	url = "https://aapi3.autotrac-online.com.br/aticapi/v1/accounts"
	payload = {}
	files={}
	headers = {
	'Authorization': 'Basic atic@amazon:api@2024', 'Ocp-Apim-Subscription-Key': '011cb03f29064101858f71356ac6f6e5','Content-Type': 'application/json'}
	response = requests.request("GET", url, headers=headers, data=payload, files=files)
	objetos    = json.loads(response.text)
	dados      = objetos

	df = pd.DataFrame(dados)

	for col in df.columns:
		df[col] = df[col].apply(str)

	for i in df.index:
		
		#Verifica se o código já existe:
		if accounts.query.filter_by(code=df['Code'][i]).first():
			print('Registro já existe')
		else:
			account = accounts(	df['Code'][i],
								df['Name'][i],
								df['FamilyNumber'][i],
								df['FamilyDescription'][i],
								df['Number'][i],
								df['AdministrativeUnitCode'][i])
			db.session.add(account)
			db.session.commit()
	return render_template("contas.html", accounts=accounts.query.all())

@app.route('/mensagens/<int:code>/<int:address>/', methods=["GET", "POST"])
def mensagens(code,address):

	url = "https://aapi3.autotrac-online.com.br/aticapi/v1/accounts/11035/vehicles/"+str(code)+"/returnmessages"
	print(url)
	payload = {}
	files={}
	headers = {	'Authorization': 'Basic suporte@amazon:juez@2017',
  				'Ocp-Apim-Subscription-Key': '011cb03f29064101858f71356ac6f6e5',
  				'Content-Type': 'application/json'}

	response = requests.request("GET", url, headers=headers, data=payload, files=files)
	objetos    = json.loads(response.text)
	print(response.status_code)
	if (response.status_code) == 200:
		dados      = objetos['Data']
		
		df = pd.DataFrame(dados)

		for col in df.columns:
			df[col] = df[col].apply(str)
			
			for i in df.index:
				if not messages.query.filter_by(id=df['ID'][i]).first():
					menssage = messages(df['ID'][i],
						df['AccountNumber'][i],
						df['VehicleAddress'][i],
						df['Priority'][i],
						df['Grmn'][i],
						df['Ignition'][i],
						df['MacroNumber'][i],
						df['MacroVersion'][i],
						df['BinaryDataType'][i],
						df['MsgSubType'][i],
						df['MessageTime'][i],
						df['MessageText'][i],
						df['Latitude'][i],
						df['Longitude'][i],
						df['PositionTime'][i],
						df['Landmark'][i],
						df['TransmissionChannel'][i])
					db.session.add(menssage)
					db.session.commit()

			#Recurso de Paginação
			# page = request.args.get('page', 1, type=int)
			# per_page = 4
			# #todos_messages = messages.query.paginate(page, per_page)
			return render_template("mensagens.html", messages=messages.query.filter_by(vehicleaddress=address))
	elif (response.status_code) == 422:
			return render_template("non_actorized_vehicle.html")
				

#Roda para Posição de Veiculos

@app.route('/veiculos', methods=["GET", "POST"])
def veiculos():

	url = "https://aapi3.autotrac-online.com.br/aticapi/v1/accounts/11035/vehicles?_limit=10000&_offset=1"

	payload = {}
	files={}
	headers = {
		  'Authorization': 'Basic atic@amazon:api@2024',
			  'Ocp-Apim-Subscription-Key': '011cb03f29064101858f71356ac6f6e5'}
	
	response = requests.request("GET", url, headers=headers, data=payload, files=files)
	objetos    = json.loads(response.text)
	dados      = objetos['Data']

	df = pd.DataFrame(dados)

	for col in df.columns:
		df[col] = df[col].apply(str)	
	
	for i in df.index:
		if not vehicles.query.filter_by(code = df['Code'][i]).first():			
			vehicle = vehicles(	df['Code'][i],
								df['Name'][i],
								df['Address'][i],
								df['TripName'][i],
								False)	
			db.session.add(vehicle)
			db.session.commit()


	return render_template("veiculos.html", vehicles = vehicles.query.all())

@app.route('/<int:code>/auth_vehicles', methods=["GET","POST"])
def auth_vehicles(code):
	
	#Busca dados de veiculo
	vehicle = vehicles.query.filter_by(code = code).first()
	if request.method == 'POST':				
		authorization = True

		vehicles.query.filter_by(code = code).update({'authorization':authorization})
		db.session.commit()
		return redirect(url_for('auth_vehicles_success'))

	return render_template('auth_vehicles.html', vehicle=vehicle)

@app.route('/auth_vehicles_success', methods=["GET","POST"])
def auth_vehicles_success():

	return render_template('auth_vehicles_success.html')

@app.errorhandler(401)
def unauthorized_page(error):
    return render_template("errors/401.html"), 401

@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500

if __name__ =="__main__":
	db.create_all()
	app.run(debug=True)