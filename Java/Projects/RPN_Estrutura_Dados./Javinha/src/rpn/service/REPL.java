/*
 * Caio Henrique Santos Carvalho RA: 10425408
 * Diogo Fassina Garcia - RA: 10417030
 * Rafael de Souza Alves de Lima RA: 10425819
 * Lucas Fernandes de Camargo RA: 10419400
 *
 * */




package rpn.service;

import java.util.Scanner;
import rpn.model.ConversorInfixoParaPosfixo;

// """GRUB""" da calculadora
public class REPL {
    private static final String COMANDO_VARS = "VARS";   // Lista variáveis
    private static final String COMANDO_RESET = "RESET"; // Limpa variáveis
    private static final String COMANDO_EXIT = "EXIT";   // Meio auto explicativo né

    private final AvaliadorPosfixo avaliador;
    private final Scanner scanner;

    public REPL() {
        this.avaliador = new AvaliadorPosfixo();
        this.scanner = new Scanner(System.in);
    }

    // Loop principal
    public void iniciar() {
        System.out.println("Calculadora de Expressões (digite EXIT para sair)");

        while (true) {
            System.out.print("> ");
            String entrada = scanner.nextLine().trim();
            if (entrada.isEmpty()) continue; // Ignora partes vazias

            try {
                if (entrada.equalsIgnoreCase(COMANDO_EXIT)) break;
                else if (entrada.equalsIgnoreCase(COMANDO_VARS)) exibirVariaveis();
                else if (entrada.equalsIgnoreCase(COMANDO_RESET)) {
                    avaliador.reset();
                    System.out.println("Variáveis reiniciadas.");
                }
                else if (isAtribuicaoValida(entrada)) processarAtribuicao(entrada);
                else processarExpressao(entrada); // Se não for 1 dos  comandos do topo vai ler como expressão
            }
            catch (Exception e) {
                System.out.println("Erro: " + e.getMessage());
            }
        }

        scanner.close();
        System.out.println("Programa encerrado.");
    }


    private boolean isAtribuicaoValida(String entrada) {
        String[] partes = entrada.split("\\s*=\\s*"); // Permite espaços
        if (partes.length != 2) return false;
        // Verifica se 1 letra = 1 numero
        return partes[0].length() == 1 &&
                Character.isLetter(partes[0].charAt(0)) &&
                isNumeroValido(partes[1]);
    }

    private boolean isNumeroValido(String str) {
        try {
            Double.parseDouble(str);
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }


    private void exibirVariaveis() {
        String[] vars = avaliador.listarVariaveis(); // EX: A = 1
        if (vars.length == 0) System.out.println("Nenhuma variável definida.");
        else for (String var : vars) System.out.println(var);
    }


    private void processarAtribuicao(String entrada) {
        String[] partes = entrada.split("\\s*=\\s*");
        char var = partes[0].charAt(0);
        double valor = Double.parseDouble(partes[1]);
        avaliador.definirVariavel(var, valor);
        System.out.printf("%c = %.2f%n", Character.toUpperCase(var), valor);
    }

    // Converte e processa as infixas
    private void processarExpressao(String entrada) {
        String posfixa = ConversorInfixoParaPosfixo.converter(entrada);
        double resultado = avaliador.avaliar(posfixa);
        System.out.println(resultado);
    }
}