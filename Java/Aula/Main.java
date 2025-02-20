
public class Main{
	public static void main(String[] args) {
	    
	    Gato meuPet = new Gato("Gato", 2025, "Vira lata", "laranja", true, 15, 0.5, 5);
	    
		System.out.println(meuPet);
		System.out.println("------------------");
		
		System.out.println("Dados do meuPet:\n");
		System.out.println("Nome = " + meuPet.nome);
		System.out.println("Raça = " + meuPet.raca);
		System.out.println("Nascimento = " + meuPet.nascimento);
		System.out.println("Acordado = " + meuPet.acordado); 
	
		
		
		
	}
}