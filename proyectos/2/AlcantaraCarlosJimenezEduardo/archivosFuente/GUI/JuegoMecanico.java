
package GUI;

import java.util.logging.Level;
import java.util.logging.Logger;

// @Author: Alcantara Hoyos Carlos Eduardo & Jimenez Gonzalez Jose Eduardo

public class JuegoMecanico extends Thread {

    private String nombre;
    private int cupoMaximo; //el numero de asientos disponibles, este es el limite por vagon
    private int cupoMinimo; //el numero de personas deben ser mayor al cupo minimo
    private Cola cola; //la cola de entrada al juego
    private Cola colaSalida;
    private Espacios espacios;
    private Vagon vagonEsperando;
    private boolean juegoOperando;
    private secondView view;

    JuegoMecanico(String nombre, int espacios, int cupoMaximo, int cupoMinimo, secondView view) {
        this.nombre = nombre;
        this.cola = new Cola();
        this.espacios = new Espacios(espacios);
        this.juegoOperando = true;
        this.cupoMaximo = cupoMaximo;
        this.cupoMinimo = cupoMinimo;
        this.colaSalida = new Cola();
        this.vagonEsperando = new Vagon(this.espacios, 0, this.colaSalida, view);
        this.view = view;
    }

    public String getNombre() {
        return nombre;
    }

    public Cola getColaSalida() {
        return colaSalida;
    }

    public Cola getCola() {
        return cola;
    }

    public Vagon getVagonEsperando() {
        return vagonEsperando;
    }

    public boolean isJuegoOperando() {
        return juegoOperando;
    }
     //metodo para desencolar personas y obtener cuantas personas fueron.
    private int pasarPersonasAlVagon() {

        int segundosEspera = 0;
        //obtenemos la cantidad de personas formadas
        int personasFormadas = this.cola.getPersonasEnCola();
                //si las personas que hay en la cola son menos que el minimo, se va a dormir un momento , para volver a checar
        while (personasFormadas < this.cupoMinimo) {
            print("Esperaremos mas personas, 2 segundos.");
            esperarMasPersonas(2);
            segundosEspera = segundosEspera + 2; //sumamos a los segundos de espera que llevamos
            //si llevamos muchos segundos esperando las personas se van a ir y vamos a cerrar el juego
            if (segundosEspera > 10) {
                //si hay mas de 0 personas formadas, se van a ir del juego
                if (personasFormadas > 0) {
                    print("Las personas se cansaron de esperar en la cola y se van.");
                    view.setAlert(true);
                } else {
                    print("No hay personas");
                }
                //cambiamos el atributo de si esta abierto a falso
                this.juegoOperando = false;
                //desencolamos a las personas en la cola, para que se vayan
                for (int i = 0; i < personasFormadas; i++) {
                    cola.salirCola(); 
                    //para conectar la cantidad con la GUI
                    int temp = view.getAmout();
                    temp = temp - 1;
                    view.setAmout(temp);
                }
                //regresamos que la cantidad de personas que ingresaran al vagon es 0
                return 0;
            }
            personasFormadas = this.cola.getPersonasEnCola();
        }

        int pasarPersonas = 0;
        //si hay mas personas formadas que el cupo maximo, se usa el cupo maximo, en caso contrario, se usa el numero de personas formadas
        if (personasFormadas > this.cupoMaximo) {
            pasarPersonas = this.cupoMaximo;
        } else {
            pasarPersonas = personasFormadas;
        }
        //dejamos que las personas que determinamos pasen al juego
        System.out.println("Van personas " + pasarPersonas);
        for (int i = 0; i < pasarPersonas; i++) {
            cola.salirCola(); 
            //para conectar con la GUI
            int temp = view.getAmout();
            temp = temp - 1;
            view.setAmout(temp);
            
        }

        //regresamos las personas que dejamos pasar

        return pasarPersonas;
    }

     //metodo para esperar en segundos
    private void esperarMasPersonas(int segundos) {
        try {
            Thread.sleep(segundos * 1000);
        } catch (InterruptedException ex) {
            Logger.getLogger(Vagon.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    @Override
    public void run() { //el primer vagon esta en 0 personas, le vamos a pasar personas
        this.vagonEsperando.setPersonasAbordo(pasarPersonasAlVagon());
        while (true) { 
            //checamos que las personas a bordo sean mayores a 0, si se cumple vamos a arrancarlo y crear otro., en caso contrario se va a cerrar el juego
            if (this.vagonEsperando.getPersonasAbordo() > 0) {
                try {
                    this.vagonEsperando.start();
                    Thread.sleep(2000);
                     //determinamos cuantas personas pasaron al vagon
                    int subirPersonas = pasarPersonasAlVagon();
                    this.vagonEsperando = new Vagon(espacios, subirPersonas, this.colaSalida, view);

                } catch (InterruptedException ex) {
                    Logger.getLogger(JuegoMecanico.class.getName()).log(Level.SEVERE, null, ex);
                }
            } else {
                print("Vamos a cerrar");
                break;
            }
        }
    }

    public void print(String s) {
        System.out.println(".....Juego " + nombre + ": " + s);
    }
}
