package modeladoObjetos;

import java.util.ArrayList;
import java.util.concurrent.Semaphore;


public class JuegoMecanico extends Thread{
	private String nombre;	//nombre del juego mecanico
	private int longitudTrayectoria;//longitud de la trayectoria que deben recorrer los vagones
	private ArrayList<Unidad> unidadesFuncionando;//las unidades funcionando
	private ArrayList<Semaphore> mutexTrayectoria;//conjunto de semaforos para que las unidades no choquen
	
	private ArrayList<Semaphore> barrerasEntrada;//barreras respetando la cantidad minima por unidad y que no sean mas de la cantidad e asientos
	
	
	
	public JuegoMecanico(String nombre, int unidadesFuncionando, int numAsientos,
			int cupoMinimo,int longitudUnidades,int longitudTrayectoria, int longitudEspacioSeguro){
		this.nombre=nombre;
		this.longitudTrayectoria=longitudTrayectoria;
		this.unidadesFuncionando=new ArrayList<Unidad>();
		this.mutexTrayectoria=new ArrayList<Semaphore>();
		
		//generamos los mutex de la trayectoria
		for(int i=0;i<longitudTrayectoria;i++) {
			this.mutexTrayectoria.add(new Semaphore(1));
		}
		
		//generamos las unidades
		for(int i=0;i<unidadesFuncionando;i++) {
			this.unidadesFuncionando.add(new Unidad(numAsientos,cupoMinimo,longitudUnidades,
					longitudEspacioSeguro,mutexTrayectoria));
		}
		
	}
	
	public String getNombre() {
		return this.nombre;
	}
	
	public int getUnidadesFuncionando() {
		return this.unidadesFuncionando.size();
	}
	

	@Override
	public void run() {
		while (true) {
			
		}
		
	}
	
}
