#!/bin/bash

echo "=== Teste do Quebra-Senhas Paralelo ==="

# Compilar o projeto
make clean
make all

if [ $? -ne 0 ]; then
    echo "Erro na compilação"
    exit 1
fi

# Testar com senha conhecida
echo "Testando com senha 'abc'..."
./coordinator "900150983cd24fb0d6963f7d28e17f72" 3 "abc" 4

if [ $? -eq 0 ] && [ -f "password_found.txt" ]; then
    echo "✓ Teste passou: Senha encontrada"
    cat password_found.txt
else
    echo "✗ Teste falhou: Senha não encontrada"
    exit 1
fi

# Limpar
rm -f password_found.txt

echo "=== Todos os testes passaram ==="
