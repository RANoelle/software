from flask import Flask, render_template, session, flash, request
from flask_pymongo import PyMongo


app = Flask(__name__)

# MongoDB Connection
app.config['MONGO_DBNAME'] = 'lonzabd'
app.config['MONGO_URI'] = 'mongodb://lonzabd:lonzabd123@ds257564.mlab.com:57564/lonzabd'

mongo = PyMongo(app)

CUENTAUSUARIO   = mongo.db.cuentausuario
PROVEEDORES     = mongo.db.proveedores
RECEPCIONES     = mongo.db.recepciones
CLIENTEEMP      = mongo.db.clienteempresa
DESPACHOS       = mongo.db.despachos
PRODUCTOS       = mongo.db.productos
USUARIOS        = mongo.db.usuarios


# settings
app.secret_key = "mysecretkey"


@app.route('/')
def index():
    session['loggedIn'] = False
    return render_template('login.html')



from modulosClienteEmp import *
from modulosProveedor import *
from modulosRecepcion import *
from modulosProducto import *
from modulosDespacho import *
from modulosUsuario import *
from modulosCuenta import *
from modulosBuscar import *
from modulosLogin import *
from modulosReporte import *


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)