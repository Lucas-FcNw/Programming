// 2. Fundamentos de Programação Orientada a Objetos (POO)

// Conceitos de POO:
// Encapsulamento: É o princípio de esconder os detalhes internos de um objeto e expor apenas o que é necessário.
// Exemplo:
class Retangulo {
    private double largura; // Atributo privado para encapsulamento
    private double altura;

    // Construtor para inicializar os atributos
    public Retangulo(double largura, double altura) {
        this.largura = largura;
        this.altura = altura;
    }

    // Método público para calcular a área do retângulo
    public double calcularArea() {
        return largura * altura;
    }

    // Métodos públicos para acessar e modificar os atributos privados
    public double getLargura() {
        return largura;
    }

    public void setLargura(double largura) {
        this.largura = largura;
    }

    public double getAltura() {
        return altura;
    }

    public void setAltura(double altura) {
        this.altura = altura;
    }
}
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
// Classe PilhaStrings para armazenar strings
class PilhaStrings {
    private String[] elementos; // Array para armazenar os elementos da pilha
    private int topo; // Índice do topo da pilha

    // Construtor para inicializar a pilha com uma capacidade específica
    public PilhaStrings(int capacidade) {
        elementos = new String[capacidade]; // Cria o array com a capacidade fornecida
        topo = -1; // Inicializa o topo como -1, indicando que a pilha está vazia
    }

    // Método para adicionar um elemento à pilha
    public void push(String elemento) {
        if (topo == elementos.length - 1) { // Verifica se a pilha está cheia
            throw new StackOverflowError("Pilha cheia"); // Lança uma exceção se a pilha estiver cheia
        }
        elementos[++topo] = elemento; // Incrementa o topo e adiciona o elemento
    }

    // Método para remover e retornar o elemento no topo da pilha
    public String pop() {
        if (isEmpty()) { // Verifica se a pilha está vazia
            throw new IllegalStateException("Pilha vazia"); // Lança uma exceção se a pilha estiver vazia
        }
        return elementos[topo--]; // Retorna o elemento no topo e decrementa o índice do topo
    }

    // Método para visualizar o elemento no topo da pilha sem removê-lo
    public String peek() {
        if (isEmpty()) { // Verifica se a pilha está vazia
            throw new IllegalStateException("Pilha vazia"); // Lança uma exceção se a pilha estiver vazia
        }
        return elementos[topo]; // Retorna o elemento no topo sem removê-lo
    }

    // Método para verificar se a pilha está vazia
    public boolean isEmpty() {
        return topo == -1; // Retorna true se o topo for -1, indicando que a pilha está vazia
    }
}
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