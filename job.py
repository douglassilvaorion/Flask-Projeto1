import requests, json
from flask import Flask, render_template, jsonify, request
from urllib.parse import urlparse
from flask_sqlalchemy import SQLAlchemy
from database import db

app = Flask(__name__)

#Inicia comunicação com o Banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///autotrac.db"

app.app_context().push()
db.init_app(app)
	
url = "http://192.168.144.239:5000/veiculos"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print("Leitura do cadastro de veículos!")

url = "http://192.168.144.239:5000/mensagens"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print("Leitura das mensagens por veiculo!")
