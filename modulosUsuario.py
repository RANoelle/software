from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, url_for
from principal import *
from datetime import datetime
import formulariosUsuario



def buscaUsuarioDB(ID):
    cursor = mongo.db.usuarios
    x = cursor
    return x

@app.route('/addUsuario', methods=['GET', 'POST'])
def addUsuario():
    if session['privilegios'] != 'ADMINISTRADOR':
        return render_template('login.html')

    form_usuario = formulariosUsuario.formUsuario(request.form)

    if request.method == 'POST' and form_usuario.validate():
        USUARIOS.insert({
            'rut': form_usuario.rut.data,
            'nombres': form_usuario.nombres.data,
            'apellido1': form_usuario.apellido1.data,
            'apellido2': form_usuario.apellido2.data,
            'nacimiento': str(form_usuario.nacimiento.data),
            'sueldo': int(form_usuario.sueldo.data),
            'direccion': form_usuario.direccion.data,
            'estado': form_usuario.estado.data,
            'cargo': form_usuario.cargo.data})
        flash('Usuario ingresado correctamente.')
        return render_template('index.html')


    return render_template('registrarUsuario.html', form=form_usuario, accion='Registrar')


@app.route('/listUsuario', methods=['GET', 'POST'])
def listUsuario():
    if session['privilegios'] != 'ADMINISTRADOR':
        return render_template('login.html')

    output = USUARIOS.find()
    return render_template('listarUsuarios.html', usuarios=output)

@app.route('/editUsuario/<rutModificar>', methods=['GET', 'POST'])
def editUsuario(rutModificar):
    if session['privilegios'] != 'ADMINISTRADOR':
        return render_template('login.html')

    form_usuario = formulariosUsuario.formUsuario(request.form)
    ponerDatosOriginales = True

    if request.method == 'POST':

        form_usuario.rut.data = rutModificar
        form_usuario.nombres.data = request.form['nombres']
        form_usuario.apellido1.data = request.form['apellido1']
        form_usuario.apellido2.data = request.form['apellido2']
        form_usuario.nacimiento.data = request.form['nacimiento']
        form_usuario.sueldo.data = int(request.form['sueldo'])
        form_usuario.direccion.data = request.form['direccion']
        form_usuario.estado.data = request.form['estado']
        form_usuario.cargo.data = request.form['cargo']
        ponerDatosOriginales = False

        if form_usuario.validate():
            USUARIOS.update_one({"rut": rutModificar}, {"$set": {
                'nombres': request.form['nombres'],
                'apellido1': request.form['apellido1'],
                'apellido2': request.form['apellido2'],
                'nacimiento': request.form['nacimiento'],
                'sueldo': request.form['sueldo'],
                'direccion': request.form['direccion'],
                'estado': request.form['estado'],
                'cargo': request.form['cargo']
            }})
            flash('Los datos del Usuario se actualizaron correctamente.')
            return render_template('index.html')

    if ponerDatosOriginales:
        output = USUARIOS.find_one({"rut": rutModificar})
        cadena = output['nacimiento'].split("-")
        output['nacimiento'] = datetime.strptime(cadena[2] + '/' + cadena[1] + '/' + cadena[0], '%d/%m/%Y')

        form_usuario.rut.data = output['rut']
        form_usuario.nombres.data = output['nombres']
        form_usuario.apellido1.data = output['apellido1']
        form_usuario.apellido2.data = output['apellido2']
        form_usuario.nacimiento.data = output['nacimiento']
        form_usuario.sueldo.data = int(output['sueldo'])
        form_usuario.direccion.data = output['direccion']
        form_usuario.estado.data = output['estado']
        form_usuario.cargo.data = output['cargo']

    return render_template('registrarUsuario.html', form=form_usuario, accion='Modificar')

@app.route('/deleteUsuario/<rutEliminar>')
def deleteUsuario(rutEliminar):
    if session['privilegios'] != 'ADMINISTRADOR':
        return render_template('login.html')

    USUARIOS.delete_one({ 'rut': rutEliminar })
    flash('El Usuario se elimino correctamente.')
    return render_template('index.html')
