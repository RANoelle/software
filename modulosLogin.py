from validaciones.validaRUT import esRut, darFormatoRut
from flask import Flask, render_template, session, flash, request
from principal import *


@app.route('/login', methods=['GET', 'POST'])
def login():
    datos = None

    if request.method == 'POST':
        resultado = esRut(request.form['rut'])
        if resultado == True:
            nuevoRut = darFormatoRut(request.form['rut'])
            datos = CUENTAUSUARIO.find_one({"rut": nuevoRut})
            user = USUARIOS.find_one({"rut": nuevoRut})
        else:
            flash(resultado)
            return render_template('login.html')
        if datos == None:
            flash('Rut no encontrado.')
            return render_template('login.html')
        else:
            if request.form['password'] == datos['password']:
                if datos['estado'] == 'BLOQUEADO':
                    flash('La cuenta ingresada esta desactivada.')
                    return render_template('login.html')
                else:
                    session.clear()
                    session['rut'] = datos['rut']
                    session['password'] = datos['password']
                    session['nombre'] = user['nombres']+' '+user['apellido1']+' '+user['apellido2']
                    session['privilegios'] = datos['privilegios']
                    session['estado'] = datos['estado']
                    session['loggedIn'] = True
                    return render_template('index.html')
            else:
                flash('La contraseña es incorrecta.')
                return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    session.pop('rut', None)
    session.pop('password', None)
    session.pop('nombre', None)
    session.pop('privilegios', None)
    session.pop('estado', None)
    session.pop('loggedIn', None)
    return render_template('login.html')