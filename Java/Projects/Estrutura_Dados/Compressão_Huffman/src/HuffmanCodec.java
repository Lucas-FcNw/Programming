import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * Integrantes do grupo:
 * - Lucas Fernandes de Camargo (10419400)
 * - Rafael Lima (10425819)
 */
class HuffmanCodec {
    private static final int MAGIC = 0x48554631; // HUF1

    static void comprimir(String caminhoEntrada, String caminhoSaida) throws IOException {
        byte[] dados = Files.readAllBytes(Path.of(caminhoEntrada));

        int[] frequencias = new int[256];
        for (byte b : dados) {
            frequencias[b & 0xFF]++;
        }

        imprimirTabelaFrequencia(frequencias);

        MinHeap heap = new MinHeap();
        for (int i = 0; i < 256; i++) {
            if (frequencias[i] > 0) {
                heap.inserir(new No((char) i, frequencias[i]));
            }
        }

        imprimirHeapInicial(heap.snapshot());

        No raiz = construirArvore(heap);
        imprimirArvore(raiz);

        String[] codigos = new String[256];
        gerarCodigos(raiz, "", codigos);
        imprimirTabelaCodigos(codigos, frequencias);

        StringBuilder bits = new StringBuilder();
        for (byte b : dados) {
            bits.append(codigos[b & 0xFF]);
        }

        int tamanhoOriginalBits = dados.length * 8;
        int tamanhoComprimidoBits = bits.length();
        byte[] bytesCompactados = empacotarBits(bits);

        try (DataOutputStream out = new DataOutputStream(new BufferedOutputStream(Files.newOutputStream(Path.of(caminhoSaida))))) {
            out.writeInt(MAGIC);
            out.writeInt(dados.length);
            for (int f : frequencias) {
                out.writeInt(f);
            }
            out.writeInt(tamanhoComprimidoBits);
            out.write(bytesCompactados);
        }

        imprimirResumoCompressao(tamanhoOriginalBits, tamanhoComprimidoBits);
    }

    static void descomprimir(String caminhoEntrada, String caminhoSaida) throws IOException {
        int[] frequencias = new int[256];
        int tamanhoOriginal;
        int tamanhoBits;
        byte[] dadosCompactados;

        try (DataInputStream in = new DataInputStream(new BufferedInputStream(Files.newInputStream(Path.of(caminhoEntrada))))) {
            int magicLido = in.readInt();
            if (magicLido != MAGIC) {
                throw new IllegalArgumentException("Arquivo comprimido inválido (assinatura desconhecida).");
            }

            tamanhoOriginal = in.readInt();
            for (int i = 0; i < 256; i++) {
                frequencias[i] = in.readInt();
            }
            tamanhoBits = in.readInt();

            dadosCompactados = in.readAllBytes();
        }

        No raiz = construirArvoreDeFrequencias(frequencias);

        byte[] restaurado = new byte[tamanhoOriginal];
        if (tamanhoOriginal == 0) {
            Files.write(Path.of(caminhoSaida), restaurado);
            return;
        }

        if (raiz != null && raiz.ehFolha()) {
            for (int i = 0; i < tamanhoOriginal; i++) {
                restaurado[i] = (byte) raiz.caractere;
            }
            Files.write(Path.of(caminhoSaida), restaurado);
            return;
        }

        int escritos = 0;
        No atual = raiz;

        for (int i = 0; i < tamanhoBits && escritos < tamanhoOriginal; i++) {
            int byteIndex = i / 8;
            int bitIndex = 7 - (i % 8);
            int bit = (dadosCompactados[byteIndex] >> bitIndex) & 1;

            atual = (bit == 0) ? atual.esquerda : atual.direita;
            if (atual.ehFolha()) {
                restaurado[escritos++] = (byte) atual.caractere;
                atual = raiz;
            }
        }

        if (escritos != tamanhoOriginal) {
            throw new IllegalArgumentException("Falha ao descomprimir: fluxo de bits inconsistente.");
        }

        Files.write(Path.of(caminhoSaida), restaurado);
        System.out.println("Descompressão concluída com sucesso.");
    }

    private static No construirArvore(MinHeap heap) {
        if (heap.tamanho() == 0) {
            return null;
        }

        while (heap.tamanho() > 1) {
            No a = heap.extrairMin();
            No b = heap.extrairMin();
            No pai = new No(a.frequencia + b.frequencia, a, b);
            heap.inserir(pai);
        }

        return heap.extrairMin();
    }

    private static No construirArvoreDeFrequencias(int[] frequencias) {
        MinHeap heap = new MinHeap();
        for (int i = 0; i < 256; i++) {
            if (frequencias[i] > 0) {
                heap.inserir(new No((char) i, frequencias[i]));
            }
        }
        return construirArvore(heap);
    }

    private static void gerarCodigos(No no, String caminho, String[] codigos) {
        if (no == null) {
            return;
        }

        if (no.ehFolha()) {
            codigos[no.caractere & 0xFF] = caminho.isEmpty() ? "0" : caminho;
            return;
        }

        gerarCodigos(no.esquerda, caminho + "0", codigos);
        gerarCodigos(no.direita, caminho + "1", codigos);
    }

    private static byte[] empacotarBits(CharSequence bits) {
        int nBytes = (bits.length() + 7) / 8;
        byte[] saida = new byte[nBytes];

        for (int i = 0; i < bits.length(); i++) {
            if (bits.charAt(i) == '1') {
                int byteIndex = i / 8;
                int bitIndex = 7 - (i % 8);
                saida[byteIndex] |= (byte) (1 << bitIndex);
            }
        }
        return saida;
    }

    private static void imprimirTabelaFrequencia(int[] frequencias) {
        System.out.println("--------------------------------------------------");
        System.out.println("ETAPA 1: Tabela de Frequencia de Caracteres");
        System.out.println("--------------------------------------------------");
        for (int i = 0; i < 256; i++) {
            if (frequencias[i] > 0) {
                System.out.printf("Caractere '%s' (ASCII: %d): %d%n", representar((char) i), i, frequencias[i]);
            }
        }
    }

    private static void imprimirHeapInicial(List<No> heap) {
        System.out.println("--------------------------------------------------");
        System.out.println("ETAPA 2: Min-Heap Inicial (Vetor)");
        System.out.println("--------------------------------------------------");

        List<String> partes = new ArrayList<>();
        for (No n : heap) {
            partes.add("No('" + representar(n.caractere) + "'," + n.frequencia + ")");
        }
        System.out.println("[ " + String.join(", ", partes) + " ]");
    }

    private static void imprimirArvore(No raiz) {
        System.out.println("--------------------------------------------------");
        System.out.println("ETAPA 3: Arvore de Huffman");
        System.out.println("--------------------------------------------------");
        imprimirArvoreRec(raiz, "", "RAIZ");
    }

    private static void imprimirArvoreRec(No no, String indent, String rotulo) {
        if (no == null) {
            return;
        }

        if (no.ehFolha()) {
            System.out.printf("%s- ('%s', %d)%n", indent, representar(no.caractere), no.frequencia);
            return;
        }

        System.out.printf("%s- (%s, %d)%n", indent, rotulo, no.frequencia);
        imprimirArvoreRec(no.esquerda, indent + "  ", "N");
        imprimirArvoreRec(no.direita, indent + "  ", "N");
    }

    private static void imprimirTabelaCodigos(String[] codigos, int[] frequencias) {
        System.out.println("--------------------------------------------------");
        System.out.println("ETAPA 4: Tabela de Codigos de Huffman");
        System.out.println("--------------------------------------------------");
        for (int i = 0; i < 256; i++) {
            if (frequencias[i] > 0) {
                System.out.printf("Caractere '%s': %s%n", representar((char) i), codigos[i]);
            }
        }
    }

    private static void imprimirResumoCompressao(int originalBits, int comprimidoBits) {
        int originalBytes = (originalBits + 7) / 8;
        int comprimidoBytes = (comprimidoBits + 7) / 8;
        double taxa = originalBits == 0
                ? 0.0
                : (1.0 - ((double) comprimidoBits / (double) originalBits)) * 100.0;

        System.out.println("--------------------------------------------------");
        System.out.println("ETAPA 5: Resumo da Compressao");
        System.out.println("--------------------------------------------------");
        System.out.printf("Tamanho original....: %d bits (%d bytes)%n", originalBits, originalBytes);
        System.out.printf("Tamanho comprimido..: %d bits (%d bytes)%n", comprimidoBits, comprimidoBytes);
        System.out.printf(Locale.US, "Taxa de compressao..: %.2f%%%n", taxa);
        System.out.println("--------------------------------------------------");
    }

    private static String representar(char c) {
        if (c == '\n') return "\\n";
        if (c == '\r') return "\\r";
        if (c == '\t') return "\\t";
        if (Character.isISOControl(c)) return "?";
        return String.valueOf(c);
    }
}