#include <stdio.h>
#include <string.h>

#define MAX_FILMES 100
#define TAM_MAX_STRING 100

typedef struct {
    char nome[TAM_MAX_STRING];
    char genero[TAM_MAX_STRING];
    int ano;
    char classificacao_etaria[TAM_MAX_STRING];
    float nota;
} Filme;

Filme catalogo[MAX_FILMES];
int num_filmes = 0;

void cadastrarFilme() {
    if (num_filmes < MAX_FILMES) {
        Filme novoFilme;
        printf("Nome do filme: ");
        scanf(" %[^\n]s", novoFilme.nome);
        printf("Gênero: ");
        scanf(" %[^\n]s", novoFilme.genero);
        printf("Ano de lançamento: ");
        scanf("%d", &novoFilme.ano);
        printf("Classificação etária (G, PG, PG-13, R, NC-17): ");
        scanf(" %[^\n]s", novoFilme.classificacao_etaria);
        printf("Ranking de votação: ");
        scanf("%f", &novoFilme.nota);

        catalogo[num_filmes] = novoFilme;
        num_filmes++;

        FILE *arquivo = fopen("Filmes.txt", "a");
        if (arquivo != NULL) {
            fprintf(arquivo, "%s;%s;%d;%s;%.2f\n", novoFilme.nome, novoFilme.genero, novoFilme.ano, novoFilme.classificacao_etaria, novoFilme.nota);
            fclose(arquivo);
        } else {
            printf("Erro ao abrir o arquivo.\n");
        }

        printf("Filme cadastrado com sucesso!\n");
    } else {
        printf("Não é possível cadastrar mais filmes. Limite máximo atingido.\n");
    }
}

void listarTodosFilmes() {
    printf("Listando todos os filmes:\n");
    for (int i = 0; i < num_filmes; i++) {
        printf("%s\n", catalogo[i].nome);
    }
}

void listarFilmesPorGenero() {
    char genero[TAM_MAX_STRING];
    printf("Digite o gênero do filme: ");
    scanf(" %[^\n]s", genero);

    printf("Filmes do gênero '%s':\n", genero);
    for (int i = 0; i < num_filmes; i++) {
        if (strcmp(catalogo[i].genero, genero) == 0) {
            printf("%s\n", catalogo[i].nome);
        }
    }
}

void listarFilmesPorClassificacao() {
    char classificacao[4];
    printf("Digite a classificação etária desejada (G, PG, PG-13, R, NC-17): ");
    scanf(" %[^\n]s", classificacao);

    printf("Filmes com classificação etária '%s':\n", classificacao);
    for (int i = 0; i < num_filmes; i++) {
        if (strcmp(catalogo[i].classificacao_etaria, classificacao) == 0) {
            printf("%s\n", catalogo[i].nome);
        }
    }
}

void removerFilme() {
    char titulo[TAM_MAX_STRING];
    printf("Digite o filme que deseja remover: ");
    scanf(" %[^\n]s", titulo);

    int encontrado = 0;
    for (int i = 0; i < num_filmes; i++) {
        if (strcmp(catalogo[i].nome, titulo) == 0) {
            encontrado = 1;
            for (int j = i; j < num_filmes - 1; j++) {
                catalogo[j] = catalogo[j + 1];
            }
            num_filmes--;

            FILE *arquivo = fopen("Filmes.txt", "w");
            if (arquivo != NULL) {
                for (int j = 0; j < num_filmes; j++) {
                    fprintf(arquivo, "%s;%s;%d;%s;%.2f\n", catalogo[j].nome, catalogo[j].genero, catalogo[j].ano, catalogo[j].classificacao_etaria, catalogo[j].nota);
                }
                fclose(arquivo);
            } else {
                printf("Erro ao abrir o arquivo.\n");
            }

            printf("Filme removido com sucesso!\n");
            break;
        }
    }
    if (!encontrado) {
        printf("Filme não encontrado.\n");
    }
}

void carregarCatalogo() {
    FILE *arquivo = fopen("Filmes.txt", "r");
    if (arquivo != NULL) {
        while (fscanf(arquivo, " %[^\n]s", catalogo[num_filmes].nome) != EOF) {
            fscanf(arquivo, " %[^\n]s", catalogo[num_filmes].genero);
            fscanf(arquivo, "%d", &catalogo[num_filmes].ano);
            fscanf(arquivo, " %[^\n]s", catalogo[num_filmes].classificacao_etaria);
            fscanf(arquivo, "%f", &catalogo[num_filmes].nota);
            num_filmes++;
        }
        fclose(arquivo);
    } else {
        printf("Arquivo de catálogo não encontrado.\n");
    }
}

int main() {
    carregarCatalogo();

    int opcao;
    do {
        printf("\n   Sistema de Gerenciamento de Filmes \n");
        printf("1. Cadastrar novo filme\n");
        printf("2. Listar todos os filmes\n");
        printf("3. Listar filmes por gênero\n");
        printf("4. Listar filmes por classificação etária\n");
        printf("5. Remover filme\n");
        printf("0. Sair\n");
        printf("Escolha uma opção: ");
        scanf("%d", &opcao);

        switch (opcao) {
            case 1:
                cadastrarFilme();
                break;
            case 2:
                listarTodosFilmes();
                break;
            case 3:
                listarFilmesPorGenero();
                break;
            case 4:
                listarFilmesPorClassificacao();
                break;
            case 5:
                removerFilme();
                break;
            case 0:
                printf("Saindo...\n");
                break;
            default:
                printf("Opção inválida. Tente novamente.\n");
        }
    } while (opcao != 0);

    return 0;
}
