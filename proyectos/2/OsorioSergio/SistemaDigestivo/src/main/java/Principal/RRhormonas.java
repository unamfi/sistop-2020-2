package Principal;

//Clase para simular el efecto de las hormonas en el sistema digestivo

import java.util.ArrayList;
import java.util.List;



//La idea es que cada hormona tiene disntinto tiempo de efecto sobre el 
//sistema
//Se utiliza el algoritmo RoundRobin para simular el tiempo
//que cada hormona esta en el sistema 
public class RRhormonas {

    //Metodo para encontrar el tiempo de espera de los procesos
    static void hallarEspera(int procesos[], int n, int tiempoProc[], int tiempoEspera[], int quantum,List<Integer> ListaEjecucion) {
        int tiempoProcRestante[] = new int[n];
        for (int i = 0; i < n; i++) {
            tiempoProcRestante[i] = tiempoProc[i];
                            

        }

        int t = 0; // tiempo transcurrido
        //Ejecutar los procesos en RoundRobin
        //Hormonas haciendo efecto sobre el individuo
        while (true) {
            boolean done = true;
            //Iterar entre todos los procesos
            for (int i = 0; i < n; i++) {
                ListaEjecucion.add(i);
                if (tiempoProcRestante[i] > 0) {
                    done = false; // Aún hay un proceso pendiente

                    if (tiempoProcRestante[i] > quantum) {
                        t += quantum;

                        tiempoProcRestante[i] -= quantum;
                    } else {
                        t = t + tiempoProcRestante[i];

                        tiempoEspera[i] = t - tiempoProc[i];

                        tiempoProcRestante[i] = 0;
                    }
                }
            }

            //Cuando todos los procesos hayan terminado
            if (done == true) {
                break;
            }
        }
    }

    //Método para calcular el tiempo de respuesta
    //El tiempo que ha tomado una hormona para cumplir su funcion
    static void tiempoRespuesta(int procesos[], int n, int tiempoProc[], int tiempoEspera[], int tiempoDeRespuesta[]) {
        
        for (int i = 0; i < n; i++) {
            tiempoDeRespuesta[i] = tiempoProc[i] + tiempoEspera[i];
        }
    }

    static void promediosTiempo(int procesos[], int n, int tiempoProc[], int quantum,List<Integer> ListaEjecucion) {
        int tiempoEspera[] = new int[n], tiempoDeRespuesta[] = new int[n];
        int total_tiempoEspera = 0, total_tat = 0;

        //Hallar el tiempo de espera de cada proceso
        hallarEspera(procesos, n, tiempoProc, tiempoEspera, quantum,ListaEjecucion);

        //Funcion para encontrar el tiempo de respuesta 
        tiempoRespuesta(procesos, n, tiempoProc, tiempoEspera, tiempoDeRespuesta);

        //Imprimir procesos
        System.out.println("Proceso " + "Tiempo Ejecucion " + " Tiempo Espera " + " Tiempo de Respuesta");

        for (int i = 0; i < n; i++) {
            total_tiempoEspera = total_tiempoEspera + tiempoEspera[i];
            total_tat = total_tat + tiempoDeRespuesta[i];
            System.out.println(" " + (i + 1) + "\t\t" + tiempoProc[i] + "\t\t "+ tiempoEspera[i] + "\t\t " + tiempoDeRespuesta[i]);
        }

        System.out.println("Promedio tiempo de espera = "+ (float) total_tiempoEspera / (float) n);
        System.out.println("Promedio tiempo de Respuesta = "+ (float) total_tat / (float) n);
    }

    public List<Integer> RoundRobin() {
        List<Integer> ListaEjecucion = new ArrayList<>();
        //ID de los procesos
        //ID de las hormonas
        int procesos[] = {1, 2, 3};
        int n = procesos.length;

        //Tiempo de ejecución
        //Tiempo en el sistema digestivo
        //de cada hormona
        int tiempo_procesamiento[] = {10, 5, 8};
        //Valor de Quantum
        int quantum = 2;
        promediosTiempo(procesos, n, tiempo_procesamiento, quantum,ListaEjecucion);
        System.out.println("Orden de Ejecución");
        System.out.println(ListaEjecucion);
        return ListaEjecucion;
    }
    
}
