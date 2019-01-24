from wtforms.fields.html5 import TelField, IntegerField, EmailField, DateField
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

class formUsuario(Form):
    rut = StringField('rut',[
            validators.Required(message = 'Debe ingresar un RUT.'),
            validarRut
    ])
    nombres = StringField('nombres',[
            validators.Required(message = 'Debe ingresar Nombres.'),
            verificarCadena
    ])
    apellido1 = StringField('apellido1',[
            validators.Required(message = 'Debe ingresar Apellido Paterno.'),
            verificarCadena
    ])
    apellido2 = StringField('apellido2',[
            validators.Required(message = 'Debe ingresar Apellido Materno.'),
            verificarCadena
    ])
    nacimiento = DateField('nacimiento',[
            validators.Required(message = 'Debe ingresar fecha de nacimiento.')
    ])
    sueldo = IntegerField('sueldo',[
            validators.Required(message = 'Debe ingresar el sueldo.')
    ])
    direccion = StringField('direccion',[
            validators.Required(message = 'Debe ingresar una direccion.')
    ])
    estado = SelectField('estado',
            [validators.Required(message = 'Debe seleccionar un estado.')],
            choices=[('', 'Seleccionar'),('ACTIVO', 'Activo'), ('INACTIVO', 'Inavilitado')]
    )
    cargo = StringField('cargo',[
            validators.Required(message = 'Debe ingresar el cargo.'),
            verificarCadena
    ])


