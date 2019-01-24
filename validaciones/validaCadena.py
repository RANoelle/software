
def validaCadena(cadena, caracterExtra):
    enter = '\n\t '
    enie = '\u00f1\u00d1'
    caracteres = 'abcdefghijklmnopqrstuvwxyzñABCDEFGHIJKLMNOPQRSTUVWXYZÑáéíóúÁÉÍÓÚ'+enter+caracterExtra+enie

    contador = 0

    for i in range(len(cadena)):
        ubicacion = cadena[i:i+1]
        if caracteres.find(ubicacion) != -1:
            contador+=1
        else:
            return False

    return True