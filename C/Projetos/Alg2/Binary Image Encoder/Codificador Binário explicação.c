#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

inclui bibliotecas padrão necessárias:
stdio.h: Para entrada e saída.
stdlib.h: Para alocação dinâmica de memória e controle de execução.
stdbool.h: Para uso de valores booleanos (true e false).
string.h: Para manipulação de strings.
ctype.h: Para verificar caracteres (como espaço em branco).


Estrutura de Dados para Imagem  
typedef struct {
    int width;   // Largura da imagem.
    int height;  // Altura da imagem.
    int *pixels; // Matriz de pixels armazenada como um array unidimensional.
} Image;



Declaração de funções

void help();
void manual();
void file();
void read_file();
bool is_pbm_file(FILE *image_file);
Image read_binary_image(const char path[]);
bool is_uniform(Image image, int start_row, int end_row, int start_col, int end_col);
void encode(Image image, int start_row, int end_row, int start_col, int end_col, char *code);
void print_help();

Declara funções para modularizar o programa, permitindo um código mais limpo em geral.


int main() {
    int option;
    // Loop principal para exibir o menu até que o usuário escolha sair.
    do {
        printf("========== Menu ==========\n");
        printf("1 - Ajuda\n");
        printf("2 - Modo manual\n");
        printf("3 - Modo arquivo\n");
        printf("4 - Ler arquivo\n");
        printf("0 - Sair\n");
        printf("==========================\n");
        printf("Escolha uma opção: ");
        scanf("%d", &option);

        // Processa a escolha do usuário.
        switch (option) {
            case 1:
                help(); // Mostra o menu de ajuda.
                break;
            case 2:
                manual(); // Entrada manual da imagem.
                break;
            case 3:
                file(); // Codificação baseada em arquivo.
                break;
            case 4:
                read_file(); // Exibição do conteúdo de um arquivo.
                break;
            case 0:
                printf("Saindo...\n");
                printf("\nTrabalho feito por Lucas Fernandes 10419400\n\n");
                break;
            default:
                printf("Opção inválida! Tente novamente.\n");
        }
    } while (option != 0);

    return 0;
}

Menu simples de navegação pelo úsuario



void help() {
    puts("\n \nCodifica imagens binárias dadas em arquivos PBM ou por dados informados manualmente.");
    puts("\nOpções do menu:");
    puts("1 - Ajuda: Apresenta esta ajuda.");
    puts("2 - Modo manual: Ativa o modo de entrada manual, em que o usuário fornece todos os dados da imagem informando-os através do teclado.");
    puts("3 - Modo arquivo: Processa um arquivo PBM informado pelo usuário.");
    puts("4 - Ler arquivo: Exibe o conteúdo de um arquivo informado pelo usuário.");
    puts("0 - Sair: Encerra o programa.");
    puts("\n==========================\n");
}


Apenas um menu com maior detalhamento.

void manual() {
    // Inicializa a estrutura de imagem.
    Image img;
    img.width = 0;
    img.height = 0;
    img.pixels = NULL;

    // Obtém dimensões e pixels manualmente do usuário.
    printf("Informe a largura e a altura da imagem: ");
    scanf("%d %d", &img.width, &img.height);
    img.pixels = (int *)malloc(img.width * img.height * sizeof(int));

    printf("Informe os pixels da imagem (linha por linha):\n");
    for (int i = 0; i < img.height; ++i) {
        char line[MAX_LINE_SIZE];
        scanf(" %[^\n]", line);

        // Divide os valores da linha para preencher a matriz.
        char *token = strtok(line, " ");
        int j = 0;
        while (token != NULL && j < img.width) {
            img.pixels[i * img.width + j] = atoi(token);
            token = strtok(NULL, " ");
            j++;
        }
    }

    // Gera o código de compressão da imagem.
    char *code = (char *)malloc(sizeof(char));
    code[0] = '\0';
    encode(img, 0, img.height - 1, 0, img.width - 1, code);
    printf("Código gerado: %s\n", code);

    free(code);
    free(img.pixels); // Libera a memória alocada.
}

Essa é a MAIN


Função FILE uma das mais importantes

void file() {
    char path[MAX_LINE_SIZE];
    printf("Informe o caminho do arquivo PBM: ");
    scanf(" %[^\n]", path);

    // Lê a imagem do arquivo.
    Image img = read_binary_image(path);

    // Gera e exibe o código.
    char *code = (char *)malloc(sizeof(char));
    code[0] = '\0';
    encode(img, 0, img.height - 1, 0, img.width - 1, code);
    printf("Código gerado: %s\n", code);

    free(code);
    free(img.pixels);
}

É aqui que é feito a mágica da identificação e abertura e leitura de arquivos no formato PBM

Funções Auxiliares
is_pbm_file: Verifica se o arquivo é um PBM válido.
read_binary_image: Lê e processa uma imagem em formato PBM.
is_uniform: Verifica se uma submatriz de pixels é uniforme.
encode: Gera o código de compressão recursivamente.


Verificação da matriz e o passo a passo para a codificação

 (is_uniform(image, start_row, end_row, start_col, end_col)) {
        int first_pixel = image.pixels[start_row * image.width + start_col];
        sprintf(code, "%s%c", code, (first_pixel == 0) ? 'B' : 'P');
    } else {
        strcat(code, "D");

        int mid_row = (start_row + end_row) / 2;
        int mid_col = (start_col + end_col) / 2;

        encode(image, start_row, mid_row, start_col, mid_col, code);
        encode(image, start_row, mid_row, mid_col + 1, end_col, code);
        encode(image, mid_row + 1, end_row, start_col, mid_col, code);
        encode(image, mid_row + 1, end_row, mid_col + 1, end_col, code);
    }
}

