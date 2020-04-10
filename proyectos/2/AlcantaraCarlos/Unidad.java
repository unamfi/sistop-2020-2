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
		int trayectoriaTotal=this.mutexEspacial.size();//la cantidad de mutex, son el total de espacios para recorrer todo el juego mecanico
		int espaciosNecesariosNetos=this.longitud+this.espacioEntreUnidades;// Nos dice los espacios que debe ocupar una unidad contando los de seguridad
		
		print("Arrancamos");
		ocuparLugar(0,espaciosNecesariosNetos);//con esto ya contemplamos que la unidad ya avanzó y ya dejó marcados los espacios de seguridad en la parte de atras
		
		//mientras vamos avanzando, liberamos los espacios de seguridad, avanza 1, liberamos 1 para que otros hilos lo comiencen a ocupar
		int i=0;//contador que nos dice en que punto de la trayectoria vamos
		for (i=espaciosNecesariosNetos;i<trayectoriaTotal;i++) {
			ocuparLugar(i);
			desocuparLugar(i-espaciosNecesariosNetos);//
		}
		
		//aun tenemos lugares que no desocupamos, estos ultimos son los correspondientes a la salida del vagon de la trayectoria, por ello liberamos
		for(i=trayectoriaTotal-espaciosNecesariosNetos;i<trayectoriaTotal;i++) {
			desocuparLugar(i);
		}
		
	}
	
	private void print(String s){
		System.out.println("Unidad "+this.getId()+":\t"+s);
	}
}
