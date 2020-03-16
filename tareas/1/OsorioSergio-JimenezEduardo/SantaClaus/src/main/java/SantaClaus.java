
import java.util.Random;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.Semaphore;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.ArrayList;

public class SantaClaus {

    private boolean SantaTieneNavidades = true;
    private final Semaphore Matar_Santa = new Semaphore(0);
    private int FinNavidades = 2030;
    private AtomicInteger year = new AtomicInteger(2020);
    private static final Random generador_aleatorios = new Random();

    // Cantidad de elfos, renos y tamaño de la barrera para despertar a Santa 
    private int numero_renos = 9;
    private int numero_elfos = 10;
    private int despertarSanta = 3;

    // synchronisation variables
    private final Semaphore colaDeElfos;
    private final CyclicBarrier tresElfos;
    private final CyclicBarrier elfosAyudados;
    private final CyclicBarrier grupoRenos;
    private final CyclicBarrier trineo;
    private final Semaphore atencionDeSanta;
    private final static int ultimoReno = 0;
    private final static int tercerElfo = 0;

    class Reno implements Runnable {

        int id;

        Reno(int id) {
            this.id = id;
        }

        @Override
        public void run() {
            while (SantaTieneNavidades) {
                try {
                    // espera hasta que llega Santa
                    Thread.sleep(900 + generador_aleatorios.nextInt(200));

                    // Santa solo despierta si todos los renos estan reunidos
                    int reno = grupoRenos.await();
                    // el ultimo reno en regresar de vacaciones debe despertar a Santa
                    if (reno == ultimoReno) {
                        atencionDeSanta.acquire();
                        System.out.println("Entrega de jueguetes para " + year);
                        if (year.incrementAndGet() == FinNavidades) {
                            SantaTieneNavidades = false;
                            Matar_Santa.release();
                        }
                    }
                    //Para llevar juguetes los renos deben estar amarrados al trineo
                    trineo.await();
                    Thread.sleep(generador_aleatorios.nextInt(20));
                    reno = trineo.await();
                    if (reno == ultimoReno) {
                        atencionDeSanta.release();
                        System.out.println("¡¡¡Ya es Navidad!!! Repartiendo juguetes...");
                    }
                } catch (InterruptedException | BrokenBarrierException e) {
                }
            }
            System.out.println("Reno " + id + " se va de vacaciones");
        }
    }

    class Elfo implements Runnable {

        int id;

        Elfo(int id) {
            this.id = id;
        }

        @Override
        public void run() {
            try {
                Thread.sleep(generador_aleatorios.nextInt(2000));
                System.out.println("...Elfos creando Juguetes...");
                while (SantaTieneNavidades) {

                    // Solo 3 elfos agrupados pueden despertar a Santa
                    colaDeElfos.acquire();
                    System.out.println("El elfo " + id + " necesita ayuda");

                    //espera hasta que se junten 3 elfos 
                    int elf = tresElfos.await();

                    //el tercer elfo despierta a Santa
                    if (elf == tercerElfo) {
                        atencionDeSanta.acquire();
                    }

                    // espera hasta que Santa los termine de ayudar 
                    Thread.sleep(generador_aleatorios.nextInt(500));
                    System.out.println("El elfo " + id + " resolvió el problema con Santa");
                    elfosAyudados.await();

                    if (elf == tercerElfo) {
                        atencionDeSanta.release();
                    }

                    //limpiar la cola para que mas elfos puedan esperar a la ayuda de Santa
                    colaDeElfos.release();

                    // volver a hacer juguetes hasta tener problemas otra vez
                    Thread.sleep(generador_aleatorios.nextInt(2000));
                }
            } catch (InterruptedException | BrokenBarrierException e) {

            }
            System.out.println("Elfo  " + id + " se va a dormir");
        }
    }

    class estadoBarrera implements Runnable {

        String mensaje;

        estadoBarrera(String mensaje) {
            this.mensaje = mensaje;
        }

        @Override
        public void run() {
            System.out.println(mensaje);
        }
    }

    class atarRenos implements Runnable {

        boolean estaAtadoAlTrineo;

        atarRenos() {
            estaAtadoAlTrineo = false;
        }

        @Override
        public void run() {
            estaAtadoAlTrineo = !estaAtadoAlTrineo;
            if (estaAtadoAlTrineo) {
                System.out.println("===Renos atados===");
            } else {
                System.out.println("===Renos esperando en la pista===");
            }
        }
    }

    public SantaClaus() {
        atencionDeSanta = new Semaphore(1, true);
        colaDeElfos = new Semaphore(despertarSanta, true);    // use a fair semaphore
        tresElfos = new CyclicBarrier(despertarSanta, new estadoBarrera("--- " + despertarSanta + " elfos están esperando por Santa ---"));

        elfosAyudados = new CyclicBarrier(despertarSanta, new estadoBarrera("--- Los elfos regresan al trabajo ---"));
        grupoRenos = new CyclicBarrier(numero_renos, () -> {
            System.out.println("===Renos regresan para iniciar la Navidad " + year + " ===");
        });
        trineo = new CyclicBarrier(numero_renos, new atarRenos());

        ArrayList<Thread> hilos = new ArrayList<>();
        for (int i = 0; i < numero_elfos; ++i) {
            hilos.add(new Thread(new Elfo(i)));
        }
        for (int i = 0; i < numero_renos; ++i) {
            hilos.add(new Thread(new Reno(i)));
        }
        System.out.println("Año: " + year);
        hilos.forEach((t) -> {
            t.start();
        });

        try {
            // espera hasta que se hayan terminado las Navidades
            Matar_Santa.acquire();
            System.out.println("Ha terminado la Navidad :( ");
            hilos.forEach((t) -> {
                t.interrupt();
            });
            for (Thread t : hilos) {
                t.join();
            }
        } catch (InterruptedException e) {
        }
        System.out.println("Santa Claus se va a dormir");
    }

    public static void main(String[] args) {
        SantaClaus santaClaus = new SantaClaus();

    }
}
