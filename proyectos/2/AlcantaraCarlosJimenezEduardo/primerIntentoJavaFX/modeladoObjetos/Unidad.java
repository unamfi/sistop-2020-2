package modeladoObjetos;

import java.util.ArrayList;
import java.util.concurrent.Semaphore;

public class Unidad extends Thread{
	private int numAsientos;
	private int cupoMinimo;			//numero de asientos que se deben cubrir para comenzar a avanzar
	private ArrayList<Semaphore> mutexTrayectoria; //va de acuerdo con los espacios del juego en los carriles, es proporcionado por el JUEGO MECANICO
	private int longitud;			//la longitud del vagon- unidad
	private int espacioEntreUnidades;//espacio seguro que debe haber entre unidades
	
	private int factorTiempoDeEspera;
	private boolean pudeArrancar;
	private Semaphore entradaPersonas;
	private Semaphore salidaPersonas;
	private Semaphore salidaUnidad;
	private Fila colaEntrada;
	private Semaphore mutexCola;
	
	public Unidad(int numAsientos,int cupoMinimo,int longitud,
			int espacioEntreUnidades,ArrayList<Semaphore> mutexTrayectoria) {
		
		this.numAsientos=numAsientos;
		this.cupoMinimo=cupoMinimo;
		this.longitud=longitud;
		this.mutexTrayectoria=mutexTrayectoria;
		this.espacioEntreUnidades=espacioEntreUnidades;
		this.pudeArrancar=true;
	}
	
	public Fila getColaEntrada() {
		return colaEntrada;
	}
	
	public void setColaEntrada(Fila colaEntrada) {
		this.colaEntrada=colaEntrada;
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
	
	public Semaphore getEntradaPersonas() {
		return this.entradaPersonas;
	}
	
	public Semaphore getSalidaPersonas() {
		return this.salidaPersonas;
	}
	
	public synchronized boolean getPudeArrancar() {
		return this.pudeArrancar;
	}
	
	public void setFactorTiempoDeEspera(int popularidadJuegoMecanico) {
		factorTiempoDeEspera=popularidadJuegoMecanico;
	}
	
	public Semaphore getSalidaUnidad() {
		return this.salidaUnidad;
	}
	
	public Semaphore getMutexCola() {
		return this.mutexCola;
	}
	
	public void setMutexCola(Semaphore mutexCola) {
		this.mutexCola=mutexCola;
	}
	
	public void setBarrerasPersonas(Semaphore entradaPersonas,Semaphore salidaPersonas,Semaphore salidaUnidad) {
		this.entradaPersonas=entradaPersonas;
		this.salidaPersonas=salidaPersonas;
		this.salidaUnidad=salidaUnidad;
	}
	
	private void ocuparLugar(int desdeLugar,int hastaLugar) {
		for (int i=desdeLugar;i<=hastaLugar;i++) {
			ocuparLugar(i);
		}
	}
	
	private void ocuparLugar(int indiceDelLugar) {
		
		try {
			Thread.sleep(500);
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
	
	private int personasEsperando() {
		try {
			mutexCola.acquire();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		int numeroDeEspera=0;
		int personasEsperando=0;
		//vamos a decidir si la unidad avanza o no, y si avanza, vamos a dejar pasar la cantidad exacta de personas
		
		while (true) {
			boolean personasPuedenEsperar; 
			
			personasEsperando=colaEntrada.getCola();
			print("---------------La cola es de :"+personasEsperando);
			if(personasEsperando<this.cupoMinimo) {
				personasPuedenEsperar=esperarMasPersonas((numeroDeEspera+1)*factorTiempoDeEspera,numeroDeEspera,factorTiempoDeEspera);
				numeroDeEspera++;
			}else if(personasEsperando>this.numAsientos) {
				personasEsperando=this.numAsientos;
				break;
			}else {
				break;
			}
			
			if(personasPuedenEsperar==false) {
				print("Las personas dejaron de esperar, se van a otro juego");
				this.pudeArrancar=false;//se pudo manejar la variable pudeArrancar y personasPuedenEsperar como una sola, pero se hizo de esta manera para que fuera mas legible
				break;
			}
			
		}
		//liberamos a las personas, si pudeArrancar es true, entonces se arrancara.
		for(int i=0;i<personasEsperando;i++) {
			this.colaEntrada.salirCola();
			this.entradaPersonas.release();
		}
		//print("Deje la cola con:"+this.getColaEntrada().getCola());
		mutexCola.release();
		return personasEsperando;
	}
	
	public void run() {
		int trayectoriaTotal=this.mutexTrayectoria.size();//la cantidad de mutex, son el total de espacios para recorrer todo el juego mecanico
		int espaciosNecesariosNetos=this.longitud+this.espacioEntreUnidades;// Nos dice los espacios que debe ocupar una unidad contando los de seguridad
		
		print("Iniciamos seccion critica");
		int personasEsperando=personasEsperando();
		print("-----------Personas Esperando despues de operar: "+personasEsperando);
		print("Terminamos seccion critica");
		
		
		if(personasEsperando==0) {
			print("No tenemos personas.");
			this.pudeArrancar=false;
		}
		
		if(this.pudeArrancar==false) {
			print("Ya conclui mi trabajo, bai");
			
			return;
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
		
		//esperamos a que todos se hayan bajado
		for(int j=0;j<personasEsperando;j++) {
			try {
				this.salidaUnidad.acquire();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		
		//aun tenemos lugares que no desocupamos del la via, estos ultimos son los correspondientes a la salida del vagon de la trayectoria, por ello liberamos
		for(i=trayectoriaTotal-espaciosNecesariosNetos;i<trayectoriaTotal;i++) {
			desocuparLugar(i);
		}
		
		print("Ya conclui mi trabajo, bai");
		
	}
	
	private void print(String s){
		System.out.println("--Unidad "+this.getId()+":\t"+s);
	}
	
	private boolean esperarMasPersonas(int segundos,int veces,int maximoVeces) {
		boolean pudeEsperar;
		if(veces<maximoVeces) {
			try {
				print("Voy a dormir: "+segundos*1000);
				Thread.sleep(segundos*1000);
				pudeEsperar=true;
			} catch (InterruptedException e) {
				e.printStackTrace();
				pudeEsperar=false;
			}
		}else {
			pudeEsperar=false;
		}
		return pudeEsperar;
	}
	
}
