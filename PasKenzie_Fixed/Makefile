
CC=gcc
CFLAGS=-Wall -Wno-unused-result -g -Og
INCLUDE=-Iinclude

SRC=src/compilador.c src/lexer.c src/parser.c src/tokens.c
OBJ=$(SRC:.c=.o)

compilador: $(OBJ)
	$(CC) $(CFLAGS) -o $@ $(OBJ)

%.o: %.c
	$(CC) $(CFLAGS) $(INCLUDE) -c $< -o $@

clean:
	rm -f src/*.o compilador
