import java.util.Scanner;
// -----------------------------
// YTarefa Filas
// -----------------------------
public class FilaMain {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        // Exercício 1
        System.out.println("--- Exercício 1: Fila de inteiros ---");
        FilaInt filaInt = new FilaInt(10);

        System.out.println("Digite 5 números inteiros:");
        for (int i = 0; i < 5; i++) {
            int num = sc.nextInt();
            filaInt.inserir(num);
        }

        filaInt.mostrar();

        System.out.println("Removendo 2 elementos...");
        filaInt.remover();
        filaInt.remover();
        filaInt.mostrar();

        // Exercício 2
        System.out.println("\n--- Exercício 2: Fila Genérica ---");

        Fila<Integer> filaInteger = new Fila<>(5);
        Fila<String> filaString = new Fila<>(5);
        Fila<Double> filaDouble = new Fila<>(5);

        filaInteger.inserir(10);
        filaInteger.inserir(20);
        filaInteger.inserir(30);

        System.out.println("Primeiro da filaInteger: " + filaInteger.primeiro());
        filaInteger.remover();
        System.out.println("Primeiro após remover: " + filaInteger.primeiro());

        filaString.inserir("Ana");
        filaString.inserir("Beto");
        System.out.println("Primeiro da filaString: " + filaString.primeiro());

        filaDouble.inserir(1.5);
        filaDouble.inserir(2.7);
        System.out.println("Primeiro da filaDouble: " + filaDouble.primeiro());

        // Exercício 3
        System.out.println("\n--- Exercício 3: Fila de Atendimento ---");

        Fila<String> filaAtendimento = new Fila<>(100);

        System.out.println("Digite nomes dos clientes (digite 'fim' para encerrar):");
        sc.nextLine(); // limpar buffer

        while (true) {
            String nome = sc.nextLine();
            if (nome.equalsIgnoreCase("fim"))
                break;

            filaAtendimento.inserir(nome);
        }

        while (!filaAtendimento.estaVazia()) {
            String cliente = filaAtendimento.remover();
            System.out.println("\n  Atendendo cliente: " + cliente);
        }
    System.out.println("\nFeito por: Lucas Fernandes de Camargo 10419400");

        sc.close();
    }
}