import requests, json
import pandas as pd
from flask import Flask, render_template, jsonify
from urllib.parse import urlparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
		if not accounts.query.filter_by(code=df['Code'][i]).first():
			account = accounts(	df['Code'][i],
								df['Name'][i],
								df['FamilyNumber'][i],
								df['FamilyDescription'][i],
								df['Number'][i],
								df['AdministrativeUnitCode'][i])
			db.session.add(account)
			db.session.commit()
	
	return jsonify({'Dados':objetos})		

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


	return jsonify(objetos)

@app.route('/veiculos_autorizados')
def veiculos_autorizados():

	url = "https://aapi3.autotrac-online.com.br/aticapi/v1/accounts/11035/authorizedvehicles?_limit=1000"
	payload = {}
	files={}
	headers = { 'Authorization': 'Basic atic@amazon:api@2024', 'Ocp-Apim-Subscription-Key': '011cb03f29064101858f71356ac6f6e5', 'Content-Type': 'application/json' }
	response = requests.request("GET", url, headers=headers, data=payload, files=files)
	objetos    = json.loads(response.text)

	return jsonify(objetos)

@app.route('/mensagens', methods=["GET", "POST"])
def mensagens():

	#Busca dados de veículos autorizados:
	url = "http://127.0.0.1:5000/veiculos_autorizados"
	response 	= requests.request("GET", url)
	objetos    	= json.loads(response.text)
	veiculos	= objetos['Data']
	
	df = pd.DataFrame(veiculos)

	for col in df.columns:
		df[col] = df[col].apply(str)	

	for i in df.index:
		
		url = "https://aapi3.autotrac-online.com.br/aticapi/v1/accounts/11035/vehicles/"+df['VehicleCode'][i]+"/returnmessages"
		payload = {}
		files={}
		headers = {	'Authorization': 'Basic suporte@amazon:juez@2017', 'Ocp-Apim-Subscription-Key': '011cb03f29064101858f71356ac6f6e5', 'Content-Type': 'application/json'}
		response = requests.request("GET", url, headers=headers, data=payload, files=files)
		objetos    = json.loads(response.text)
		
		if (response.status_code) == 200:
			dados      = objetos['Data']
			
			dw = pd.DataFrame(dados)
			
			for col in dw.columns:
				dw[col] = dw[col].apply(str)
				
			for i in dw.index:
				if not messages.query.filter_by(id=dw['ID'][i]).first():
					menssage = messages(dw['ID'][i],
						 				dw['AccountNumber'][i],
										dw['VehicleAddress'][i],
										dw['Priority'][i],
										dw['Grmn'][i],
										dw['Ignition'][i],
										dw['MacroNumber'][i],
										dw['MacroVersion'][i],
										dw['BinaryDataType'][i],
										dw['MsgSubType'][i],
										dw['MessageTime'][i],
										dw['MessageText'][i],
										dw['Latitude'][i],
										dw['Longitude'][i],
										dw['PositionTime'][i],
										dw['Landmark'][i],
										dw['TransmissionChannel'][i])
					
					db.session.add(menssage)
					db.session.commit()		

			return jsonify({'Data':objetos})
		elif (response.status_code) == 422:
			return jsonify({'Data':objetos})
	
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