# Funciones Relacionadas con Manejo de Archivos

def tamano_archivo(ubicacion):
    temp = open(ubicacion, "rb+")
    cantidad = len(temp.read())
    temp.close()
    return cantidad

def escribir(inicio, contenido, ubicacion, codificacion = "utf-8"):
    if contenido:
        contenido = bytes(contenido, codificacion)
    archivo = open(ubicacion, "rb+")
    archivo.seek(inicio)
    archivo.write(contenido)
    archivo.close()

def leer(inicio, cantidad, ubicacion, codificacion = "utf-8"):
    archivo = open(ubicacion, "rb+")
    archivo.seek(inicio)
    lectura = archivo.read(cantidad)
    archivo.close()
    try:
        return lectura.decode(codificacion)  # hex => str
    except:
        return lectura