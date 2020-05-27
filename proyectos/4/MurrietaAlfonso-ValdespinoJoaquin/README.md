# MICRO SISTEMA DE ARCHIVOS - PROYECTO 4

## Integrantes:

- Alfonso Murrieta Villegas
- Valdespino Mendieta Joaquín

## Aspectos generales del proyecto 

    1. Listado los contenidos del directorio
    2. Copiado de uno de los archivos de dentro del FiUnamFS hacia el sistema propio
    3. Copiado de un archivo de la computadora propia hacia FiUnamFS
    4. Eliminado de un archivo de FiUnamFS
    5. Programa para desfragmentar a FiUnamFS  
        - La defragmentación debe hacerse dentro del sistema de archivos 
          (no creando un sistema de archivos nuevo y copiando hacia éste).

## Especificaciones generales del Proyecto



.
├── proyecto4
│   ├── fiunamfs.img
│   ├── FSFI.ui
│   ├── Myapp.py
│   └── obb
│       ├── entry_fs.py
│       └── sblock.py
└── README.md

2 directories, 6 files
 
## Especificaciones generales del Proyecto

Lenguaje de programación: 
- Python en su versión 3.X

Bibliotecas, módulos y dependencias:
- qt 5 
- os

## Compilación y Ejecución

Para poder compilar el proyecto es necesario tener cualquier versión de python 3, 
y los respectivos módulos necesarios, como son el caso de os  y Qt5.

  - Para instalar/descargar qt5 se puede utilizar el siguiente comando en linux: 
    ``` apt install qttools5-dev-tools``` 
    también puede usarse 
        ``` apt install python3-pyqt5 ```

Ejecución del programa:

- Entra a la carpeta 'proyecto4' y ejecutar en terminal la siguiente instrucción (Compilar MyApp.py que 
  es el main de todo el código):
    ``` python3 MyApp.py ``` 


## NOTAS

Para mayor comprensión del código, se puede checar los comentarios que se han realizado en
las clases realizadas 

