
package apl2;

public class DLinkedList {
    private Node head;
    private Node tail;
    private int count;

    public DLinkedList() {
        head = null;
        tail = null;
        count = 0;
    }

    public void insert(String id, String nome, float nota) {
        Node newNode = new Node(id, nome, nota);
        if (isEmpty()) {
            head = tail = newNode;
        } else {
            newNode.setNext(head);
            head.setPrev(newNode);
            head = newNode;
        }
        count++;
    }

    public void append(String id, String nome, float nota) {
        Node newNode = new Node(id, nome, nota);
        if (isEmpty()) {
            head = tail = newNode;
        } else {
            tail.setNext(newNode);
            newNode.setPrev(tail);
            tail = newNode;
        }
        count++;
    }

    public Node removeHead() {
        if (isEmpty()) return null;
        Node removed = head;
        if (head == tail) {
            head = tail = null;
        } else {
            head = head.getNext();
            head.setPrev(null);
        }
        count--;
        return removed;
    }

    public Node removeTail() {
        if (isEmpty()) return null;
        Node removed = tail;
        if (head == tail) {
            head = tail = null;
        } else {
            tail = tail.getPrev();
            tail.setNext(null);
        }
        count--;
        return removed;
    }

    public Node removeNode(String id) {
        Node current = head;
        while (current != null) {
            if (current.getId().equals(id)) {
                if (current == head) return removeHead();
                if (current == tail) return removeTail();
                current.getPrev().setNext(current.getNext());
                current.getNext().setPrev(current.getPrev());
                count--;
                return current;
            }
            current = current.getNext();
        }
        return null;
    }

    public Node getHead() { return head; }

    public Node getTail() { return tail; }

    public Node getNode(String id) {
        Node current = head;
        while (current != null) {
            if (current.getId().equals(id)) return current;
            current = current.getNext();
        }
        return null;
    }

    public int count() { return count; }

    public boolean isEmpty() { return count == 0; }

    public void clear() {
        while (!isEmpty()) {
            removeHead();
        }
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("(").append(count).append(") \n");
        Node current = head;
        while (current != null) {
            sb.append(current.toString()).append(" -> \n");
            current = current.getNext();
        }
        sb.append("null.");
        return sb.toString();
    }
}
