# Identificación y Descripción del Problema

Describan la situación que moldearán:

>Trabajando en un restaurante donde los comensales al llegar se someterán a un proceso donde se les otorgará una mesa acorde a la espera en una cola.
>
>Los meseros deben recoger los platos de distintas mesas. Tomando cada uno un área para sí. Cada mesero atenderá a las nuevas mesas conforme a un RR, ya que de este modo ningún cliente debería quedarse sin comer. Los meseros recogen los platos de un área de salida.
>
>Los chefs reciben en el área de salida la orden a hacer (en una cola) y estos la preparan. La preparación será a través de un FiFo.

Resumiendo tareas:

**Cliente:**

1. Espera mesa
2. Toma la mesa
3. Dice lo que quiere comer y que sea rápido
4. Come
5. Pagar

**Mesero:**

1. Toma orden
2. Recibe la orden
3. Sirve la comida
4. Lleva la cuenta
5. Recoge la mesa

**Chef:**

1. Recoge la orden
2. Cocina
3. Deja la comida en la barra de entregas.

¿Dónde pueden verse las consecuencias nocivas de la concurrencia? ¿Qué eventos pueden ocurrir que queramos controlar?:

>Condiciones de carrera al ver el número de mesas disponibles.
>Que una mesa nunca sea servida o tarde mucho tiempo y los comensales se cansen de esperar.
>Que una orden que requiera n chefs tarde mucho en ser preparada.
>Que por prioridad a platos complejos no se hagan las órdenes pequeñas.

¿Hay eventos concurrentes para los cuales el ordenamiento relativo no resulta importante?
>No hay ninguno, todos en cierto modo requieren de conocer el orden en que llegaron los procesos.
>Aunque en algunos no será unicamente acorde a esto que se trabajará.
