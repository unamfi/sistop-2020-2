package modeladoObjetos;

import java.util.ArrayList;
import java.util.concurrent.Semaphore;

public class ParqueDeDiversiones extends Thread{
	private String nombre;
	private ArrayList<JuegoMecanico> juegos;
	private Semaphore torniqueteEntrada;
	
	public ParqueDeDiversiones(String nombre) {
		this.nombre=nombre;
		juegos=new ArrayList<>();
		torniqueteEntrada=new Semaphore(1);
	}
	
	public String getNombre() {
		return this.nombre;
	}
	
	public Semaphore getTorniquete(){
		return this.torniqueteEntrada;
	}
	
	public void abreJuego(String nombre,int unidadesFuncionando,int numAsientos,int cupoMinimo,
			int longitudUnidades,int longitudTrayectoria,int longitudEspacioSeguro) {
		this.juegos.add(new JuegoMecanico(nombre,unidadesFuncionando,numAsientos,cupoMinimo,
				longitudUnidades,longitudTrayectoria,longitudEspacioSeguro));
	}
	
	public void run() {
		for(JuegoMecanico x:juegos ) {
			x.start();
		
		}
		
	}
	
	
}
