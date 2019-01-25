from wtforms import validators,StringField,SelectField
from wtforms.fields.html5 import TelField, IntegerField, EmailField, DateField
from validaciones.validaRUT import esRut, darFormatoRut
from datetime import datetime, date, timedelta
from wtforms import Form
from principal import *

def existeUser(form, field):
    resultado = esRut(field.data)
    if resultado == True:
        field.data = darFormatoRut(field.data)
        existe = USUARIOS.find_one({"rut": field.data})
        if existe == None:
            raise validators.ValidationError('RUT no encontrado.')
    else:
        raise validators.ValidationError(resultado)

def validaFecha(form, field):
    if form.fechaInicio.data > form.fechaFin.data:
        raise validators.ValidationError('Fecha inicio no debe ser mayor a la fecha Termino.')

def validaFechaTermino(form, field):
    fechaActual = datetime.now().date()
    if field.data > fechaActual:
        raise validators.ValidationError('Fecha termino no debe ser superior a fecha acyual.')


def existeCliente(form, field):
    resultado = esRut(field.data)
    if resultado == True:
        field.data = darFormatoRut(field.data)
        existe = CLIENTEEMP.find_one({"rut": field.data})
        if existe == None:
            raise validators.ValidationError('RUT no encontrado.')
    else:
        raise validators.ValidationError(resultado)



class formReportUser(Form):
    rutUser = StringField('rutUser',[
            validators.Required(message = 'Debe ingresar un RUT.'),
            existeUser
    ])
    buscaGuia = SelectField('estado',
            [validators.Required(message='Debe seleccionar un tipo de guia.')],
            choices=[('', 'Seleccionar...'), ('AMBOS', 'AMBOS'),('DESPACHOS', 'DESPACHOS'), ('RECEPCIONES', 'RECEPCIONES')]
    )
    fechaInicio = DateField('fechaInicio', [
        validators.Required(message='Debe ingresar una Fecha de Inicio.'),
        validaFecha
    ])
    fechaFin = DateField('fechaFin', [
        validators.Required(message='Debe ingresar una Fecha de Termino.'),
        validaFechaTermino
    ])


class formReportCliente(Form):
    rutCliente = StringField('rutCliente',[
            validators.Required(message = 'Debe ingresar un RUT.'),
            existeCliente
    ])
    fechaInicio = DateField('fechaInicio', [
        validators.Required(message='Debe ingresar una Fecha de Inicio.'),
        validaFecha
    ])
    fechaFin = DateField('fechaFin', [
        validators.Required(message='Debe ingresar una Fecha de Termino.'),
        validaFechaTermino
    ])