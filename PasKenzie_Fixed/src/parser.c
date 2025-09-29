
#include "parser.h"
#include "lexer.h"
#include <stdio.h>
#include <stdlib.h>

static TInfoAtomo LA; // lookahead token

static void erro_sintatico(TAtomo esperado){
    fprintf(stdout, "#  %d:erro sintatico, esperado [%s] encontrado [%s]\n",
            LA.linha, token_name(esperado), token_name(LA.atomo));
    exit(1);
}

static void print_token(const TInfoAtomo *t){
    switch(t->atomo){
        case TK_COMENTARIO:
            fprintf(stdout, "#  %d:%s\n", t->linha, token_name(t->atomo));
            break;
        case TK_IDENTIFIER:
            fprintf(stdout, "#  %d:%s : %s\n", t->linha, token_name(t->atomo), t->atributo.id);
            break;
        case TK_CONSTINT:
            fprintf(stdout, "#  %d:%s : %d\n", t->linha, token_name(t->atomo), t->atributo.numero);
            break;
        case TK_CONSTCHAR:
            fprintf(stdout, "#  %d:%s : %c\n", t->linha, token_name(t->atomo), t->atributo.ch);
            break;
        default:
            fprintf(stdout, "#  %d:%s\n", t->linha, token_name(t->atomo));
    }
}

void consome(TAtomo esperado){
    if(LA.atomo==esperado){
        print_token(&LA);
        LA = obter_atomo();
        // skip and print any comments transparently
        while(LA.atomo==TK_COMENTARIO){
            print_token(&LA);
            LA = obter_atomo();
        }
    }else{
        erro_sintatico(esperado);
    }
}

// Forward decls
static void block(void);
static void statement_part(void);
static void statement(void);
static void assignment_statement(void);
static void read_statement(void);
static void write_statement(void);
static void if_statement(void);
static void while_statement(void);
static void expression(void);
static void simple_expression(void);
static void term(void);
static void factor(void);
static int is_relop(TAtomo t);
static int is_addop(TAtomo t);
static int is_mulop(TAtomo t);

void parse_program(void){
    LA = obter_atomo();
    while(LA.atomo==TK_COMENTARIO){ print_token(&LA); LA = obter_atomo(); }

    consome(TK_PROGRAM);
    consome(TK_IDENTIFIER);
    consome(TK_SEMI);
    block();
    consome(TK_DOT);

    // after successful parse, count lines from lexer
    extern int lexer_line(void);
    int lines = lexer_line();
    fprintf(stdout, "%d linhas analisadas, programa sintaticamente correto\n", lines);
}

static void block(void){
    // <block> ::= <variable_declaration_part> <statement_part>
    // <variable_declaration_part> ::= [ var <variable_declaration> ';' { <variable_declaration> ';' } ]
    if(LA.atomo==TK_VAR){
        consome(TK_VAR);
        // first declaration
        // <variable_declaration> ::= identifier { ',' identifier } ':' <type>
        consome(TK_IDENTIFIER);
        while(LA.atomo==TK_COMMA){
            consome(TK_COMMA);
            consome(TK_IDENTIFIER);
        }
        consome(TK_COLON);
        if(LA.atomo==TK_CHAR || LA.atomo==TK_INTEGER || LA.atomo==TK_BOOLEAN){
            consome(LA.atomo);
        }else{
            erro_sintatico(TK_INTEGER); // generic expected type
        }
        consome(TK_SEMI);
        while(LA.atomo==TK_IDENTIFIER){
            consome(TK_IDENTIFIER);
            while(LA.atomo==TK_COMMA){
                consome(TK_COMMA);
                consome(TK_IDENTIFIER);
            }
            consome(TK_COLON);
            if(LA.atomo==TK_CHAR || LA.atomo==TK_INTEGER || LA.atomo==TK_BOOLEAN){
                consome(LA.atomo);
            }else{
                erro_sintatico(TK_INTEGER);
            }
            consome(TK_SEMI);
        }
    }
    statement_part();
}

static void statement_part(void){
    // <statement_part> ::= begin <statement> { ';' <statement> } end
    consome(TK_BEGIN);
    statement();
    while(LA.atomo==TK_SEMI){
        consome(TK_SEMI);
        statement();
    }
    consome(TK_END);
}

static void statement(void){
    switch(LA.atomo){
        case TK_IDENTIFIER: assignment_statement(); break;
        case TK_READ: read_statement(); break;
        case TK_WRITE: write_statement(); break;
        case TK_IF: if_statement(); break;
        case TK_WHILE: while_statement(); break;
        case TK_BEGIN: statement_part(); break;
        default: erro_sintatico(TK_IDENTIFIER);
    }
}

static void assignment_statement(void){
    // <assignment_statement> ::= identifier ':=' <expression>
    consome(TK_IDENTIFIER);
    consome(TK_ASSIGN);
    expression();
}

static void read_statement(void){
    // read '(' identifier { ',' identifier } ')'
    consome(TK_READ);
    consome(TK_LPAR);
    consome(TK_IDENTIFIER);
    while(LA.atomo==TK_COMMA){
        consome(TK_COMMA);
        consome(TK_IDENTIFIER);
    }
    consome(TK_RPAR);
}

static void write_statement(void){
    // write '(' identifier { ',' identifier } ')'
    consome(TK_WRITE);
    consome(TK_LPAR);
    consome(TK_IDENTIFIER);
    while(LA.atomo==TK_COMMA){
        consome(TK_COMMA);
        consome(TK_IDENTIFIER);
    }
    consome(TK_RPAR);
}

static void if_statement(void){
    // if <expression> then <statement> [ else <statement> ]
    consome(TK_IF);
    expression();
    consome(TK_THEN);
    statement();
    if(LA.atomo==TK_ELSE){
        consome(TK_ELSE);
        statement();
    }
}

static void while_statement(void){
    // while <expression> do <statement>
    consome(TK_WHILE);
    expression();
    consome(TK_DO);
    statement();
}

static int is_relop(TAtomo t){
    return t==TK_NE || t==TK_LT || t==TK_LE || t==TK_GE || t==TK_GT || t==TK_EQ || t==TK_OR || t==TK_AND;
}

static int is_addop(TAtomo t){
    return t==TK_PLUS || t==TK_MINUS;
}

static int is_mulop(TAtomo t){
    return t==TK_STAR || t==TK_DIV;
}

static void expression(void){
    // <expression> ::= <simple_expression> [ <relational_operator> <simple expression> ]
    simple_expression();
    if(is_relop(LA.atomo)){
        consome(LA.atomo);
        simple_expression();
    }
}

static void simple_expression(void){
    // <simple_expression> ::= <term> { <adding_operator> <term> }
    term();
    while(is_addop(LA.atomo)){
        consome(LA.atomo);
        term();
    }
}

static void term(void){
    // <term> ::= <factor> { <multiplying_operator> <factor> }
    factor();
    while(is_mulop(LA.atomo)){
        consome(LA.atomo);
        factor();
    }
}

static void factor(void){
    // <factor> ::= identifier | constint | constchar | '(' <expression> ')' | not <factor> | true | false
    switch(LA.atomo){
        case TK_IDENTIFIER: consome(TK_IDENTIFIER); break;
        case TK_CONSTINT: consome(TK_CONSTINT); break;
        case TK_CONSTCHAR: consome(TK_CONSTCHAR); break;
        case TK_LPAR: consome(TK_LPAR); expression(); consome(TK_RPAR); break;
        case TK_NOT: consome(TK_NOT); factor(); break;
        case TK_TRUE: consome(TK_TRUE); break;
        case TK_FALSE: consome(TK_FALSE); break;
        default: erro_sintatico(TK_IDENTIFIER);
    }
}
