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
class deputados(db.Model):
	id = db.Column(db.Integer, primary_key=True)  
	nome = db.Column(db.String(100))
	partido = db.Column(db.String(20))
	estado = db.Column(db.String(2))
	legendaid = db.Column(db.Integer)
	fotourl = db.Column(db.String(100))
	email = db.Column(db.String(200))
	
	def __init__(self, nome, partido, estado, legendaid, fotourl, email):
		self.nome = nome
		self.partido = partido
		self.estado = estado
		self.legendaid = legendaid
		self.fotourl = fotourl
		self.email = email

#Fim da Montagem de Dados do Banco

#Inicia Busca de Dados API
url        = 'https://dadosabertos.camara.leg.br/api/v2/deputados'
parametros = {}
resposta   = requests.request("GET", url, params=parametros)
objetos    = json.loads(resposta.text)
dados      = objetos['dados']

df = pd.DataFrame(dados)

for col in df.columns:
  df[col] = df[col].apply(str)
#Fim tratamento dos dados

#Leitura dos dados e Gravação no Banco de dados

for i in df.index:
	
	deputado = deputados(df['nome'][i], df['siglaPartido'][i], df['siglaUf'][i], df['idLegislatura'][i],df['urlFoto'][i],df['email'][i])
	db.session.add(deputado)
	db.session.commit()
  
@app.route('/', methods=["GET", "POST"])
def principal():	
	return render_template("deputados.html", deputados=deputados.query.all())

if __name__ =="__main__":
	db.create_all()
	app.run(debug=True)

