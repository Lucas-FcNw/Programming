// Lucas Fernandes 10419400

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

// Define constantes para facilitar a leitura e manipulação de dados.
#define PBM_CODE_SIZE 3       // Tamanho do código mágico "P1" para arquivos PBM.
#define MAX_LINE_SIZE 1024    // Tamanho máximo de uma linha de entrada/arquivo.

// Estrutura para armazenar informações sobre a imagem.
typedef struct {
    int width;   // Largura da imagem.
    int height;  // Altura da imagem.
    int *pixels; // Matriz de pixels armazenada como um array unidimensional.
} Image;

// Declarações de funções para modularizar o programa.
void help(); 
void manual();
void file();
void read_file();
bool is_pbm_file(FILE *image_file);
Image read_binary_image(const char path[]);
bool is_uniform(Image image, int start_row, int end_row, int start_col, int end_col);
void encode(Image image, int start_row, int end_row, int start_col, int end_col, char *code);

// Função principal que exibe o menu e gerencia o fluxo do programa.
int main() {
    int option;

    do {
        // Exibe o menu principal.
        printf("========== Menu ==========\n");
        printf("1 - Ajuda\n");
        printf("2 - Modo manual\n");
        printf("3 - Modo arquivo\n");
        printf("4 - Ler arquivo\n");
        printf("0 - Sair\n");
        printf("==========================\n");
        printf("Escolha uma opção: ");
        scanf("%d", &option);

        // Gerencia a escolha do usuário.
        switch (option) {
            case 1:
                help(); // Exibe informações de ajuda.
                break;
            case 2:
                manual(); // Permite entrada manual dos dados da imagem.
                break;
            case 3:
                file(); // Processa um arquivo PBM para gerar o código.
                break;
            case 4:
                read_file(); // Lê e exibe o conteúdo de um arquivo.
                break;
            case 0:
                printf("Saindo...\n");
                printf("\nTrabalho feito por Lucas Fernandes 10419400\n\n");
                break;
            default:
                printf("Opção inválida! Tente novamente.\n");
        }
    } while (option != 0); // Continua exibindo o menu até que o usuário escolha sair.

    return 0;
}

// Exibe o menu de ajuda com descrições detalhadas.
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

// Permite ao usuário fornecer manualmente os dados da imagem.
void manual() {
    // Inicializa uma estrutura de imagem.
    Image img;
    img.width = 0;
    img.height = 0;
    img.pixels = NULL;

    // Obtém as dimensões da imagem.
    printf("Informe a largura e a altura da imagem: ");
    scanf("%d %d", &img.width, &img.height);

    // Aloca memória para a matriz de pixels.
    img.pixels = (int *)malloc(img.width * img.height * sizeof(int));

    // Solicita ao usuário que informe os pixels linha por linha.
    printf("Informe os pixels da imagem (linha por linha):\n");
    for (int i = 0; i < img.height; ++i) {
        char line[MAX_LINE_SIZE];
        scanf(" %[^\n]", line);

        // Divide a linha em tokens para preencher a matriz.
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

    // Libera memória alocada.
    free(code);
    free(img.pixels);
}

// Lê uma imagem a partir de um arquivo PBM e gera o código correspondente.
void file() {
    char path[MAX_LINE_SIZE];
    printf("Informe o caminho do arquivo PBM: ");
    scanf(" %[^\n]", path);

    // Lê a imagem do arquivo.
    Image img = read_binary_image(path);

    // Gera o código de compressão.
    char *code = (char *)malloc(sizeof(char));
    code[0] = '\0';
    encode(img, 0, img.height - 1, 0, img.width - 1, code);
    printf("Código gerado: %s\n", code);

    // Libera memória alocada.
    free(code);
    free(img.pixels);
}

// Lê e exibe o conteúdo de um arquivo qualquer.
void read_file() {
    char path[MAX_LINE_SIZE];
    printf("Informe o caminho do arquivo: ");
    scanf(" %[^\n]", path);

    FILE *file = fopen(path, "r");
    if (file == NULL) {
        perror("Erro ao abrir o arquivo");
        return;
    }

    printf("Conteúdo do arquivo:\n");
    char line[MAX_LINE_SIZE];
    while (fgets(line, sizeof(line), file) != NULL) {
        printf("%s", line);
    }

    fclose(file);
}

// Verifica se o arquivo fornecido é um arquivo PBM válido.
bool is_pbm_file(FILE *image_file) {
    char magic_number[PBM_CODE_SIZE];
    fscanf(image_file, "%2s", magic_number);
    return strcmp(magic_number, "P1") == 0;
}

// Lê e processa uma imagem em formato PBM.
Image read_binary_image(const char path[]) {
    FILE *image_file = fopen(path, "r");

    if (image_file == NULL) {
        perror("Erro ao abrir o arquivo");
        exit(EXIT_FAILURE);
    }

    Image img;
    img.width = 0;
    img.height = 0;
    img.pixels = NULL;

    if (!is_pbm_file(image_file)) {
        fprintf(stderr, "Formato PBM inválido\n");
        fclose(image_file);
        exit(EXIT_FAILURE);
    }

    // Ignora comentários no cabeçalho do arquivo.
    int break_char;
    while ((break_char = fgetc(image_file)) == '#' || isspace(break_char)) {
        if (break_char == '#') {
            fscanf(image_file, "%*[^\n]");
        }
    }
    ungetc(break_char, image_file);

    // Lê dimensões da imagem.
    if (fscanf(image_file, "%d %d", &img.width, &img.height) != 2) {
        fprintf(stderr, "Erro ao ler largura e altura.\n");
        fclose(image_file);
        exit(EXIT_FAILURE);
    }

    // Aloca memória para armazenar os pixels.
    img.pixels = (int *)malloc(img.width * img.height * sizeof(int));

    // Lê os valores dos pixels.
    for (int i = 0; i < img.height; ++i) {
        for (int j = 0; j < img.width; ++j) {
            int pixel;
            fscanf(image_file, "%d", &pixel);
            img.pixels[i * img.width + j] = pixel;
        }
    }

    fclose(image_file);
    return img;
}

// Verifica se uma submatriz de pixels é uniforme.
bool is_uniform(Image image, int start_row, int end_row, int start_col, int end_col) {
    bool uniform = true;
    int first_pixel = image.pixels[start_row * image.width + start_col];

    for (int i = start_row; i <= end_row; ++i) {
        for (int j = start_col; j <= end_col; ++j) {
            if (image.pixels[i * image.width + j] != first_pixel) {
                uniform = false;
                break;
            }
        }

        if (!uniform) {
            break;
        }
    }

    return uniform;
}

// Gera o código de compressão da imagem recursivamente.
void encode(Image image, int start_row, int end_row, int start_col, int end_col, char *code) {
    if (start_row > end_row || start_col > end_col) {
        return;
    }

    code = realloc(code, strlen(code) + 2);

    if (is_uniform(image, start_row, end_row, start_col, end_col)) {
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
