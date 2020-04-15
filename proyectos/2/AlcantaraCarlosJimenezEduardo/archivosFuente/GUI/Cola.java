package GUI;

import java.util.concurrent.Semaphore;
import java.util.logging.Level;
import java.util.logging.Logger;

// @Author: Alcantara Hoyos Carlos Eduardo & Jimenez Gonzalez Jose Eduardo

public class Cola {
    private int personasEnCola;//cantidad de personas en la cola
    private Semaphore barreraCola;//esta es la barrera para que las personas detengan su ejecucion cuando se forman
    
    public Cola(){
        this.personasEnCola=0;
        this.barreraCola= new Semaphore(0);
    }
    
    //funcion para regresar la cantidad de personas en la cola
    public int getPersonasEnCola() {
        return personasEnCola;
    }
    
    //este metodo regresa la barrera de la cola
    public Semaphore getBarreraCola() {
        return barreraCola;
    }
    
    //este metodo es para que una persona se forme en la cola e incrementar la cola
    public void formarCola(){
        this.personasEnCola++;
        try {
            this.barreraCola.acquire();
        } catch (InterruptedException ex) {
            Logger.getLogger(Cola.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    //este metodo es usado por el juego mecanico o por el vagon para indicarle a las personas que pueden continuar ademas de decrementar los encolados
    public void salirCola(){
        this.personasEnCola--;
        this.barreraCola.release();
    }
}