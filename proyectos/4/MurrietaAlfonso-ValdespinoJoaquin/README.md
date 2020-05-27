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

A continuación el árbol del proyecto donde se pueden observar los 3 archivos de python que cotienen toda la lógica del proyecto (Mayor descripción en la parte inferior), la imagen .img y un archivo .ui que es el mapeo de la interfaz gráfica <br>

.<br>
├── proyecto4 <br>
│   ├── fiunamfs.img<br>
│   ├── FSFI.ui<br>
│   ├── Myapp.py<br>
│   └── obb<br>
│       ├── entry_fs.py<br>
│       └── sblock.py<br>
└── README.md


Los 2 archivos que contienen toda la lógica de nuestro micro sistema de archivos están en la carpeta o modulo obb, por otro lado, MyApp.py solamente se encarga de hacer la llamada a la interfaz gráfica de QT (Archivo .ui) además de instanciar las clases principales del proyecto ubicadas en el modulo obb.

 
## Especificaciones generales del Proyecto

Lenguaje de programación: 
- Python en su versión 3.X

Bibliotecas, módulos y dependencias:
- qt 5 
- os
- mmap
- math
- time 

## Compilación y Ejecución

Para poder compilar el proyecto es necesario tener cualquier versión de python 3, 
y los respectivos módulos necesarios.

### Instalación de dependencias 
Para instalar/descargar qt5 se puede utilizar el siguiente comando en linux: 
    ``` apt install qttools5-dev-tools``` 
    también puede usarse 
        ``` apt install python3-pyqt5 ```

### Ejecución del programa:

Entra a la carpeta 'proyecto4' y ejecutar en terminal la siguiente instrucción (Compilar MyApp.py que 
  es el main de todo el código):
    ``` python3 MyApp.py ``` 

## Manejo de la aplicación y descripción de cada método asociado a la GUI

- Añadir
  En el editText (En el box blanco) se necesita colocar el nombre del archivo que se va a agregar, después dar click para añadir a fiunamfs.

- Copiar a 
  Se necesitas seleccionar el elemento a copiar en la lista desplegada dentro de la GUI, además en el editText colocar la ruta absoluta del destino donde se quiere copiar el archivo.
  Posteriormente, teniendo estos elementos se pulsa el botón "copiar a"  para así copiar un elemento de fiunamfs a la PC del usuario.

- eliminar
  Se necesita seleccionar el archivo que se desee eliminar dentro de fiunam
  
- iniciar 
  sirve para mostrar todo los datos dentro de nuestra imagen 

- desfragmentar 
  Sólo se necesita dar click para hacer la desfragmentación


## NOTAS

  1. Para mayor comprensión del código, se puede checar los comentarios que se han realizado en las clases realizadas 
  
  2. Los archivos .ui son un mapeo mediante xml para la biblioteca gráfica qt, realmente no es un archivo que contenga código en python, sino que es un recurso que auxilia a la biblioteca, para más información link https://www.qt.io/product/ui-design-tools

  3. Se dejaron algunos archivos dentro de la imagen fiunamfs.img sobre todo para poder "jugar " un poco con archivos propios 

  4. No modificar el directorio ni la ubicación de la imagen que se usa para el proyecto :( 
