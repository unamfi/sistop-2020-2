'''
Archivo principal, 

'''
from servicio import Servicio
from comensal import Clientes
from cocina import Cocina

import argparse
from time import sleep
class Restaurante:
    """
    Representa el concepto del restaurante

    Atributos:  
    servicio (Servicio): Permite manipular a los meseros de una forma sencilla   
    cocina (Cocina): Permite manipular a los cocineros de una forma sencilla  
    clientes (Clientes): Permite manipular a los clientes de una forma sencila  
    """
    pass

    def main(self):
        parser = argparse.ArgumentParser(description="""Este programa permite simular el comportamiento de un\
            de un restaurante. Y los distintos comportamientos concurrentes que estos presentan. 

            Ejemplo de uso:
            python3 restaurante.py 6 3 2 2
            """)
        parser.add_argument("grupos",type=int,help="Numero de grupos de clientes")
        parser.add_argument("maxgrupos",type=int,help="Numero maximo de  clientes por grupo")
        parser.add_argument("meseros",type=int,help="Numero de meseros")
        parser.add_argument("mesas",type=int,help="Numero de mesas")
        parser.add_argument("chefs",type=int,help="Numero de chefs")
        arg = parser.parse_args()
        return arg        


if __name__ == "__main__":
    restarurantito = Restaurante()
    arg = restarurantito.main()

    num_mesas = arg.mesas
    num_meseros = arg.meseros
    num_cocineros = arg.chefs
    num_grupos = arg.grupos
    max_por_grupo = arg.maxgrupos

    cocina =  Cocina(num_cocineros)
    servicio = Servicio(cocina, num_mesas, num_meseros)
    cocina.anadir_servicio(servicio)
    clientes = Clientes(num_grupos, max_por_grupo, servicio)
    servicio.start()

    cocina.start()
    clientes.iniciar()
    