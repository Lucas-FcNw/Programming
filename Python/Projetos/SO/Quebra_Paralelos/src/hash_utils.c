#include <stdio.h>
#include <string.h>
#include <openssl/md5.h>
#include "hash_utils.h"
#define OPENSSL_SUPPRESS_DEPRECATED 1

void md5_string(const char *input, char output[33]) {
    unsigned char digest[MD5_DIGEST_LENGTH];
    MD5((unsigned char*)input, strlen(input), digest);

    for (int i = 0; i < 16; i++) {
        sprintf(&output[i*2], "%02x", (unsigned int)digest[i]);
    }
    output[32] = '\0';
}

int increment_password(char *password, const char *charset, int charset_len, int password_len) {
    for (int i = password_len - 1; i >= 0; i--) {
        int index = 0;
        while (index < charset_len && charset[index] != password[i]) {
            index++;
        }

        if (index >= charset_len) return 0;

        if (index + 1 < charset_len) {
            password[i] = charset[index + 1];
            return 1;
        } else {
            password[i] = charset[0];
        }
    }
    return 0;
}
