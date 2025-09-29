#include "../include/scanner.h"

typedef struct { const char *kw; TokenKind kind; } Kw;
static const Kw KW_TABLE[] = {
    {"program", TK_PROGRAM}, {"var", TK_VAR}, {"begin", TK_BEGIN},
    {"end", TK_END}, {"if", TK_IF}, {"then", TK_THEN}, {"else", TK_ELSE},
    {"while", TK_WHILE}, {"do", TK_DO}, {"read", TK_READ}, {"write", TK_WRITE},
    {"char", TK_CHAR}, {"integer", TK_INTEGER}, {"boolean", TK_BOOLEAN},
    {"div", TK_DIV}, {"or", TK_OR}, {"and", TK_AND}, {"not", TK_NOT},
    {"true", TK_TRUE}, {"false", TK_FALSE}, {NULL, TK_ERRO}
};

static char g_lexeme[32];

void pkz_scan_init(char *buffer) {
    g_buffer = buffer;
    g_line = 1;
}

static void skip_ws() {
    while (*g_buffer == ' ' || *g_buffer == '\t' || *g_buffer == '\r' || *g_buffer == '\n') {
        if (*g_buffer == '\n') g_line++;
        g_buffer++;
    }
}

static int is_ident_start(char c) { return isalpha((unsigned char)c) || c=='_'; }
static int is_ident_body(char c)  { return isalnum((unsigned char)c) || c=='_'; }

static int to_int_pow10(int base, int exp) {
    for (int i=0;i<exp;i++) base *= 10;
    return base;
}

static Token scan_number() {
    const char *start = g_buffer;
    while (isdigit((unsigned char)*g_buffer)) g_buffer++;
    int value = 0, exp = 0;
    if (*g_buffer=='d' || *g_buffer=='D') {
        g_buffer++;
        int sign = 1;
        if (*g_buffer=='+') { sign = 1; g_buffer++; }
        else if (*g_buffer=='-') { sign = -1; g_buffer++; }
        const char *exp_start = g_buffer;
        while (isdigit((unsigned char)*g_buffer)) g_buffer++;
        exp = atoi(exp_start) * sign;
    }
    char tmp[32];
    size_t len = (size_t)(g_buffer - start);
    if (len >= sizeof(tmp)) len = sizeof(tmp)-1;
    memcpy(tmp, start, len); tmp[len]='\0';
    value = atoi(tmp);
    if (exp != 0) {
        if (exp < 0) exp = 0;
        value = to_int_pow10(value, exp);
    }
    Token t; t.kind=TK_NUMBER; t.line=g_line; t.attr.number=value;
    return t;
}

static Token scan_ident_or_kw() {
    const char *start = g_buffer;
    int n = 0;
    while (is_ident_body(*g_buffer)) {
        if (n < 15) n++;
        g_buffer++;
    }
    size_t total = (size_t)(g_buffer - start);
    size_t copy = total < 15 ? total : 15;
    memcpy(g_lexeme, start, copy);
    g_lexeme[copy] = '\0';

    for (int i=0; KW_TABLE[i].kw; ++i) {
        if (strncmp(g_lexeme, KW_TABLE[i].kw, 16) == 0 && total == strlen(KW_TABLE[i].kw)) {
            Token t; t.kind=KW_TABLE[i].kind; t.line=g_line; return t;
        }
    }
    Token t; t.kind=TK_IDENT; t.line=g_line; memcpy(t.attr.ident, g_lexeme, copy+1);
    return t;
}

static Token scan_char() {
    g_buffer++; // '
    Token t; t.kind=TK_ERRO; t.line=g_line;
    if (*g_buffer=='\0' || *g_buffer=='\n' || *g_buffer=='\'') return t;
    t.attr.ch = *g_buffer++;
    if (*g_buffer!='\'') return t;
    g_buffer++; // fecha '
    t.kind = TK_CHARCONST;
    return t;
}

static Token scan_comment_or_paren() {
    if (*g_buffer=='(' && *(g_buffer+1)=='*') {
        g_buffer+=2;
        while (*g_buffer) {
            if (*g_buffer=='\n') g_line++;
            if (*g_buffer=='*' && *(g_buffer+1)==')') { g_buffer+=2; break; }
            g_buffer++;
        }
        Token t; t.kind=TK_COMMENT; t.line=g_line; return t;
    } else {
        Token t; t.kind=TK_LPAR; t.line=g_line; g_buffer++; return t;
    }
}

Token pkz_next() {
    skip_ws();
    Token t; t.kind=TK_ERRO; t.line=g_line;
    if (*g_buffer=='\0') { t.kind=TK_EOS; return t; }

    if (*g_buffer=='(' && *(g_buffer+1)=='*') return scan_comment_or_paren();
    if (isdigit((unsigned char)*g_buffer)) return scan_number();
    if (is_ident_start(*g_buffer)) return scan_ident_or_kw();
    if (*g_buffer=='\'') return scan_char();

    switch (*g_buffer) {
        case '+': g_buffer++; t.kind=TK_PLUS; return t;
        case '-': g_buffer++; t.kind=TK_MINUS; return t;
        case '*': g_buffer++; t.kind=TK_STAR; return t;
        case ';': g_buffer++; t.kind=TK_SEMI; return t;
        case ',': g_buffer++; t.kind=TK_COMMA; return t;
        case '.': g_buffer++; t.kind=TK_DOT; return t;
        case '(': return scan_comment_or_paren();
        case ')': g_buffer++; t.kind=TK_RPAR; return t;
        case ':': g_buffer++; if (*g_buffer=='=') { g_buffer++; t.kind=TK_ASSIGN; } else t.kind=TK_COLON; return t;
        case '=': g_buffer++; t.kind=TK_EQ; return t;
        case '>': g_buffer++; if (*g_buffer=='=') { g_buffer++; t.kind=TK_GE; } else t.kind=TK_GT; return t;
        case '<': g_buffer++; if (*g_buffer=='=') { g_buffer++; t.kind=TK_LE; } else if (*g_buffer=='>') { g_buffer++; t.kind=TK_NE; } else t.kind=TK_LT; return t;
        default: g_buffer++; t.kind=TK_ERRO; return t;
    }
}
