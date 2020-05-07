#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <limits.h>
#include <unistd.h>
#include <sys/types.h>
#include <errno.h>

void terminar(char *error, ...)
{
    va_list a;
    va_start(a, error);
    vfprintf(stderr, error, a);
    va_end(a);
    exit(1);
}//Funcion para cerrar el archivo y terminar el programa en caso de no encontrar el proceso

void nombre_proceso(pid_t pid)
{
    char nombre[PATH_MAX];  //PATH_MAX es el arreglo que almacena el mapeo
    int cont;                  //distintos procesos con distintos tamaños hacen necesario el uso de PATH_MAX que equivale a 260 caracteres
    int i = 0;  
    FILE *archivo;

    sprintf(nombre, "/proc/%ld/cmdline", (long) pid);
    archivo = fopen(nombre, "r");
    if(!archivo){

         terminar("%s: %s\n", nombre, strerror(errno));
         //Error al leer el nombre del proceso
         }

    while((cont = getc(archivo)) != EOF && cont != 0){
	    nombre[i++] = cont;
        nombre[i] = '\0';
    }
    printf("%s(%ld)\n", nombre, (long)pid);

    fclose(archivo);
}

void mostrar_mapa(pid_t pid)
{
    char nombre_archivo[PATH_MAX];
    unsigned long writable = 0; 
    unsigned long total = 0; 
    unsigned long compartido = 0;
    FILE *archivo;

    sprintf(nombre_archivo, "/proc/%ld/maps", (long)pid);  
    archivo = fopen(nombre_archivo, "r");

    if(!archivo){
	terminar("%s: %s\n", nombre_archivo, strerror(errno));
    }

    while(!feof(archivo)) { //Mientras no se llegue al final del archivo
	char buf[PATH_MAX+100]; //Buffer que almacena los datos del PID con 260+100 caracteres
    char perm[5];           //Arreglo con el String de los permisos
    char dispositivos[6];   //Arreglo con el formato xx:xx del dispositivo
    char mapeo[PATH_MAX];   //Arreglo de tamaño de acuerdo al String del mapeo
	unsigned long inicio;   //Direccion de inicio en memoria de la pagina
    unsigned long final;    //Final de la pagina
    unsigned long tamano;   //Tamaño de la pagina en Bytes
    unsigned long inode;    //Nodo
    unsigned long foo;      
	int n;                  //Se irán añadiendo los outpus en este int para 
                            //poder tener un formato como "tabla"

	if(fgets(buf, sizeof(buf), archivo) == 0){
	    break;
    }     
	mapeo[0] = '\0';
	sscanf(buf, "%lx-%lx %4s %lx %5s %ld %s", &inicio, &final, perm,&foo, dispositivos, &inode, mapeo);
	tamano = final - inicio;
	total += tamano;
	
	if(perm[3] == 'p') {
	    if(perm[1] == 'w')
		writable += tamano;
	}else if(perm[3] == 's'){
	    compartido += tamano;
	}else{
	    terminar("No se pudo leer la cadena de permisos: '%s'\n", perm);
    }
    n = printf("\033[0m 	\033[0;34m%08lx \033[0m - \033[0;35m %08lx	\033[0m| \033[0;31m%ld ", inicio,final,((final-inicio)/1024)/4);
    //Print para las paginas
    int pag=((final-inicio)/1024)/4;
    int cont2=0;
    while((pag/10)>0){   //While para contar la cantidad de digitos que tiene "paginas"
        pag=pag/10;      //y ajustar su impresion en pantalla
        cont2++;
    }    
    printf("\033[0m");
    if(cont2==1){
        n+=printf("         |");
    }else if(cont2==2){
        n+=printf("        |");
    }else if(cont2==3){
        n+=printf("       |");
    }else if(cont2==4){
        n+=printf("      |");
    }else if(cont2==5){
        n+=printf("     |");
    }else if(cont2==0){
        n+=printf("          |");
    }else if(cont2==6){
        n+=printf("    |");
     }   
    //Termina print paginas
    //Print de permisos
    n+=printf("     \033[0;33m %s",perm);
    printf("\033[0m       |");
    //Print de los tamaños
    int num=(final - inicio)/1024;
    int cont=0;
    while((num/10)>0)
    {
        num=num/10;
        cont++;
    }
    printf("\033[0m");
    //Printf de los dispositivos 
    n+=printf("\033[0;32m (%ld KB)",(final - inicio)/1024);
    printf("\033[0m");

    if (cont==1){
        n += printf("      |    %5s       |  ", dispositivos);
    }else if(cont==2){
        n += printf("     |    %5s       |  ", dispositivos);
    }else if(cont==3){
        n += printf("    |    %5s       |  ", dispositivos);
    }else if(cont==4){
        n += printf("   |    %5s       |  ", dispositivos);
    }else if(cont==5){
        n += printf("  |    %5s       |  ", dispositivos);
    }else if(cont==6){
        n += printf(" |    %5ss       |  ", dispositivos);
    }else if(cont==0){
        n+=printf("       |                |  ");
    }else{
        n+=printf("       |                |  ");
    }
    //Print del mapeo
    printf("\033[1;36m");
    n+=printf("%s\n",mapeo);
	printf("\033[0m;");

    }
    printf("Fueron mapeados:   %ld KB modificables | privados: %ld KB | compartidos: %ld KB\n",
	    total/1024, writable/1024, compartido/1024);
              printf("\033[0m;");

    fclose(archivo);
}

pid_t obtenerID(char *apuntador)
{
    while(!isdigit(*apuntador) && *apuntador)
	apuntador++;
    return strtol(apuntador, 0, 0);//Convierte cadena del ID a entero 
}

int main(int argc, char **argv)
{
    int i;

    if(argc < 2)
	terminar("Proceso: %s [pid|/proc/pid] ...\n", argv[0]);
    for(i=1; argv[i]; i++) {
	char *ppid;    //Parent Process ID = ID del proceso padre
	pid_t pid;     //Process ID 
                   //Struct tipo pid_t obtenido de la biblioteca Sys/types.h y unistd.h

	ppid = argv[i];
	pid = obtenerID(ppid);
 
  printf("\t Proceso: ");
  nombre_proceso(pid);
  printf("-------------------------------------------------------------------------------------------------------------------------------------------------------------\n");
  printf("\033[0m \033[0;34m\tPagina Inicio \033[0m- \033[0;35mPagina Fin\t\033[0m|\033[0;31m  Páginas    \033[0m|  \033[0;33m   Permisos    \033[0m|\033[0;32m    Tamaño    \033[0m|  Dispositivos  |\033[0;36m       Mapeo\n");
  printf("\033[0m-------------------------------------------------------------------------------------------------------------------------------------------------------------\n");
  printf("\033[0m");
  mostrar_mapa(pid);
    }
    return 0;
}
