from flask import Flask, render_template, request
import requests, json
import pandas as pd
from urllib.parse import urlparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Inicia comunicação com o Banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///autotrac.db"

app.app_context().push()
db = SQLAlchemy(app)

##criando estrutura do banco de dados
##Montagem da tabela Accounts
class accounts(db.Model):
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
		
#Fim da Montagem de Dados do Banco
  
@app.route('/contas', methods=["GET", "POST"])
def contas():	

	#Inicia Busca de Dados API
	url = "https://wapi.autotrac-online.com.br/sandboxaticapi/v1/accounts"
	payload = {}
	files={}
	headers = {
	'Authorization': 'Basic c3Vwb3J0ZUBhbWF6b246anVlekAyMDE3',
	'Cookie': 'TS01f4576b=01325e1fda423838059e1ff009030f3383a152900d8347161a61e4dbff94f240131947b0aa9d0b66603b9384f73359519a2e58691c'}
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

@app.route('/mensagens', methods=["GET", "POST"])
def mensagens():

	url = "https://wapi.autotrac-online.com.br/sandboxaticapi/v1/accounts/11/vehicles/651/returnmessages"
	payload = {}
	files={}
	headers = {
  	'Authorization': 'Basic c3Vwb3J0ZUBhbWF6b246anVlekAyMDE3',
  	'Cookie': 'TS01f4576b=01325e1fda33a063404ba6946937f1da03f1aea65fd080a1c7db1dd57cfb82803618df4f926084704c6324aa4fa124398d0a056acc'}

	response = requests.request("GET", url, headers=headers, data=payload, files=files)
	objetos    = json.loads(response.text)
	dados      = objetos['Data']

	df = pd.DataFrame(dados)

	for col in df.columns:
		df[col] = df[col].apply(str)

	for i in df.index:
		if messages.query.filter_by(id=df['ID'][i]).first():
			print('Registro já existe')
		else:
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

	return render_template("mensagens.html", messages=messages.query.all())

if __name__ =="__main__":
	db.create_all()
	app.run(debug=True)