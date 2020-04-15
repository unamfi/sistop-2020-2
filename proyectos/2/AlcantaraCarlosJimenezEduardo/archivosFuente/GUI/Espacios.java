
package GUI;

import java.util.ArrayList;
import java.util.concurrent.Semaphore;


// @Author: Alcantara Hoyos Carlos Eduardo & Jimenez Gonzalez Jose Eduardo

public class Espacios {
    private ArrayList<Semaphore> mutexEspacios;//mutex de los espacios
    private ArrayList<Boolean> espacioOcupado;//lista de lugares ocupados

    public Espacios(int espacios) {
        this.mutexEspacios = new ArrayList<>();
        this.espacioOcupado = new ArrayList<>();
        
        for(int i=0;i<espacios;i++){
            this.mutexEspacios.add(new Semaphore(1));
            this.espacioOcupado.add(false);
        }
        
    }
    //metodo para obtener el nuemero de espacios en la trayectoria
    public int getEspacios(){
        
        return this.mutexEspacios.size();
    }
    
    //ocupamos el espacio del indice que le indicamos
    public void ocuparEspacio(int numeroEspacio){
        try {
            Thread.sleep(500);//simulamos que el vagon se tarda este tiempo en ocupar un espacio
            this.mutexEspacios.get(numeroEspacio).acquire();
            this.espacioOcupado.set(numeroEspacio,true);
        } catch (InterruptedException ex) {
            System.out.println("Problema en Clase Espacios");
        }
    }
    public void desocuparEspacio(int numeroEspacio){
        this.mutexEspacios.get(numeroEspacio).release();
        this.espacioOcupado.set(numeroEspacio,false);
    }
}
