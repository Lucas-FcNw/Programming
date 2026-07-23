/**
 * @file codificador_bin.c
 * @brief Codificador de Imagens Binárias usando Decomposição em Quadtree (PBM P1).
 *
 * Este programa realiza a compressão espacial de imagens binárias no formato
 * PBM (Portable Bitmap - P1) ou inseridas manualmente, utilizando uma estrutura
 * recursiva baseada em Quadtree (decomposição em quatro quadrantes).
 *
 * Simbologia do Código Gerado:
 * - 'B': Região uniforme de cor branca (valor 0).
 * - 'P': Região uniforme de cor preta (valor 1).
 * - 'X': Região não-uniforme (dividida recursivamente em 4 subquadrantes).
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

#define MAX_LINE_SIZE 1024
#define PBM_CODE_SIZE 3

/**
 * @brief Estrutura para representação de imagem binária.
 */
typedef struct {
    int width;   /**< Largura em pixels */
    int height;  /**< Altura em pixels */
    int *pixels; /**< Matriz de pixels em representação unidimensional */
} Image;

/**
 * @brief Buffer dinâmico de string para acúmulo eficiente e seguro do código gerado.
 */
typedef struct {
    char *data;
    size_t length;
    size_t capacity;
} StringBuffer;

/**
 * @brief Inicializa o buffer dinâmico de string.
 */
static StringBuffer *sb_create(void) {
    StringBuffer *sb = (StringBuffer *)malloc(sizeof(StringBuffer));
    if (!sb) {
        perror("Erro ao alocar StringBuffer");
        exit(EXIT_FAILURE);
    }
    sb->capacity = 64;
    sb->length = 0;
    sb->data = (char *)malloc(sb->capacity);
    if (!sb->data) {
        perror("Erro ao alocar data do StringBuffer");
        free(sb);
        exit(EXIT_FAILURE);
    }
    sb->data[0] = '\0';
    return sb;
}

/**
 * @brief Adiciona um caractere ao buffer dinâmico.
 */
static void sb_append_char(StringBuffer *sb, char ch) {
    if (sb->length + 2 > sb->capacity) {
        sb->capacity *= 2;
        char *new_data = (char *)realloc(sb->data, sb->capacity);
        if (!new_data) {
            perror("Erro ao realocar StringBuffer");
            free(sb->data);
            free(sb);
            exit(EXIT_FAILURE);
        }
        sb->data = new_data;
    }
    sb->data[sb->length++] = ch;
    sb->data[sb->length] = '\0';
}

/**
 * @brief Libera a memória alocada pelo buffer de string.
 */
static void sb_free(StringBuffer *sb) {
    if (sb) {
        free(sb->data);
        free(sb);
    }
}

/**
 * @brief Libera a memória alocada pela imagem.
 */
static void free_image(Image *img) {
    if (img && img->pixels) {
        free(img->pixels);
        img->pixels = NULL;
    }
}

/**
 * @brief Verifica se o arquivo aberto é um PBM válido (número mágico P1).
 */
bool is_pbm_file(FILE *image_file) {
    char magic_number[PBM_CODE_SIZE] = {0};
    if (fscanf(image_file, "%2s", magic_number) != 1) {
        return false;
    }
    return strcmp(magic_number, "P1") == 0;
}

/**
 * @brief Lê uma imagem binária PBM no formato P1 a partir do caminho especificado.
 */
Image read_binary_image(const char path[]) {
    FILE *image_file = fopen(path, "r");
    if (image_file == NULL) {
        perror("Erro ao abrir o arquivo PBM");
        exit(EXIT_FAILURE);
    }

    Image img = {0, 0, NULL};

    if (!is_pbm_file(image_file)) {
        fprintf(stderr, "Erro: O arquivo '%s' não está no formato PBM P1 válido.\n", path);
        fclose(image_file);
        exit(EXIT_FAILURE);
    }

    // Ignorar comentários e espaços em branco
    int ch;
    while ((ch = fgetc(image_file)) != EOF) {
        if (ch == '#') {
            // Descarta o comentário até o fim da linha
            while ((ch = fgetc(image_file)) != EOF && ch != '\n');
        } else if (!isspace(ch)) {
            ungetc(ch, image_file);
            break;
        }
    }

    // Lê largura e altura
    if (fscanf(image_file, "%d %d", &img.width, &img.height) != 2 || img.width <= 0 || img.height <= 0) {
        fprintf(stderr, "Erro ao ler as dimensões da imagem (largura x altura).\n");
        fclose(image_file);
        exit(EXIT_FAILURE);
    }

    img.pixels = (int *)malloc(img.width * img.height * sizeof(int));
    if (!img.pixels) {
        perror("Erro ao alocar memória para os pixels");
        fclose(image_file);
        exit(EXIT_FAILURE);
    }

    // Lê a matriz de pixels
    for (int i = 0; i < img.height; ++i) {
        for (int j = 0; j < img.width; ++j) {
            int pixel;
            if (fscanf(image_file, "%d", &pixel) != 1) {
                fprintf(stderr, "Erro na leitura do pixel na posição (%d, %d).\n", i, j);
                free_image(&img);
                fclose(image_file);
                exit(EXIT_FAILURE);
            }
            img.pixels[i * img.width + j] = pixel;
        }
    }

    fclose(image_file);
    return img;
}

/**
 * @brief Verifica se a região da imagem definida por [start_row, end_row] x [start_col, end_col] é uniforme.
 */
bool is_uniform(Image image, int start_row, int end_row, int start_col, int end_col) {
    int first_pixel = image.pixels[start_row * image.width + start_col];

    for (int i = start_row; i <= end_row; ++i) {
        for (int j = start_col; j <= end_col; ++j) {
            if (image.pixels[i * image.width + j] != first_pixel) {
                return false;
            }
        }
    }
    return true;
}

/**
 * @brief Codifica recursivamente a região da imagem via Quadtree.
 */
void encode(Image image, int start_row, int end_row, int start_col, int end_col, StringBuffer *sb) {
    if (start_row > end_row || start_col > end_col) {
        return; // Subimagem inválida / caso base
    }

    if (is_uniform(image, start_row, end_row, start_col, end_col)) {
        int first_pixel = image.pixels[start_row * image.width + start_col];
        // 0 = Branco ('B'), 1 = Preto ('P')
        sb_append_char(sb, (first_pixel == 0) ? 'B' : 'P');
    } else {
        // Região mista: acrescenta 'X' e divide nos 4 quadrantes
        sb_append_char(sb, 'X');

        int mid_row = start_row + (end_row - start_row) / 2;
        int mid_col = start_col + (end_col - start_col) / 2;

        // Quadrante Superior Esquerdo (NO)
        encode(image, start_row, mid_row, start_col, mid_col, sb);
        // Quadrante Superior Direito (NE)
        encode(image, start_row, mid_row, mid_col + 1, end_col, sb);
        // Quadrante Inferior Esquerdo (SO)
        encode(image, mid_row + 1, end_row, start_col, mid_col, sb);
        // Quadrante Inferior Direito (SE)
        encode(image, mid_row + 1, end_row, mid_col + 1, end_col, sb);
    }
}

/**
 * @brief Exibe as instruções e o manual de ajuda do programa.
 */
void help(void) {
    puts("==========================================================================");
    puts("                   ImageEncoder - Codificador PBM                         ");
    puts("==========================================================================");
    puts("Uso: ./codificador_bin [-? | --help] [-m | --manual] [-f | --file ARQUIVO]");
    puts("Codifica imagens binárias dadas em arquivos PBM (P1) ou informadas manualmente.");
    puts("\nOpções:");
    puts("  -?, --help    : Exibe este manual de instruções.");
    puts("  -m, --manual  : Ativa o modo de entrada manual pelo teclado.");
    puts("  -f, --file ARQ: Processa e codifica a imagem contida no arquivo PBM especificado.");
    puts("==========================================================================");
}

/**
 * @brief Realiza a leitura dos dados da imagem diretamente da entrada padrão.
 */
void manual(void) {
    Image img = {0, 0, NULL};

    printf("Insira as dimensões da imagem (largura altura): ");
    if (scanf("%d %d", &img.width, &img.height) != 2 || img.width <= 0 || img.height <= 0) {
        fprintf(stderr, "Dimensões inválidas.\n");
        return;
    }

    img.pixels = (int *)malloc(img.width * img.height * sizeof(int));
    if (!img.pixels) {
        perror("Erro ao alocar memória");
        return;
    }

    printf("Insira os pixels da imagem (0 para branco, 1 para preto, linha por linha):\n");
    for (int i = 0; i < img.height; ++i) {
        char line[MAX_LINE_SIZE];
        if (scanf(" %[^\n]", line) != 1) {
            fprintf(stderr, "Erro ao ler a linha %d.\n", i);
            free_image(&img);
            return;
        }

        char *token = strtok(line, " \t");
        int j = 0;

        while (token != NULL && j < img.width) {
            img.pixels[i * img.width + j] = atoi(token);
            token = strtok(NULL, " \t");
            j++;
        }
    }

    StringBuffer *sb = sb_create();
    encode(img, 0, img.height - 1, 0, img.width - 1, sb);

    printf("\n>>> Código gerado (Quadtree): %s\n\n", sb->data);

    sb_free(sb);
    free_image(&img);
}

int main(int argc, char const *argv[]) {
    if (argc == 2) {
        if (strcmp(argv[1], "-?") == 0 || strcmp(argv[1], "--help") == 0) {
            help();
            return 0;
        }

        if (strcmp(argv[1], "-m") == 0 || strcmp(argv[1], "--manual") == 0) {
            manual();
            return 0;
        }
    }

    if (argc == 3) {
        if (strcmp(argv[1], "-f") == 0 || strcmp(argv[1], "--file") == 0) {
            Image img = read_binary_image(argv[2]);

            StringBuffer *sb = sb_create();
            encode(img, 0, img.height - 1, 0, img.width - 1, sb);

            printf("\n>>> Código gerado (Quadtree): %s\n\n", sb->data);

            sb_free(sb);
            free_image(&img);
            return 0;
        }
    }

    // Caso nenhum argumento ou argumento inválido seja passado
    help();
    return 0;
}

