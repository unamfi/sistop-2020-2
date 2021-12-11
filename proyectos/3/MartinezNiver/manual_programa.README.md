# Proyecto 3. Asignación de memoria en un sistema real.

## Parte uno.

La asignación de memoria es una tarea que requieren los sitemas operativos de hoy en día. Hoy en día, casi todas nuestras 
computadoras usan una técnica deasignación conocida como paginación. En esta se asignan o una combinación diferentes bloques
de memoria que pueden estar asociados a un mismo proceso y acciones, de tal forma que mientras este bloque mide alrededor de
los 4KB, se le considera una sola página, pero con más de ese tamaño hay que empezar a hacer cuentas para calcular los bloques
de memoria. Por otra parte, esta información puede consultarse por medio de programas como pmap y en archivos propios del
sistema operativo como /proc/PID/maps o /proc/PID/smaps. A continucación, tenemos un programa que se encarga de realizar 
algunas operaciones a partir de ingresar un PID para poder entregar el mapa de memoria del proceso.


## Archivos definidos:

- memmap.py : Código fuente del programa para mapear la memoria.
- temp.txt : puede llegar a aparecer y se utliza para algunas acciones temporales. Se recomienda borrarlo en caso de que exista antes de iniciar el programa.
## Ejecución:
   
   $python3 <nombre_archivo> ${PID}
   
   - ${PID} : Es el identificador de un proceso en el sistema. Tiene alrededor de 4 a 5 cifras de tipo entero.
              Se puede consultar el PID de un proceso con el comando del sistema pidof.
              
<p align="center"><img src="Captura de pantalla de 2020-05-08 20-31-58.png" width="350"/> </p>
  Ejecución a patir de un PID válido
              
<p align="center"><img src="Captura de pantalla de 2020-05-08 20-32-07.png" width="350"/> </p>
  Ejecución hacia final de las secciones

## Notas:

- Sobre los parámetros. Es importante pasar un PID dejando un espacio como se pasan lo psrámetro en linux. Ya que con esto podemos ver resultado. No ingresar números inválidos.
- Algunas cosas como la memoria anónima y las secciones no identificadas, no están del todo calrificadas en este programa.
- Algunos de los métodos son extraídos o insprados de autores que comparten conocimiento colectivo en plataformas intereactivas, pero no dejan su nombre real. Pondremos algunos links:
      
      https://stackoverflow.com/questions/12611264/how-to-cause-stack-overflow-and-heap-overflow-in-python
      https://ozzmaker.com/add-colour-to-text-in-python/
      https://airbrake.io/blog/python-exception-handling/python-indexerror
      https://stackoverflow.com/questions/40640956/python-with-open-except-filenotfounderror/40641103

## Parte dos

Se realizó a aprtir del análisis del comportamiento de la asignación de memoria, con herrmientas complmentarias con hexdump.
Se encuentra el pdf entre los archivos...
