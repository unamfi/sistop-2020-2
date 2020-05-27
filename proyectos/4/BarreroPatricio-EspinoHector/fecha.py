import datetime


##Convierte de la fecha lineal a un string formatareado
def formatear(fecha_lineal):
    formato = "%Y%m%d%H%M%S"
    return str(datetime.datetime.strptime(fecha_lineal,formato))

##Convierte de un string formateado a una fecha lineal
def compactar(fecha):
    formato = "%Y%m%d%H%M%S"
    formato_original = "%Y-%m-%d %H:%M:%S"
    fecha_obj=datetime.datetime.strptime(fecha,formato_original)
    return datetime.datetime.strftime(fecha_obj,formato)

def fecha_actual():
    return datetime.datetime.now()

if __name__ == "__main__":
    a = formatear("20190509182600")
    print(a)
    print(compactar(a))
