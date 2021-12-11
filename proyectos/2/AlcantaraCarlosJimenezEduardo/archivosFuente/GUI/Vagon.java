
package GUI;

import java.util.logging.Level;
import java.util.logging.Logger;

// @Author: Alcantara Hoyos Carlos Eduardo & Jimenez Gonzalez Jose Eduardo

public class Vagon extends Thread {

private int personasAbordo;
    private Espacios espacios;
    private Cola colaParaSalir;
    private secondView view;

    public Vagon(Espacios espacios, int personasAbordo, Cola colaParaSalir, secondView view) {
        this.espacios = espacios;
        this.personasAbordo = personasAbordo;
        this.colaParaSalir = colaParaSalir;
        this.view = view;
    }

    public void setPersonasAbordo(int personasAbordo) {
        this.personasAbordo = personasAbordo;
    }

    public int getPersonasAbordo() {
        return personasAbordo;
    }

    public Cola getColaParaSalir() {
        return this.colaParaSalir;
    }

    @Override
    public void run() {
        //obtenemos la cantidad de zonas que tiene la trayectoria
        int espacios = this.espacios.getEspacios();
        print("Arrancamos");
        //ocupamos el espacio 0 
        this.espacios.ocuparEspacio(0);
        for (int i = 1; i < espacios; i++) {
            //ocupamos un espacio mas
            print("Voy en " + i);
            this.espacios.ocuparEspacio(i);
            //desocupamos el espacio anterior
            print("Libere " + (i - 1));
            this.espacios.desocuparEspacio(i - 1);
            //conexion con la GUI
            view.setCar(i+1, i);
        }

        //Vamos dandole paso a las personas para que se vayan
        for (int i = 0; i < this.personasAbordo; i++) {

            this.colaParaSalir.salirCola();
        }
        //desocupamos el ultimo espacio
        this.espacios.desocuparEspacio(espacios - 1);
        //Terminamos el recorrido
        terminarRecorrido();
    }

    private void terminarRecorrido() {
        try {
            //se duerme para simular que ya esta saliendo de la trayectoria
            Thread.sleep(500);
        } catch (InterruptedException ex) {
            Logger.getLogger(Vagon.class.getName()).log(Level.SEVERE, null, ex);
        }
        print("He terminado el recorrido");
    }

    public void print(String s) {
        System.out.println("----Vagon " + this.getId() + ": " + s);
    }
}
