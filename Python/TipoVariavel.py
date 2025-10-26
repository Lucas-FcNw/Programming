print('Teste')
pi = 3.14
raio = 5 
area = pi * raio ** 2
print(area)

#! Tipos de print

print('Ele disse "Olá"')     # aspas simples para permitir a aparição de aspas duplas

texto = """ \n Linha 1 
Linha 2 
Linha 3
"""

print(texto)

codigo = 10
salario = 2500.50
nome = 'Harry Guzman'
situacao = True

tipo = type(salario)

#? O f"" chamado de f-string é o que permite me python usar texto e comando em um print.
#! Uma forma de colocar mais de 1 comando em uma unica linha 

# print(f"{type(salario)}, {salario:.2f} e {type(codigo)}, {codigo}")
#* f-sring só executa o que está dentro de {} o resto sai como texto

"""
===== USANDO IDENTIFICADORES (MÁSCARAS) COM %d, %i, %f, %s =====

Esses são os IDENTIFICADORES (ou máscaras) da sintaxe antiga do Python:
%d ou %i  → int (inteiro)
%f        → float (decimal)
%s        → string (texto)

ANTES (sem identificadores - espaços automáticos):
"""
print(salario, tipo )

"""
AGORA (com identificadores - você controla tudo):
%d substitui o valor inteiro (codigo)
%f substitui o valor decimal (salario)
%s substitui o texto (nome)

Esse % depois de aspas ativa o modo de SUBSTITUIÇÃO!
"""
print("\ncódigo: %d, Nome: %s, salário atual de: %.2f" % (codigo, nome, salario))

"""
EXPLICAÇÃO DO CÓDIGO ACIMA:
print("texto com %d %s %.2f" % (valor1, valor2, valor3))
        ↓         ↓   ↓    ↓                          ↓
     string    int  str float                    tupla com valores

%.2f = float com 2 casas decimais (2500.50 não fica 2500.5)
%d = inteiro (10 apenas)
%s = string/texto (Harry Guzman como está)

A ORDEM IMPORTA! %d pega o PRIMEIRO valor da tupla (codigo)
                  %s pega o SEGUNDO valor da tupla (nome)
                  %.2f pega o TERCEIRO valor da tupla (salario)
"""

#! Versão f-string que permite tirar os espaços automáticos da vírgula , e permite usar o numero de casas decimais totais sem ignorar o zero final
#TODO print(f"\nCódigo: {codigo}, Nome: {nome}, Salário atual de: {salario:.2f}")

"""
===== COMPARAÇÃO: 3 FORMAS DE FAZER A MESMA COISA =====

1️⃣ COM VÍRGULAS (espaços automáticos - RUIM):
print("Código:", codigo, "Nome:", nome, "salário:", salario)
Resultado: Código: 10 Nome: Harry Guzman salário: 2500.5
❌ Espaços extras, sem controle

2️⃣ COM IDENTIFICADORES % (ANTIGO - mas funciona):
print("Código: %d, Nome: %s, salário: %.2f" % (codigo, nome, salario))
Resultado: Código: 10, Nome: Harry Guzman, salário: 2500.50
✅ Controle total, mas sintaxe estranha

3️⃣ COM f-string (MODERNO - RECOMENDADO ✅✅✅):
print(f"Código: {codigo}, Nome: {nome}, Salário: R$ {salario:.2f}")
Resultado: Código: 10, Nome: Harry Guzman, Salário: R$ 2500.50
✅ Controle total, sintaxe clara e moderna
"""

# TODO MELHOR USAR F-STRING INVÉS DE IDENTIFICADORES % DENTRO DE PRINTS (são antigos e menos legíveis)