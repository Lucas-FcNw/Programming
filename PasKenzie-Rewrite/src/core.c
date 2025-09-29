#include "../include/core.h"

char *g_buffer = NULL;
int   g_line   = 1;
Token g_tok;
TokenKind g_la;
FILE *g_file = NULL;

const char* pkz_tok_name(TokenKind k) {
    switch (k) {
        case TK_PROGRAM: return "program";
        case TK_VAR: return "var";
        case TK_BEGIN: return "begin";
        case TK_END: return "end";
        case TK_IF: return "if";
        case TK_THEN: return "then";
        case TK_ELSE: return "else";
        case TK_WHILE: return "while";
        case TK_DO: return "do";
        case TK_READ: return "read";
        case TK_WRITE: return "write";
        case TK_CHAR: return "char";
        case TK_INTEGER: return "integer";
        case TK_BOOLEAN: return "boolean";
        case TK_DIV: return "div";
        case TK_OR: return "or";
        case TK_AND: return "and";
        case TK_NOT: return "not";
        case TK_TRUE: return "true";
        case TK_FALSE: return "false";
        case TK_IDENT: return "identificador";
        case TK_NUMBER: return "numero";
        case TK_CHARCONST: return "caracter";
        case TK_EQ: return "=";
        case TK_NE: return "<>";
        case TK_LT: return "<";
        case TK_LE: return "<=";
        case TK_GT: return ">";
        case TK_GE: return ">=";
        case TK_PLUS: return "+";
        case TK_MINUS: return "-";
        case TK_STAR: return "*";
        case TK_SEMI: return ";";
        case TK_COMMA: return ",";
        case TK_COLON: return ":";
        case TK_ASSIGN: return ":=";
        case TK_LPAR: return "(";
        case TK_RPAR: return ")";
        case TK_DOT: return ".";
        case TK_COMMENT: return "comentario";
        case TK_EOS: return "fim de arquivo";
        case TK_ERRO: default: return "erro";
    }
}
