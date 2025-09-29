
#include "tokens.h"

const char* token_name(TAtomo t){
    switch(t){
        case TK_EOF: return "EOF";
        case TK_ERRO: return "erro";
        case TK_COMENTARIO: return "comentario";
        case TK_IDENTIFIER: return "identifier";
        case TK_CONSTINT: return "constint";
        case TK_CONSTCHAR: return "constchar";
        case TK_PROGRAM: return "program";
        case TK_VAR: return "var";
        case TK_BEGIN: return "begin";
        case TK_END: return "end";
        case TK_READ: return "read";
        case TK_WRITE: return "write";
        case TK_IF: return "if";
        case TK_THEN: return "then";
        case TK_ELSE: return "else";
        case TK_WHILE: return "while";
        case TK_DO: return "do";
        case TK_CHAR: return "char";
        case TK_INTEGER: return "integer";
        case TK_BOOLEAN: return "boolean";
        case TK_TRUE: return "true";
        case TK_FALSE: return "false";
        case TK_DIV: return "div";
        case TK_OR: return "or";
        case TK_AND: return "and";
        case TK_NOT: return "not";
        case TK_SEMI: return "ponto_virgula";
        case TK_COMMA: return "virgula";
        case TK_COLON: return "dois_pontos";
        case TK_DOT: return "ponto";
        case TK_ASSIGN: return "atribuicao";
        case TK_LPAR: return "abre_par";
        case TK_RPAR: return "fecha_par";
        case TK_PLUS: return "+";
        case TK_MINUS: return "-";
        case TK_STAR: return "*";
        case TK_EQ: return "=";
        case TK_NE: return "<>";
        case TK_LT: return "<";
        case TK_LE: return "<=";
        case TK_GT: return ">";
        case TK_GE: return ">=";
        default: return "??";
    }
}
