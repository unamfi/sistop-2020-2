
package GUI;

// @Author: Alcantara Hoyos Carlos Eduardo & Jimenez Gonzalez Jose Eduardo

public class Persona extends Thread{
    private String nombre;
    private JuegoMecanico juego;
    private Cola colaEntrarAlJuego;
    private Cola colaSalirDelVagon;
    
    public Persona(String nombre,JuegoMecanico juego){
        this.nombre=nombre;
        this.juego=juego;
        this.colaEntrarAlJuego=this.juego.getCola();
    }
    
    public void setJuego(JuegoMecanico juego){
        this.juego=juego;
        this.colaEntrarAlJuego=this.juego.getCola();
    }
    
    @Override
    public void run(){
        print("Voy a pasar al juego "+this.juego.getNombre());
        this.colaEntrarAlJuego.formarCola(); //la persona se va a formar en la cola
         //decidimos que si el juego no esta operando, se va a ir. Si esta funcionando, se forma en la cola de salida del vagon
        if(this.juego.isJuegoOperando()==false){
            print("Me voy");
        }else{
            this.colaSalirDelVagon=this.juego.getColaSalida();
            print("Wohooooo");
            this.colaSalirDelVagon.formarCola();
        }
        //termina la visita al juego.
        print("Termine mi visita");
    }
    
    private void print(String s){
        System.out.println("++++Persona "+nombre+": "+s);
    }
}
