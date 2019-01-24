from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, url_for
from principal import *
from generaPDF import *
from datetime import datetime
import formulariosUsuario
import webbrowser as wb


@app.route('/creaDocumento')
def creaDocumento():
    datos = []
    datos.append({"DNI": "1110800310", "NOMBRE": "Andres", "APELLIDO": "Niño", "FECHA_NACIMIENTO": "06/06/2019", "HOLA": "hola"})
    datos.append({"DNI": "1110800311", "NOMBRE": "Andres", "APELLIDO": "Niño", "FECHA_NACIMIENTO": "06/06/2019", "HOLA": "chao"})

    titulo = "LISTADO DE USUARIOS"

    cabecera = (
        ("DNI", "D.N.I"),
        ("NOMBRE", "NOMBRE"),
        ("APELLIDO", "APELLIDO"),
        ("HOLA", "HOLA"),
        ("FECHA_NACIMIENTO", "FECHA DE NACIMIENTO"),
        ("FECHA_NACIMIENTO", "FECHA DE NACIMIENTO"),
    )

    nombrePDF = "reportes/reporte.pdf"

    reporte = reportePDF(titulo, cabecera, datos, nombrePDF).Exportar()
    wb.open_new('C:/Users/Reynier/AppData/Local/Programs/Python/Python37-32/Scripts/miproyecto/Scripts/Proyecto6/reportes/reporte.pdf')
    return render_template('index.html')