// 2. Fundamentos de Programação Orientada a Objetos (POO)

// Conceitos de POO:

/*Abstração: É o processo de ocultar os detalhes de implementação e mostrar apenas a funcionalidade essencial de um objeto.
 Exemplo: */
class Pessoa {
    private String nome; // Modificador de acesso 'private' para encapsulamento
    private int idade;

    // Construtor: Método especial usado para inicializar objetos
    public Pessoa(String nome, int idade) {
        this.nome = nome;
        this.idade = idade;
    }

    // Métodos públicos para acessar os atributos privados
    public String getNome() {
        return nome;
    }

    public int getIdade() {
        return idade;
    }
}

// Exercícios de POO/Java:
// 1. Crie uma classe "Carro" com atributos privados, construtor e métodos para acessar os atributos.
// 2. Implemente uma classe "ContaBancaria" com métodos para depósito e saque.

// 3. Tipos Abstratos de Dados (TAD)

// a. Pilhas
// TAD Pilha sequencial:
class Pilha {
    private int[] elementos;
    private int topo;

    public Pilha(int capacidade) {
        elementos = new int[capacidade];
        topo = -1;
    }

    public void push(int elemento) {
        if (topo == elementos.length - 1) {
            throw new StackOverflowError("Pilha cheia");
        }
        elementos[++topo] = elemento;
    }

    public int pop() {
        if (isEmpty()) {
            throw new IllegalStateException("Pilha vazia");
        }
        return elementos[topo--];
    }

    public boolean isEmpty() {
        return topo == -1;
    }
}

// Exercícios POO/Java aplicados a TAD Pilha sequencial:
// 1. Implemente uma pilha que armazene strings.
// 2. Adicione um método para visualizar o elemento no topo da pilha sem removê-lo.

// TAD Pilha sequencial genérica:
class PilhaGenerica<T> {
    private T[] elementos;
    private int topo;

    @SuppressWarnings("unchecked")
    public PilhaGenerica(int capacidade) {
        elementos = (T[]) new Object[capacidade];
        topo = -1;
    }

    public void push(T elemento) {
        if (topo == elementos.length - 1) {
            throw new StackOverflowError("Pilha cheia");
        }
        elementos[++topo] = elemento;
    }

    public T pop() {
        if (isEmpty()) {
            throw new IllegalStateException("Pilha vazia");
        }
        return elementos[topo--];
    }

    public boolean isEmpty() {
        return topo == -1;
    }
}

// b. Filas
// TAD Fila sequencial:
class Fila {
    private int[] elementos;
    private int inicio, fim, tamanho;

    public Fila(int capacidade) {
        elementos = new int[capacidade];
        inicio = fim = tamanho = 0;
    }

    public void enqueue(int elemento) {
        if (tamanho == elementos.length) {
            throw new IllegalStateException("Fila cheia");
        }
        elementos[fim] = elemento;
        fim = (fim + 1) % elementos.length;
        tamanho++;
    }

    public int dequeue() {
        if (isEmpty()) {
            throw new IllegalStateException("Fila vazia");
        }
        int elemento = elementos[inicio];
        inicio = (inicio + 1) % elementos.length;
        tamanho--;
        return elemento;
    }

    public boolean isEmpty() {
        return tamanho == 0;
    }
}

// c. Listas Encadeadas
// TAD Lista encadeada:
class Nodo {
    int dado;
    Nodo proximo;

    public Nodo(int dado) {
        this.dado = dado;
        this.proximo = null;
    }
}

class ListaEncadeada {
    private Nodo cabeca;

    public void adicionar(int dado) {
        Nodo novoNodo = new Nodo(dado);
        if (cabeca == null) {
            cabeca = novoNodo;
        } else {
            Nodo atual = cabeca;
            while (atual.proximo != null) {
                atual = atual.proximo;
            }
            atual.proximo = novoNodo;
        }
    }

    public void imprimir() {
        Nodo atual = cabeca;
        while (atual != null) {
            System.out.print(atual.dado + " ");
            atual = atual.proximo;
        }
        System.out.println();
    }
}

// Exercícios:
// 1. Implemente métodos para remover um elemento da lista encadeada.
// 2. Adicione um método para buscar um elemento na lista encadeada.

// TAD Lista encadeada circular:
class ListaEncadeadaCircular {
    private Nodo cabeca;

    public void adicionar(int dado) {
        Nodo novoNodo = new Nodo(dado);
        if (cabeca == null) {
            cabeca = novoNodo;
            cabeca.proximo = cabeca;
        } else {
            Nodo atual = cabeca;
            while (atual.proximo != cabeca) {
                atual = atual.proximo;
            }
            atual.proximo = novoNodo;
            novoNodo.proximo = cabeca;
        }
    }

    public void imprimir() {
        if (cabeca == null) return;
        Nodo atual = cabeca;
        do {
            System.out.print(atual.dado + " ");
            atual = atual.proximo;
        } while (atual != cabeca);
        System.out.println();
    }
}

// Exercícios:
// 1. Implemente métodos para remover um elemento da lista encadeada circular.
// 2. Adicione um método para verificar se a lista está vazia.