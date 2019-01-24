from itertools import cycle

def esRut(rut):
    caracteres = '0123456789kK.-'

    contador = 0

    for i in range(len(rut)):
        ubicacion = rut[i:i + 1]
        if caracteres.find(ubicacion) != -1:
            contador += 1
        else:
            return 'El caracter ' + ubicacion + ' no es admitido'

    rut = rut.upper()
    rut = rut.replace("-", "")
    rut = rut.replace(".", "")
    aux = rut[:-1]
    dv = rut[-1:]

    revertido = map(int, reversed(str(aux)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(revertido, factors))
    res = (-s) % 11

    if str(res) == dv:
        return True
    elif dv == "K" and res == 10:
        return True
    else:
        return 'El RUT no es valido.'


def darFormatoRut(rut):
    rut = rut.upper();
    rut = rut.replace("-", "")
    rut = rut.replace(".", "")

    rutInverso = rut[::-1]

    for i in range(len(rutInverso)):
        digito = rutInverso[i:i+1]
        if i == 0:
            rutFinal = digito
            rutFinal += '-'
        else:
            rutFinal += digito
        if i == 3 or i == 6:
            rutFinal += '.'

    rutFinal = rutFinal[::-1]

    return rutFinal