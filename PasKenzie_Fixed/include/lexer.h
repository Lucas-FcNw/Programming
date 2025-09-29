
#ifndef LEXER_H
#define LEXER_H

#include "tokens.h"
#include <stdio.h>

void lexer_init(FILE *fonte);
TInfoAtomo obter_atomo(void);
int lexer_line(void);

#endif
