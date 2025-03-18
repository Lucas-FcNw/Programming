public class Stack{
    private static final int DEFAULT_SIZE = 10;
    private int data[];
    private int count;

    //Método construtor padrão de classe
    public Stack(){
        this (DEFAULT_SIZE);
        
    }
;

    /* Construtor que recebe o tamanho do array
     e inicializa o array de inteiros */
public Stack(int size){
    count = 0;
    data = new int[size];
}

// Inserção de elemento no topo da pilha
public boolean push (int value){
    if (count == data.length){
        return false; // Pilha cheia


    }
    data[count] = value; // Adiciona o elemento no topo
    ++count; // Incrementa o contador
    return true; // Sucesso na inserção

}
// Remoção do elemento do topo da pilha
public int StackResult(){
    if (isEmpty()){
        return new StackResult(false, 0);
        
        return -1; // Pilha vazia, não há elemento para remover.
    }
    
    --count; // Decrementa o contador
    int top = data[count]; // Armazena o elemento do topo
    data[count] = 0; // Remove o elemento do topo (opcional)
    return top; // Retorna o elemento do topo
}

public boolean isFull(){
    return count == data.length; // Verifica se a pilha está cheia
}
public boolean isEmpty(){
    return count == 0; // Verifica se a pilha está vazia
    //Só funciona nessa implementação
}
}