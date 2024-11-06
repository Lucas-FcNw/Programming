#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Structure to represent a binary image
typedef struct {
    int rows;
    int cols;
    int **pixels;
} Image;

// Function to check uniformity
int isUniform(Image *img, int startRow, int startCol, int numRows, int numCols) {
    int firstPixel = img->pixels[startRow][startCol];

    for (int i = startRow; i < startRow + numRows; i++) {
        for (int j = startCol; j < startCol + numCols; j++) {
            if (img->pixels[i][j] != firstPixel) {
                return 0; // Not uniform
            }
        }
    }

    return 1; // Uniform
}

// Function to divide the image and encode recursively
void divideAndEncode(Image *img, int startRow, int startCol, int numRows, int numCols) {
    // Uniform image
    if (isUniform(img, startRow, startCol, numRows, numCols)) {
        printf("%c", img->pixels[startRow][startCol] ? 'P' : 'B');
    } else {
        // Division and encoding of each quadrant
        printf("X");

        int midRow = startRow + numRows / 2;
        int midCol = startCol + numCols / 2;

        // Division and encoding of each quadrant
        divideAndEncode(img, startRow, startCol, midRow - startRow, midCol - startCol);
        divideAndEncode(img, startRow, midCol, midRow - startRow, startCol + numCols - midCol);
        divideAndEncode(img, midRow, startCol, startRow + numRows - midRow, midCol - startCol);
        divideAndEncode(img, midRow, midCol, startRow + numRows - midRow, startCol + numCols - midCol);
    }
}

// Function to encode the image
void encodeImage(Image *img) {
    divideAndEncode(img, 0, 0, img->rows, img->cols);
}

// Function to free the memory allocated for the image
void freeImage(Image *img) {
    for (int i = 0; i < img->rows; i++) {
        free(img->pixels[i]);
    }
    free(img->pixels);
    free(img);
}

// Function for manual input
Image *manualInput() {
    int rows, cols;

    printf("Modo Manual: Insira as dimensões (largura altura): ");
    scanf("%d %d", &cols, &rows);

    Image *img = (Image *)malloc(sizeof(Image));
    img->rows = rows;
    img->cols = cols;
    img->pixels = (int **)malloc(rows * sizeof(int *));
    for (int i = 0; i < rows; i++) {
        img->pixels[i] = (int *)malloc(cols * sizeof(int));
    }

    printf("Insira os pixels (0 para branco, 1 para preto):\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            scanf("%d", &img->pixels[i][j]);
        }
    }

    return img;
}

// Function for file input
Image *fileInput() {
    char filename[100];
    printf("Digite o nome do arquivo PBM: ");
    scanf("%s", filename);

    FILE *file = fopen(filename, "r");
    if (!file) {
        printf("Erro ao abrir o arquivo.\n");
        return NULL;
    }

    char magicNumber[3];
    fscanf(file, "%2s", magicNumber);

    if (magicNumber[0] != 'P' && magicNumber[0] != 'p') {
        printf("Erro: Formato de arquivo PBM inválido.\n");
        fclose(file);
        return NULL;
    }

    int cols, rows;
    fscanf(file, "%d %d", &cols, &rows);

    Image *img = (Image *)malloc(sizeof(Image));
    img->rows = rows;
    img->cols = cols;
    img->pixels = (int **)malloc(rows * sizeof(int *));
    for (int i = 0; i < rows; i++) {
        img->pixels[i] = (int *)malloc(cols * sizeof(int));
    }

    // Read pixels from the file
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            fscanf(file, "%d", &img->pixels[i][j]);
        }
    }

    fclose(file);

    return img;
}

// Function to display usage instructions
void displayHelp() {
    printf("Uso: ImageEncoder [-? | -m | -f ARQ]\n");
    printf("Codifica imagens binárias dadas em arquivos PBM ou por dados informados manualmente.\n");
    printf("Argumentos:\n");
    printf("-?, --help  : apresenta essa orientação na tela.\n");
    printf("-m, --manual: ativa o modo de entrada manual.\n");
    printf("-f, --file ARQ: considera a imagem representada no arquivo PBM.\n");
}

// Function for user interaction and program execution
void interactiveMenu() {
    char choice[2]; // Use an array of characters to accept a string

    while (1) {
        printf("\nSelecione uma opcao:\n");
        printf("1. Modo Manual\n");
        printf("2. Modo Arquivo PBM\n");
        printf("3. Ajuda\n");
        printf("0. Sair\n");

        printf("Opcao: ");

        // Use %1s to read at most 1 character
        if (scanf("%1s", choice) != 1) {
            // Clear the input buffer
            while (getchar() != '\n');
            printf("Entrada inválida. ");
            // Call displayHelp for invalid input
            displayHelp();
            continue;
        }

        // Compare the choice string
        if (strcmp(choice, "1") == 0 || strcmp(choice, "m") == 0) {
            // Manual Mode
            Image *img = manualInput();
            if (img != NULL) {
                encodeImage(img);
                freeImage(img);
            }
        } else if (strcmp(choice, "2") == 0 || strcmp(choice, "f") == 0) {
            // File Mode
            Image *img = fileInput();
            if (img != NULL) {
                encodeImage(img);
                freeImage(img);
            }
        } else if (strcmp(choice, "3") == 0 || strcmp(choice, "?") == 0) {
            // Help
            displayHelp();
        } else if (strcmp(choice, "0") == 0) {
            // Exit
            printf("Saindo do programa.\n");
            return;
        } else {
            // Invalid choice
            printf("Opcao invalida. ");
            // Call displayHelp for invalid input
            displayHelp();
        }

        // Clear the input buffer
        while (getchar() != '\n');
    }
}

// Main function
int main() {   
    // Call the interactive menu
    interactiveMenu();

    return 0;
}