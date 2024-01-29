import requests, json
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from urllib.parse import urlparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#Inicia comunicação com o Banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///autotrac.db"

app.app_context().push()
db = SQLAlchemy(app)

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

@app.route('/mensagens/<int:code>', methods=["GET", "POST"])
def mensagens(code):

	
	url = "https://aapi3.autotrac-online.com.br/aticapi/v1/accounts/11035/vehicles/"+str(code)+"/returnmessages"	
	payload = {}
	files = {}
	headers = {	'Authorization': 'Basic suporte@amazon:juez@2017',
  				'Ocp-Apim-Subscription-Key': '011cb03f29064101858f71356ac6f6e5',
  				'Content-Type': 'application/json'}

	response = requests.request("GET", url, headers=headers, data=payload, files=files)
	objetos    = json.loads(response.text)
	
	if (response.status_code) == 200:
		dados      = objetos['Data']
		
		df = pd.DataFrame(dados)
		
		for col in df.columns:
			df[col] = df[col].apply(str)
		
		return render_template("mensagens.html", len = len(objetos['Data']), messages = objetos['Data'] )
	else:
		return redirect(url_for('non_date_vehicle'))

#Roda para Posição de Veiculos
@app.route('/veiculos', methods=["GET", "POST"])
def veiculos():
	
	url = "https://aapi3.autotrac-online.com.br/aticapi/v1/accounts/11035/vehicles?_limit=1000"

	payload = {}
	files={}
	headers = { 'Authorization': 'Basic suporte@amazon:juez@2017', 'Ocp-Apim-Subscription-Key': '011cb03f29064101858f71356ac6f6e5','Content-Type': 'application/json'}
	
	response = requests.request("GET", url, headers=headers, data=payload, files=files)
	objetos    = json.loads(response.text)
	dados      = objetos['Data']

	df = pd.DataFrame(dados)

	for col in df.columns:
		df[col] = df[col].apply(str)	

	return render_template("veiculos.html", len = len(objetos['Data']), veiculos = objetos['Data'] )

@app.route('/veiculos_autorizados')
def veiculos_autorizados():

	url = "https://aapi3.autotrac-online.com.br/aticapi/v1/accounts/11035/authorizedvehicles?_limit=1000"

	payload = {}
	files={}
	headers = { 'Authorization': 'Basic suporte@amazon:juez@2017', 'Ocp-Apim-Subscription-Key': '011cb03f29064101858f71356ac6f6e5', 'Content-Type': 'application/json' }

	response = requests.request("GET", url, headers=headers, data=payload, files=files)
	objetos    = json.loads(response.text)
	dados      = objetos['Data']

	df = pd.DataFrame(dados)

	for col in df.columns:
		df[col] = df[col].apply(str)	

	return render_template("veiculos_autorizados.html", len = len(objetos['Data']), veiculos = objetos['Data'] )

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

@app.route('/auth_vehicles_success/<int:code>', methods=["GET","POST"])
def auth_vehicles_success(code):

	#Leitura dos campos do Formulário
	code = request.form.get('code')

	if request.method == 'POST':
		#Realiza autorização do veículo via API:
		url = "https://aapi3.autotrac-online.com.br/aticapi/v1/accounts/11035/authorizedvehicle/" + str(code)
		payload = {}
		files={}
		headers = { 'Authorization': 'Basic suporte@amazon:juez@2017', 'Ocp-Apim-Subscription-Key': '011cb03f29064101858f71356ac6f6e5', 'Content-Type': 'application/json' }
		response = requests.request("POST", url, headers=headers, data=payload, files=files)

	return render_template('auth_vehicles_success.html')

@app.route('/<int:code>/revoke_vehicles', methods=["GET","POST"])
def revoke_vehicles(code):	
	#Busca dados de veiculo
	vehicle = vehicles.query.filter_by(code = code).first()
	if request.method == 'POST':				
		authorization = False

		vehicles.query.filter_by(code = code).update({'authorization':authorization})
		db.session.commit()
		return redirect(url_for('revoke_vehicles_success'))

	return render_template('revoke_vehicles.html', vehicle=vehicle)

@app.route('/revoke_vehicles_success/<int:code>', methods=["GET","POST"])
def revoke_vehicles_success(code):

	#Leitura dos campos do Formulário
	code = request.form.get('code')

	if request.method == 'POST':
		#Realiza autorização do veículo via API:
		url = "https://aapi3.autotrac-online.com.br/aticapi/v1/accounts/11035/authorizedvehicle/" + str(code)
		payload = {}
		files={}
		headers = { 'Authorization': 'Basic suporte@amazon:juez@2017', 'Ocp-Apim-Subscription-Key': '011cb03f29064101858f71356ac6f6e5', 'Content-Type': 'application/json' }
		response = requests.request("DELETE", url, headers=headers, data=payload, files=files)

	return render_template('revoke_vehicles_success.html')

@app.route('/non_actorized_vehicle', methods=["GET","POST"])
def non_actorized_vehicle():
    return render_template("non_actorized_vehicle.html")

@app.route('/non_date_vehicle', methods=["GET","POST"])
def non_date_vehicle():
    return render_template("non_date_vehicle.html")

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
	app.run(port=8085, host='0.0.0.0',debug=True)