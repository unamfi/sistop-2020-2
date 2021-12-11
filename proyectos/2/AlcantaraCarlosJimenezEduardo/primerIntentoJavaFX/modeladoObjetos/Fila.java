package modeladoObjetos;

public class Fila{
	private int cola;
	
	public Fila() {
		cola=0;
	}
	
	public synchronized void formarCola() {
		cola++;
	}
	
	public synchronized void salirCola() {
		cola--;
	}
	
	public synchronized int getCola() {
		return cola;
	}
}
