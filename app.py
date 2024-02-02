import requests, json
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash,session
from urllib.parse import urlparse
from flask_sqlalchemy import SQLAlchemy
from database import db
from models import vehicles, macros, vehicles, accounts, messages

app = Flask(__name__)

#Inicia comunicação com o Banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///autotrac.db"

app.app_context().push()
db.init_app(app)


@app.route('/mensagens/<int:code>', methods=["GET", "POST"])
def mensagens(code):
	
	# Encontrando as mensagens
	message = messages.query.filter(messages.vehicleaddress == code)
	
	# Encontro o Veículo na base
	vehicle = vehicles.query.filter_by(address = code).first()

	nome_vic = vehicle.name

	if not message is None and not vehicle is None:
		return render_template("mensagens.html", message = message,nome_vic=nome_vic)
	else:
		return redirect(url_for('non_date_vehicle'))

# Redirecionamento
@app.route('/')
def principal():
	return redirect(url_for('veiculos'))


#Roda para Posição de Veiculos
@app.route('/veiculos', methods=["GET", "POST"])
def veiculos():
	page = int(request.args.get('page', 1))
	per_page = int(request.args.get('per_page',13))
	page_obj = vehicles.query.paginate(page=page,per_page=per_page)
	
	return render_template("veiculos.html", veiculos = page_obj )

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

@app.route('/macros', methods=["GET","POST"])
def macros_view():
	
	return render_template('macros.html',macro = macros.query.all())

@app.route('/macros_add',methods=["GET","POST"])
def macros_add():

	code = request.form.get('code')
	name = request.form.get('name')

	if request.method == 'POST':
		if not code or not name:
			flash("Preencha todos os campos do formulário","error")
		else:
			macro = macros(code, name)
			db.session.add(macro)
			db.session.commit()
			return redirect(url_for('macros'))
		
	return render_template('/macros_add.html')

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
	app.run(port=8085, host='0.0.0.0',debug=True)