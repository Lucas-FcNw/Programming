// Lucas Fernandes 10419400
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

#define PBM_CODE_SIZE 3
#define MAX_LINE_SIZE 1024

typedef struct {
    int width;
    int height;
    int *pixels;
} Image;

// Declarações de funções
void help();
void manual();
void file();
void read_file();
bool is_pbm_file(FILE *image_file);
Image read_binary_image(const char path[]);
bool is_uniform(Image image, int start_row, int end_row, int start_col, int end_col);
void encode(Image image, int start_row, int end_row, int start_col, int end_col, char *code);

int main() {
    int option;

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

        switch (option) {
            case 1:
                help();
                break;
            case 2:
                manual();
                break;
            case 3:
                file();
                break;
            case 4:
                read_file();
                break;
            case 0:
                printf("Saindo...\n");
                break;
            default:
                printf("Opção inválida! Tente novamente.\n");
        }
    } while (option != 0);

    return 0;
}

void help() {
    puts("Uso: ImageEncoder [-? | -m | -f ARQ]");
    puts("Codifica imagens binárias dadas em arquivos PBM ou por dados informados manualmente.");
    puts("Opções do menu:");
    puts("1 - Apresenta esta ajuda.");
    puts("2 - Ativa o modo de entrada manual.");
    puts("3 - Processa um arquivo PBM informado pelo usuário.");
    puts("4 - Exibe o conteúdo de um arquivo informado pelo usuário.");
    puts("0 - Encerra o programa.");
}

void manual() {
    Image img;
    img.width = 0;
    img.height = 0;
    img.pixels = NULL;

    printf("Informe a largura e a altura da imagem: ");
    scanf("%d %d", &img.width, &img.height);

    img.pixels = (int *)malloc(img.width * img.height * sizeof(int));

    printf("Informe os pixels da imagem (linha por linha):\n");
    for (int i = 0; i < img.height; ++i) {
        char line[MAX_LINE_SIZE];
        scanf(" %[^\n]", line);

        char *token = strtok(line, " ");
        int j = 0;

        while (token != NULL && j < img.width) {
            img.pixels[i * img.width + j] = atoi(token);
            token = strtok(NULL, " ");
            j++;
        }
    }

    char *code = (char *)malloc(sizeof(char));
    code[0] = '\0';
    encode(img, 0, img.height - 1, 0, img.width - 1, code);
    printf("Código gerado: %s\n", code);

    free(code);
    free(img.pixels);
}

void file() {
    char path[MAX_LINE_SIZE];
    printf("Informe o caminho do arquivo PBM: ");
    scanf(" %[^\n]", path);

    Image img = read_binary_image(path);

    char *code = (char *)malloc(sizeof(char));
    code[0] = '\0';
    encode(img, 0, img.height - 1, 0, img.width - 1, code);
    printf("Código gerado: %s\n", code);

    free(code);
    free(img.pixels);
}

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

bool is_pbm_file(FILE *image_file) {
    char magic_number[PBM_CODE_SIZE];
    fscanf(image_file, "%2s", magic_number);
    return strcmp(magic_number, "P1") == 0;
}

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

    int break_char;
    while ((break_char = fgetc(image_file)) == '#' || isspace(break_char)) {
        if (break_char == '#') {
            fscanf(image_file, "%*[^\n]");
        }
    }
    ungetc(break_char, image_file);

    if (fscanf(image_file, "%d %d", &img.width, &img.height) != 2) {
        fprintf(stderr, "Erro ao ler largura e altura.\n");
        fclose(image_file);
        exit(EXIT_FAILURE);
    }

    img.pixels = (int *)malloc(img.width * img.height * sizeof(int));

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

void encode(Image image, int start_row, int end_row, int start_col, int end_col, char *code) {
    if (start_row > end_row || start_col > end_col) {
        return;
    }

    code = realloc(code, strlen(code) + 2);

    if (is_uniform(image, start_row, end_row, start_col, end_col)) {
        int first_pixel = image.pixels[start_row * image.width + start_col];
        sprintf(code, "%s%c", code, (first_pixel == 0) ? 'B' : 'P');
    } else {
        sprintf(code, "%sX", code);

        int mid_row = (start_row + end_row) / 2;
        int mid_col = (start_col + end_col) / 2;

        encode(image, start_row, mid_row, start_col, mid_col, code);
        encode(image, start_row, mid_row, mid_col + 1, end_col, code);
        encode(image, mid_row + 1, end_row, start_col, mid_col, code);
        encode(image, mid_row + 1, end_row, mid_col + 1, end_col, code);
    }
}
