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

### Descripción de uso de hilos y sincronización:


De manera general, cada clase ubicada dentro de la carpeta modulos,hace uso de las bibliotecas:
 - threading 
 - time

Esto debido al uso necesario para poder simular cada clase mediante un proceso. Cabe destacar que 
tanto cliente como compania usan:
- random

Para escoger de forma aleatoria un asiento de un avión, entre otras cosas (Más información dentro de cada código).




