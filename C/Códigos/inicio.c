
#include <stdio.h>  // Biblioteca padrão para funções de entrada e saída (printf, scanf, etc.)
#include <stdlib.h> // Biblioteca para gerenciamento de memória e utilitários do sistema

/**
 * @file inicio.c
 * @brief Programa introdutório demonstrando a estrutura básica da linguagem C,
 *        saída de texto e declaração correta de tipos de dados primitivos.
 */

int main(void)
{
    // Exibição de mensagem inicial
    printf("Hello, World!\n\n");

    printf("=== Exemplo de Declaração de Variáveis em C ===\n");

    // Declaração de variáveis dos tipos fundamentais em C:
    char caractere = 'A';                // Tipo caractere (1 byte)
    int inteiro = 42;                    // Tipo número inteiro (geralmente 4 bytes)
    float decimal_simples = 3.14f;       // Tipo ponto flutuante de precisão simples (~6-7 dígitos)
    double decimal_duplo = 3.1415926535; // Tipo ponto flutuante de precisão dupla (~15-17 dígitos)

    // Exibindo os valores no terminal
    printf("Caractere (char): %c\n", caractere);
    printf("Inteiro (int): %d\n", inteiro);
    printf("Ponto Flutuante (float): %.2f\n", decimal_simples);
    printf("Precisão Dupla (double): %.10lf\n", decimal_duplo);

    // Regras de nomeação em C:
    // 1. Não usar palavras reservadas da linguagem (ex: int, char, return).
    // 2. Os nomes podem conter letras, números e underscores (_), mas devem iniciar com letra ou '_'.
    // 3. A linguagem C é case-sensitive (diferencia maiúsculas e minúsculas).

    return 0;
}
