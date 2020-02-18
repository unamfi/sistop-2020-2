/* ¿Cómo puedo averiguar los límites de un tipo de datos en C? Esta es
   una manera --- No la mejor, no la más eficiente, pero sí una que
   nos muestra claramente el resultado del _comportamiento indefinido_
   en C: Sumar más allá del valor más alto posible para un tipo de datos.

   La variable sobre la que realizamos la prueba es i. Hagan la prueba:

   - ¿Qué pasa si i es short en vez de int?
   - ¿Y qué pasa si es long? ¿Sólo dejarían que avance hasta llegar al
     desbordamiento? ¿Cómo harían más eficiente el encontrar su límite?
   - Este código tal como está no funciona para enteros sin signo (unsigned
     short, unsigned int, unsigned long). Es trivial extenderlo para que
     sí lo haga. ¿Qué modificarían?
*/

#include <stdio.h>

void main() {
  int i = 0;
  while (i >= 0) {
    i++;
    if (i % 1000000 == 0) printf("Millón: %d\t", i);
  }

  printf("\n\nListo. Ahora i vale %d\n", i);
}
