#include <stdio.h>
#include "hash_utils.h"

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <string>\n", argv[0]);
        return 1;
    }

    char hash[33];
    md5_string(argv[1], hash);
    printf("MD5('%s') = %s\n", argv[1], hash);

    return 0;
}
