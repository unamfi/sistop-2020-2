package modeladoObjetos;
import java.util.concurrent.Semaphore;

public class Persona extends Thread {
	private String numero;
	private boolean tienePase;
	private Unidad u;
	
	public Persona(Unidad u) {
		this.u=u;
	}
	
	
	public void run() {
		print("Voy a entrar al juego");
		entrarJuego();
		if(this.u.getPudeArrancar()==true) {
			print("Lei pude arrancar= "+this.u.getPudeArrancar());
			print("Estoy dentro del juego");
			salirJuego();
		}
		
		print("Termine mi visita");
	}
	
	private void entrarJuego() {
		try {
			this.u.getColaEntrada().formarCola();
			print("Personas en cola: "+u.getColaEntrada().getCola());
			this.u.getEntradaPersonas().acquire();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	private void salirJuego() {
		try {
			this.u.getSalidaPersonas().acquire();
			Thread.sleep(5000);//tiempo que paso para bajar
			this.u.getSalidaUnidad().release();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	private void print(String s) {
		System.out.println("++Persona "+this.getId()+": "+s);
	}
}
