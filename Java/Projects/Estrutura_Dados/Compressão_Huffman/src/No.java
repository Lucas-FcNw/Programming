/**
 * Integrantes do grupo:
 * - Lucas Fernandes de Camargo (10419400)
 * - Rafael Lima (10425819)
 */
class No implements Comparable<No> {
    char caractere;
    int frequencia;
    No esquerda;
    No direita;

    No(char caractere, int frequencia) {
        this.caractere = caractere;
        this.frequencia = frequencia;
    }

    No(int frequencia, No esquerda, No direita) {
        this.caractere = '\0';
        this.frequencia = frequencia;
        this.esquerda = esquerda;
        this.direita = direita;
    }

    boolean ehFolha() {
        return esquerda == null && direita == null;
    }

    @Override
    public int compareTo(No outroNo) {
        return Integer.compare(this.frequencia, outroNo.frequencia);
    }
}