public class Cliente implements Runnable {
	    private final String nombre;
	    private final TiendaCafe tienda;
	     
	    public Cliente(TiendaCafe tienda, String nombre) {
	        this.tienda = tienda;
	        this.nombre = nombre;
	    }
	     
	    @Override
	    public void run() {
	        try {
	            tienda.compraCafe(nombre);
	        } catch (InterruptedException e) {
	            System.out.println("Compra Interrumpida");
	        }
	    }
}


