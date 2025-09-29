#include "include/core.h"
#include "include/scanner.h"
#include "include/analyzer.h"
#include "src/core.c"
#include "src/scanner.c"
#include "src/analyzer.c"

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Uso: %s <arquivo.txt>\n", argv[0]);
        return 1;
    }

    g_file = fopen(argv[1], "r");
    if (!g_file) { perror("Erro ao abrir o arquivo"); return 1; }

    char *buf = (char*)malloc(PKZ_BUFFER_CAP);
    if (!buf) { fprintf(stderr, "Sem memoria\n"); fclose(g_file); return 1; }
    buf[0]='\0';

    char line[512];
    while (fgets(line, sizeof(line), g_file)) {
        strncat(buf, line, PKZ_BUFFER_CAP - strlen(buf) - 1);
    }
    fclose(g_file);

    pkz_scan_init(buf);
    g_tok = pkz_next();
    g_la  = g_tok.kind;
    pkz_analyze();

    free(buf);
    return 0;
}
