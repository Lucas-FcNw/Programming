/*
 * Caio Henrique Santos Carvalho RA: 10425408
 * Diogo Fassina Garcia - RA: 10417030
 * Rafael de Souza Alves de Lima RA: 10425819
 * Lucas Fernandes de Camargo RA: 10419400
 *
 * */



package rpn.util;


public class ValidadorExpressao {
    // Checa se os parenteses estão certos.
    public static boolean validarParenteses(String expressao) {
        int balanceamento = 0;
        for (char c : expressao.toCharArray()) {
            if (c == '(') balanceamento++;
            else if (c == ')') {
                balanceamento--;
                if (balanceamento < 0) return false; // Fecha sem abrir
            }
        }
        return balanceamento == 0; // True se todos estiverem corretos(fechados)
    }


    public static boolean validarCaracteres(String expressao) {
        for (char c : expressao.toCharArray()) {
            if (!isCaracterValido(c)) return false;
        }
        return true;
    }

    private static boolean isCaracterValido(char c) {
        return Character.isLetterOrDigit(c) ||
                isOperadorValido(c) ||
                c == '(' || c == ')' ||
                c == '.' || Character.isWhitespace(c);
    }

    private static boolean isOperadorValido(char c) {
        return c == '+' || c == '-' || c == '*' || c == '/' || c == '^' || c == '=';
    }
}