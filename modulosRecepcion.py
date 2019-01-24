from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, url_for
from principal import *
import time

def obtenerID(coleccion):
    ID = 0
    datos = coleccion.find()
    for dato in datos:
        if dato['_id'] > ID:
            ID = dato['_id']

    return ID+1

def validaCampos(inputs,item):
    falta = 'NINGUNO'
    if inputs['precio'] == '':
        falta = 'precio'
    if inputs['cantidad'] == '':
        falta = 'cantidad'
    if inputs['descripcion'] == '':
        falta = 'descripcion'
    if inputs['nombre'] == '':
        falta = 'nombre'
    if inputs['codigo'] == '':
        falta = 'codigo'
    if falta != 'NINGUNO':
        flash('Debe ingresar '+falta+' del producto en el ITEM '+str(item+1))
        return False
    if int(inputs['cantidad']) < 1:
        flash('Cantidad invalida del producto en el ITEM '+str(item+1))
        return False
    return True

@app.route('/addRecepcion/<rutProveedor>', methods=['GET', 'POST'])
def addRecepcion(rutProveedor):
    datosProveedor = PROVEEDORES.find_one({"rut": rutProveedor})
    listaProductos = []
    temporales = []
    contador = 1
    info = []
    TOTAL = 0

    info.append(time.strftime("%d/%m/%y"))
    info.append(time.strftime("%H:%M:%S"))

    if request.method == 'POST':
        info.append(request.form['factura'])
        info.append(request.form['guiaDespacho'])

        contador = int(request.form['contador'])
        accion = request.form['accion']

        for i in range(contador):
            temporales.append({
                'codigo': request.form['codigo' + str(i)],
                'nombre': request.form['nombre' + str(i)],
                'descripcion': request.form['descripcion' + str(i)],
                'cantidad': request.form['cantidad' + str(i)],
                'precio': request.form['precio' + str(i)]
            })
            #TOTAL += (int(request.form['cantidad' + str(i)])*int(request.form['precio' + str(i)]))

            listaProductos.append({
                'codigo': request.form['codigo' + str(i)],
                'cantidad': request.form['cantidad' + str(i)]
            })

        if accion == 'Registrar':
            recepcion = ({
                '_id': obtenerID(RECEPCIONES),
                'rutresponsable': session['rut'],
                'rutproveedor': datosProveedor['rut'],
                'fecha': info[0],
                'hora': info[1],
                'factura': request.form['factura'],
                'guiadespacho': request.form['guiaDespacho'],
                'listaproductos': listaProductos
            })
            if request.form['factura'] == '':
                flash('Debe ingresar numero de factura.')
                return render_template('registrarRecepcion.html', contador=contador, productos=temporales, info=info,proveedor=datosProveedor)

            if request.form['guiaDespacho'] == '':
                flash('Debe ingresar numero de guia de despacho.')
                return render_template('registrarRecepcion.html', contador=contador, productos=temporales, info=info,proveedor=datosProveedor)


            for i in range(contador):
                if validaCampos(temporales[i], i) == False:
                    return render_template('registrarRecepcion.html', contador=contador, productos=temporales,info=info, proveedor=datosProveedor)

                existe = PRODUCTOS.find_one({"codigo": int(listaProductos[i]['codigo'])})
                if existe == None:
                    PRODUCTOS.insert({
                        'codigo': int(request.form['codigo' + str(i)]),
                        'nombre': request.form['nombre' + str(i)],
                        'descripcion': request.form['descripcion' + str(i)],
                        'disponible': 'SI',
                        'precio': int(request.form['precio' + str(i)]),
                        'stock': int(request.form['cantidad' + str(i)])
                    })

                else:
                    newStock = int(existe['stock']) + int(request.form['cantidad' + str(i)])
                    PRODUCTOS.update_one({"codigo": int(exite['codigo'])}, {"$set": {
                        'stock': newStock
                    }})

            RECEPCIONES.insert(recepcion)

            flash('Recepcion ingresada correctamente.')
            return render_template('index.html')


        if accion == 'agregar':
            contador += 1
        if accion == 'quitar':
            contador -= 1
        if contador < 1:
            contador = 1

    temporales.append({
        'codigo': '',
        'nombre': '',
        'descripcion': '',
        'cantidad': '',
        'precio': ''
    })

    return render_template('registrarRecepcion.html',contador=contador,productos=temporales,info=info,proveedor=datosProveedor)


@app.route('/listRecepcion', methods=['GET', 'POST'])
def listRecepcion():

    output = RECEPCIONES.find()
    return render_template('listarRecepciones.html', recepciones=output)