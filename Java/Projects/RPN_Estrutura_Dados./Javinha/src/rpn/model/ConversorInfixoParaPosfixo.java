/*
 * Caio Henrique Santos Carvalho RA: 10425408
 * Diogo Fassina Garcia - RA: 10417030
 * Rafael de Souza Alves de Lima RA: 10425819
 * Lucas Fernandes de Camargo RA: 10419400
 *
 * */


package rpn.model;

// ISSO É o RPN, Notação Polonesa Inversa  ' a b + '
public class ConversorInfixoParaPosfixo {
    // Ordem de operação matemática, adnedo que o '1' é 'especial'
    private static final char[] OPERADORES = {'^', '*', '/', '+', '-', '('};
    private static final int[] PREFERENCIAS = {4, 3, 3, 2, 2, 1};

    // Mapeia operador -> precedência
    private static int obterPreferencia(char operador) {
        for (int i = 0; i < OPERADORES.length; i++) {
            if (OPERADORES[i] == operador) return PREFERENCIAS[i];
        }
        return -1; // Não é operador
    }

    // Chegamos no converosr  isso é criado pelo Dijkstra (traumas) chamdo Algoritmo Shunting-yard
    // Referencia https://mauromartins.wordpress.com/2009/06/15/rpn/   Obrigado mãe por me ensinar a usar uma HP financeira, primeiro contato com RPN.
    public static String converter(String expressaoInfixa) {
        StringBuilder posfixa = new StringBuilder(); // Saída RPN
        Pilha<Character> pilha = new Pilha<>(expressaoInfixa.length());

        for (int i = 0; i < expressaoInfixa.length(); i++) {
            char c = expressaoInfixa.charAt(i);
            if (Character.isWhitespace(c)) continue; // Ignora espaços

            if (Character.isLetter(c)) {
                posfixa.append(Character.toUpperCase(c)).append(' ');
            }
            else if (c == '(') {
                pilha.empilhar(c);
            }
            else if (c == ')') {
                // Desempilha até encontrar '('
                while (!pilha.estaVazia() && pilha.topo() != '(') {
                    posfixa.append(pilha.desempilhar()).append(' ');
                }
                if (pilha.estaVazia()) throw new IllegalArgumentException("Parênteses desbalanceados");
                pilha.desempilhar(); // Remove '('
            }
            else if (obterPreferencia(c) > 0) {
                while (!pilha.estaVazia() && obterPreferencia(pilha.topo()) >= obterPreferencia(c)) {
                    posfixa.append(pilha.desempilhar()).append(' ');
                }
                pilha.empilhar(c); // Empilha novo operador
            }
            else {
                throw new IllegalArgumentException("Caractere inválido: " + c);
            }
        }

        // Desempilha o restante
        while (!pilha.estaVazia()) {
            char op = pilha.desempilhar();
            if (op == '(') throw new IllegalArgumentException("Parênteses desbalanceados");
            posfixa.append(op).append(' ');
        }

        return posfixa.toString().trim(); // Remove espaço extra
    }
}