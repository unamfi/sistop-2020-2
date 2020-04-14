public class DemoTiendaCafe {
	public static void main(String[] args) throws InterruptedException {
	    TiendaCafe tienda = new TiendaCafe();
	    Thread t1 = new Thread(new Cliente(tienda, "Miguel"));
	    Thread t2 = new Thread(new Cliente(tienda, "Juan"));
	    Thread t3 = new Thread(new Cliente(tienda, "Anita"));
	    Thread t4 = new Thread(new Cliente(tienda, "Christopher"));
	     
	    long startTime = System.currentTimeMillis();
	    t1.start();
	    t2.start();
	    t3.start();
	    t4.start();
	     
	    t1.join();
	    t2.join();
	    t3.join();
	    t4.join();
	     
	    long totalTime = System.currentTimeMillis() - startTime;
	    System.out.println("Cafe vendido: " + tienda.countSoldCoffees());
	    System.out.println("Ultimo Cliente: " + tienda.getLastClient());
	    System.out.println("Tiempo total: " + totalTime + " ms");
	}
}
