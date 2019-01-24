from wtforms import validators, StringField, TextField, SelectField
from validaciones.validaRUT import esRut, darFormatoRut
from validaciones.validaCadena import validaCadena
from wtforms import Form


def verificarCadena(form, field):
    if validaCadena(field.data, '-') == False:
        raise validators.ValidationError('El valor ingresado no es valido.')

def validarRut(form, field):
    resultado = esRut(field.data)
    if resultado == True:
        field.data = darFormatoRut(field.data)
    else:
        raise validators.ValidationError(resultado)

class formProveedor(Form):
    rut = StringField('rut', [
        validators.Required(message='Debe ingresar un RUT.'),
        validarRut
    ])
    nombre = StringField('nombre', [
        validators.Required(message='Debe ingresar Nombre.')
    ])
    ciudad = StringField('ciudad', [
        validators.Required(message='Debe ingresar Ciudad.'),
        verificarCadena
    ])
    comuna = StringField('comuna', [
        validators.Required(message='Debe ingresar Comuna.'),
        verificarCadena
    ])
    correo = StringField('correo', [
        validators.Required(message='Debe ingresar Email.')
    ])
    nombreContacto = StringField('nombreContacto', [
        validators.Required(message='Debe ingresar Nombre de Contacto.'),
        verificarCadena
    ])
    celularContacto = StringField('celularContacto', [
        validators.Required(message='Debe ingresar Celular de Contacto.')
    ])

