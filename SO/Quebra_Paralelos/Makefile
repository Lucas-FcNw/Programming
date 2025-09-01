CC = gcc
CFLAGS = -Wall -Wextra -std=c99
LDFLAGS = -lcrypto

SRC_DIR = src
BIN_DIR = .
TESTS_DIR = tests

all: coordinator worker

coordinator: $(SRC_DIR)/coordinator.c $(SRC_DIR)/hash_utils.o
	$(CC) $(CFLAGS) -o $(BIN_DIR)/coordinator $(SRC_DIR)/coordinator.c $(SRC_DIR)/hash_utils.o $(LDFLAGS)

worker: $(SRC_DIR)/worker.c $(SRC_DIR)/hash_utils.o
	$(CC) $(CFLAGS) -o $(BIN_DIR)/worker $(SRC_DIR)/worker.c $(SRC_DIR)/hash_utils.o $(LDFLAGS)

$(SRC_DIR)/hash_utils.o: $(SRC_DIR)/hash_utils.c $(SRC_DIR)/hash_utils.h
	$(CC) $(CFLAGS) -c $(SRC_DIR)/hash_utils.c -o $(SRC_DIR)/hash_utils.o

test_hash: $(SRC_DIR)/test_hash.c $(SRC_DIR)/hash_utils.o
	$(CC) $(CFLAGS) -o $(BIN_DIR)/test_hash $(SRC_DIR)/test_hash.c $(SRC_DIR)/hash_utils.o $(LDFLAGS)

clean:
	rm -f $(BIN_DIR)/coordinator $(BIN_DIR)/worker $(BIN_DIR)/test_hash $(SRC_DIR)/*.o password_found.txt

.PHONY: all clean test
