#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LINE_SIZE 1024
#define PBM_CODE_SIZE 3  // Tamanho do código PBM (P1)

typedef struct {
    int width;
    int height;
    int *pixels;
} Image;

// Função para verificar se um arquivo é um arquivo PBM válido
bool is_pbm_file(FILE *image_file)
{
    char magic_number[PBM_CODE_SIZE];
    fscanf(image_file, "%2s", magic_number);
    return strcmp(magic_number, "P1") == 0;
}

// Função para ler uma imagem binária de um arquivo PBM
Image read_binary_image(const char path[])
{
    FILE *image_file = fopen(path, "r");

    if (image_file == NULL)
    {
        perror("Erro ao abrir o arquivo");
        exit(EXIT_FAILURE);
    }

    Image img;
    img.width = 0;
    img.height = 0;
    img.pixels = NULL;

    if (!is_pbm_file(image_file))
    {
        fprintf(stderr, "Formato PBM inválido\n");
        exit(EXIT_FAILURE);
    }

    // Ignorar comentários
    int break_char;
    while ((break_char = fgetc(image_file)) == '#' || isspace(break_char))
    {
        if (break_char == '#')
        {
            fscanf(image_file, "%*[^\n]"); // Pular a linha de comentário
        }
    }
    ungetc(break_char, image_file); // Devolver o caractere que encerrou o loop

    // Ler largura e altura do arquivo
    if (fscanf(image_file, "%d %d", &img.width, &img.height) != 2)
    {
        fprintf(stderr, "Erro ao ler largura e altura.\n");
        exit(EXIT_FAILURE);
    }

    img.pixels = (int *)malloc(img.width * img.height * sizeof(int));

    // Ler os pixels
    for (int i = 0; i < img.height; ++i)
    {
        for (int j = 0; j < img.width; ++j)
        {
            int pixel;
            fscanf(image_file, "%d", &pixel);
            img.pixels[i * img.width + j] = pixel;
        }
    }

    fclose(image_file);
    return img;
}

// Função para verificar se uma parte da imagem é uniforme
bool is_uniform(Image image, int start_row, int end_row, int start_col, int end_col)
{
    bool uniform = true;
    int first_pixel = image.pixels[start_row * image.width + start_col];

    for (int i = start_row; i <= end_row; ++i)
    {
        for (int j = start_col; j <= end_col; ++j)
        {
            if (image.pixels[i * image.width + j] != first_pixel)
            {
                uniform = false;
                break;
            }
        }

        if (!uniform)
        {
            break;
        }
    }

    return uniform;
}

// Função recursiva para codificar a imagem
void encode(Image image, int start_row, int end_row, int start_col, int end_col, char *code)
{
    if (start_row > end_row || start_col > end_col)
    {
        return; // Caso base: subimagem inválida
    }

    // Se for uniforme, adicionar o código correspondente
    if (is_uniform(image, start_row, end_row, start_col, end_col))
    {
        int first_pixel = image.pixels[start_row * image.width + start_col];
        // Realloc só se necessário e garantir espaço suficiente
        size_t len = strlen(code);
        code = realloc(code, len + 2);
        sprintf(code + len, "%c", (first_pixel == 0) ? 'B' : 'P');
    }
    else
    {
        // Se não for uniforme, adicionar 'X' e dividir a imagem em 4 quadrantes
        size_t len = strlen(code);
        code = realloc(code, len + 2);
        sprintf(code + len, "X");

        int mid_row = (start_row + end_row) / 2;
        int mid_col = (start_col + end_col) / 2;

        // Chamar a função recursivamente para cada quadrante
        encode(image, start_row, mid_row, start_col, mid_col, code);     // 1º quadrante
        encode(image, start_row, mid_row, mid_col + 1, end_col, code);   // 2º quadrante
        encode(image, mid_row + 1, end_row, start_col, mid_col, code);   // 3º quadrante
        encode(image, mid_row + 1, end_row, mid_col + 1, end_col, code); // 4º quadrante
    }
}

// Função para exibir o manual de ajuda
void help()
{
    puts("Uso: ImageEncoder [-? | -m | -f ARQ]");
    puts("Codifica imagens binárias dadas em arquivos PBM ou por dados informados manualmente.");
    puts("Argumentos:");
    puts("-?, --help  : apresenta essa orientação na tela.");
    puts("-m, --manual: ativa o modo de entrada manual, em que o usuário fornece todos os dados da imagem informando-os através do teclado.");
    puts("-f, --file: considera a imagem representada no arquivo PBM (Portable bitmap).");
}

// Função para leitura manual da imagem
void manual()
{
    Image img;
    img.width = 0;
    img.height = 0;
    img.pixels = NULL;

    printf("Insira as dimensões da imagem (largura altura): ");
    scanf("%d %d", &img.width, &img.height);

    img.pixels = (int *)malloc(img.width * img.height * sizeof(int));

    printf("Insira os pixels da imagem (0 para branco, 1 para preto):\n");
    for (int i = 0; i < img.height; ++i)
    {
        char line[MAX_LINE_SIZE];
        scanf(" %[^\n]", line); // Adicionando um espaço antes de %[^\n] para consumir o \n no buffer

        char *token = strtok(line, " ");
        int j = 0;

        while (token != NULL && j < img.width)
        {
            img.pixels[i * img.width + j] = atoi(token);

            token = strtok(NULL, " ");
            j++;
        }
    }

    // Codificação da imagem
    char *code = (char *)malloc(1);  // Começando com um tamanho de 1 byte (para o '\0')
    code[0] = '\0';

    encode(img, 0, img.height - 1, 0, img.width - 1, code);

    printf("Código gerado: %s\n", code);

    // Liberação de memória
    free(code);
    free(img.pixels);
}

// Função para processar os argumentos de linha de comando
int main(int argc, char const *argv[])
{
    if (argc == 2)
    {
        if (strcmp(argv[1], "-?") == 0 || strcmp(argv[1], "--help") == 0)
        {
            help();
            return 0;
        }

        if (strcmp(argv[1], "-m") == 0 || strcmp(argv[1], "--manual") == 0)
        {
            manual();
            return 0;
        }
    }

    if (argc == 3)
    {
        if (strcmp(argv[1], "-f") == 0 || strcmp(argv[1], "--file") == 0)
        {
            Image img = read_binary_image(argv[2]);

            // Codificação da imagem
            char *code = (char *)malloc(1);  // Começando com um tamanho de 1 byte
            code[0] = '\0';

            encode(img, 0, img.height - 1, 0, img.width - 1, code);

            printf("Código gerado: %s\n", code);

            // Liberação de memória
            free(code);
            free(img.pixels);
            return 0;
        }
    }

    // Caso não tenha argumentos ou argumentos inválidos
    help();
    return 0;
}
