import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintStream;
import java.nio.file.Files;
import java.nio.file.Path;

/**
 * Integrantes do grupo:
 * - Lucas Fernandes de Camargo (10419400)
 * - Rafael Lima (10425819)
 */
public class Benchmark {
    public static void main(String[] args) throws IOException {
        if (args.length == 0) {
            System.out.println("Uso: java -cp src Benchmark <arquivo1> <arquivo2> ...");
            return;
        }

        System.out.println("arquivo,tamanho_bytes,compressao_ms,descompressao_ms,taxa_compressao_percentual");

        for (String arquivo : args) {
            Path in = Path.of(arquivo);
            Path huff = Path.of(arquivo + ".huff");
            Path out = Path.of(arquivo + ".out");

            long tamanhoOriginal = Files.size(in);

            PrintStream originalOut = System.out;
            PrintStream sink = new PrintStream(OutputStream.nullOutputStream());

            long iniC;
            long fimC;
            long iniD;
            long fimD;

            try {
                System.setOut(sink);
                iniC = System.nanoTime();
                HuffmanCodec.comprimir(in.toString(), huff.toString());
                fimC = System.nanoTime();

                iniD = System.nanoTime();
                HuffmanCodec.descomprimir(huff.toString(), out.toString());
                fimD = System.nanoTime();
            } finally {
                System.setOut(originalOut);
                sink.close();
            }

            long tamanhoComprimido = Files.size(huff);
            double taxa = (tamanhoOriginal == 0)
                    ? 0.0
                    : (1.0 - ((double) tamanhoComprimido / (double) tamanhoOriginal)) * 100.0;

            double msC = (fimC - iniC) / 1_000_000.0;
            double msD = (fimD - iniD) / 1_000_000.0;

            System.out.printf(java.util.Locale.US,
                    "%s,%d,%.3f,%.3f,%.2f%n",
                    arquivo, tamanhoOriginal, msC, msD, taxa);
        }
    }
}
