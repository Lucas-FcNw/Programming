public class Gato{

    String nome;
    int nascimento;
    String raca;
    String cor;
    boolean acordado;
    int tamanho; // em centímetros
    double peso;    
    //construtor
    public Gato(String nome, int nasc, String raca, String cor, 
                   boolean acordado, int tamanho, double peso) {
        
        this.nome = nome;
        this.nascimento = nasc;
        this.raca = raca;
        this.cor = cor;
        this.acordado = acordado;
        this.tamanho = tamanho;
        this.peso = peso;
    }
    
    public Gato(String string, int i, String string2, String string3, boolean b, int j, double d, int k) {
        this.nome = "sem nome";
        this.raca = "não definida";
    }
    
    //métodos
    
    
    public String toString() {
        String s;
        s = "Nome = " + this.nome 
        + "\nRaça = " + this.raca
		+ "\nNascimento = " + this.nascimento
		+ "\nAcordado = " + this.acordado;
		
		return s;
    }
    
    public void acordar() {
        acordado = true;
    }
    public void dormir() {
        acordado = false;
    }

    public void latir() {
        System.out.println("Miau Miau Miau Caralho!!");
    }
}
