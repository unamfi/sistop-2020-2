package modeladoObjetos;

import java.util.ArrayList;
import java.util.concurrent.Semaphore;

public class Unidad extends Thread{
	private int numAsientos;
	private int cupoMinimo;			//numero de asientos que se deben cubrir para comenzar a avanzar
	private ArrayList<Semaphore> mutexTrayectoria; //va de acuerdo con los espacios del juego en los carriles, es proporcionado por el JUEGO MECANICO
	private int longitud;			//la longitud del vagon- unidad
	private int espacioEntreUnidades;//espacio seguro que debe haber entre unidades
	
	private Semaphore entradaPersonas;
	private Semaphore salidaPersonas;
	
	public Unidad(int numAsientos,int cupoMinimo,int longitud,
			int espacioEntreUnidades,ArrayList<Semaphore> mutexTrayectoria) {
		
		this.numAsientos=numAsientos;
		this.cupoMinimo=cupoMinimo;
		this.longitud=longitud;
		this.mutexTrayectoria=mutexTrayectoria;
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
			mutexTrayectoria.get(indiceDelLugar).acquire();
			print(" Vamos en "+indiceDelLugar);
			
		} catch (InterruptedException e) {
			print("Se produjo un error en Mutex, no se pudo adquirir... "
					+ "Objeto Unidad"+this.getId());
		}
	}
	
	private void desocuparLugar(int indiceDelLugar) {
		
		if(indiceDelLugar>=this.mutexTrayectoria.size()) {
			print("Este mutex no existe");
		}

		mutexTrayectoria.get(indiceDelLugar).release();
		print("Libere espacio: "+indiceDelLugar);

	}
	
	public void run() {
		int trayectoriaTotal=this.mutexTrayectoria.size();//la cantidad de mutex, son el total de espacios para recorrer todo el juego mecanico
		int espaciosNecesariosNetos=this.longitud+this.espacioEntreUnidades;// Nos dice los espacios que debe ocupar una unidad contando los de seguridad
		
		int personasEsperando= entradaPersonas.getQueueLength();//determinamos el numero de personas que quiere entrar
		
		//decidimos cuantos vamos a dejar pasar
		if(personasEsperando>this.numAsientos) {
			personasEsperando=this.numAsientos;
		}else if(personasEsperando<this.cupoMinimo) {
			
		}
		
		
		//dejamos pasar hasta el numero dicho
		for(int i=0;i<personasEsperando;i++) {
			this.entradaPersonas.release();
		}
		
		
		print("Arrancamos");
		ocuparLugar(0,espaciosNecesariosNetos-1);//con esto ya contemplamos que la unidad ya avanzó y ya dejó marcados los espacios de seguridad en la parte de atras
		
		//mientras vamos avanzando, liberamos los espacios de seguridad, avanza 1, liberamos 1 para que otros hilos lo comiencen a ocupar
		int i=0;//contador que nos dice en que punto de la trayectoria vamos
		for (i=espaciosNecesariosNetos;i<trayectoriaTotal;i++) {
			ocuparLugar(i);
			desocuparLugar(i-espaciosNecesariosNetos);//
		}
		
		//al terminar el recorrido, dejamos a las personas irse
		for(int j=0;j<personasEsperando;j++) {
			this.salidaPersonas.release();
		}
		
		//aun tenemos lugares que no desocupamos del la via, estos ultimos son los correspondientes a la salida del vagon de la trayectoria, por ello liberamos
		for(i=trayectoriaTotal-espaciosNecesariosNetos;i<trayectoriaTotal;i++) {
			desocuparLugar(i);
		}
		
	}
	
	private void print(String s){
		System.out.println("Unidad "+this.getId()+":\t"+s);
	}
}
