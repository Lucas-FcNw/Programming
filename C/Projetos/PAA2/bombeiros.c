//Henrique Pena 10417975 & Lucas Fernandes 10419400
    
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#define MAX 100 // Número máximo de esquinas

int T[MAX];          // Vetor de tempos mínimos
int R[MAX][MAX];     // Matriz para armazenar as rotas mais rápidas
int adj[MAX][MAX];   // Matriz de adjacência para armazenar os tempos entre esquinas
int n;               // Número de esquinas

// Função para inicializar o mapa e os vetores T e R
void inicializar(int inicio) {
    for (int i = 0; i < n; i++) {
        T[i] = INT_MAX;
        for (int j = 0; j < n; j++) {
            R[i][j] = -1;  // Inicializa rota com -1
        }
    }
    T[inicio] = 0;
    R[inicio][0] = inicio; // Início da rota
}

// Função principal para encontrar a rota mais rápida
void rotaMaisRapida(int inicio) {
    int E[MAX];
    for (int i = 0; i < n; i++) E[i] = 1; // Todas as esquinas estão em E
    
    while (1) {
        int v = -1;
        int menorTempo = INT_MAX;
        
        for (int i = 0; i < n; i++) {
            if (E[i] && T[i] < menorTempo) {
                menorTempo = T[i];
                v = i;
            }
        }

        if (v == -1) break; // Não há mais esquinas acessíveis

        E[v] = 0; // Remove v do conjunto E

        // Atualiza tempos e rotas para as esquinas interligadas a v
        for (int e = 0; e < n; e++) {
            if (adj[v][e] > 0 && E[e]) {
                int novoTempo = T[v] + adj[v][e];
                if (T[e] > novoTempo) {
                    T[e] = novoTempo;
                    
                    // Copia a rota de v para e
                    int j = 0;
                    while (R[v][j] != -1) {
                        R[e][j] = R[v][j];
                        j++;
                    }
                    R[e][j] = e; // Adiciona e à rota e define o final da rota
                    R[e][j + 1] = -1; // Marca o final da rota com -1
                }
            }
        }
    }
}

// Função para ler o arquivo de entrada e preencher a matriz de adjacência
void lerArquivo() {
    char caminhoArquivo[] = "/home/lucasfc/Documentos/PAA2/teste.txt";
    FILE *arquivo = fopen(caminhoArquivo, "r");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo.\n");
        exit(1);
    }

    int esquinaIncendio;
    fscanf(arquivo, "%d", &esquinaIncendio); // Lê a esquina onde ocorre o incêndio

    fscanf(arquivo, "%d", &n); // Lê o número de esquinas
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            adj[i][j] = 0; // Inicializa as conexões como não existentes
        }
    }

    int origem, destino, tempo;
    while (fscanf(arquivo, "%d %d %d", &origem, &destino, &tempo) == 3) {
        if (origem == 0) break; // Fim dos dados de ruas
        adj[origem - 1][destino - 1] = tempo; // Configura a conexão e o tempo de mão-única
    }

    fclose(arquivo);

    // Calcula a rota mais rápida a partir da esquina 1
    inicializar(0); // Esquina inicial é 1 (índice 0)
    rotaMaisRapida(0);
}

// Função para imprimir o tempo e a rota até a esquina escolhida pelo usuário
void imprimirRota(int destino) {
    printf("Rota até a esquina #%d: ", destino + 1);
    for (int i = 0; R[destino][i] != -1; i++) {
        printf("%d ", R[destino][i] + 1); // Imprime a rota convertida para 1-based
    }
    printf("\nTempo calculado para rota = %d min.\n", T[destino]);
}

int main() {
    lerArquivo();

    int esquinaDestino;
    printf("Digite o número da esquina de destino: ");
    scanf("%d", &esquinaDestino);
    esquinaDestino -= 1; // Ajusta para índice 0-based

    // Verifica se a esquina de destino é válida
    if (esquinaDestino >= 0 && esquinaDestino < n) {
        imprimirRota(esquinaDestino);
    } else {
        printf("Esquina de destino inválida.\n");
    }

    return 0;
}
