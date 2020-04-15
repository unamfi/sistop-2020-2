# Descripción
La tarea #9 consistió en crear un módulo de pruebas -de simulación- aleatorias de los distintos planificadores además de las implementaciones de cada uno de estos.  

Para la implementación de las posibles conceptualidades -tanto naturales y las artificiales creadas para un mejor manejo del sistema-   se trabajó bajo el paradigma POO en el lenguaje de programación Python3. Aunado a lo anterior, se siguió el estilo de guia de Python PEP8. 

El proyecto consta -en una visión de alto nivel- de procesos, cuyo manejo será responsabilidad de la clase Manipulador. Además de esto, el Manipulador realiza la liberación de procesos -con base en sí el proceso ya puede ser ejecutado-, permite realizar cargas predefinidas o  crear cargas aleatorias de procesos. También Manipulador hará muestra de los efectos de los planificadores tic a tic.  

Para la estructura de los planificadores se utilizó una clase abstracta de nombre Planificador. Dicha clase definirá el comportamiento de los diferentes planificadores mediante la creación del método siguiente_proceso, el cual retorna el próximo proceso a ejecutar junto con el tiempo que este se encontrará en estado ejecución.  

Se definieron los siguientes planificadores y sus consideraciones:
* **FCFS:** Ninguna
* **SPN:** Ninguna
* **FB:** Este planificador al ser instanciado recibe una función que determina quantum del proceso a ejecutar. Trabajando en función de la cola en que se encuentre el proceso por el momento. 
* **RR:** Su constructor recibe el número de tics que dura un pato -quantum-. Es imperativo notar que para nuestra implementación, primero se añade a la cola los nuevos procesos y hasta el final el anterior proceso en haberse ejecutado.
* **SRR:** Su constructor recibe el número de tics que dura un pato -quantum- y los parámetros a y b. Los cuales son respectivamente: Constante de crecimiento de la cola de procesos nuevos y la constante de crecimiento de la cola de aceptados.

# Requerimientos
## Lenguaje
* python 3.6.9
* Modulos scipy, numpy
### Instalación modulos
La instalación de los modulos para linux en python 3 es:  

```
pip3 install scipy
pip3 install numpy
```
### Utilización de modulos externos
Se utilizan para la creación de procesos aleatorios

# Ejecución
## Linux/Mac Os:
```
python3 planificador.py
```
## Windows:
```
python planificador.py
```

**Para mas información consultar el pdf**
