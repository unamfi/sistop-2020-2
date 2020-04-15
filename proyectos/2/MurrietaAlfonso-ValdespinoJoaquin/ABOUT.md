# SIMULADOR DE AGENCIAS DE VIAJE - PROYECTO 2 

## Integrantes:

- Alfonso Murrieta Villegas
- Valdespino Mendieta Joaquín

## Especificaciones generales y de ejecución:

Lenguaje de programación: 
- Python - versión 3.8

Ejecución del programa:
- Entra a la carpeta correspondiente y ejecutar en terminal la siguiente instrucción:
``` python3 main.py ``` 

## Descripción general del código:

Cabe destacar que dentro de cada código de python hay comentarios relevantes para una mayor comprensión del código,
sin embargo, en este apartado sólamente se tratará de la distribución u organización del código:

### Árbol del proyecto

Descripción general de la ubicación y códigos que conforman a este proyecto:

    - main.py
    - modulos 
        - agencia.py 
        - compania.py
        - cliente.py

Como se muestra previamente, dentro de la carpeta modulos, se encuentran 3 códigos de python que de manera general, cada uno tienen una clase encargada de definir el comportamiento de cada elemento.

### Conceptos usados:
        - Lists, exception handling, modules

        - Programación Orientada a Objetos: 
                - Classes, Methods, Instances 

        - Programación Paralela: 
                - Multithreading
                - Mutex (mutual exclusion), Multiplex, GIL (Global Interpreter Lock)
                - Rlock -> Función incluida en threading que tiene el comportamiento entre semáforo y torniquete

### Descripción de uso de hilos y sincronización:


De manera general, cada clase ubicada dentro de la carpeta modulos,hace uso de las bibliotecas:
 - threading 
 - time

Esto debido al uso necesario para poder simular cada clase mediante un proceso. Cabe destacar que 
tanto cliente como compania usan:
- random

Para escoger de forma aleatoria un asiento de un avión, entre otras cosas (Más información dentro de cada código).


## Prueba de escritorio:

python3 main.py

        Iniciando coppelViajes
        Iniciando despegar.com
        Iniciando mundomex
        Iniciando bestday
        Iniciando viajesPalacio

        ####################################################
        #Agencia:  coppelViajes  | Compania:  Aereomexico  | Asiento:  0  | Precio:  281.6 
        ####################################################


        -> El manager loco ha subido los precios de  Aereomexico
        despegar.com  no pudo vender a: Aereomexico  el asiento  0
        [Asiento no disponible - Vendido actualmente]

        -> El manager loco ha subido los precios de  Aereomexico
        bestday  no pudo vender a: Aereomexico  el asiento  0
        [Asiento no disponible - Vendido actualmente]

        ####################################################
        #Agencia:  coppelViajes  | Compania:  volaris  | Asiento:  4  | Precio:  294.8 
        ####################################################


        ####################################################
        #Agencia:  despegar.com  | Compania:  volaris  | Asiento:  3  | Precio:  324.28000000000003 
        ####################################################


        ####################################################
        #Agencia:  bestday  | Compania:  Aeromar  | Asiento:  1  | Precio:  305.8 
        ####################################################

        mundomex ha dejado de operar.
        coppelViajes ha dejado de operar.
        despegar.com ha dejado de operar.
        viajesPalacio ha dejado de operar.
        bestday ha dejado de operar.

