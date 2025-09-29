#ifndef ANALYZER_H
#define ANALYZER_H
#include "core.h"

void pkz_accept(TokenKind expected);
void pkz_analyze();
void pkz_parse_program();

#endif // ANALYZER_H
