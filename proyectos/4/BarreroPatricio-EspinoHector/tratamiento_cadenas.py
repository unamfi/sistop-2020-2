##Comprobamos que el nombre este en  asccii
def validar_nombre(nombre):
    if all(ord(char) < 128 for char in nombre):
        if len(nombre) <= 15:
            return True
    return False

def agregar_espacios(cadena, num):
    num_espacios =  num - len(str(cadena))
    if num_espacios <= 0:
        return cadena
    return ' ' * num_espacios + str(cadena)
