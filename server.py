from flask import Flask, request, render_template
from flask_socketio import *
from validationPose import validate
from log_test import print_name
from ast import literal_eval
import json


app =Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)




@app.route('/')
def index():
	return render_template("index.html")

@app.route('/captura')
def captura():
	return render_template("captura_sesion.html")

@app.route('/capturar_pruebas', methods = ['POST'])
def captura_pruebas():
	name  =  request.form['name_log']

	print_name(name)

	return render_template("capturar_pruebas.html")

@app.route('/succed')
def succed():
	return render_template("succed.html")

@app.route('/get_rutine/<id>')
def get_rutine(id):
	with open(("rutine_{}.json").format(id)) as file:
		data = json.load(file)
		
	return data

#la funcion debe recibir un json el cual como primera componente tiene una variable "model" que es el modelo con el que se va a comparar
#la pose que esta haciendo el usuario
@socketio.on('stream')
def compare( user_json):
	# Transform the string json recived to a dictionary	
	dict_json = literal_eval(user_json)
	return validate(dict_json)	
@socketio.on('modelo')
def compare( user_json):
	# Transform the string json recived to a dictionary
	print(user_json)
	



socketio.run(app, debug = True)
