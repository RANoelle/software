from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, url_for
from principal import *
from generaPDF import *
from datetime import datetime
import formulariosReporte
import webbrowser as wb


@app.route('/creaDocumento1', methods=['GET', 'POST'])
def creaDocumento1():
    if session['privilegios'] != 'ADMINISTRADOR':
        return render_template('login.html')

    form_reporte = formulariosReporte.formReportUser(request.form)

    if request.method == 'POST' and form_reporte.validate():

        cadena = request.form['fechaInicio'].split("-")
        inicio = datetime.strptime(cadena[2] + '/' + cadena[1] + '/' + cadena[0], '%d/%m/%Y')
        cadena = request.form['fechaFin'].split("-")
        fin = datetime.strptime(cadena[2] + '/' + cadena[1] + '/' + cadena[0], '%d/%m/%Y')

        if request.form['buscaGuia']=='RECEPCIONES':
            encontrados = RECEPCIONES.find({"rutresponsable": request.form['rutUser']})
            cabecera = (
                ("_id", "ID"),
                ("rutresponsable", "RESPONSABLE"),
                ("rutproveedor", "PROVEEDOR"),
                ("fecha", "FECHA"),
                ("hora", "HORA"),
                ("factura", "FACTURA"),
                ("guiadespacho", "G. DESPACHO"),
            )

        if request.form['buscaGuia']=='DESPACHOS':
            encontrados = DESPACHOS.find({"rutresponsable": request.form['rutUser']})
            cabecera = (
                ("_id", "ID"),
                ("rutresponsable", "RESPONSABLE"),
                ("rutproveedor", "PROVEEDOR"),
                ("fecha", "FECHA"),
                ("hora", "HORA"),
                ("factura", "FACTURA"),
                ("ordencompra", "O. COMPRA"),
            )

        seleccionados = []

        for encontrado in encontrados:
            cadena = encontrado['fecha'].split("/")
            fecha = datetime.strptime(cadena[0] + '/' + cadena[1] + '/20' + cadena[2], '%d/%m/%Y')
            if fecha >= inicio and fecha <= fin:
                seleccionados.append(encontrado)


        titulo = "LISTADO DE "+request.form['buscaGuia']

        nombrePDF = "reportes/reporteUsuario"+request.form['rutUser']+".pdf"

        reporte = reportePDF(titulo, cabecera, seleccionados, nombrePDF).Exportar()
        #wb.open_new('C:/Users/Reynier/AppData/Local/Programs/Python/Python37-32/Scripts/miproyecto/Scripts/Proyecto6/reportes/'+nombrePDF)
        flash('El Reporte se creo correctamente.')
        return render_template('index.html')

    return render_template('reporteUsuario.html',form=form_reporte)


@app.route('/creaDocumento2', methods=['GET', 'POST'])
def creaDocumento2():
    if session['privilegios'] != 'ADMINISTRADOR':
        return render_template('login.html')

    form_reporte = formulariosReporte.formReportCliente(request.form)

    if request.method == 'POST' and form_reporte.validate():

        cadena = request.form['fechaInicio'].split("-")
        inicio = datetime.strptime(cadena[2] + '/' + cadena[1] + '/' + cadena[0], '%d/%m/%Y')
        cadena = request.form['fechaFin'].split("-")
        fin = datetime.strptime(cadena[2] + '/' + cadena[1] + '/' + cadena[0], '%d/%m/%Y')


        encontrados = DESPACHOS.find({"rutcliente": request.form['rutCliente']})
        cabecera = (
                ("_id", "ID"),
                ("rutresponsable", "RESPONSABLE"),
                ("rutcliente", "PROVEEDOR"),
                ("fecha", "FECHA"),
                ("hora", "HORA"),
                ("factura", "FACTURA"),
                ("ordencompra", "O. COMPRA"),
            )

        seleccionados = []

        for encontrado in encontrados:
            cadena = encontrado['fecha'].split("/")
            fecha = datetime.strptime(cadena[0] + '/' + cadena[1] + '/20' + cadena[2], '%d/%m/%Y')
            if fecha >= inicio and fecha <= fin:
                seleccionados.append(encontrado)


        titulo = "LISTADO DE DESPACHOS"

        nombrePDF = "reportes/reporteCliente"+request.form['rutCliente']+".pdf"

        reporte = reportePDF(titulo, cabecera, seleccionados, nombrePDF).Exportar()
        #wb.open_new('C:/Users/Reynier/AppData/Local/Programs/Python/Python37-32/Scripts/miproyecto/Scripts/Proyecto6/'+nombrePDF)
        flash('El Reporte se creo correctamente.')
        return render_template('index.html')

    return render_template('reporteCliente.html',form=form_reporte)