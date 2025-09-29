
#include "lexer.h"
#include <ctype.h>
#include <string.h>

static FILE *g_src = NULL;
static int g_line = 1;
static int g_look = EOF;   // one-char lookahead

static int nextc(void){
    int c = fgetc(g_src);
    return c;
}
static void unread(int c){
    if(c!=EOF) ungetc(c, g_src);
}

static int is_ident_start(int c){
    return (c=='_' || (c>='a'&&c<='z') || (c>='A'&&c<='Z'));
}
static int is_ident_char(int c){
    return is_ident_start(c) || isdigit(c);
}

static void skip_ws(void){
    int c;
    while(1){
        c = nextc();
        if(c==' ' || c=='\t' || c=='\r'){
            continue;
        }else if(c=='\n'){
            g_line++;
        }else{
            unread(c);
            return;
        }
    }
}

// Comments: (* ... *)
static int try_comment(TInfoAtomo *t){
    int c1 = nextc();
    if(c1!='('){ unread(c1); return 0; }
    int c2 = nextc();
    if(c2!='*'){ unread(c2); unread(c1); return 0; }

    // we have a comment
    int prev=' ';
    int c;
    while( (c=nextc())!=EOF ){
        if(c=='\n') g_line++;
        if(prev=='*' && c==')'){
            // end of comment
            t->atomo = TK_COMENTARIO;
            t->linha = g_line;
            return 1;
        }
        prev = c;
    }
    // EOF before end: lexical error
    t->atomo = TK_ERRO;
    t->linha = g_line;
    return 1;
}

static int read_constchar(TInfoAtomo *t){
    int c = nextc(); // should be '
    if(c!='\''){ unread(c); return 0; }
    int ch = nextc();
    int close = nextc();
    if(close!='\''){
        t->atomo = TK_ERRO;
        t->linha = g_line;
        if(close=='\n') g_line++;
        else if(close!=EOF) unread(close);
        return 1;
    }
    t->atomo = TK_CONSTCHAR;
    t->linha = g_line;
    t->atributo.ch = (char)ch;
    return 1;
}

// constint: digito+((d(+|ε)digito+)|ε)
// Examples: 1, 000, 124, 12d2, 12d+2
static int read_number(TInfoAtomo *t, int first){
    char buf[64];
    int len=0;
    buf[len++] = (char)first;
    int c;

    // more digits
    while( (c=nextc())!=EOF && isdigit(c) ){
        if(len< (int)sizeof(buf)-1) buf[len++] = (char)c;
    }

    if(c=='d'){
        buf[len++] = 'd';
        c = nextc();
        if(c=='+'){
            buf[len++] = '+';
            c = nextc();
        }
        if(!isdigit(c)){
            // malformed exponent
            t->atomo = TK_ERRO;
            t->linha = g_line;
            if(c!=EOF) unread(c);
            return 1;
        }
        // digits of exponent
        while(c!=EOF && isdigit(c)){
            if(len< (int)sizeof(buf)-1) buf[len++] = (char)c;
            c = nextc();
        }
    }
    if(c!=EOF) unread(c);
    buf[len]=0;

    // convert buf to integer value with 'd' exponent base 10
    // split at 'd' if present
    int base=0, exp=0, hasExp=0, i=0, sign=1;
    while(buf[i] && buf[i]!='d'){ base = base*10 + (buf[i]-'0'); i++; }
    if(buf[i]=='d'){
        hasExp=1; i++;
        if(buf[i]=='+'){ sign=1; i++; }
        // no minus in spec
        while(buf[i]){ exp = exp*10 + (buf[i]-'0'); i++; }
    }
    long long val=base;
    if(hasExp){
        for(int k=0;k<exp;k++) val*=10;
    }
    t->atomo = TK_CONSTINT;
    t->linha = g_line;
    t->atributo.numero = (int)val;
    return 1;
}

static int read_ident_or_kw(TInfoAtomo *t, int first){
    char buf[64];
    int len=0;
    buf[len++]=(char)first;
    int c;
    while( (c=nextc())!=EOF && is_ident_char(c)){
        if(len< (int)sizeof(buf)-1) buf[len++]=(char)c;
    }
    if(c!=EOF) unread(c);
    buf[len]=0;

    // identifier length limit 15
    if(len>15){
        t->atomo = TK_ERRO;
        t->linha = g_line;
        return 1;
    }

    // keywords (lowercase only, case-sensitive)
    #define KW(eq, tok) if(strcmp(buf, eq)==0){ t->atomo=tok; t->linha=g_line; return 1; }
    KW("program", TK_PROGRAM)
    KW("var", TK_VAR)
    KW("begin", TK_BEGIN)
    KW("end", TK_END)
    KW("read", TK_READ)
    KW("write", TK_WRITE)
    KW("if", TK_IF)
    KW("then", TK_THEN)
    KW("else", TK_ELSE)
    KW("while", TK_WHILE)
    KW("do", TK_DO)
    KW("char", TK_CHAR)
    KW("integer", TK_INTEGER)
    KW("boolean", TK_BOOLEAN)
    KW("true", TK_TRUE)
    KW("false", TK_FALSE)
    KW("div", TK_DIV)
    KW("or", TK_OR)
    KW("and", TK_AND)
    KW("not", TK_NOT)
    #undef KW

    // identifier
    t->atomo = TK_IDENTIFIER;
    t->linha = g_line;
    strncpy(t->atributo.id, buf, sizeof(t->atributo.id));
    t->atributo.id[sizeof(t->atributo.id)-1] = 0;
    return 1;
}

void lexer_init(FILE *fonte){
    g_src = fonte;
    g_line = 1;
    g_look = EOF;
}

int lexer_line(void){ return g_line; }

TInfoAtomo obter_atomo(void){
    TInfoAtomo t; memset(&t,0,sizeof(t));
    skip_ws();

    // try comment (must be returned to parser)
    if(try_comment(&t)) return t;

    int c = nextc();
    if(c==EOF){ t.atomo=TK_EOF; t.linha=g_line; return t; }

    // single-quoted char?
    if(c=='\''){ unread(c); if(read_constchar(&t)) return t; }

    // number?
    if(isdigit(c)){ if(read_number(&t, c)) return t; }

    // identifier / keyword?
    if(is_ident_start(c)){ if(read_ident_or_kw(&t, c)) return t; }

    // operators / punctuation
    switch(c){
        case '+': t.atomo=TK_PLUS; t.linha=g_line; return t;
        case '-': t.atomo=TK_MINUS; t.linha=g_line; return t;
        case '*': t.atomo=TK_STAR; t.linha=g_line; return t;
        case ';': t.atomo=TK_SEMI; t.linha=g_line; return t;
        case ',': t.atomo=TK_COMMA; t.linha=g_line; return t;
        case '.': t.atomo=TK_DOT; t.linha=g_line; return t;
        case '(': t.atomo=TK_LPAR; t.linha=g_line; return t;
        case ')': t.atomo=TK_RPAR; t.linha=g_line; return t;
        case ':': {
            int d = nextc();
            if(d=='='){ t.atomo=TK_ASSIGN; t.linha=g_line; return t; }
            unread(d);
            t.atomo=TK_COLON; t.linha=g_line; return t;
        }
        case '=': t.atomo=TK_EQ; t.linha=g_line; return t;
        case '<': {
            int d = nextc();
            if(d=='>'){ t.atomo=TK_NE; t.linha=g_line; return t; }
            if(d=='='){ t.atomo=TK_LE; t.linha=g_line; return t; }
            unread(d);
            t.atomo=TK_LT; t.linha=g_line; return t;
        }
        case '>': {
            int d = nextc();
            if(d=='='){ t.atomo=TK_GE; t.linha=g_line; return t; }
            unread(d);
            t.atomo=TK_GT; t.linha=g_line; return t;
        }
        default:
            t.atomo=TK_ERRO; t.linha=g_line; return t;
    }
}
