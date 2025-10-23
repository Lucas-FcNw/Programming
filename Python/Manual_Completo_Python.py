 # ============================================================================
# MANUAL COMPLETO DE PYTHON - DO BÁSICO AO AVANÇADO
# ============================================================================

# ============================================================================
# 1. CONCEITOS BÁSICOS
# ============================================================================
# ! 
# *
# *
# ?
# TODO:


# 1.1 Variáveis e Tipos de Dados
# --------------------------------

# Variáveis não precisam de declaração de tipo
nome = "Python"  # String
idade = 30  # Integer
altura = 1.75  # Float
ativo = True  # Boolean
nada = None  # NoneType

# Verificar tipo de variável
print(type(nome))  # <class 'str'>

# 1.2 Operadores
# --------------------------------

# Operadores Aritméticos
soma = 10 + 5  # Adição
subtracao = 10 - 5  # Subtração
multiplicacao = 10 * 5  # Multiplicação
divisao = 10 / 5  # Divisão (retorna float)
divisao_inteira = 10 // 3  # Divisão inteira
resto = 10 % 3  # Módulo (resto da divisão)
potencia = 2 ** 3  # Exponenciação

# Operadores de Comparação
igual = (5 == 5)  # True
diferente = (5 != 3)  # True
maior = (5 > 3)  # True
menor = (3 < 5)  # True
maior_igual = (5 >= 5)  # True
menor_igual = (3 <= 5)  # True

# Operadores Lógicos
e_logico = True and False  # False
ou_logico = True or False  # True
negacao = not True  # False

# 1.3 Strings
# --------------------------------

texto = "Python é incrível!"

# Concatenação
saudacao = "Olá" + " " + "Mundo"

# Formatação de strings
nome = "João"
idade = 25
# f-strings (Python 3.6+)
mensagem = f"Meu nome é {nome} e tenho {idade} anos"
# format()
mensagem2 = "Meu nome é {} e tenho {} anos".format(nome, idade)
# Operador %
mensagem3 = "Meu nome é %s e tenho %d anos" % (nome, idade)

# Métodos de string
texto_maiusculo = texto.upper()  # PYTHON É INCRÍVEL!
texto_minusculo = texto.lower()  # python é incrível!
texto_titulo = texto.title()  # Python É Incrível!
texto_sem_espacos = "  texto  ".strip()  # Remove espaços das extremidades
texto_substituido = texto.replace("incrível", "fantástico")
texto_dividido = texto.split()  # Divide em lista de palavras
inicio = texto.startswith("Python")  # True
fim = texto.endswith("!")  # True

# Slicing (fatiamento)
palavra = "Python"
print(palavra[0])  # P (primeiro caractere)
print(palavra[-1])  # n (último caractere)
print(palavra[0:3])  # Pyt (do índice 0 ao 2)
print(palavra[::2])  # Pto (a cada 2 caracteres)
print(palavra[::-1])  # noht (inverte a string)

# ============================================================================
# 2. ESTRUTURAS DE DADOS
# ============================================================================

# 2.1 Listas
# --------------------------------

# Criação de listas
frutas = ["maçã", "banana", "laranja"]
numeros = [1, 2, 3, 4, 5]
mista = [1, "texto", True, 3.14]

# Métodos de lista
frutas.append("uva")  # Adiciona no final
frutas.insert(1, "morango")  # Adiciona em posição específica
frutas.remove("banana")  # Remove item específico
ultimo = frutas.pop()  # Remove e retorna o último item
primeiro = frutas.pop(0)  # Remove e retorna item do índice 0
frutas.sort()  # Ordena a lista
frutas.reverse()  # Inverte a lista
tamanho = len(frutas)  # Retorna tamanho da lista
frutas.clear()  # Limpa a lista

# Compreensão de lista (List Comprehension)
quadrados = [x**2 for x in range(10)]  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
pares = [x for x in range(20) if x % 2 == 0]  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# 2.2 Tuplas
# --------------------------------

# Tuplas são imutáveis (não podem ser alteradas)
coordenadas = (10, 20)
cores = ("vermelho", "verde", "azul")

# Desempacotamento
x, y = coordenadas
r, g, b = cores

# Métodos de tupla
contagem = cores.count("vermelho")  # Conta ocorrências
indice = cores.index("verde")  # Retorna índice do elemento

# 2.3 Dicionários
# --------------------------------

# Criação de dicionários
pessoa = {
    "nome": "João",
    "idade": 30,
    "cidade": "São Paulo"
}

# Acessar valores
nome = pessoa["nome"]
idade = pessoa.get("idade")  # Mais seguro, retorna None se não existir
cidade = pessoa.get("estado", "Não informado")  # Valor padrão

# Modificar e adicionar
pessoa["idade"] = 31
pessoa["profissao"] = "Desenvolvedor"

# Métodos de dicionário
chaves = pessoa.keys()  # Retorna as chaves
valores = pessoa.values()  # Retorna os valores
itens = pessoa.items()  # Retorna pares chave-valor
pessoa.update({"telefone": "123456"})  # Atualiza/adiciona múltiplos itens
profissao = pessoa.pop("profissao")  # Remove e retorna valor
pessoa.clear()  # Limpa o dicionário

# Compreensão de dicionário
quadrados_dict = {x: x**2 for x in range(5)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 2.4 Conjuntos (Sets)
# --------------------------------

# Conjuntos não permitem duplicatas e não são ordenados
numeros_set = {1, 2, 3, 4, 5}
frutas_set = {"maçã", "banana", "laranja"}

# Métodos de conjunto
numeros_set.add(6)  # Adiciona elemento
numeros_set.remove(1)  # Remove elemento (erro se não existir)
numeros_set.discard(10)  # Remove elemento (sem erro se não existir)

# Operações de conjunto
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
uniao = a | b  # {1, 2, 3, 4, 5, 6}
intersecao = a & b  # {3, 4}
diferenca = a - b  # {1, 2}
diferenca_simetrica = a ^ b  # {1, 2, 5, 6}

# ============================================================================
# 3. ESTRUTURAS DE CONTROLE
# ============================================================================

# 3.1 Condicionais (if, elif, else)
# --------------------------------
# * O if é um avaliador, se no if a condição for verdade ele executa o que vem depois do :
idade = 18

if idade < 18:
    print("Menor de idade")
elif idade == 18:
    print("Tem 18 anos")
else:
    print("Maior de idade")

# Operador ternário
status = "Adulto" if idade >= 18 else "Criança"

# 3.2 Loops (for, while)
# --------------------------------

# Loop for
for i in range(5):  # 0 a 4
    print(i)

for i in range(2, 10, 2):  # De 2 a 9, pulando de 2 em 2
    print(i)

# Iterando sobre listas
frutas = ["maçã", "banana", "laranja"]
for fruta in frutas:
    print(fruta)

# Enumerate (obtém índice e valor)
for indice, fruta in enumerate(frutas):
    print(f"{indice}: {fruta}")

# Zip (itera sobre múltiplas listas simultaneamente)
nomes = ["João", "Maria", "Pedro"]
idades = [25, 30, 35]
for nome, idade in zip(nomes, idades):
    print(f"{nome} tem {idade} anos")

# Loop while
contador = 0
while contador < 5:
    print(contador)
    contador += 1

# Break e Continue
for i in range(10):
    if i == 3:
        continue  # Pula para próxima iteração
    if i == 7:
        break  # Sai do loop
    print(i)

# Loop com else (executado se não houver break)
for i in range(5):
    print(i)
else:
    print("Loop concluído sem break")

# ============================================================================
# 4. FUNÇÕES
# ============================================================================

# 4.1 Definição básica
# --------------------------------

def saudacao():
    """Função simples sem parâmetros"""
    print("Olá, Mundo!")

saudacao()

# 4.2 Funções com parâmetros
# --------------------------------

def saudar_pessoa(nome, idade):
    """Função com parâmetros posicionais"""
    return f"Olá, {nome}! Você tem {idade} anos."

mensagem = saudar_pessoa("João", 30)

# Parâmetros com valores padrão
def criar_perfil(nome, idade=18, cidade="São Paulo"):
    return f"{nome}, {idade} anos, {cidade}"

perfil1 = criar_perfil("Maria")
perfil2 = criar_perfil("João", 25)
perfil3 = criar_perfil("Pedro", cidade="Rio de Janeiro")

# 4.3 *args e **kwargs
# --------------------------------

# *args - aceita qualquer número de argumentos posicionais
def somar(*numeros):
    total = 0
    for num in numeros:
        total += num
    return total

resultado = somar(1, 2, 3, 4, 5)  # 15

# **kwargs - aceita qualquer número de argumentos nomeados
def exibir_info(**info):
    for chave, valor in info.items():
        print(f"{chave}: {valor}")

exibir_info(nome="João", idade=30, cidade="SP")

# 4.4 Funções Lambda
# --------------------------------

# Funções anônimas de uma linha
quadrado = lambda x: x ** 2
soma = lambda a, b: a + b

print(quadrado(5))  # 25
print(soma(3, 7))  # 10

# Uso com map, filter, reduce
numeros = [1, 2, 3, 4, 5]
quadrados = list(map(lambda x: x**2, numeros))  # [1, 4, 9, 16, 25]
pares = list(filter(lambda x: x % 2 == 0, numeros))  # [2, 4]

from functools import reduce
produto = reduce(lambda x, y: x * y, numeros)  # 120

# 4.5 Decoradores
# --------------------------------

def meu_decorador(funcao):
    """Decorador básico"""
    def wrapper(*args, **kwargs):
        print("Antes da função")
        resultado = funcao(*args, **kwargs)
        print("Depois da função")
        return resultado
    return wrapper

@meu_decorador
def dizer_ola(nome):
    print(f"Olá, {nome}!")

dizer_ola("João")

# Decorador com parâmetros
def repetir(vezes):
    def decorador(funcao):
        def wrapper(*args, **kwargs):
            for _ in range(vezes):
                funcao(*args, **kwargs)
        return wrapper
    return decorador

@repetir(3)
def saudar():
    print("Olá!")

saudar()

# ============================================================================
# 5. PROGRAMAÇÃO ORIENTADA A OBJETOS (POO)
# ============================================================================

# 5.1 Classes e Objetos
# --------------------------------

class Pessoa:
    """Classe básica representando uma pessoa"""
    
    # Atributo de classe (compartilhado por todas as instâncias)
    especie = "Homo sapiens"
    
    def __init__(self, nome, idade):
        """Construtor - inicializa a instância"""
        self.nome = nome  # Atributo de instância
        self.idade = idade
    
    def apresentar(self):
        """Método de instância"""
        return f"Olá, meu nome é {self.nome} e tenho {self.idade} anos"
    
    def fazer_aniversario(self):
        """Método que modifica atributo"""
        self.idade += 1
    
    @classmethod
    def criar_anonimo(cls):
        """Método de classe - cria instância padrão"""
        return cls("Anônimo", 0)
    
    @staticmethod
    def eh_maior_idade(idade):
        """Método estático - não acessa instância ou classe"""
        return idade >= 18

# Criando objetos
pessoa1 = Pessoa("João", 30)
pessoa2 = Pessoa("Maria", 25)

print(pessoa1.apresentar())
pessoa1.fazer_aniversario()
print(pessoa1.idade)  # 31

pessoa_anonima = Pessoa.criar_anonimo()
print(Pessoa.eh_maior_idade(20))  # True

# 5.2 Herança
# --------------------------------

class Estudante(Pessoa):
    """Classe que herda de Pessoa"""
    
    def __init__(self, nome, idade, matricula):
        super().__init__(nome, idade)  # Chama construtor da classe pai
        self.matricula = matricula
    
    def apresentar(self):
        """Sobrescrita de método (override)"""
        return f"{super().apresentar()} e sou estudante (matrícula: {self.matricula})"

estudante = Estudante("Pedro", 20, "2024001")
print(estudante.apresentar())

# 5.3 Encapsulamento
# --------------------------------

class ContaBancaria:
    """Demonstra encapsulamento com atributos privados"""
    
    def __init__(self, titular, saldo_inicial=0):
        self.titular = titular
        self.__saldo = saldo_inicial  # Atributo privado (convenção com __)
    
    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            return True
        return False
    
    def sacar(self, valor):
        if 0 < valor <= self.__saldo:
            self.__saldo -= valor
            return True
        return False
    
    @property
    def saldo(self):
        """Property - acesso controlado ao saldo"""
        return self.__saldo
    
    @saldo.setter
    def saldo(self, valor):
        """Setter - validação ao definir saldo"""
        if valor >= 0:
            self.__saldo = valor

conta = ContaBancaria("João", 1000)
conta.depositar(500)
print(conta.saldo)  # 1500

# 5.4 Polimorfismo
# --------------------------------

class Animal:
    def fazer_som(self):
        pass

class Cachorro(Animal):
    def fazer_som(self):
        return "Au au!"

class Gato(Animal):
    def fazer_som(self):
        return "Miau!"

# Polimorfismo em ação
animais = [Cachorro(), Gato(), Cachorro()]
for animal in animais:
    print(animal.fazer_som())

# 5.5 Métodos Especiais (Dunder Methods)
# --------------------------------

class Ponto:
    """Demonstra uso de métodos especiais"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        """Representação legível para humanos"""
        return f"Ponto({self.x}, {self.y})"
    
    def __repr__(self):
        """Representação para desenvolvedores"""
        return f"Ponto(x={self.x}, y={self.y})"
    
    def __add__(self, outro):
        """Sobrecarga do operador +"""
        return Ponto(self.x + outro.x, self.y + outro.y)
    
    def __eq__(self, outro):
        """Sobrecarga do operador =="""
        return self.x == outro.x and self.y == outro.y
    
    def __len__(self):
        """Retorna comprimento"""
        return int((self.x**2 + self.y**2)**0.5)

p1 = Ponto(3, 4)
p2 = Ponto(1, 2)
p3 = p1 + p2  # Usa __add__
print(p3)  # Usa __str__

# ============================================================================
# 6. MANIPULAÇÃO DE ARQUIVOS
# ============================================================================

# 6.1 Leitura de arquivos
# --------------------------------

# Modo 'r' - leitura (padrão)
# Usar 'with' garante fechamento automático do arquivo
with open('arquivo.txt', 'r', encoding='utf-8') as arquivo:
    conteudo = arquivo.read()  # Lê todo o conteúdo
    print(conteudo)

with open('arquivo.txt', 'r', encoding='utf-8') as arquivo:
    linha = arquivo.readline()  # Lê uma linha
    print(linha)

with open('arquivo.txt', 'r', encoding='utf-8') as arquivo:
    linhas = arquivo.readlines()  # Lê todas as linhas em uma lista
    for linha in linhas:
        print(linha.strip())  # Remove quebras de linha

# Iterando sobre o arquivo
with open('arquivo.txt', 'r', encoding='utf-8') as arquivo:
    for linha in arquivo:
        print(linha.strip())

# 6.2 Escrita em arquivos
# --------------------------------

# Modo 'w' - escrita (sobrescreve o arquivo)
with open('saida.txt', 'w', encoding='utf-8') as arquivo:
    arquivo.write("Primeira linha\n")
    arquivo.write("Segunda linha\n")

# Modo 'a' - append (adiciona ao final do arquivo)
with open('saida.txt', 'a', encoding='utf-8') as arquivo:
    arquivo.write("Linha adicional\n")

# Escrevendo múltiplas linhas
linhas = ["Linha 1\n", "Linha 2\n", "Linha 3\n"]
with open('saida.txt', 'w', encoding='utf-8') as arquivo:
    arquivo.writelines(linhas)

# 6.3 Trabalhando com JSON
# --------------------------------

import json

# Escrevendo JSON
dados = {
    "nome": "João",
    "idade": 30,
    "hobbies": ["leitura", "programação"]
}

with open('dados.json', 'w', encoding='utf-8') as arquivo:
    json.dump(dados, arquivo, indent=4, ensure_ascii=False)

# Lendo JSON
with open('dados.json', 'r', encoding='utf-8') as arquivo:
    dados_lidos = json.load(arquivo)
    print(dados_lidos)

# Conversão entre JSON e string
json_string = json.dumps(dados, indent=2)
dados_de_string = json.loads(json_string)

# 6.4 Trabalhando com CSV
# --------------------------------

import csv

# Escrevendo CSV
with open('dados.csv', 'w', newline='', encoding='utf-8') as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(['Nome', 'Idade', 'Cidade'])
    escritor.writerow(['João', 30, 'São Paulo'])
    escritor.writerow(['Maria', 25, 'Rio de Janeiro'])

# Lendo CSV
with open('dados.csv', 'r', encoding='utf-8') as arquivo:
    leitor = csv.reader(arquivo)
    for linha in leitor:
        print(linha)

# Usando DictReader e DictWriter
with open('dados.csv', 'w', newline='', encoding='utf-8') as arquivo:
    campos = ['nome', 'idade', 'cidade']
    escritor = csv.DictWriter(arquivo, fieldnames=campos)
    escritor.writeheader()
    escritor.writerow({'nome': 'Pedro', 'idade': 35, 'cidade': 'Brasília'})

with open('dados.csv', 'r', encoding='utf-8') as arquivo:
    leitor = csv.DictReader(arquivo)
    for linha in leitor:
        print(linha['nome'], linha['idade'])

# ============================================================================
# 7. TRATAMENTO DE EXCEÇÕES
# ============================================================================

# 7.1 Try-Except básico
# --------------------------------

try:
    numero = int(input("Digite um número: "))
    resultado = 10 / numero
    print(f"Resultado: {resultado}")
except ValueError:
    print("Erro: Você não digitou um número válido!")
except ZeroDivisionError:
    print("Erro: Não é possível dividir por zero!")
except Exception as e:
    print(f"Erro inesperado: {e}")

# 7.2 Try-Except-Else-Finally
# --------------------------------

try:
    arquivo = open('arquivo.txt', 'r')
    conteudo = arquivo.read()
except FileNotFoundError:
    print("Arquivo não encontrado!")
else:
    # Executado se não houver exceção
    print("Arquivo lido com sucesso!")
finally:
    # Sempre executado
    print("Finalizando operação...")
    if 'arquivo' in locals():
        arquivo.close()

# 7.3 Levantando exceções
# --------------------------------

def calcular_raiz_quadrada(numero):
    if numero < 0:
        raise ValueError("Número não pode ser negativo")
    return numero ** 0.5

try:
    resultado = calcular_raiz_quadrada(-4)
except ValueError as e:
    print(f"Erro: {e}")

# 7.4 Criando exceções personalizadas
# --------------------------------

class SaldoInsuficienteError(Exception):
    """Exceção customizada para saldo insuficiente"""
    def __init__(self, saldo, valor):
        self.saldo = saldo
        self.valor = valor
        super().__init__(f"Saldo insuficiente: R${saldo:.2f} < R${valor:.2f}")

def sacar(saldo, valor):
    if valor > saldo:
        raise SaldoInsuficienteError(saldo, valor)
    return saldo - valor

try:
    novo_saldo = sacar(100, 150)
except SaldoInsuficienteError as e:
    print(e)

# ============================================================================
# 8. MÓDULOS E PACOTES
# ============================================================================

# 8.1 Importando módulos
# --------------------------------

# Importar módulo completo
import math
print(math.pi)
print(math.sqrt(16))

# Importar funções específicas
from math import pi, sqrt
print(pi)
print(sqrt(16))

# Importar com alias
import math as m
print(m.pi)

from math import sqrt as raiz
print(raiz(25))

# Importar tudo (não recomendado)
from math import *

# 8.2 Módulos úteis da biblioteca padrão
# --------------------------------

# datetime - Trabalhar com datas e horas
from datetime import datetime, date, time, timedelta

agora = datetime.now()
hoje = date.today()
hora_atual = datetime.now().time()
amanha = hoje + timedelta(days=1)
print(agora.strftime("%d/%m/%Y %H:%M:%S"))

# random - Geração de números aleatórios
import random

numero_aleatorio = random.randint(1, 100)  # Inteiro entre 1 e 100
decimal_aleatorio = random.random()  # Float entre 0 e 1
escolha = random.choice(['maçã', 'banana', 'laranja'])
numeros = [1, 2, 3, 4, 5]
random.shuffle(numeros)  # Embaralha a lista

# os - Interação com sistema operacional
import os

diretorio_atual = os.getcwd()  # Diretório atual
os.makedirs('nova_pasta', exist_ok=True)  # Cria diretório
arquivos = os.listdir('.')  # Lista arquivos
caminho = os.path.join('pasta', 'arquivo.txt')  # Cria caminho
existe = os.path.exists('arquivo.txt')  # Verifica existência

# sys - Interação com interpretador Python
import sys

print(sys.version)  # Versão do Python
print(sys.argv)  # Argumentos de linha de comando
sys.exit()  # Sai do programa

# collections - Estruturas de dados especializadas
from collections import Counter, defaultdict, namedtuple

# Counter - conta ocorrências
palavras = ['python', 'java', 'python', 'c++', 'python']
contador = Counter(palavras)
print(contador.most_common(2))  # [('python', 3), ('java', 1)]

# defaultdict - dicionário com valor padrão
dd = defaultdict(int)
dd['contador'] += 1  # Não gera erro se chave não existir

# namedtuple - tupla com campos nomeados
Ponto = namedtuple('Ponto', ['x', 'y'])
p = Ponto(10, 20)
print(p.x, p.y)

# 8.3 Criando seus próprios módulos
# --------------------------------

# Criar arquivo meu_modulo.py com funções
# Depois importar: import meu_modulo ou from meu_modulo import funcao

# ============================================================================
# 9. COMPREENSÕES AVANÇADAS
# ============================================================================

# 9.1 List Comprehension
# --------------------------------

# Sintaxe básica: [expressão for item in iterável if condição]
quadrados = [x**2 for x in range(10)]
pares = [x for x in range(20) if x % 2 == 0]
maiusculas = [palavra.upper() for palavra in ['python', 'java', 'c++']]

# Compreensão aninhada
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
achatada = [num for linha in matriz for num in linha]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# If-else em compreensão
resultado = [x if x % 2 == 0 else -x for x in range(10)]
# [0, -1, 2, -3, 4, -5, 6, -7, 8, -9]

# 9.2 Dictionary Comprehension
# --------------------------------

quadrados_dict = {x: x**2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Invertendo chave-valor
original = {'a': 1, 'b': 2, 'c': 3}
invertido = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}

# Com condição
pares_dict = {x: x**2 for x in range(10) if x % 2 == 0}

# 9.3 Set Comprehension
# --------------------------------

quadrados_set = {x**2 for x in range(-5, 6)}
# {0, 1, 4, 9, 16, 25} - sem duplicatas

# 9.4 Generator Expression
# --------------------------------

# Similar a list comprehension, mas usa () e é lazy (avalia sob demanda)
quadrados_gen = (x**2 for x in range(1000000))  # Não ocupa muita memória
print(next(quadrados_gen))  # 0
print(next(quadrados_gen))  # 1

# Uso com sum, max, min, etc.
soma = sum(x**2 for x in range(100))

# ============================================================================
# 10. GERADORES E ITERADORES
# ============================================================================

# 10.1 Funções Geradoras
# --------------------------------

def contador(maximo):
    """Gerador simples que conta até o máximo"""
    n = 0
    while n < maximo:
        yield n  # Pausa a função e retorna o valor
        n += 1

for num in contador(5):
    print(num)  # 0, 1, 2, 3, 4

# Gerador Fibonacci
def fibonacci(n):
    """Gera os primeiros n números de Fibonacci"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for fib in fibonacci(10):
    print(fib, end=' ')  # 0 1 1 2 3 5 8 13 21 34

# 10.2 Iteradores Personalizados
# --------------------------------

class ContagemRegressiva:
    """Iterador customizado para contagem regressiva"""
    def __init__(self, inicio):
        self.inicio = inicio
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.inicio <= 0:
            raise StopIteration
        self.inicio -= 1
        return self.inicio + 1

for num in ContagemRegressiva(5):
    print(num)  # 5, 4, 3, 2, 1

# 10.3 itertools - Ferramentas de iteração
# --------------------------------

import itertools

# count - contador infinito
# contador = itertools.count(start=10, step=2)
# Cuidado: é infinito!

# cycle - repete iterável infinitamente
# cores = itertools.cycle(['vermelho', 'verde', 'azul'])

# repeat - repete elemento
repetidos = list(itertools.repeat('Python', 3))
# ['Python', 'Python', 'Python']

# chain - encadeia iteráveis
lista1 = [1, 2, 3]
lista2 = [4, 5, 6]
encadeada = list(itertools.chain(lista1, lista2))
# [1, 2, 3, 4, 5, 6]

# combinations - combinações
letras = ['A', 'B', 'C']
combinacoes = list(itertools.combinations(letras, 2))
# [('A', 'B'), ('A', 'C'), ('B', 'C')]

# permutations - permutações
permutacoes = list(itertools.permutations([1, 2, 3], 2))
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

# groupby - agrupa elementos consecutivos
dados = [1, 1, 2, 2, 2, 3, 1, 1]
for chave, grupo in itertools.groupby(dados):
    print(chave, list(grupo))

# ============================================================================
# 11. EXPRESSÕES REGULARES (REGEX)
# ============================================================================

import re

# 11.1 Funções básicas
# --------------------------------

texto = "Python é incrível! Python versão 3.11"

# search - encontra primeira ocorrência
match = re.search(r'Python', texto)
if match:
    print(match.group())  # 'Python'
    print(match.start())  # posição inicial

# findall - encontra todas as ocorrências
ocorrencias = re.findall(r'Python', texto)
print(ocorrencias)  # ['Python', 'Python']

# finditer - retorna iterador de matches
for match in re.finditer(r'Python', texto):
    print(match.group(), match.start())

# match - verifica se início da string corresponde
match = re.match(r'Python', texto)
if match:
    print("Começa com Python!")

# fullmatch - verifica se string inteira corresponde
match = re.fullmatch(r'Python', 'Python')

# 11.2 Padrões comuns
# --------------------------------

# . - qualquer caractere (exceto quebra de linha)
# ^ - início da string
# $ - fim da string
# * - 0 ou mais repetições
# + - 1 ou mais repetições
# ? - 0 ou 1 repetição
# {n} - exatamente n repetições
# {n,} - n ou mais repetições
# {n,m} - entre n e m repetições
# [] - conjunto de caracteres
# | - ou
# () - grupo de captura
# \ - escape

# Exemplos práticos
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
telefone_pattern = r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}'
cpf_pattern = r'\d{3}\.\d{3}\.\d{3}-\d{2}'
url_pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b'

# Validando email
email = "usuario@exemplo.com"
if re.match(email_pattern, email):
    print("Email válido!")

# 11.3 Grupos e substituição
# --------------------------------

# Grupos de captura
texto = "João tem 25 anos e Maria tem 30 anos"
pattern = r'(\w+) tem (\d+) anos'

for match in re.finditer(pattern, texto):
    nome = match.group(1)
    idade = match.group(2)
    print(f"{nome}: {idade}")

# sub - substituir
novo_texto = re.sub(r'\d+', 'XX', texto)
print(novo_texto)  # "João tem XX anos e Maria tem XX anos"

# Substituição com função
def duplicar_numero(match):
    return str(int(match.group()) * 2)

resultado = re.sub(r'\d+', duplicar_numero, "Tenho 10 maçãs e 5 laranjas")
# "Tenho 20 maçãs e 10 laranjas"

# split - dividir string por padrão
partes = re.split(r'[,;]', "maçã,banana;laranja")
# ['maçã', 'banana', 'laranja']

# 11.4 Flags
# --------------------------------

texto_multi = """Primeira linha
Segunda linha
Terceira linha"""

# re.IGNORECASE ou re.I - ignorar maiúsculas/minúsculas
matches = re.findall(r'python', "Python PYTHON python", re.I)

# re.MULTILINE ou re.M - ^ e $ funcionam em cada linha
linhas = re.findall(r'^.*linha$', texto_multi, re.M)

# re.DOTALL ou re.S - . corresponde a qualquer caractere, incluindo \n
conteudo = re.search(r'Primeira.*Terceira', texto_multi, re.S)

# ============================================================================
# 12. PROGRAMAÇÃO FUNCIONAL
# ============================================================================

# 12.1 Map, Filter, Reduce
# --------------------------------

# map - aplica função a cada elemento
numeros = [1, 2, 3, 4, 5]
quadrados = list(map(lambda x: x**2, numeros))
# [1, 4, 9, 16, 25]

# Múltiplos iteráveis
lista1 = [1, 2, 3]
lista2 = [4, 5, 6]
soma = list(map(lambda x, y: x + y, lista1, lista2))
# [5, 7, 9]

# filter - filtra elementos
pares = list(filter(lambda x: x % 2 == 0, numeros))
# [2, 4]

# reduce - reduz iterável a um único valor
from functools import reduce

produto = reduce(lambda x, y: x * y, numeros)
# 120 (1 * 2 * 3 * 4 * 5)

# 12.2 Funções de Alta Ordem
# --------------------------------

def aplicar_operacao(funcao, lista):
    """Função que recebe outra função como argumento"""
    return [funcao(x) for x in lista]

def quadrado(x):
    return x ** 2

resultado = aplicar_operacao(quadrado, [1, 2, 3, 4])
# [1, 4, 9, 16]

# Retornando funções
def criar_multiplicador(n):
    """Função que retorna outra função"""
    def multiplicar(x):
        return x * n
    return multiplicar

dobro = criar_multiplicador(2)
triplo = criar_multiplicador(3)

print(dobro(5))  # 10
print(triplo(5))  # 15

# 12.3 Closures
# --------------------------------

def contador():
    """Closure - função interna acessa variável da função externa"""
    count = 0
    
    def incrementar():
        nonlocal count  # Permite modificar variável da função externa
        count += 1
        return count
    
    return incrementar

meu_contador = contador()
print(meu_contador())  # 1
print(meu_contador())  # 2
print(meu_contador())  # 3

# 12.4 Partial Functions
# --------------------------------

from functools import partial

def potencia(base, expoente):
    return base ** expoente

# Criar função com argumento pré-definido
quadrado = partial(potencia, expoente=2)
cubo = partial(potencia, expoente=3)

print(quadrado(5))  # 25
print(cubo(5))  # 125

# ============================================================================
# 13. CONTEXT MANAGERS
# ============================================================================

# 13.1 Usando with
# --------------------------------

# Arquivo (já visto anteriormente)
with open('arquivo.txt', 'r') as f:
    conteudo = f.read()
# Arquivo fechado automaticamente

# 13.2 Criando Context Managers com Classes
# --------------------------------

class GerenciadorArquivo:
    """Context manager customizado"""
    
    def __init__(self, nome_arquivo, modo):
        self.nome_arquivo = nome_arquivo
        self.modo = modo
        self.arquivo = None
    
    def __enter__(self):
        """Executado ao entrar no bloco with"""
        self.arquivo = open(self.nome_arquivo, self.modo)
        return self.arquivo
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Executado ao sair do bloco with"""
        if self.arquivo:
            self.arquivo.close()
        # Retorna False para propagar exceções
        return False

with GerenciadorArquivo('teste.txt', 'w') as f:
    f.write('Testando context manager')

# 13.3 Context Managers com Decoradores
# --------------------------------

from contextlib import contextmanager

@contextmanager
def gerenciador_simples():
    """Context manager usando decorador"""
    print("Entrando no contexto")
    try:
        yield "Recurso"
    finally:
        print("Saindo do contexto")

with gerenciador_simples() as recurso:
    print(f"Usando {recurso}")

# ============================================================================
# 14. MULTITHREADING E MULTIPROCESSING
# ============================================================================

# 14.1 Threading
# --------------------------------

import threading
import time

def tarefa(nome, duracao):
    """Função que será executada em uma thread"""
    print(f"{nome} iniciada")
    time.sleep(duracao)
    print(f"{nome} concluída")

# Criar e iniciar threads
thread1 = threading.Thread(target=tarefa, args=("Thread 1", 2))
thread2 = threading.Thread(target=tarefa, args=("Thread 2", 3))

thread1.start()
thread2.start()

# Aguardar conclusão das threads
thread1.join()
thread2.join()

print("Todas as threads concluídas")

# Threading com classes
class MinhaThread(threading.Thread):
    def __init__(self, nome):
        super().__init__()
        self.nome = nome
    
    def run(self):
        print(f"{self.nome} executando")
        time.sleep(1)
        print(f"{self.nome} concluída")

t = MinhaThread("Thread Customizada")
t.start()
t.join()

# Lock para sincronização
lock = threading.Lock()
contador = 0

def incrementar():
    global contador
    for _ in range(100000):
        with lock:  # Garante acesso exclusivo
            contador += 1

threads = [threading.Thread(target=incrementar) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Contador: {contador}")

# 14.2 Multiprocessing
# --------------------------------

from multiprocessing import Process, Queue, Pool

def worker(numero):
    """Função que será executada em processo separado"""
    print(f"Processo {numero} iniciado")
    time.sleep(1)
    return numero ** 2

# Criando processos
if __name__ == '__main__':
    processos = []
    for i in range(5):
        p = Process(target=worker, args=(i,))
        processos.append(p)
        p.start()
    
    for p in processos:
        p.join()
    
    # Pool - gerencia pool de processos
    with Pool(processes=4) as pool:
        resultados = pool.map(worker, range(10))
        print(resultados)

# ============================================================================
# 15. TÓPICOS AVANÇADOS
# ============================================================================

# 15.1 Type Hints (Anotações de Tipo)
# --------------------------------

def saudacao(nome: str, idade: int) -> str:
    """Função com type hints"""
    return f"Olá, {nome}! Você tem {idade} anos."

from typing import List, Dict, Tuple, Optional, Union, Any

def processar_lista(numeros: List[int]) -> List[int]:
    return [n * 2 for n in numeros]

def obter_dados() -> Dict[str, Any]:
    return {"nome": "João", "idade": 30, "ativo": True}

def buscar_usuario(id: int) -> Optional[str]:
    """Retorna nome do usuário ou None"""
    return "João" if id == 1 else None

def processar(valor: Union[int, str]) -> str:
    """Aceita int ou str"""
    return str(valor)

# 15.2 Dataclasses
# --------------------------------

from dataclasses import dataclass, field
from typing import List

@dataclass
class Pessoa:
    """Classe de dados - gera automaticamente __init__, __repr__, etc."""
    nome: str
    idade: int
    email: str = "não informado"  # Valor padrão
    hobbies: List[str] = field(default_factory=list)  # Lista mutável
    
    def __post_init__(self):
        """Executado após __init__"""
        if self.idade < 0:
            raise ValueError("Idade não pode ser negativa")

pessoa = Pessoa("João", 30, hobbies=["leitura", "programação"])
print(pessoa)

# 15.3 Enums
# --------------------------------

from enum import Enum, auto

class Status(Enum):
    """Enumeração de status"""
    PENDENTE = 1
    EM_ANDAMENTO = 2
    CONCLUIDO = 3
    CANCELADO = 4

class Cor(Enum):
    """Usando auto() para valores automáticos"""
    VERMELHO = auto()
    VERDE = auto()
    AZUL = auto()

status = Status.PENDENTE
print(status.name)  # PENDENTE
print(status.value)  # 1

# 15.4 Property Decorators
# --------------------------------

class Circulo:
    def __init__(self, raio):
        self._raio = raio
    
    @property
    def raio(self):
        """Getter para raio"""
        return self._raio
    
    @raio.setter
    def raio(self, valor):
        """Setter para raio com validação"""
        if valor < 0:
            raise ValueError("Raio não pode ser negativo")
        self._raio = valor
    
    @property
    def area(self):
        """Propriedade calculada (somente leitura)"""
        import math
        return math.pi * self._raio ** 2
    
    @property
    def perimetro(self):
        """Propriedade calculada"""
        import math
        return 2 * math.pi * self._raio

c = Circulo(5)
print(c.area)
c.raio = 10
print(c.area)

# 15.5 Metaclasses
# --------------------------------

class SingletonMeta(type):
    """Metaclasse para implementar padrão Singleton"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    def __init__(self, valor):
        self.valor = valor

s1 = Singleton(10)
s2 = Singleton(20)
print(s1 is s2)  # True - mesma instância
print(s1.valor)  # 20

# 15.6 Descriptors
# --------------------------------

class Validador:
    """Descriptor para validação de atributos"""
    
    def __init__(self, minimo=None, maximo=None):
        self.minimo = minimo
        self.maximo = maximo
    
    def __set_name__(self, owner, name):
        self.nome = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.nome)
    
    def __set__(self, obj, valor):
        if self.minimo is not None and valor < self.minimo:
            raise ValueError(f"{self.nome} deve ser >= {self.minimo}")
        if self.maximo is not None and valor > self.maximo:
            raise ValueError(f"{self.nome} deve ser <= {self.maximo}")
        obj.__dict__[self.nome] = valor

class Pessoa:
    idade = Validador(minimo=0, maximo=150)
    altura = Validador(minimo=0, maximo=3)
    
    def __init__(self, idade, altura):
        self.idade = idade
        self.altura = altura

p = Pessoa(25, 1.75)
# p.idade = -5  # Levantaria ValueError

# ============================================================================
# 16. BOAS PRÁTICAS E PADRÕES
# ============================================================================

# 16.1 PEP 8 - Guia de Estilo
# --------------------------------

# - Use 4 espaços para indentação (não tabs)
# - Linhas com no máximo 79 caracteres
# - Duas linhas em branco entre definições de classes/funções de nível superior
# - Uma linha em branco entre métodos de uma classe
# - Imports no topo do arquivo, agrupados: biblioteca padrão, terceiros, locais
# - Use snake_case para variáveis e funções
# - Use PascalCase para classes
# - Use UPPER_CASE para constantes
# - Sempre use self como primeiro parâmetro de métodos de instância
# - Sempre use cls como primeiro parâmetro de métodos de classe

# 16.2 Docstrings
# --------------------------------

def calcular_area_retangulo(largura, altura):
    """
    Calcula a área de um retângulo.
    
    Args:
        largura (float): A largura do retângulo em metros.
        altura (float): A altura do retângulo em metros.
    
    Returns:
        float: A área do retângulo em metros quadrados.
    
    Raises:
        ValueError: Se largura ou altura forem negativas.
    
    Examples:
        >>> calcular_area_retangulo(5, 3)
        15.0
    """
    if largura < 0 or altura < 0:
        raise ValueError("Dimensões não podem ser negativas")
    return largura * altura

# 16.3 List vs Generator
# --------------------------------

# Use list comprehension quando precisar usar a lista múltiplas vezes
quadrados_lista = [x**2 for x in range(1000)]

# Use generator quando iterar apenas uma vez (economiza memória)
quadrados_gen = (x**2 for x in range(1000000))

# 16.4 Uso de enumerate e zip
# --------------------------------

# Sempre use enumerate em vez de range(len())
# RUIM
frutas = ['maçã', 'banana', 'laranja']
for i in range(len(frutas)):
    print(f"{i}: {frutas[i]}")

# BOM
for i, fruta in enumerate(frutas):
    print(f"{i}: {fruta}")

# Use zip para iterar sobre múltiplas listas
nomes = ['João', 'Maria', 'Pedro']
idades = [25, 30, 35]
for nome, idade in zip(nomes, idades):
    print(f"{nome}: {idade}")

# 16.5 Context Managers para Recursos
# --------------------------------

# Sempre use 'with' para gerenciar recursos
# BOM
with open('arquivo.txt', 'r') as f:
    dados = f.read()

# RUIM
f = open('arquivo.txt', 'r')
dados = f.read()
f.close()  # Pode não ser executado se houver exceção

# ============================================================================
# FIM DO MANUAL
# ============================================================================

# Este manual cobre os principais conceitos de Python, desde o básico até
# tópicos avançados. Continue praticando e explorando a documentação oficial
# em https://docs.python.org/pt-br/3/

print("Manual de Python concluído!")