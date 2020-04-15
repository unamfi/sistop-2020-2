package modeladoObjetos;

import java.util.concurrent.Semaphore;
import java.util.ArrayList;

public class Prueba {

	public static void main(String[] args) {
		ArrayList<Semaphore> s=new ArrayList<Semaphore>();
		
		for(int i=0;i<50;i++) {
			s.add(new Semaphore(1));
		}
		
		ArrayList<Unidad> unidades=new ArrayList<Unidad>();
		Semaphore entrada=new Semaphore(0);
		Semaphore salida= new Semaphore(0);
		Semaphore salidaUnidad= new Semaphore(0);
		int numAsientos=2;
		int cupoMinimo=2;
		int longitud=5;
		int espacioEntreUnidades=10;
		Fila cola=new Fila();
		Semaphore mutexCola=new Semaphore(1);
		
		unidades.add(new Unidad(numAsientos,cupoMinimo,longitud,espacioEntreUnidades,s));
		unidades.add(new Unidad(numAsientos,cupoMinimo,longitud,espacioEntreUnidades,s));
		
		for(Unidad u:unidades) {
			u.setBarrerasPersonas(entrada, salida,salidaUnidad);
			u.setColaEntrada(cola);
			u.setFactorTiempoDeEspera(3);
			u.setMutexCola(mutexCola);
		}
		
		
		Persona p= new Persona(unidades.get(0));
		Persona p1= new Persona(unidades.get(0));
		Persona p2= new Persona(unidades.get(0));
		
		
		p.start();
		p1.start();
		p2.start();
		
		unidades.get(0).start();
		unidades.get(1).start();
		
		
		
		
		System.out.println("Ya termine hilo principal");
	}

}
