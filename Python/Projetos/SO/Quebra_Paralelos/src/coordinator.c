#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>
#include "hash_utils.h"

#define RESULT_FILE "password_found.txt"

// Função strdup alternativa
char* my_strdup(const char* s) {
    if (s == NULL) return NULL;
    size_t len = strlen(s) + 1;
    char* new_str = malloc(len);
    if (new_str) {
        memcpy(new_str, s, len);
    }
    return new_str;
}

// Função para calcular o tamanho do intervalo por worker
void calculate_range(const char *charset, int pass_len, int num_workers,
                     char **ranges_start, char **ranges_end) {
    int charset_len = strlen(charset);
    long total_combinations = 1;

    for (int i = 0; i < pass_len; i++) {
        total_combinations *= charset_len;
    }

    long combinations_per_worker = total_combinations / num_workers;
    long remainder = total_combinations % num_workers;

    char *current = malloc(pass_len + 1);
    for (int i = 0; i < pass_len; i++) {
        current[i] = charset[0];
    }
    current[pass_len] = '\0';

    for (int i = 0; i < num_workers; i++) {
        ranges_start[i] = my_strdup(current);

        // Avançar combinations_per_worker posições
        long to_advance = combinations_per_worker + (i < remainder ? 1 : 0);

        for (long j = 0; j < to_advance; j++) {
            if (!increment_password(current, charset, charset_len, pass_len)) {
                break;
            }
        }

        ranges_end[i] = my_strdup(current);
    }

    free(current);
                     }

                     int main(int argc, char *argv[]) {
                         if (argc != 5) {
                             fprintf(stderr, "Uso: %s <target_hash> <pass_len> <charset> <num_workers>\n", argv[0]);
                             exit(1);
                         }

                         char *target_hash = argv[1];
                         int pass_len = atoi(argv[2]);
                         char *charset = argv[3];
                         int num_workers = atoi(argv[4]);

                         printf("=== Quebra de Senhas Paralela ===\n");
                         printf("Hash alvo: %s\n", target_hash);
                         printf("Tamanho da senha: %d\n", pass_len);
                         printf("Charset: %s\n", charset);
                         printf("Número de workers: %d\n", num_workers);

                         // Calcular intervalos para cada worker
                         char **ranges_start = malloc(num_workers * sizeof(char *));
                         char **ranges_end = malloc(num_workers * sizeof(char *));

                         calculate_range(charset, pass_len, num_workers, ranges_start, ranges_end);

                         // Criar workers
                         pid_t *workers = malloc(num_workers * sizeof(pid_t));

                         for (int i = 0; i < num_workers; i++) {
                             printf("Criando worker %d: %s a %s\n", i, ranges_start[i], ranges_end[i]);

                             pid_t pid = fork();

                             if (pid < 0) {
                                 perror("Erro no fork");
                                 exit(1);
                             } else if (pid == 0) {
                                 // Processo filho
                                 char pass_len_str[12], worker_id_str[12];
                                 sprintf(pass_len_str, "%d", pass_len);
                                 sprintf(worker_id_str, "%d", i);

                                 execl("./worker", "worker", target_hash, ranges_start[i],
                                       ranges_end[i], charset, pass_len_str, worker_id_str, NULL);

                                 perror("Erro no execl");
                                 exit(1);
                             } else {
                                 // Processo pai
                                 workers[i] = pid;
                             }
                         }

                         // Aguardar todos os workers terminarem
                         int status;
                         pid_t pid;
                         while ((pid = wait(&status)) > 0) {
                             printf("Worker %d terminou com status %d\n", pid, WEXITSTATUS(status));
                         }

                         // Verificar se a senha foi encontrada
                         FILE *file = fopen(RESULT_FILE, "r");
                         if (file != NULL) {
                             char line[256];
                             if (fgets(line, sizeof(line), file)) {
                                 char *colon = strchr(line, ':');
                                 if (colon != NULL) {
                                     *colon = '\0';
                                     int worker_id = atoi(line);
                                     char *password = colon + 1;
                                     password[strcspn(password, "\n")] = '\0';

                                     // Verificar se a senha está correta
                                     char computed_hash[33];
                                     md5_string(password, computed_hash);

                                     if (strcmp(computed_hash, target_hash) == 0) {
                                         printf("\n✓ Senha encontrada pelo worker %d: %s\n", worker_id, password);
                                     } else {
                                         printf("\n✗ Senha incorreta encontrada: %s\n", password);
                                     }
                                 }
                             }
                             fclose(file);
                         } else {
                             printf("\n✗ Senha não encontrada\n");
                         }

                         // Liberar memória
                         for (int i = 0; i < num_workers; i++) {
                             free(ranges_start[i]);
                             free(ranges_end[i]);
                         }
                         free(ranges_start);
                         free(ranges_end);
                         free(workers);

                         return 0;
                     }
