
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;

public class BarreraPrueba {

    private CyclicBarrier cyclicBarrier;
    private List<List<Integer>> resultados_parciales
            = Collections.synchronizedList(new ArrayList<>());
    private Random random = new Random();
    private int NUM_PARTIAL_RESULTS;
    private int Numero_hilos;
    // Previous code

    class NumberCruncherThread implements Runnable {

        @Override
        public void run() {
            String thisThreadName = Thread.currentThread().getName();
            List<Integer> partialResult = new ArrayList<>();

            // Crunch some numbers and store the partial result
            for (int i = 0; i < NUM_PARTIAL_RESULTS; i++) {
                Integer num = random.nextInt(10);
                System.out.println(thisThreadName
                        + ": ...sumando numeros al azar     Resultado Final: " + num);
                partialResult.add(num);
            }

            resultados_parciales.add(partialResult);
            try {
                System.out.println(thisThreadName
                        + " esperando a otros hilos en la barrera");
                cyclicBarrier.await();
            } catch (InterruptedException | BrokenBarrierException e) {
                // ...
            }
            // ...

        }
    }

    class Sumador implements Runnable {

        @Override
        public void run() {

            String thisThreadName = Thread.currentThread().getName();

            System.out.println(
                    thisThreadName + ": Sumando " + Numero_hilos
                    + " hilos, con " + NUM_PARTIAL_RESULTS + " resultados cada uno.");
            int sum = 0;

            for (List<Integer> threadResult : resultados_parciales) {

                System.out.print("Añadiendo ");
                for (Integer partialResult : threadResult) {
                    System.out.print(partialResult + " ");
                    sum += partialResult;
                }
                System.out.println();
            }
            System.out.println(thisThreadName + ": Resultado Final = " + sum);
        }
    }

    public void crearHilos(int numWorkers, int numberOfPartialResults) {
        NUM_PARTIAL_RESULTS = numberOfPartialResults;
        Numero_hilos = numWorkers;

        cyclicBarrier = new CyclicBarrier(Numero_hilos, new Sumador());

        System.out.println("Generando " + Numero_hilos
                + " hilos con "
                + NUM_PARTIAL_RESULTS + " resultados parciales cada uno");

        for (int i = 0; i < Numero_hilos; i++) {
            Thread worker = new Thread(new NumberCruncherThread());
            worker.setName("Hilo " + i);
            worker.start();
        }
    }

    public static void main(String[] args) {
        //Implementacion de una barrera para sincronizacion entre hilos obtenida de https://github.com/eugenp/tutorials/tree/master/core-java-modules/core-java-concurrency-advanced
        //Se realiza la suma de 5 hilos, cada uno genera y suma numeros aleatorios. 
        //Utilizando una barrera que al llenarse suma los 3 resultados de los 5 hilos
        BarreraPrueba demo = new BarreraPrueba();
        demo.crearHilos(5, 3);
    }
}
