
PasKenzie - Compilador (Fase 1: Léxico + Sintático)
===================================================

Atende ao enunciado "2025_2_trab1_lex_asdr_v3.pdf".

Como compilar (MinGW/VSCode ou terminal):
-----------------------------------------
> gcc -Wall -Wno-unused-result -g -Og src/compilador.c src/lexer.c src/parser.c src/tokens.c -Iinclude -o compilador
ou simplesmente:
> make

Como executar:
--------------
> ./compilador samples/ex1.pzk

Saída esperada (para programa correto):
---------------------------------------
- Lista todos os átomos reconhecidos no formato do PDF, incluindo comentários.
- Ao final, imprime:
  "N linhas analisadas, programa sintaticamente correto"

Erros:
------
- Em caso de erro léxico ou sintático, é impressa mensagem com a linha e
  detalhes do esperado/encontrado, e o programa termina com código de erro.

Observações de implementação:
-----------------------------
- Identificadores: máx. 15 caracteres; acima disso -> TK_ERRO.
- Palavras reservadas conforme especificação; case-sensitive.
- Comentários '(* ... *)' são tokens TK_COMENTARIO e obedecem contagem de linha.
- constint suporta notação com 'd' e 'd+': ex: 12d2, 12d+2.
- constchar aceita um caractere ASCII entre apóstrofos.

Arquivos:
---------
- include/tokens.h  : enum TAtomo e TInfoAtomo
- include/lexer.h   : interface do analisador léxico
- include/parser.h  : interface do analisador sintático
- src/tokens.c      : nomes dos tokens (para impressão)
- src/lexer.c       : implementação do léxico (obter_atomo)
- src/parser.c      : implementação do sintático (consome e gramática)
- src/compilador.c  : main
- samples/ex1.pzk   : exemplo do PDF
