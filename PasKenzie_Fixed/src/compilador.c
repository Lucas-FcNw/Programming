
#include <stdio.h>
#include <stdlib.h>
#include "lexer.h"
#include "parser.h"

int main(int argc, char **argv){
    if(argc<2){
        fprintf(stderr, "Uso: %s <arquivo.pzk>\n", argv[0]);
        return 1;
    }
    FILE *f = fopen(argv[1], "r");
    if(!f){
        perror("Erro abrindo arquivo");
        return 1;
    }
    lexer_init(f);
    parse_program();
    fclose(f);
    return 0;
}
