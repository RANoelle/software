from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, url_for
import formulariosBuscar
from principal import *
import time

def obtenerID(coleccion):
    ID = 0
    datos = coleccion.find()
    for dato in datos:
        if dato['_id'] > ID:
            ID = dato['_id']

    return ID+1

def validaCampos(lista,cont,fac, oc):

    if fac == '':
        flash('Debe ingresar numero de factura')
        return False
    if oc == '':
        flash('Debe ingresar numero de Orden de Compra.')
        return False
    for i in range(cont):
        if lista[i]['cantidad'] == '':
            flash('Debe ingresar cantidad del producto en el ITEM '+str(i+1))
            return False
        if int(lista[i]['cantidad']) < 1:
            flash('Cantidad invalida del producto en el ITEM '+str(i+1))
            return False
        buscado = PRODUCTOS.find_one({"codigo": int(lista[i]['codigo'])})
        if int(buscado['stock']) < int(lista[i]['cantidad']):
            flash('El STOCK es insuficiente para la cantidad del ITEM ' + str(i + 1))
            return False

    return True

@app.route('/addDespacho', methods=['GET', 'POST'])
def addDespacho():

    form_buscar = formulariosBuscar.formBuscarProducto(request.form)
    listaProductos = []
    temporales = []
    contador = 0
    info = []

    info.append(time.strftime("%d/%m/%y"))
    info.append(time.strftime("%H:%M:%S"))

    if request.method == 'POST' and form_buscar.validate():

        info.append(request.form['factura'])
        info.append(request.form['ordenCompra'])
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
            listaProductos.append({
                'codigo': request.form['codigo' + str(i)],
                'cantidad': request.form['cantidad' + str(i)]
            })

        if accion == 'Registrar':
            despacho = ({
                '_id': obtenerID(DESPACHOS),
                'rutresponsable': session['rut'],
                'fecha': info[0],
                'hora': info[1],
                'factura': request.form['factura'],
                'ordencompra': request.form['ordenCompra'],
                'listaproductos': listaProductos
            })

            if validaCampos(temporales, contador, request.form['factura'],request.form['ordenCompra']) == False:
                    return render_template('registrarDespacho.html', form=form_buscar, contador=contador, productos=temporales,info=info)

            for producto in listaProductos:
                buscado = PRODUCTOS.find_one({"codigo": int(producto['codigo'])})
                newStock = int(buscado['stock']) - int(producto['cantidad'])
                PRODUCTOS.update_one({"codigo": int(buscado['codigo'])}, {"$set": {
                        'stock': newStock
                    }})

            DESPACHOS.insert(despacho)

            flash('Despacho ingresado correctamente.')
            return render_template('index.html')


        if request.form['accion'] == 'Quitar':
            temporales.pop(int(request.form['IDquitar']))
            contador -= 1
            return render_template('registrarDespacho.html', form=form_buscar, contador=contador,productos=temporales, info=info)

        datosProducto = PRODUCTOS.find_one({"codigo": form_buscar.productoBuscado.data})
        for i in range(contador):
            if int(temporales[i]['codigo']) == int(datosProducto['codigo']):
                return render_template('registrarDespacho.html', form=form_buscar, contador=contador,productos=temporales, info=info)

        temporales.append(datosProducto)
        contador += 1
        return render_template('registrarDespacho.html', form=form_buscar,contador=contador, productos=temporales, info=info)


    return render_template('registrarDespacho.html',form=form_buscar,productos=temporales,contador=contador, info=info)


@app.route('/listDespachos', methods=['GET', 'POST'])
def listDespachos():

    output = DESPACHOS.find()
    return render_template('listarDespachos.html', despachos=output)