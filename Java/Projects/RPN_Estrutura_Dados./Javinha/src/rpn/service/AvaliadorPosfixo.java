/*
 * Caio Henrique Santos Carvalho RA: 10425408
 * Diogo Fassina Garcia - RA: 10417030
 * Rafael de Souza Alves de Lima RA: 10425819
 * Lucas Fernandes de Camargo RA: 10419400
 *
 * */


package rpn.service;

import rpn.model.GerenciadorVariaveis;
import rpn.model.Pilha;

// Calcula resultados do RPN
public class AvaliadorPosfixo {
    private final GerenciadorVariaveis gerenciador; // Armazena valores A-Z

    public AvaliadorPosfixo() {
        this.gerenciador = new GerenciadorVariaveis();
    }

    // Atribui valor a variável (ex: A=5)
    public void definirVariavel(char var, double valor) {
        gerenciador.definirVariavel(var, valor);
    }

    // Processa expressão RPN usando pilha
    public double avaliar(String expressaoPosfixa) {
        Pilha<Double> pilha = new Pilha<>(expressaoPosfixa.length());
        String[] tokens = expressaoPosfixa.split("\\s+"); // Divide em pedaços(tokens)  a+b  ('a' '+' 'b')

        for (String token : tokens) {
            if (token.length() == 1) {
                char c = token.charAt(0);
                if (Character.isLetter(c)) { // Vê se é variavel.
                    if (!gerenciador.estaDefinida(c))
                        throw new IllegalArgumentException("Variável " + c + " não definida");
                    pilha.empilhar(gerenciador.obterValor(c));
                    continue;
                }
            }

            if (isOperador(token.charAt(0))) { // Vê se é operador.
                if (pilha.tamanho() < 2) throw new IllegalArgumentException("Faltam operandos");
                double b = pilha.desempilhar();
                double a = pilha.desempilhar();
                pilha.empilhar(aplicarOperador(a, b, token.charAt(0))); // Calcula e empilha resultado
            }
            else {
                throw new IllegalArgumentException("Token inválido: " + token); //Não funciona muito bem, mas ao tentar remover o } se perdia, não aguentava mais modificar o projeto. Isso se repete em algumas partes.
            }
        }

        if (pilha.tamanho() != 1) throw new IllegalArgumentException("Expressão incompleta");
        return pilha.desempilhar(); // Resultado final
    }

    // Operações básicas
    private double aplicarOperador(double a, double b, char operador) {
        switch (operador) {
            case '+': return a + b;
            case '-': return a - b;
            case '*': return a * b;
            case '/':
                if (b == 0) throw new ArithmeticException("Divisão por zero");
                return a / b;
            case '^': return Math.pow(a, b);
            default: throw new IllegalArgumentException("Operador inválido: " + operador); //Não funciona muito bem 2.
        }
    }

    // Vê os operadores válidos
    private boolean isOperador(char c) {
        return c == '+' || c == '-' || c == '*' || c == '/' || c == '^';
    }

    // Apaga as variáveis
    public void reset() {
        gerenciador.reset();
    }

    // Lista variáveis inseridas pelo usuário
    public String[] listarVariaveis() {
        return gerenciador.listarVariaveisDefinidas();
    }
}