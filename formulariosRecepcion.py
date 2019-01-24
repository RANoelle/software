from wtforms.fields.html5 import TelField, IntegerField, EmailField, DateField
from wtforms import validators, StringField, TextField, SelectField
from validaciones.validaCadena import validaCadena
from wtforms import Form

def verificarCadena(form, field):
    if validaCadena(field.data, '-') == False:
        raise validators.ValidationError('El valor ingresado no es valido.')

class formRecepcion(Form):
    codigo = IntegerField('codigo', [
        validators.Required(message='Debe ingresar un codigo.')
    ])
    nombre = StringField('nombre', [
        validators.Required(message='Debe ingresar Nombre del producto.'),
        verificarCadena
    ])
    descripcion = StringField('descripcion', [
        validators.Required(message='Debe ingresar Descripcion del producto.')
    ])
    cantidad = IntegerField('cantidad', [
        validators.Required(message='Debe ingresar cantidad.')
    ])
    precio = IntegerField('precio', [
        validators.Required(message='Debe ingresar Precio.')
    ])