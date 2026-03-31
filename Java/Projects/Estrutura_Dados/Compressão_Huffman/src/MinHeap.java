import java.util.ArrayList;
import java.util.List;

/**
 * Integrantes do grupo:
 * - Lucas Fernandes de Camargo (10419400)
 * - Rafael Lima (10425819)
 */
class MinHeap {
    private final ArrayList<No> heap = new ArrayList<>();

    void inserir(No no) {
        heap.add(no);
        subir(heap.size() - 1);
    }

    No extrairMin() {
        if (heap.isEmpty()) {
            return null;
        }
        No min = heap.get(0);
        No ultimo = heap.remove(heap.size() - 1);
        if (!heap.isEmpty()) {
            heap.set(0, ultimo);
            descer(0);
        }
        return min;
    }

    int tamanho() {
        return heap.size();
    }

    List<No> snapshot() {
        return new ArrayList<>(heap);
    }

    private void subir(int i) {
        while (i > 0) {
            int pai = (i - 1) / 2;
            if (heap.get(i).compareTo(heap.get(pai)) >= 0) {
                break;
            }
            trocar(i, pai);
            i = pai;
        }
    }

    private void descer(int i) {
        int n = heap.size();
        while (true) {
            int esq = 2 * i + 1;
            int dir = 2 * i + 2;
            int menor = i;

            if (esq < n && heap.get(esq).compareTo(heap.get(menor)) < 0) {
                menor = esq;
            }
            if (dir < n && heap.get(dir).compareTo(heap.get(menor)) < 0) {
                menor = dir;
            }
            if (menor == i) {
                break;
            }
            trocar(i, menor);
            i = menor;
        }
    }

    private void trocar(int i, int j) {
        No tmp = heap.get(i);
        heap.set(i, heap.get(j));
        heap.set(j, tmp);
    }
}