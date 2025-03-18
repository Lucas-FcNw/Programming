public class App {
    public static void main(String[] args) {
        Stack stack = new Stack();
        
        // Adicionando elementos à pilha
        stack.push(10);
        stack.push(20);
        stack.push(30);
        if (!stack.push(40)) {
            System.out.println("Pilha cheia! Não foi possível adicionar o elemento.");
        }
        // Exibindo os elementos da pilha
    }
}
