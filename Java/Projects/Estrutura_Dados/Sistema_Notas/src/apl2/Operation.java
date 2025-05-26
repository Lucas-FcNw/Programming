
package apl2;

public class Operation {
    public static DLinkedList map(final LinkedListOriginal original) {
        DLinkedList list = new DLinkedList();
        NodeOriginal current = original.getHead();
        while (current != null) {
            String id = String.format("25.S1-%03d", current.getId());
            String nome = current.getNome();
            int inteiro = current.getInteiro();
            int decimo = current.getDecimo();

            float nota = (inteiro == -1 || decimo == -1) ? 99.9f : Float.parseFloat(inteiro + "." + decimo);

            list.append(id, nome, nota);
            current = current.getNext();
        }
        return list;
    }

    public static DLinkedList filterRemoveNonGraded(final DLinkedList data) {
        DLinkedList result = new DLinkedList();
        Node current = data.getHead();
        while (current != null) {
            if (current.getNota() != 99.9f) {
                result.append(current.getId(), current.getNome(), current.getNota());
            }
            current = current.getNext();
        }
        return result;
    }

    public static DLinkedList filterRemoveGraded(final DLinkedList data) {
        DLinkedList result = new DLinkedList();
        Node current = data.getHead();
        while (current != null) {
            if (current.getNota() == 99.9f) {
                result.append(current.getId(), current.getNome(), current.getNota());
            }
            current = current.getNext();
        }
        return result;
    }

    public static DLinkedList filterRemoveBelowAverage(final DLinkedList data, float average) {
        DLinkedList result = new DLinkedList();
        Node current = data.getHead();
        while (current != null) {
            if (current.getNota() > average) {
                result.append(current.getId(), current.getNome(), current.getNota());
            }
            current = current.getNext();
        }
        return result;
    }

    public static float reduce(final DLinkedList data) {
        Node current = data.getHead();
        float soma = 0;
        int quantidade = 0;
        while (current != null) {
            soma += current.getNota();
            quantidade++;
            current = current.getNext();
        }
        return quantidade == 0 ? 0 : soma / quantidade;
    }

    public static String mapToString(final DLinkedList data) {
        StringBuilder sb = new StringBuilder();
        Node current = data.getHead();
        while (current != null) {
            sb.append(current.toString()).append("\n");
            current = current.getNext();
        }
        return sb.toString();
    }
}
