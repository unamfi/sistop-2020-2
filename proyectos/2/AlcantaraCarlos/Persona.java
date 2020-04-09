package modeladoObjetos;
import java.util.concurrent.Semaphore;

public class Persona extends Thread {
	private Semaphore s;
	
	public Persona() {
		
	}
	
	public Persona(Semaphore s) {
		this.s=s;
	}
	
	public void run() {
		try {
			s.acquire();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		System.out.println("Hola hilo:"+this.getId());
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			
			e.printStackTrace();
		}
		
	}
}
