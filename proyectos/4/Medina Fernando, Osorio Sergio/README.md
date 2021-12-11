# Proyecto 3: (Micro) Sistema de Archivos
* Osorio Robles Sergio de Jesús

* Medina Molina Fernando Arturo
## Requerimientos
- Python 3.7.2
- Sistema de archivos fiunamfs.img
## Descripción de la solución
La implementación de nuestra solución se realizó utilizando Python 3.7.2 con el package `tkinter` para crear la interfaz
gráfica. Se crearon dos archivos: `FIFS.py` y `FiUnamFs.py`; `FIFS.py` contiene los métodos necesarios para realizar las 
acciones de enlistar archivos, copiar hacía el sistema, copiar desde el sistema y la definición del súperbloque. 

El método para obtener los archivos contenidos dentro del `fiunamfs.img` fue utilizando la función `mmap`, realizando 
el mapeo del sistema podemos obtener el primer cluster que contiene los detalles de los archivos (nombre, fecha de creación, etc).

Utilizando el paradigma orientado a objetos definimos 3 objetos, el objeto FIFS (Facultad de Ingeniería File System) que tiene 
como atributos la información de los archivos, el objeto SuperBloque que contiene la información del cluster 1 con los detalles 
de los archivos y el objeto DIRENTRY que contiene los inodos de cada archivo en el sistema. 

En el archivo `FiUnamFs.py` se maneja la creación de la interfaz y se ajusta la salida en el listBox para que se vea con forma de tabla. Esta es nuestra clase principal por lo que debe ejecutarse este archivo para probar el sistema de archivos. 

En la interfaz se pueden realizar las operaciones de eliminar archivos del sistema, añadir archivos al sistema, hacer una copia local de los archivos, desfragmentar la unidad. 

Para poder ejecutar el sistema de archivos debe ejecutar el archivo `FiUnamFs.py` inmediatamente después el programa le pedirá la ruta del archivo.img que contiene el sistema de archivos para este proyecto. 

![alt text](https://github.com/fernando170/sistop-2020-2/blob/master/proyectos/4/Medina%20Fernando%2C%20Osorio%20Sergio/inputRuta.png)

Una vez proporcionada se desplegará esta ventana


![alt text](https://github.com/fernando170/sistop-2020-2/blob/master/proyectos/4/Medina%20Fernando%2C%20Osorio%20Sergio/captura.png)

### Nota
Para la implementación de esta solución nos basamos en ejemplos de la implementación de Fuse obtenidos de esta liga: 
http://thepythoncorner.com/dev/writing-a-fuse-filesystem-in-python/

También de ejemplos de implementaciones anteriores hechas por Ricardo Rosales en el siguiente repositorio:
https://github.com/unamfi/sistop-2020-1/blob/master/proyectos/3/RosalesRicardo/main.py




