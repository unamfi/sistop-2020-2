# Develemos algunos mitos

	Planteamiento: 2020.02.13
	Entreta: 2020.02.20

En esta primera unidad comenzamos a estudiar qué es un sistema
operativo y cómo *opera su magia*. Apenas vamos calentando
motores... Pero tengo que evaluarlos 😉

Como vamos apenas iniciando, sin embargo, no hemos cubierto material
técnico suficiente para que les deje un desarrollo de proyecto. Me veo
obligado a evaluar a partir de un *control de lectura*. Les presento a
continuación una serie de artículos, y les pediré que los lean, y
entreguen un *mapa conceptual*. Y, dado que los proyectos los pueden
realizar de forma individual o en equipos de dos personas, aprovecho
para darles una oportunidad: Pueden elegir trabajar de forma
individual con artículos más sencillos, o en equipo, con artículos un
poco más complejos. Claro, también pueden elegir trabajar
individualmente con un artículo complejo (pero serán calificados en
pie de igualdad con los demás).

## Los artículos

Los siguientes artículos son relativamente sencillos; pueden
presentarlos únicamente de forma individual:

1. [Open Source
   Firmware](https://cacm.acm.org/magazines/2019/10/239673-open-source-firmware/fulltext),
   publicado por Jessie Frazelle en la revista *Communications of the
   ACM* a fines de 2019. Sobra contarles acerca de los muchos
   programas que pueden bajar y correr que son software
   libre. Conocemos ya a Linux, y probablemente a algunos otros
   sistemas operativos libres. Pero... ¿Podemos bajar un poco más?
   ¿Qué hay acerca de lo que va antes –y debajo– del sistema
   operativo? ¿Conocen *firmware* libre?
2. [C Is Not a Low-level Language; your computer is not a fast
   PDP-11.](https://queue.acm.org/detail.cfm?id=3212479), publicado
   por David Chisnall en la revista *Queue* de la ACM. Frecuentemente
   nos presentan a C como el principal ejemplo de un lenguaje de bajo
   nivel. Pero... ¿Es cierto eso?

Los siguientes son un poquito más *divertidos*, para trabajar ya sea
en forma individual o en equipos:

1. [Tearing apart
   `printf()`](https://www.maizure.org/projects/printf/index.html)
   (desmenuzando a `printf()`), un artículo en el *blog* de
   *MaiZure*. Explica qué es lo que hace una de nuestras funciones
   favoritas, `printf()`, capa por capa.
2. [Another level of
   indirection](https://www2.dmst.aueb.gr/dds/pubs/inbook/beautiful_code/html/Spi07g.pdf),
   de Diomidis Spinellis. Este artículo es uno de los capítulos del
   libro [Beautiful Code: Leading programmers explain how they
   think](http://shop.oreilly.com/product/9780596510046.do). Vimos ya
   en clase que una de las principales tareas del sistema operativo es
   proveer *abstracciones*. Este texto nos lleva desmontando las
   abstracciones relacionadas con el acceso a datos en sistemas de
   archivos en el sistema operativo FreeBSD, para apreciar la cantidad
   de capas que deben atravesar nuestras llamadas al sistema.
3. [What's new in CPUs since the
   80s?](https://danluu.com/new-cpu-features/), de Dan Luu, responde a
   una pregunta relativamente frecuente entre los alumnos que he
   tenido de la Facultad: En la materia abordamos *fundamentos* de los
   sistemas operativos. Trabajamos sobre *modelos simplificados* de
   los procesadores, en buena medida heredados de cómo eran hace 30
   años. ¿Y qué tanto ha cambiado un CPU desde entonces?

Y siempre se puede... Ir más allá. Quise compartir los siguientes con
ustedes en caso de que alguien sea masoquista o quiera ponerse un reto
fuerte; son textos muy interesantes, muy relacionados con la materia,
pero que entran a niveles de profundización superiores a lo que espero
cubrir.

1. [Evolution of the x86 context switch in
   Linux](https://www.maizure.org/projects/evolution_x86_context_switch_linux/index.html)
   (La evolución del cambio de contexto en x86 en Linux), también del
   *blog* de *MaiZure*. Veremos al cambio de contexto muchas veces a
   lo largo del cursado de nuestra materia. Si quieren tener
   suficiente material para contradecirme y ganar, revisen este texto.
2. [A dive into the world of MS-DOS
   viruses](https://blog.benjojo.co.uk/post/dive-into-the-world-of-dos-viruses),
   transcripción de la ponencia presentada por Ben Cox *Benjojo* en el
   [Chaos Computer Congress
   2018](https://events.ccc.de/congress/2018/wiki/index.php/Main_Page).
   ¿Cómo era escribir un virus en los viejos tiempos? ¿Cómo
   funcionaban los víruses *reales*? (inlcuye animaciones mostrando
   su comportamiento) Este artículo entra bastante en detalles
   técnicos, y cubre buena parte del material que vamos a ver en clase
   (particularmente en el tema de administración de memoria).

## La entrega

Una vez que leas y comprendas (o comprendan) qué tema van a
desarrollar, la entrega es muy sencilla: Preparen un mapa conceptual
presentando los principales elementos del texto, *de la manera que les
resulte más cómodo*. Pueden hacerlo en una hoja de papel (tómenle una
*buena* foto, que se pueda leer), en software genérico o
especializado. Lo importante es que lo entreguen en el directorio
correspondiente al proyecto 1, y bajo la nomenclatura que se
especificó en el [punto 4 de la práctica
1](../../practicas/1/README.md).

Les sugiero, claro está, crear una *rama temática* para desarrollar
este trabajo.
