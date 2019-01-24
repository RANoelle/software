from wtforms import validators,StringField, IntegerField
from validaciones.validaRUT import esRut, darFormatoRut
from wtforms import Form
from principal import *

def existeProducto(form, field):
    existe = PRODUCTOS.find_one({"codigo": field.data})
    if existe == None:
        raise validators.ValidationError('Codigo no encontrado.')

def existeRecepcion(form, field):
    existe = RECEPCIONES.find_one({"_id": field.data})
    if existe == None:
        raise validators.ValidationError('ID no encontrado.')

def existeDespacho(form, field):
    existe = DESPACHOS.find_one({"_id": field.data})
    if existe == None:
        raise validators.ValidationError('ID no encontrado.')

def validarRut(form, field):
    resultado = esRut(field.data)
    if resultado == True:
        field.data = darFormatoRut(field.data)
    else:
        raise validators.ValidationError(resultado)

def existeClienteEmp(form, field):
    resultado = esRut(field.data)
    if resultado == True:
        field.data = darFormatoRut(field.data)
        existe = CLIENTEEMP.find_one({"rut": field.data})
        if existe == None:
            raise validators.ValidationError('RUT no encontrado.')
    else:
        raise validators.ValidationError(resultado)




class formBuscarRUT(Form):
    rutbuscado = StringField('rutbuscado',[
            validators.Required(message = 'Debe ingresar un RUT.'),
            validarRut
    ])

class formBuscarProducto(Form):
    productoBuscado = IntegerField('productoBuscado',[
            validators.Required(message = 'Debe ingresar un Codigo valido.'),
            existeProducto
    ])

class formBuscarRecepcion(Form):
    recepcionBuscada = IntegerField('recepcionBuscada',[
            validators.Required(message = 'Debe ingresar un ID de Recepcion valido.'),
            existeRecepcion
    ])

class formBuscarDespacho(Form):
    despachoBuscado = IntegerField('despachoBuscado',[
            validators.Required(message = 'Debe ingresar un ID de Despacho valido.'),
            existeDespacho
    ])

class formBuscarRutEmp(Form):
    rutEmpBuscado = StringField('rutEmpBuscado',[
            validators.Required(message = 'Debe ingresar un RUT.'),
            existeClienteEmp
    ])