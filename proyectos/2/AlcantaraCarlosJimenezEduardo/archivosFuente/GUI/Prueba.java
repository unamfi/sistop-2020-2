
package GUI;

// @Author: Alcantara Hoyos Carlos Eduardo & Jimenez Gonzalez Jose Eduardo

public class Prueba {

    
    public static void mainRun(secondView view,int maxAmountPeople) {
        String nombre="Superman"; // Nombre ilustrativo
        int cupoMaximo=5;
        int cupoMinimo=4;
        int espacios=26;
        
        JuegoMecanico juego1=new JuegoMecanico(nombre, espacios, cupoMaximo, cupoMinimo,view); // Se crea el juego 
        
        view.setAlert(false); // Se desactiva la alerta, de la iteracion anterior, y tambien para el inicio del programa.
        
        for(int i=0;i<maxAmountPeople;i++){
            
            Persona p=new Persona("#"+i, juego1); // Se crean las personas.
            p.start(); // Se arranca el hilo de las personas.
        }
        juego1.start(); // Se arranca el hilo del juego.
        
        System.out.println("Ya hilo principal");

    }
    
}
