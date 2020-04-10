package modeladoObjetos;

import java.util.concurrent.Semaphore;
import java.util.ArrayList;

public class Prueba {

	public static void main(String[] args) {
		ArrayList<Semaphore> s=new ArrayList<Semaphore>();
		
		for(int i=0;i<100;i++) {
			s.add(new Semaphore(1));
		}
		
		
		Unidad u=new Unidad(5,1,3,3,s);
		Unidad u1=new Unidad(5,1,3,3,s);
		u.start();
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		u1.start();
		
		System.out.println("Ya termine hilo principal");
	}

}
