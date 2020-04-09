package modeladoObjetos;

import java.util.concurrent.Semaphore;

public class Prueba {

	public static void main(String[] args) {
		//Probaremos las clases Semaphore, Thread, etc.
		
		Semaphore s= new Semaphore(1);
		Persona p =new Persona(s);
		Persona p1= new Persona(s);
		p.run();
		p1.run();
		
	}

}
