from flask import Flask, render_template, session, flash, request
from principal import *
import formulariosProveedor

@app.route('/addClienteEmp', methods=['GET', 'POST'])
def addClienteEmp():
    if session['privilegios'] != 'ADMINISTRADOR':
        return render_template('login.html')

    form_empresa = formulariosProveedor.formProveedor(request.form)

    if request.method == 'POST' and form_empresa.validate():
        CLIENTEEMP.insert({
            'rut': form_empresa.rut.data,
            'nombre': form_empresa.nombre.data,
            'ciudad': form_empresa.ciudad.data,
            'comuna': form_empresa.comuna.data,
            'correo':form_empresa.correo.data,
            'nombreContacto': form_empresa.nombreContacto.data,
            'celularContacto': form_empresa.celularContacto.data
        })
        flash('Empresa cliente ingresada correctamente')
        return render_template('index.html')

    return render_template('registrarClienteEmp.html', form=form_empresa, accion='Registrar')

@app.route('/editClienteEmp/<rutModificar>', methods=['GET', 'POST'])
def editClienteEmp(rutModificar):
    if session['privilegios'] != 'ADMINISTRADOR':
        return render_template('login.html')

    form_empresa = formulariosProveedor.formProveedor(request.form)
    ponerDatosOriginales = True

    if request.method == 'POST':

        form_empresa.rut.data = rutModificar
        form_empresa.nombre.data = request.form['nombre']
        form_empresa.ciudad.data = request.form['ciudad']
        form_empresa.comuna.data = request.form['comuna']
        form_empresa.correo.data = request.form['correo']
        form_empresa.nombreContacto.data = request.form['nombreContacto']
        form_empresa.celularContacto.data = request.form['celularContacto']
        ponerDatosOriginales = False

        if form_empresa.validate():
            PROVEEDORES.update_one({"rut": rutModificar}, {"$set": {
                'nombre': request.form['nombre'],
                'ciudad': request.form['ciudad'],
                'comuna': request.form['comuna'],
                'correo': request.form['correo'],
                'nombreContacto': request.form['nombreContacto'],
                'celularContacto': request.form['celularContacto']
            }})
            flash('Los datos de la Empresa se actualizaron correctamente.')
            return render_template('index.html')

    if ponerDatosOriginales:
        output = CLIENTEEMP.find_one({"rut": rutModificar})

        form_empresa.rut.data = rutModificar
        form_empresa.nombre.data = output['nombre']
        form_empresa.ciudad.data = output['ciudad']
        form_empresa.comuna.data = output['comuna']
        form_empresa.correo.data = output['correo']
        form_empresa.nombreContacto.data = output['nombreContacto']
        form_empresa.celularContacto.data = output['celularContacto']

    return render_template('registrarProveedor.html', form=form_empresa, accion='Modificar')

@app.route('/deleteClienteEmp/<rutEliminar>')
def deleteClienteEmp(rutEliminar):
    if session['privilegios'] != 'ADMINISTRADOR':
        return render_template('login.html')

    CLIENTEEMP.delete_one({ 'rut': rutEliminar })
    flash('Empresa Cliente eliminada Correctamente')
    return render_template('index.html')

@app.route('/listClienteEmp', methods=['GET', 'POST'])
def listClienteEmp():

    output = CLIENTEEMP.find()
    return render_template('listarClienteEmp.html', empresas=output)