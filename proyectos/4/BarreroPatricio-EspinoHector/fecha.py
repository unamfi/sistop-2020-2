import datetime


def convertir(fecha_lineal):
    formato = "%Y%m%d%H%M%S"
    return str(datetime.datetime.strptime(fecha_lineal,formato))

if __name__ == "__main__":
    a = convertir("20190509182600")
    print(a)