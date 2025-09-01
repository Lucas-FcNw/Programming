public class StackResult {
    public static void main(String[] args) {
        Stack stack = new Stack();
        
        // Adicionando elementos à pilha
        stack.push(10);
        stack.push(20);
        stack.push(30);
        
        // Tentando adicionar um elemento a uma pilha cheia
        if (!stack.push(40)) {
            System.out.println("Pilha cheia! Não foi possível adicionar o elemento.");
        }
        
        // Exibindo os elementos da pilha
        while (!stack.isEmpty()) {
            System.out.println("Elemento removido: " + stack.pop());
        }
    }
}