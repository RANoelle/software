from wtforms import validators, StringField, SelectField
from wtforms import Form
from flask import session


def confirmaClave(form, field):
    if session['password'] != field.data:
        raise validators.ValidationError('Clave incorrecta.')

def comparaClave(form, field):
    if form.claveNueva1.data != form.claveNueva2.data:
        raise validators.ValidationError('Las claves no coinciden.')

class formCuenta(Form):
    claveSesion = StringField('claveSesion',[
            validators.Required(message = 'Debe ingresar clave actual.'),
            confirmaClave
            ])
    claveNueva1 = StringField('claveNueva1',[
            validators.Required(message = 'Debe ingresar nueva clave.'),
            comparaClave
            ])
    claveNueva2 = StringField('claveNueva2',[
            validators.Required(message = 'Debe volver a ingresar la nueva clave.'),
            comparaClave
            ])
    privilegios = SelectField('privilegios',
                              [validators.Required(message='Debe seleccionar un privilegio.')],
                              choices=[('', 'Seleccionar..'), ('BASICO', 'BASICO'), ('ADMINISTRADOR', 'ADMINISTRADOR')]
                              )
    estado = SelectField('estado',
                              [validators.Required(message='Debe seleccionar un estado.')],
                              choices=[('', 'Seleccionar...'), ('ACTIVO', 'ACTIVO'), ('BLOQUEADO', 'BLOQUEADO')]
                              )