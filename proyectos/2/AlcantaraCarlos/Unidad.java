package modeladoObjetos;

import java.util.ArrayList;
import java.util.concurrent.Semaphore;

public class Unidad extends Thread{
	private int numAsientos;
	private int cupoMinimo;			//numero de asientos que se deben cubrir para comenzar a avanzar
	private ArrayList<Semaphore> mutexEspacial; //va de acuerdo con los espacios del juego
	private int longitud;			//la longitud del vagon- unidad
	private int espacioEntreUnidades;//espacio seguro que debe haber entre unidades
	
	
	public Unidad(int numAsientos,int cupoMinimo,int longitud,
			int espacioEntreUnidades,ArrayList<Semaphore> mutexEspacial) {
		
		this.numAsientos=numAsientos;
		this.cupoMinimo=cupoMinimo;
		this.longitud=longitud;
		this.mutexEspacial=mutexEspacial;
		this.espacioEntreUnidades=espacioEntreUnidades;
	}
	
	public int getNumAsientos(){
		return this.numAsientos;
	}
	
	public int getCupoMinimo() {
		return this.cupoMinimo;
	}
	
	public int getLongitud() {
		return longitud;
	}
	
	private void ocuparLugar(int desdeLugar,int hastaLugar) {
		for (int i=desdeLugar;i<=hastaLugar;i++) {
			ocuparLugar(i);
		}
	}
	
	private void ocuparLugar(int indiceDelLugar) {
		
		try {
			Thread.sleep(100);
			mutexEspacial.get(indiceDelLugar).acquire();
			print(" Vamos en "+indiceDelLugar);
			
		} catch (InterruptedException e) {
			print("Se produjo un error en Mutex, no se pudo adquirir... "
					+ "Objeto Unidad"+this.getId());
		}
	}
	
	private void desocuparLugar(int indiceDelLugar) {
		
		if(indiceDelLugar>=this.mutexEspacial.size()) {
			print("Este mutex no existe");
		}

		mutexEspacial.get(indiceDelLugar).release();
		
		print("Libere espacio: "+indiceDelLugar);

	}
	
	public void run() {
		print("Arrancamos");
		ocuparLugar(0,longitud-1);
		
		for (int i=this.longitud;i<(this.espacioEntreUnidades+this.longitud);i++) {
			ocuparLugar(i);
		}
		
		//mientras vamos avanzando, liberamos los espacios de seguridad
		int i=0;
		for (i=this.espacioEntreUnidades+this.longitud;i<this.mutexEspacial.size();i++) {
			ocuparLugar(i);
			desocuparLugar(i-(this.espacioEntreUnidades+this.longitud));
		}
		for(i=this.mutexEspacial.size()-(this.espacioEntreUnidades+this.longitud);i<this.mutexEspacial.size();i++) {
			desocuparLugar(i);
		}
		
	}
	
	private void print(String s){
		System.out.println("Unidad "+this.getId()+":\t"+s);
	}
}
