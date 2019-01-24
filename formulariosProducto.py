from wtforms.fields.html5 import TelField, IntegerField, EmailField, DateField
from wtforms import validators, StringField, TextField, SelectField
from validaciones.validaCadena import validaCadena
from wtforms import Form


def verificarCadena(form, field):
    if validaCadena(field.data, '-') == False:
        raise validators.ValidationError('El valor ingresado no es valido.')

def validaPrecio(form, field):
    if int(field.data) < 1:
        raise validators.ValidationError('El precio no es valido.')

def validaStock(form, field):
    if int(field.data) < 0:
        raise validators.ValidationError('El stock no es valido.')


class formProducto(Form):
    codigo = IntegerField('codigo', [
        validators.Required(message='Debe ingresar el codigo.')
    ])
    nombre = StringField('nombre', [
        validators.Required(message='Debe ingresar un Nombre.')
    ])
    precio = IntegerField('precio', [
        validators.Required(message='Debe ingresar el Precio.'),
        validaPrecio
    ])
    disponible = SelectField('disponible', [
        validators.Required(message='Debe seleccionar disponibilidad.')],
        choices=[('', 'Seleccionar...'), ('SI', 'SI'), ('NO', 'NO')]
        )
    descripcion = StringField('descripcion', [
        validators.Required(message='Debe ingresar una Descripcion.')
    ])
    stock = IntegerField('stock', [
        validators.Required(message='Debe ingresar el Stock.'),
        validaStock
    ])

