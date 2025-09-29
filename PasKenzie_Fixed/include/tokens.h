
#ifndef TOKENS_H
#define TOKENS_H

#include <stdio.h>

typedef enum {
    // special
    TK_EOF = 0,
    TK_ERRO,
    TK_COMENTARIO,

    // identifiers and literals
    TK_IDENTIFIER,
    TK_CONSTINT,
    TK_CONSTCHAR,

    // keywords
    TK_PROGRAM, TK_VAR, TK_BEGIN, TK_END,
    TK_READ, TK_WRITE,
    TK_IF, TK_THEN, TK_ELSE,
    TK_WHILE, TK_DO,
    TK_CHAR, TK_INTEGER, TK_BOOLEAN,
    TK_TRUE, TK_FALSE,
    TK_DIV, TK_OR, TK_AND, TK_NOT,

    // punctuation / operators
    TK_SEMI,        // ;
    TK_COMMA,       // ,
    TK_COLON,       // :
    TK_DOT,         // .
    TK_ASSIGN,      // :=
    TK_LPAR,        // (
    TK_RPAR,        // )
    TK_PLUS,        // +
    TK_MINUS,       // -
    TK_STAR,        // *
    TK_EQ,          // =
    TK_NE,          // <>
    TK_LT,          // <
    TK_LE,          // <=
    TK_GT,          // >
    TK_GE           // >=
} TAtomo;

typedef struct {
    TAtomo atomo;
    int linha;
    union {
        int numero;     // constint
        char id[16];    // identifier (max 15 + \0)
        char ch;        // constchar
    } atributo;
} TInfoAtomo;

const char* token_name(TAtomo t);

#endif
