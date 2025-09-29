# Compilador a ser usado
CC = gcc

# Flags de compilação: -Wall (todos os warnings), -g (para debug)
# Adicionamos o caminho para a pasta "include" aqui
CFLAGS = -Wall -g -Iinclude

# Nome do executável final
TARGET = compilador

# Diretórios
SRC_DIR = src
# É uma boa prática colocar os arquivos objeto (.o) em sua própria pasta
OBJ_DIR = obj

# Encontra automaticamente todos os arquivos .c na pasta src
SOURCES = $(wildcard $(SRC_DIR)/*.c)

# Gera os nomes dos arquivos objeto, colocando-os na pasta obj
OBJECTS = $(SOURCES:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)

# A regra principal (default), que é chamada quando você digita "make"
all: $(TARGET)

# Regra para "linkar" o executável final a partir dos arquivos objeto
$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJECTS)

# Regra para compilar um arquivo .c da pasta src para um arquivo .o na pasta obj
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

# Regra para limpar o projeto (apagar executável e arquivos objeto)
clean:
	rm -rf $(OBJ_DIR) $(TARGET)