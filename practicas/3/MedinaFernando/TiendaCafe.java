public class TiendaCafe {
	    private String ultimCliente;
	    private int cafesVendidos;
	     
	    private void someLongRunningProcess() throws InterruptedException {
	        Thread.sleep(3000);
	    }
	     
	    public void compraCafe(String Cliente) throws InterruptedException {
	        someLongRunningProcess();
	        ultimCliente = Cliente;
	        cafesVendidos++;
	        System.out.println(Cliente + " compro un cafe");
	    }
	     
	    public int countSoldCoffees() {return cafesVendidos;}
	     
	    public String getLastClient() {return ultimCliente;}
}
