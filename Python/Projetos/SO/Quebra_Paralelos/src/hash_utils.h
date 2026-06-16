#ifndef HASH_UTILS_H
#define HASH_UTILS_H

void md5_string(const char *input, char output[33]);
int increment_password(char *password, const char *charset, int charset_len, int password_len);

#endif
