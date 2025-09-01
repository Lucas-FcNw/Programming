#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include "hash_utils.h"

#define RESULT_FILE "password_found.txt"

// Função para salvar o resultado
void save_result(int worker_id, const char *password) {
    int fd = open(RESULT_FILE, O_CREAT | O_EXCL | O_WRONLY, 0644);
    if (fd >= 0) {
        char buffer[256];
        int len = snprintf(buffer, sizeof(buffer), "%d:%s\n", worker_id, password);
        write(fd, buffer, len);
        close(fd);
        printf("[Worker %d] Resultado salvo: %s\n", worker_id, password);
    }
}

int main(int argc, char *argv[]) {
    if (argc != 7) {
        fprintf(stderr, "Uso: %s <target_hash> <start_pass> <end_pass> <charset> <pass_len> <worker_id>\n", argv[0]);
        exit(1);
    }

    char *target_hash = argv[1];
    char *start_pass = argv[2];
    char *end_pass = argv[3];
    char *charset = argv[4];
    int pass_len = atoi(argv[5]);
    int worker_id = atoi(argv[6]);

    int charset_len = strlen(charset);
    char current_password[pass_len + 1];
    char computed_hash[33];

    strncpy(current_password, start_pass, pass_len);
    current_password[pass_len] = '\0';

    printf("[Worker %d] Iniciando busca de %s a %s\n", worker_id, start_pass, end_pass);

    do {
        // Calcular hash da senha atual
        md5_string(current_password, computed_hash);

        // Comparar com o hash alvo
        if (strcmp(computed_hash, target_hash) == 0) {
            printf("[Worker %d] SENHA ENCONTRADA: %s\n", worker_id, current_password);
            save_result(worker_id, current_password);
            break;
        }

        // Incrementar senha
        if (!increment_password(current_password, charset, charset_len, pass_len)) {
            break; // Fim do espaço de busca
        }

        // Verificar se ultrapassou o fim do intervalo
        if (strcmp(current_password, end_pass) > 0) {
            break;
        }

    } while (1);

    printf("[Worker %d] Finalizado\n", worker_id);
    return 0;
}
