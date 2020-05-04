#include <stdio.h>
int main () {
   //Azul titulo de tabla
   //Cadenas a imprimir en azul 
  printf("\033[0;34m");
  printf("---------------------------------------------------------------------------------------------\n");
  printf("| Nombre Proceso | ID Proceso | Pagina Inicio | Pagina Final | Tamaño | #Paginas | Permisos |\n");
  printf("---------------------------------------------------------------------------------------------\n");
  printf("\033[0m;");
  //Termina de imprimir azul
  return 0;
}