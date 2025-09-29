#include "../include/analyzer.h"
#include "../include/scanner.h"

static void parse_block();
static void parse_var_section();
static void parse_decl();
static void parse_type_spec();
static void parse_stmt_section();
static void parse_stmt();
static void parse_assign();
static void parse_read();
static void parse_write();
static void parse_if();
static void parse_while();
static void parse_expr();
static void parse_simple_expr();
static void parse_term();
static void parse_factor();
static void parse_relop();
static void parse_addop();
static void parse_mulop();

void pkz_accept(TokenKind expected) {
    if (g_la == expected) {
        if (g_la == TK_IDENT) {
            printf("\n# %2d:identifier : %s", g_tok.line, g_tok.attr.ident);
        } else {
            printf("\n# %2d:%s", g_tok.line, pkz_tok_name(g_la));
        }
        g_tok = pkz_next();
        g_la  = g_tok.kind;
    } else {
        fprintf(stderr, "\n# %2d:Erro sintatico: esperado [%s] encontrado [%s]\n",
                g_tok.line, pkz_tok_name(expected), pkz_tok_name(g_la));
        exit(1);
    }
}

void pkz_parse_program() {
    if (g_la == TK_COMMENT) pkz_accept(TK_COMMENT);
    pkz_accept(TK_PROGRAM);
    pkz_accept(TK_IDENT);
    pkz_accept(TK_SEMI);
    parse_block();
    pkz_accept(TK_DOT);
    if (g_la == TK_COMMENT) pkz_accept(TK_COMMENT);
}

static void parse_block() {
    parse_var_section();
    parse_stmt_section();
}

static void parse_var_section() {
    if (g_la == TK_VAR) {
        pkz_accept(TK_VAR);
        parse_decl();
        pkz_accept(TK_SEMI);
        while (g_la == TK_IDENT) { parse_decl(); pkz_accept(TK_SEMI); }
    }
}

static void parse_decl() {
    pkz_accept(TK_IDENT);
    while (g_la == TK_COMMA) { pkz_accept(TK_COMMA); pkz_accept(TK_IDENT); }
    pkz_accept(TK_COLON);
    parse_type_spec();
}

static void parse_type_spec() {
    if (g_la==TK_INTEGER || g_la==TK_BOOLEAN || g_la==TK_CHAR) {
        pkz_accept(g_la);
    } else {
        fprintf(stderr, "\n#%2d:Erro sintatico: type esperado\n", g_tok.line);
        exit(1);
    }
}

static void parse_stmt_section() {
    pkz_accept(TK_BEGIN);
    parse_stmt();
    while (g_la == TK_SEMI) { pkz_accept(TK_SEMI); parse_stmt(); }
    pkz_accept(TK_END);
}

static void parse_stmt() {
    if (g_la == TK_COMMENT) pkz_accept(TK_COMMENT);

    switch (g_la) {
        case TK_IDENT:  parse_assign(); break;
        case TK_READ:   parse_read();   break;
        case TK_WRITE:  parse_write();  break;
        case TK_IF:     parse_if();     break;
        case TK_WHILE:  parse_while();  break;
        default:        parse_stmt_section(); break;
    }

    if (g_la == TK_COMMENT) pkz_accept(TK_COMMENT);
}

static void parse_assign() {
    pkz_accept(TK_IDENT);
    pkz_accept(TK_ASSIGN);
    parse_expr();
}

static void parse_read() {
    pkz_accept(TK_READ);
    pkz_accept(TK_LPAR);
    pkz_accept(TK_IDENT);
    while (g_la == TK_COMMA) { pkz_accept(TK_COMMA); pkz_accept(TK_IDENT); }
    pkz_accept(TK_RPAR);
}

static void parse_write() {
    pkz_accept(TK_WRITE);
    pkz_accept(TK_LPAR);
    pkz_accept(TK_IDENT);
    while (g_la == TK_COMMA) { pkz_accept(TK_COMMA); pkz_accept(TK_IDENT); }
    pkz_accept(TK_RPAR);
}

static void parse_if() {
    pkz_accept(TK_IF);
    parse_expr();
    pkz_accept(TK_THEN);
    parse_stmt();
    if (g_la == TK_ELSE) { pkz_accept(TK_ELSE); parse_stmt(); }
}

static void parse_while() {
    pkz_accept(TK_WHILE);
    parse_expr();
    pkz_accept(TK_DO);
    parse_stmt();
}

static void parse_expr() {
    parse_simple_expr();
    if (g_la==TK_EQ || g_la==TK_NE || g_la==TK_LT || g_la==TK_LE ||
        g_la==TK_GT || g_la==TK_GE || g_la==TK_AND || g_la==TK_OR) {
        parse_relop();
        parse_simple_expr();
    }
}

static void parse_simple_expr() {
    parse_term();
    while (g_la==TK_PLUS || g_la==TK_MINUS) { parse_addop(); parse_term(); }
}

static void parse_term() {
    parse_factor();
    while (g_la==TK_STAR || g_la==TK_DIV) { parse_mulop(); parse_factor(); }
}

static void parse_factor() {
    if (g_la==TK_IDENT || g_la==TK_NUMBER || g_la==TK_CHARCONST ||
        g_la==TK_TRUE || g_la==TK_FALSE) {
        pkz_accept(g_la);
    } else if (g_la == TK_LPAR) {
        pkz_accept(TK_LPAR);
        parse_expr();
        pkz_accept(TK_RPAR);
    } else if (g_la == TK_NOT) {
        pkz_accept(TK_NOT);
        parse_factor();
    } else {
        fprintf(stderr, "\n#%2d:Erro sintatico: fator invalido\n", g_tok.line);
        exit(1);
    }
}

static void parse_relop()  { pkz_accept(g_la); }
static void parse_addop()  { pkz_accept(g_la); }
static void parse_mulop()  { pkz_accept(g_la); }

void pkz_analyze() {
    pkz_parse_program();
    if (g_la != TK_EOS) {
        fprintf(stderr, "\n# %2d:Erro sintático: codigo extra após o fim do program\n", g_tok.line);
        exit(1);
    }
    printf("\n%d linhas analisadas, programa sintaticamente correto\n", g_tok.line);
}
