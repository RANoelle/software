from flask import Flask, render_template, session, flash, request
from principal import *
import formulariosUsuario
import formulariosCuenta
import formulariosBuscar



@app.route('/addCuenta/<rutUsuario>', methods=['GET', 'POST'])
def addCuenta(rutUsuario):
    if session['privilegios'] != 'ADMINISTRADOR':
        return render_template('login.html')

    form_usuario = formulariosBuscar.formBuscarRUT(request.form)
    if CUENTAUSUARIO.find_one({"rut": rutUsuario}) != None:
        flash('El RUT ingresado ya tiene una cuenta asociada.')
        return render_template('buscarRut.html', form=form_usuario, accion='Crear Cuenta')

    datosUsuario = USUARIOS.find_one({"rut": rutUsuario})
    form_cuenta = formulariosCuenta.formCuenta(request.form)
    form_cuenta.claveSesion.data = session['password']
    form_cuenta.estado.data = 'ACTIVO'

    if request.method == 'POST' and form_cuenta.validate():
        CUENTAUSUARIO.insert({
            'rut': rutUsuario,
            'password': form_cuenta.claveNueva1.data,
            'privilegios': form_cuenta.privilegios.data,
            'estado': form_cuenta.estado.data
        })
        flash('Nueva cuenta creada correctamente')
        return render_template('index.html')

    return render_template('crearCuenta.html',form=form_cuenta, usuario=datosUsuario)

@app.route('/showCuenta/<rutUsuario>', methods=['GET', 'POST'])
def showCuenta(rutUsuario):
    if session['privilegios'] != 'ADMINISTRADOR':
        return render_template('login.html')

    datosCuenta = CUENTAUSUARIO.find_one({"rut": rutUsuario})

    if datosCuenta == None:
        form_usuario = formulariosBuscar.formBuscarRUT(request.form)
        flash('El RUT ingresado NO tiene una cuenta asociada.')
        return render_template('buscarRut.html', form=form_usuario, accion='Buscar Cuenta')

    datosUsuario = USUARIOS.find_one({"rut": rutUsuario})

    return render_template('mostrarCuenta.html', cuenta=datosCuenta, usuario=datosUsuario)

@app.route('/editCuenta/<rutUsuario>', methods=['GET', 'POST'])
def editCuenta(rutUsuario):
    if session['privilegios'] != 'ADMINISTRADOR':
        return render_template('login.html')

    form_cuenta = formulariosCuenta.formCuenta(request.form)
    datosUsuario = USUARIOS.find_one({"rut": rutUsuario})
    ponerDatosOriginales = True

    print ('voy a modificar.')
    if request.method == 'POST':
        print('estoy actualizando.')
        print (request.form['estado'])

        form_cuenta.estado.data = request.form['estado']
        form_cuenta.privilegios.data = request.form['privilegios']
        form_cuenta.claveSesion.data = session['password']
        form_cuenta.claveNueva1.data = request.form['claveNueva1']
        form_cuenta.claveNueva2.data = request.form['claveNueva2']
        ponerDatosOriginales = False

        if form_cuenta.validate():
            CUENTAUSUARIO.update_one({"rut": rutUsuario}, {"$set": {
                'rut': rutUsuario,
                'password': request.form['claveNueva1'],
                'privilegios': request.form['privilegios'],
                'estado': request.form['estado']
            }})

            flash('Cuenta de Usuario actualizada correctamente')
            return render_template('index.html')

    if ponerDatosOriginales:
        datosCuenta = CUENTAUSUARIO.find_one({"rut": rutUsuario})

        form_cuenta.estado.data = datosCuenta['estado']
        form_cuenta.privilegios.data = datosCuenta['privilegios']
        form_cuenta.claveSesion.data = session['password']
        form_cuenta.claveNueva1.data = datosCuenta['password']
        form_cuenta.claveNueva2.data = datosCuenta['password']


    return render_template('modificarCuenta.html', form=form_cuenta, usuario=datosUsuario)


@app.route('/editClave', methods=['GET', 'POST'])
def editClave():

    form_clave = formulariosCuenta.formCuenta(request.form)
    form_clave.privilegios.data = session['privilegios']
    form_clave.estado.data = session['estado']

    if request.method == 'POST' and form_clave.validate():
        CUENTAUSUARIO.update_one({"rut": session['rut']}, {"$set": {
            'password': form_clave.claveNueva1.data
        }})
        session['password'] = form_clave.claveNueva1.data

        flash('Clave actualizada correctamente')
        return render_template('index.html')

    return render_template('cambiarClave.html', form=form_clave)