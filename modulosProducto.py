from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, url_for
from principal import *
import formulariosProducto


@app.route('/addProducto', methods=['GET', 'POST'])
def addProducto():
    form_producto = formulariosProducto.formProducto(request.form)

    if request.method == 'POST' and form_producto.validate():
        PRODUCTOS.insert({
            'codigo': int(form_producto.codigo.data),
            'nombre': form_producto.nombre.data,
            'precio': int(form_producto.precio.data),
            'stock': int(form_producto.stock.data),
            'disponible': form_producto.disponible.data,
            'descripcion': form_producto.descripcion.data
        })
        flash('Producto ingresado correctamente.')
        return render_template('index.html')

    return render_template('registrarProducto.html', form=form_producto,accion='Registrar')




@app.route('/editProducto/<codigoModificar>', methods=['GET', 'POST'])
def editProducto(codigoModificar):

    form_producto = formulariosProducto.formProducto(request.form)
    ponerDatosOriginales = True

    if request.method == 'POST':

        form_producto.codigo.data = int(request.form['codigo'])
        form_producto.nombre.data = request.form['nombre']
        form_producto.precio.data = request.form['precio']
        form_producto.stock.data = request.form['stock']
        form_producto.disponible.data = request.form['disponible']
        form_producto.descripcion.data = request.form['descripcion']
        ponerDatosOriginales = False

        if form_producto.validate():
            PRODUCTOS.update_one({"codigo": form_producto.codigo.data}, {"$set": {
                'nombre': request.form['nombre'],
                'precio': int(request.form['precio']),
                'stock': int(request.form['stock']),
                'disponible': request.form['disponible'],
                'descripcion': request.form['descripcion']
            }})
            flash('Los datos del Producto se actualizaron correctamente.')
            return render_template('index.html')

    if ponerDatosOriginales:
        output = PRODUCTOS.find_one({"codigo": int(codigoModificar)})
        form_producto.codigo.data = int(output['codigo'])
        form_producto.nombre.data = output['nombre']
        form_producto.precio.data = output['precio']
        form_producto.stock.data = output['stock']
        form_producto.disponible.data = output['disponible']
        form_producto.descripcion.data = output['descripcion']

    return render_template('registrarProducto.html', form=form_producto, accion='Modificar')



@app.route('/listProducto', methods=['GET', 'POST'])
def listProducto():

    output = PRODUCTOS.find()
    return render_template('listarProductos.html', productos=output)

@app.route('/deleteProducto/<codigoEliminar>')
def deleteProducto(codigoEliminar):
    PRODUCTOS.delete_one({ 'codigo': codigoEliminar })
    flash('El Producto se elimino correctamente.')
    return render_template('index.html')
