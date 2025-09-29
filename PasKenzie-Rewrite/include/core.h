#ifndef CORE_H
#define CORE_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define PKZ_BUFFER_CAP  65536

typedef enum {
    TK_ERRO = 0,
    TK_PROGRAM, TK_VAR, TK_BEGIN, TK_END, TK_IF, TK_THEN, TK_ELSE, TK_WHILE, TK_DO,
    TK_READ, TK_WRITE, TK_CHAR, TK_INTEGER, TK_BOOLEAN, TK_DIV, TK_OR, TK_AND, TK_NOT,
    TK_TRUE, TK_FALSE,
    TK_IDENT, TK_NUMBER, TK_CHARCONST,
    TK_EQ, TK_NE, TK_LT, TK_LE, TK_GT, TK_GE,
    TK_PLUS, TK_MINUS, TK_STAR,
    TK_SEMI, TK_COMMA, TK_COLON, TK_ASSIGN,
    TK_LPAR, TK_RPAR, TK_DOT,
    TK_COMMENT, TK_EOS
} TokenKind;

typedef struct {
    TokenKind kind;
    int line;
    union {
        int number;
        char ident[16];
        char ch;
    } attr;
} Token;

extern char *g_buffer;
extern int   g_line;
extern Token g_tok;
extern TokenKind g_la;
extern FILE *g_file;

const char* pkz_tok_name(TokenKind k);

#endif // CORE_H
