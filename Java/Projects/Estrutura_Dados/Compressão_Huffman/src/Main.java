import java.io.IOException;

/**
 * Integrantes do grupo:
 * - Lucas Fernandes de Camargo (10419400)
 * - Rafael Lima (10425819)
 */
public class Main {
    public static void main(String[] args) {
        if (args.length != 3) {
            imprimirUso();
            return;
        }

        String modo = args[0];
        String entrada = args[1];
        String saida = args[2];

        try {
            if ("-c".equals(modo)) {
                HuffmanCodec.comprimir(entrada, saida);
            } else if ("-d".equals(modo)) {
                HuffmanCodec.descomprimir(entrada, saida);
            } else {
                imprimirUso();
            }
        } catch (IOException e) {
            System.err.println("Erro de E/S: " + e.getMessage());
        } catch (IllegalArgumentException e) {
            System.err.println("Erro: " + e.getMessage());
        }
    }

    private static void imprimirUso() {
        System.out.println("Uso:");
        System.out.println("  Para comprimir:   java -jar huffman.jar -c <arquivo_original> <arquivo_comprimido>");
        System.out.println("  Para descomprimir: java -jar huffman.jar -d <arquivo_comprimido> <arquivo_restaurado>");
    }
}