/*
 * Caio Henrique Santos Carvalho RA: 10425408
 * Diogo Fassina Garcia - RA: 10417030
 * Rafael de Souza Alves de Lima RA: 10425819
 * Lucas Fernandes de Camargo RA: 10419400
 *
 * */


package rpn.model;

//  Pilha genérica com array
public class Pilha<T> {
    private Object[] elementos;  // Guarda os dados. Object para ser genérico
    private int tamanho;         // Limita o tamanho dos elementos
    private int capacidade;      // Tamanho máximo

    public Pilha(int capacidade) {
        this.capacidade = capacidade;
        this.elementos = new Object[capacidade]; // Aloca espaço
        this.tamanho = 0;
    }

    // Adiciona no topo
    public void empilhar(T elemento) {
        if (tamanho == capacidade) throw new IllegalStateException("Pilha cheia");
        elementos[tamanho++] = elemento; // Posiciona e incrementa
    }

    // Remove do topo
    @SuppressWarnings("unchecked")
    public T desempilhar() {
        if (estaVazia()) throw new IllegalStateException("Pilha vazia");
        return (T) elementos[--tamanho]; // Decrementa antes de acessar
    }

    // Espia o topo sem remover
    @SuppressWarnings("unchecked")
    public T topo() {
        if (estaVazia()) throw new IllegalStateException("Pilha vazia");
        return (T) elementos[tamanho - 1]; // Acessa sem modificar tamanho
    }

    public boolean estaVazia() { return tamanho == 0; }
    public int tamanho() { return tamanho; }
}