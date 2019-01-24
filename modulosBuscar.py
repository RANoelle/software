from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, url_for
from principal import *
import formulariosBuscar

@app.route('/findRUT/<accion>/<buscado>', methods=['GET', 'POST'])
def findRUT(accion,buscado):

    buscar_rut = formulariosBuscar.formBuscarRUT(request.form)

    if request.method == 'POST' and buscar_rut.validate():
        if buscado == 'Usuario':
            output = USUARIOS.find_one({"rut": buscar_rut.rutbuscado.data})
        if buscado == 'Proveedor':
            output = PROVEEDORES.find_one({"rut": buscar_rut.rutbuscado.data})
        if output == None:
            flash('*Rut no encontrado.')
            return render_template('buscarRut.html', form=buscar_rut, accion=accion,buscado=buscado)
        else:
            if accion == 'Crear Cuenta' and buscado == 'Usuario':
                return redirect(url_for('addCuenta',rutUsuario=output['rut']))
            if accion == 'Buscar Cuenta' and buscado == 'Usuario':
                return redirect(url_for('showCuenta',rutUsuario=output['rut']))
            if accion == 'Vincular' and buscado == 'Proveedor':
                return redirect(url_for('addRecepcion',rutProveedor=output['rut']))
            if buscado == 'Usuario':
                return render_template('mostrarUsuario.html', usuario=output, accion=accion)
            if buscado == 'Proveedor':
                return render_template('mostrarProveedor.html', proveedor=output, accion=accion)

    return render_template('buscarRut.html', form=buscar_rut, accion=accion,buscado=buscado)


@app.route('/findProducto/<accion>', methods=['GET', 'POST'])
def findProducto(accion):
    form_buscar = formulariosBuscar.formBuscarProducto(request.form)

    if request.method == 'POST' and form_buscar.validate():
        datosProducto = PRODUCTOS.find_one({"codigo": form_buscar.productoBuscado.data})
        if datosProducto == None:
            flash('*Codigo no encontrado.')
            return render_template('buscarProducto.html', form=form_buscar)
        else:
            return render_template('mostrarProducto.html', producto=datosProducto, accion=accion)


    return render_template('buscarProducto.html', form=form_buscar)


@app.route('/findRecepcion/<accion>', methods=['GET', 'POST'])
def findRecepcion(accion):
    form_buscar = formulariosBuscar.formBuscarRecepcion(request.form)

    if request.method == 'POST' and form_buscar.validate():
        datosRecepcion = RECEPCIONES.find_one({"_id": form_buscar.recepcionBuscada.data})
        if datosRecepcion == None:
            flash('*ID no encontrado.')
            return render_template('buscarRecepcion.html', form=form_buscar)
        else:
            datosResponsable = USUARIOS.find_one({"rut": datosRecepcion['rutresponsable']})
            datosProveedor = PROVEEDORES.find_one({"rut": datosRecepcion['rutproveedor']})
            datosProductos = []
            for producto in datosRecepcion['listaproductos']:
                datosProductos.append(PRODUCTOS.find_one({"codigo": int(producto['codigo'])}))


            return render_template(
                            'mostrarRecepcion.html',
                            recepcion=datosRecepcion,
                            responsable=datosResponsable,
                            proveedor=datosProveedor,
                            cantidades=datosRecepcion['listaproductos'],
                            productos=datosProductos,
                            accion=accion
                            )

    return render_template('buscarRecepcion.html', form=form_buscar)


@app.route('/findDespacho/<accion>', methods=['GET', 'POST'])
def findDespacho(accion):
    form_buscar = formulariosBuscar.formBuscarDespacho(request.form)

    if request.method == 'POST' and form_buscar.validate():
        datosDespacho = DESPACHOS.find_one({"_id": form_buscar.despachoBuscado.data})
        datosResponsable = USUARIOS.find_one({"rut": datosDespacho['rutresponsable']})
        datosProductos = []
        for producto in datosDespacho['listaproductos']:
            datosProductos.append(PRODUCTOS.find_one({"codigo": int(producto['codigo'])}))


        return render_template(
                            'mostrarDespacho.html',
                            despacho=datosDespacho,
                            responsable=datosResponsable,
                            cantidades=datosDespacho['listaproductos'],
                            productos=datosProductos,
                            accion=accion
                            )

    return render_template('buscarDespacho.html', form=form_buscar)

@app.route('/findClienteEmp/<accion>', methods=['GET', 'POST'])
def findClienteEmp(accion):
    form_buscar = formulariosBuscar.formBuscarRutEmp(request.form)

    if request.method == 'POST' and form_buscar.validate():
        empresa = CLIENTEEMP.find_one({"rut": form_buscar.rutEmpBuscado.data})
        return render_template('mostrarClienteEmp.html',empresa=empresa,accion=accion)


    return render_template('buscarClienteEmp.html', form=form_buscar,accion=accion)