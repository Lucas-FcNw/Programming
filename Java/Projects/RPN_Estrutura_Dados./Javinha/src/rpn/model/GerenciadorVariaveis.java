/*
 * Caio Henrique Santos Carvalho RA: 10425408
 * Diogo Fassina Garcia - RA: 10417030
 * Rafael de Souza Alves de Lima RA: 10425819
 * Lucas Fernandes de Camargo RA: 10419400
 *
 * */




package rpn.model;

public class GerenciadorVariaveis {
    private static final int NUM_VARIAVEIS = 26; // A até Z
    private final double[] valores;
    private final boolean[] definidas;

    public GerenciadorVariaveis() {
        valores = new double[NUM_VARIAVEIS];
        definidas = new boolean[NUM_VARIAVEIS]; // Sai tudo false de inicio
    }

    // Define ou atualiza uma variável
    public void definirVariavel(char var, double valor) {
        int indice = Character.toUpperCase(var) - 'A'; //Conversor de minusculo para Maiusculo, permitindo o usuario usar 'a' e 'A' sem conflitos.
        if (indice < 0 || indice >= NUM_VARIAVEIS) throw new IllegalArgumentException("Variável inválida");
        valores[indice] = valor;
        definidas[indice] = true;
    }

    // Recupera valor se existir
    public double obterValor(char var) {
        int indice = Character.toUpperCase(var) - 'A';
        if (indice < 0 || indice >= NUM_VARIAVEIS || !definidas[indice])
            throw new IllegalArgumentException("Variável não definida");
        return valores[indice];
    }

    // Verifica existência
    public boolean estaDefinida(char var) {
        int indice = Character.toUpperCase(var) - 'A';
        return indice >= 0 && indice < NUM_VARIAVEIS && definidas[indice];
    }

    // Limpa todas variáveis
    public void reset() {
        for (int i = 0; i < NUM_VARIAVEIS; i++) definidas[i] = false;
    }

    // Lista no formato "A = 1.00"
    public String[] listarVariaveisDefinidas() {
        int count = 0;
        for (boolean def : definidas) if (def) count++;

        String[] vars = new String[count];
        int index = 0;
        for (int i = 0; i < NUM_VARIAVEIS; i++) {
            if (definidas[i]) vars[index++] = String.format("%c = %.2f", 'A' + i, valores[i]);
        }
        return vars;
    }
}