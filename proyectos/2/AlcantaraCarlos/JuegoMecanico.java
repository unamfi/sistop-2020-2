package modeladoObjetos;

import java.util.ArrayList;
import java.util.concurrent.Semaphore;


public class JuegoMecanico implements Runnable{
	private String nombre;
	private ArrayList<Unidad> unidadesFuncionando;
	private int numLugaresAbordarJuego;
	private int longitudCarriles;
	
	public JuegoMecanico(String nombre, int unidadesFuncionando,
			int numLugaresAbordarJuego){
		this.nombre=nombre;
		this.unidadesFuncionando=new ArrayList<Unidad>(unidadesFuncionando);
		
		this.numLugaresAbordarJuego=numLugaresAbordarJuego;
	}
	
	public String getNombre() {
		return this.nombre;
	}
	
	public int getUnidadesFuncionando() {
		return this.unidadesFuncionando.size();
	}
	
	public int getNumLugaresAbordarJuego() {
		return this.numLugaresAbordarJuego;
	}

	@Override
	public void run() {
		ArrayList<Semaphore> s=new ArrayList<Semaphore>();
		for(int i=0;i<50;i++) {
			s.add(new Semaphore(1));
		}
		Unidad u=new Unidad(5,1,3,3,s);
		Unidad u1=new Unidad(5,1,3,3,s);
		
		u.run();
		u1.run();
		
	}
}
