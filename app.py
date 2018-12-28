from flask import Flask,jsonify
from flask import render_template
from flask import request
import forms
from flask_pymongo import PyMongo
from pprint import pprint



app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'software'
app.config['MONGO_URI'] = 'mongodb://cesariqq:software123@ds015953.mlab.com:15953/software'

mongo = PyMongo(app)

@app.route("/login", methods=['GET','POST'])
def login():
	if request.method == 'POST':
		aux = request.form.get('id')
		aux2 = request.form.get('password')
		coleccion=mongo.db.usuario
		busqueda = coleccion.find({'nombre' : aux})
		aux3=busqueda[0]['password']
		if aux2 == aux3:
			return render_template('index.html')
		else:
			return render_template('login.html',parametro="panchoqlo")

	return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.usuarios
        existing_user = users.find_one({'name' : request.form['username']})

        
        return 'That username already exists!'

    return render_template('register.html')

@app.route("/lista_provedor", methods=['GET', 'POST'])
def allprovedores():
	if request.method == 'POST':
		num1=request.form.get("search")
		coleccion=mongo.db.provedores
		busqueda = coleccion.find({ 'name': num1  })
		return render_template('provedortabla.html', proveedores=busqueda)
	coleccion=mongo.db.provedores
	output=[]
	for s in coleccion.find():
		output.append({'rut' : s['nombre'], 'nombre' : s['rut'],  'ciudad' : s['ciudad'],  'comuna' : s['comuna'],  'calle' : s['calle'],  'correo' : s['correo'],'telefono' : s['telefono']})
	return render_template('provedortabla.html',provedores=output)

@app.route("/ingresar_provedor", methods=['GET', 'POST'])
def addprovedor():
	if request.method == 'POST':
		#usuarios ={'rut':'194360169','nombre': 'Francisco', 'ciudad': 'Iquique','comuna':'Iquique', 'calle':'callefalsa #123', 'correo':'francisco123@gmail.com','telefono':'965465674'}
		coleccion=mongo.db.provedores
		x=coleccion.insert(usuarios)
		# agregar if para verificar si se agrego correctamente, de lo contrario volver al ingreso de nuevo provedor provedores.html*
		return render_template('succes.html')
	else:
		return render_template('provedores.html')



if __name__=="__main__":
	app.run(debug = True)
