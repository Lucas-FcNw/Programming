// Interface genérica para estruturas de dados
interface Estrutura<T> {
    void adicionar(T elemento);
    T remover();
    T topo();
    boolean estaVazia();
    int tamanho();
}

// Classe genérica Stack com encapsulamento
class Pilha<T> implements Estrutura<T> {
    private Node<T> topo;
    private int tamanho;
    
    private static class Node<T> {
        T dado;
        Node<T> proximo;
        
        Node(T dado) {
            this.dado = dado;
        }
    }
    
    public Pilha() {
        this.topo = null;
        this.tamanho = 0;
    }
    
    @Override
    public void adicionar(T elemento) {
        Node<T> novoNode = new Node<>(elemento);
        novoNode.proximo = topo;
        topo = novoNode;
        tamanho++;
    }
    
    @Override
    public T remover() {
        if (estaVazia()) {
            throw new IllegalStateException("Pilha vazia!");
        }
        T dado = topo.dado;
        topo = topo.proximo;
        tamanho--;
        return dado;
    }
    
    @Override
    public T topo() {
        if (estaVazia()) {
            throw new IllegalStateException("Pilha vazia!");
        }
        return topo.dado;
    }
    
    @Override
    public boolean estaVazia() {
        return tamanho == 0;
    }
    
    @Override
    public int tamanho() {
        return tamanho;
    }
}

// Classe com exemplo de uso
public class Revisao {
    public static void main(String[] args) {
        Pilha<Integer> pilhaNumeros = new Pilha<>();
        
        pilhaNumeros.adicionar(10);
        pilhaNumeros.adicionar(20);
        pilhaNumeros.adicionar(30);
        
        System.out.println("Topo: " + pilhaNumeros.topo());
        System.out.println("Tamanho: " + pilhaNumeros.tamanho());
        System.out.println("Removido: " + pilhaNumeros.remover());
        System.out.println("Nova pilha: " + pilhaNumeros.tamanho());
    }
}