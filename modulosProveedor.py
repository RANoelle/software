from flask import Flask, render_template, session, flash, request
from principal import *
import formulariosProveedor

@app.route('/addProveedor', methods=['GET', 'POST'])
def addProveedor():
    if session['privilegios'] != 'ADMINISTRADOR':
        return render_template('login.html')

    form_proveedor = formulariosProveedor.formProveedor(request.form)

    if request.method == 'POST' and form_proveedor.validate():
        PROVEEDORES.insert({
            'rut': form_proveedor.rut.data,
            'nombre': form_proveedor.nombre.data,
            'ciudad': form_proveedor.ciudad.data,
            'comuna': form_proveedor.comuna.data,
            'correo':form_proveedor.correo.data,
            'nombreContacto': form_proveedor.nombreContacto.data,
            'celularContacto': form_proveedor.celularContacto.data
        })
        flash('Proveedor ingresado correctamente')
        return render_template('index.html')

    return render_template('registrarProveedor.html', form=form_proveedor, accion='Registrar')

@app.route('/editProveedor/<rutModificar>', methods=['GET', 'POST'])
def editProveedor(rutModificar):
    if session['privilegios'] != 'ADMINISTRADOR':
        return render_template('login.html')

    form_proveedor = formulariosProveedor.formProveedor(request.form)
    ponerDatosOriginales = True

    if request.method == 'POST':

        form_proveedor.rut.data = rutModificar
        form_proveedor.nombre.data = request.form['nombre']
        form_proveedor.ciudad.data = request.form['ciudad']
        form_proveedor.comuna.data = request.form['comuna']
        form_proveedor.correo.data = request.form['correo']
        form_proveedor.nombreContacto.data = request.form['nombreContacto']
        form_proveedor.celularContacto.data = request.form['celularContacto']
        ponerDatosOriginales = False

        if form_proveedor.validate():
            PROVEEDORES.update_one({"rut": rutModificar}, {"$set": {
                'nombre': request.form['nombre'],
                'ciudad': request.form['ciudad'],
                'comuna': request.form['comuna'],
                'correo': request.form['correo'],
                'nombreContacto': request.form['nombreContacto'],
                'celularContacto': request.form['celularContacto']
            }})
            flash('Los datos del Proveedor se actualizaron correctamente.')
            return render_template('index.html')

    if ponerDatosOriginales:
        output = PROVEEDORES.find_one({"rut": rutModificar})

        form_proveedor.rut.data = rutModificar
        form_proveedor.nombre.data = output['nombre']
        form_proveedor.ciudad.data = output['ciudad']
        form_proveedor.comuna.data = output['comuna']
        form_proveedor.correo.data = output['correo']
        form_proveedor.nombreContacto.data = output['nombreContacto']
        form_proveedor.celularContacto.data = output['celularContacto']

    return render_template('registrarProveedor.html', form=form_proveedor, accion='Modificar')

@app.route('/deleteProveedor/<rutEliminar>')
def deleteProveedor(rutEliminar):
    if session['privilegios'] != 'ADMINISTRADOR':
        return render_template('login.html')

    PROVEEDORES.delete_one({ 'rut': rutEliminar })
    flash('Proveedor eliminado Correctamente')
    return render_template('index.html')

@app.route('/listProveedor', methods=['GET', 'POST'])
def listProveedor():

    output = PROVEEDORES.find()
    return render_template('listarProveedor.html', proveedores=output)