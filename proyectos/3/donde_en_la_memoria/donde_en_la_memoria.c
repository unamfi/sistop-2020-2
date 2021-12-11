#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

char cadena1[] = "Yo solo sé que no sé nada";
char *cadena_total;
int tamano = 30;

char* construye_final();
int main();

int main() {
  char *cadena2, *cadena3, *cadena4;
  cadena3 = (char *) malloc(tamano * sizeof(char));

  printf("Proceso filósofo, PID %d\n\n", getpid());

  strncpy(cadena2, "Yo sólo sé que nada sé", tamano * sizeof(char));
  strncpy(cadena3, "Pero si alguien sabe menos", tamano * sizeof(char));

  cadena4 = construye_final();

  cadena_total = malloc(tamano * 4 * sizeof(char));
  snprintf(cadena_total, tamano * 4 * sizeof(char), "%s\n%s\n%s\n%s\n",
	   cadena1, cadena2, cadena3, cadena4);

  puts(cadena_total);

  getc(stdin);

  free(cadena3);
  free(cadena4);
  free(cadena_total);
  return 0;
}

char* construye_final() {
  char parte1[20] = "¡siempre ";
  char parte3[20] = " usted!";
  char *parte2 = "puede ser";
  char *completa = malloc(tamano * sizeof(char));

  strncat(completa, parte1, tamano * sizeof(char));
  strncat(completa, parte2, tamano * sizeof(char));
  strncat(completa, parte3, tamano * sizeof(char));

  return completa;
}
