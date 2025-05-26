

package apl2;

public class Node {
    private String id;
    private String nome;
    private float nota;
    private Node prev;
    private Node next;

    public Node(String id, String nome, float nota) {
        this.id = id;
        this.nome = nome;
        this.nota = nota;
        this.prev = null;
        this.next = null;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getNome() { return nome; }
    public void setNome(String nome) { this.nome = nome; }

    public float getNota() { return nota; }
    public void setNota(float nota) { this.nota = nota; }

    public Node getPrev() { return prev; }
    public void setPrev(Node prev) { this.prev = prev; }

    public Node getNext() { return next; }
    public void setNext(Node next) { this.next = next; }

    @Override
    public String toString() {
        return id + ";" + nome + ";" + nota;
    }
}
