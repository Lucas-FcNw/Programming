# 🐍 Python do Zero - Guia de Estudos

## 🎯 Atalhos Úteis do VS Code

```
Ctrl + Enter          → Executar programa
Ctrl + Alt + F        → Formatar código
Ctrl + L              → Selecionar linha inteira
Shift + Alt + ↓       → Clonar linha para baixo
Shift + Alt + ↑       → Clonar linha para cima
Alt + ↓               → Mover linha para baixo
Alt + ↑               → Mover linha para cima
Ctrl + Shift + K      → Apagar linha inteira
Ctrl + ` (crase)      → Abrir terminal embutido
Ctrl + F2             → Selecionar todas as ocorrências
Ctrl + G              → Ir para a linha
Ctrl + /              → Comentar/descomentar linha
```

---

## 📑 ÍNDICE DOS CAPÍTULOS

1. [Capítulo 1: O Shebang e Execução de Scripts no Linux](#capítulo-1-o-shebang-e-execução-de-scripts-no-linux)
2. [Capítulo 2: Conceitos Básicos](#capítulo-2-conceitos-básicos)
3. [Capítulo 3: Estruturas de Dados](#capítulo-3-estruturas-de-dados)
4. [Capítulo 4: Estruturas de Controle](#capítulo-4-estruturas-de-controle)
5. [Capítulo 5: Funções](#capítulo-5-funções)
6. [Capítulo 6: Programação Orientada a Objetos](#capítulo-6-programação-orientada-a-objetos)
7. [Capítulo 7: Manipulação de Arquivos](#capítulo-7-manipulação-de-arquivos)
8. [Capítulo 8: Tratamento de Exceções](#capítulo-8-tratamento-de-exceções)
9. [Capítulo 9: Módulos e Pacotes](#capítulo-9-módulos-e-pacotes)
10. [Capítulo 10: Compreensões Avançadas](#capítulo-10-compreensões-avançadas)
11. [Capítulo 11: Geradores e Iteradores](#capítulo-11-geradores-e-iteradores)
12. [Capítulo 12: Expressões Regulares](#capítulo-12-expressões-regulares)
13. [Capítulo 13: Programação Funcional](#capítulo-13-programação-funcional)
14. [Capítulo 14: Context Managers](#capítulo-14-context-managers)
15. [Capítulo 15: Multithreading e Multiprocessing](#capítulo-15-multithreading-e-multiprocessing)
16. [Capítulo 16: Tópicos Avançados](#capítulo-16-tópicos-avançados)
17. [Capítulo 17: Boas Práticas e Padrões](#capítulo-17-boas-práticas-e-padrões)
18. [Capítulo 18: Análise e Ciência de Dados](#capítulo-18-análise-e-ciência-de-dados)

---

## Capítulo 1: O Shebang e Execução de Scripts no Linux

Quando criamos arquivos de script em Python dentro do ecossistema Linux, podemos configurar o sistema para executar o código diretamente pelo terminal, sem a necessidade de digitar python3 antes do nome do arquivo.

### 1. O que é o Shebang (`#!`)?

O Shebang é a primeira linha absoluta de um código. Ela indica ao kernel do Linux qual interpretador deve ser chamado para ler as linhas de texto a seguir.

- **Sintaxe correta e universal:**

```python
#!/usr/bin/env python3
print("Olá, mundo!")
```

- **Por que usamos `/usr/bin/env python3`?**
  Em vez de colocar o caminho fixo do Python (que pode mudar entre distribuições), o comando `env` pesquisa nas variáveis de ambiente do seu sistema onde o executável do Python 3 está ativo.

### 2. Como dar Permissão de Execução no Terminal

Mesmo com o Shebang correto, o Linux bloqueia a execução direta de novos arquivos por segurança. Para liberar o arquivo, usamos o utilitário chmod no terminal da pasta:

```bash
chmod +x meu_script.py
```

_(A flag `+x` significa "adicionar permissão de execução")_

### 3. Como Rodar o Arquivo Liberado

Após dar a permissão, você pode disparar o script usando o caminho relativo do diretório atual:

```bash
./meu_script.py
```

---

_Nota: Em arquivos que servem apenas como módulos ou bibliotecas secundárias, que serão importados por outros arquivos, o uso do Shebang não é necessário._

---

## Capítulo 2: Conceitos Básicos

### 2.1 Variáveis e Tipos de Dados

As variáveis em Python **não precisam de declaração de tipo** - a tipagem é dinâmica!

```python
# Tipos de dados básicos
nome = "Python"              # String
idade = 30                   # Integer
altura = 1.75                # Float
ativo = True                 # Boolean
nada = None                  # NoneType

# Verificar tipo de variável
print(type(nome))            # <class 'str'>
print(type(idade))           # <class 'int'>
```

#### Strings Multilinha

```python
texto_multi = """ print
multi
linha """
# Permite quebras de linha sem usar \n
print(texto_multi)
```

### 2.2 Operadores

#### Operadores Aritméticos

```python
soma = 10 + 5                # 15
subtracao = 10 - 5           # 5
multiplicacao = 10 * 5       # 50
divisao = 10 / 5             # 2.0 (retorna float)
divisao_inteira = 10 // 3    # 3
resto = 10 % 3               # 1 (módulo)
potencia = 2 ** 3            # 8 (exponenciação)
```

#### Operadores de Comparação

```python
igual = (5 == 5)             # True
diferente = (5 != 3)         # True
maior = (5 > 3)              # True
menor = (3 < 5)              # True
maior_igual = (5 >= 5)       # True
menor_igual = (3 <= 5)       # True
```

#### Operadores Lógicos

```python
e_logico = True and False    # False
ou_logico = True or False    # True
negacao = not True           # False
```

### 2.3 Strings

#### Concatenação

```python
texto = "Python é incrível!"
saudacao = "Olá" + " " + "Mundo"
print(saudacao)              # Olá Mundo
```

#### Formatação de Strings

**⭐ f-strings (Recomendado - Python 3.6+)**

```python
nome = "João"
idade = 25
mensagem = f"Meu nome é {nome} e tenho {idade} anos"
print(mensagem)
# Resultado: Meu nome é João e tenho 25 anos
```

**Método .format()**

```python
mensagem = "Meu nome é {} e tenho {} anos".format(nome, idade)
```

**Operador % (Sintaxe Antiga)**

```python
mensagem = "Meu nome é %s e tenho %d anos" % (nome, idade)
```

#### Métodos de String

```python
texto = "Python é incrível!"

texto.upper()                # PYTHON É INCRÍVEL!
texto.lower()                # python é incrível!
texto.title()                # Python É Incrível!
"  texto  ".strip()          # Remove espaços das extremidades
texto.replace("incrível", "fantástico")  # Substitui palavra
texto.split()                # Divide em lista de palavras
texto.startswith("Python")   # True
texto.endswith("!")          # True
```

#### Slicing (Fatiamento)

```python
palavra = "Python"

palavra[0]                   # 'P' (primeiro caractere)
palavra[-1]                  # 'n' (último caractere)
palavra[0:3]                 # 'Pyt' (do índice 0 ao 2)
palavra[::2]                 # 'Pto' (a cada 2 caracteres)
palavra[::-1]                # 'nohtyP' (inverte a string)
```

---

## Capítulo 3: Estruturas de Dados

### 3.1 Listas

Listas são **mutáveis** e ordenadas - podem ser alteradas!

#### Criação

```python
frutas = ["maçã", "banana", "laranja"]
numeros = [1, 2, 3, 4, 5]
mista = [1, "texto", True, 3.14]  # Pode misturar tipos
```

#### Métodos

```python
frutas.append("uva")              # Adiciona no final
frutas.insert(1, "morango")       # Adiciona em posição específica
frutas.remove("banana")           # Remove item específico
ultimo = frutas.pop()             # Remove e retorna o último
primeiro = frutas.pop(0)          # Remove e retorna item do índice 0
frutas.sort()                     # Ordena a lista
frutas.reverse()                  # Inverte a lista
tamanho = len(frutas)             # Retorna tamanho
frutas.clear()                    # Limpa a lista
```

#### List Comprehension

```python
quadrados = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

pares = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

### 3.2 Tuplas

Tuplas são **imutáveis** - não podem ser alteradas após criação!

```python
coordenadas = (10, 20)
cores = ("vermelho", "verde", "azul")

# Desempacotamento
x, y = coordenadas
r, g, b = cores

# Métodos
contagem = cores.count("vermelho")   # Conta ocorrências
indice = cores.index("verde")        # Retorna índice
```

### 3.3 Dicionários

Dicionários armazenam dados como **chave-valor**.

#### Criação e Acesso

```python
pessoa = {
    "nome": "João",
    "idade": 30,
    "cidade": "São Paulo"
}

# Acessar valores
print(pessoa["nome"])                    # João
idade = pessoa.get("idade")              # Mais seguro
estado = pessoa.get("estado", "SP")      # Com valor padrão
```

#### Modificar e Adicionar

```python
pessoa["idade"] = 31                 # Modifica
pessoa["profissao"] = "Desenvolvedor"  # Adiciona
```

#### Métodos

```python
chaves = pessoa.keys()               # Retorna chaves
valores = pessoa.values()            # Retorna valores
itens = pessoa.items()               # Retorna pares chave-valor
pessoa.update({"telefone": "123456"})  # Atualiza múltiplos
profissao = pessoa.pop("profissao")  # Remove e retorna
pessoa.clear()                       # Limpa o dicionário
```

#### Dictionary Comprehension

```python
quadrados_dict = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Invertendo chave-valor
original = {'a': 1, 'b': 2, 'c': 3}
invertido = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}
```

### 3.4 Conjuntos (Sets)

Conjuntos **não permitem duplicatas** e **não são ordenados**.

```python
numeros_set = {1, 2, 3, 4, 5}
frutas_set = {"maçã", "banana", "laranja"}

# Métodos
numeros_set.add(6)                   # Adiciona
numeros_set.remove(1)                # Remove (erro se não existir)
numeros_set.discard(10)              # Remove (sem erro)

# Operações de conjunto
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

uniao = a | b                        # {1, 2, 3, 4, 5, 6}
intersecao = a & b                   # {3, 4}
diferenca = a - b                    # {1, 2}
diferenca_simetrica = a ^ b          # {1, 2, 5, 6}
```

---

## Capítulo 4: Estruturas de Controle

### 4.1 Condicionais (if, elif, else)

**O `if` é um avaliador** - se a condição for verdadeira, executa o bloco.

```python
idade = 18

if idade < 18:
    print("Menor de idade")
elif idade == 18:
    print("Tem 18 anos")
else:
    print("Maior de idade")

# Operador ternário (em uma linha)
status = "Adulto" if idade >= 18 else "Criança"
```

### 4.2 Loops (for, while)

#### Loop for

```python
# Range básico
for i in range(5):                   # 0 a 4
    print(i)

# Range com passo
for i in range(2, 10, 2):            # De 2 a 9, pulando de 2
    print(i)

# Iterando sobre lista
frutas = ["maçã", "banana", "laranja"]
for fruta in frutas:
    print(fruta)

# Enumerate (índice + valor)
for indice, fruta in enumerate(frutas):
    print(f"{indice}: {fruta}")

# Zip (múltiplas listas)
nomes = ["João", "Maria", "Pedro"]
idades = [25, 30, 35]
for nome, idade in zip(nomes, idades):
    print(f"{nome} tem {idade} anos")
```

#### Loop while

```python
contador = 0
while contador < 5:
    print(contador)
    contador += 1
```

#### Break e Continue

```python
for i in range(10):
    if i == 3:
        continue             # Pula para próxima iteração
    if i == 7:
        break                # Sai do loop
    print(i)

# Loop com else (executa se não houver break)
for i in range(5):
    print(i)
else:
    print("Loop concluído sem break")
```

---

## Capítulo 5: Funções

### 5.1 Definição Básica

```python
def saudacao():
    """Função simples sem parâmetros"""
    print("Olá, Mundo!")

saudacao()
```

### 5.2 Funções com Parâmetros

```python
def saudar_pessoa(nome, idade):
    """Função com parâmetros posicionais"""
    return f"Olá, {nome}! Você tem {idade} anos."

mensagem = saudar_pessoa("João", 30)

# Parâmetros com valores padrão
def criar_perfil(nome, idade=18, cidade="São Paulo"):
    return f"{nome}, {idade} anos, {cidade}"

perfil1 = criar_perfil("Maria")                    # Usa valores padrão
perfil2 = criar_perfil("João", 25)                 # Sobrescreve idade
perfil3 = criar_perfil("Pedro", cidade="RJ")       # Sobrescreve cidade
```

### 5.3 \*args e \*\*kwargs

#### 5.3.1 \*args - Argumentos Posicionais Ilimitados

```python
def somar(*numeros):
    """Aceita qualquer número de argumentos"""
    total = 0
    for num in numeros:
        total += num
    return total

resultado = somar(1, 2, 3, 4, 5)  # 15
```

#### 5.3.2 \*\*kwargs - Argumentos Nomeados Ilimitados

```python
def exibir_info(**info):
    """Aceita argumentos nomeados"""
    for chave, valor in info.items():
        print(f"{chave}: {valor}")

exibir_info(nome="João", idade=30, cidade="SP")
```

### 5.4 Funções Lambda

Funções anônimas de uma linha:

```python
quadrado = lambda x: x ** 2
soma = lambda a, b: a + b

print(quadrado(5))                   # 25
print(soma(3, 7))                    # 10

# Uso com map, filter, reduce
numeros = [1, 2, 3, 4, 5]
quadrados = list(map(lambda x: x**2, numeros))
# [1, 4, 9, 16, 25]

pares = list(filter(lambda x: x % 2 == 0, numeros))
# [2, 4]

from functools import reduce
produto = reduce(lambda x, y: x * y, numeros)
# 120 (1 * 2 * 3 * 4 * 5)
```

### 5.5 Decoradores

Funções que modificam outras funções:

```python
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
# Imprime: Antes da função
#          Olá, João!
#          Depois da função

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

saudar()  # Imprime "Olá!" 3 vezes
```

---

## Capítulo 6: Programação Orientada a Objetos

### 6.1 Classes e Objetos

```python
class Pessoa:
    """Classe básica representando uma pessoa"""

    # Atributo de classe (compartilhado)
    especie = "Homo sapiens"

    def __init__(self, nome, idade):
        """Construtor - inicializa a instância"""
        self.nome = nome              # Atributo de instância
        self.idade = idade

    def apresentar(self):
        """Método de instância"""
        return f"Olá, {self.nome}! Tenho {self.idade} anos"

    def fazer_aniversario(self):
        """Método que modifica atributo"""
        self.idade += 1

    @classmethod
    def criar_anonimo(cls):
        """Método de classe"""
        return cls("Anônimo", 0)

    @staticmethod
    def eh_maior_idade(idade):
        """Método estático - não acessa instância ou classe"""
        return idade >= 18

# Criando objetos
pessoa1 = Pessoa("João", 30)
print(pessoa1.apresentar())
pessoa1.fazer_aniversario()

pessoa_anonima = Pessoa.criar_anonimo()
print(Pessoa.eh_maior_idade(20))      # True
```

### 6.2 Herança

```python
class Estudante(Pessoa):
    """Classe que herda de Pessoa"""

    def __init__(self, nome, idade, matricula):
        super().__init__(nome, idade)     # Chama construtor da classe pai
        self.matricula = matricula

    def apresentar(self):
        """Sobrescrita de método (override)"""
        return f"{super().apresentar()} e sou estudante (matrícula: {self.matricula})"

estudante = Estudante("Pedro", 20, "2024001")
print(estudante.apresentar())
```

### 6.3 Encapsulamento

Controlar acesso aos atributos:

```python
class ContaBancaria:
    """Demonstra encapsulamento com atributos privados"""

    def __init__(self, titular, saldo_inicial=0):
        self.titular = titular
        self.__saldo = saldo_inicial     # Privado (convenção com __)

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            return True
        return False

    @property
    def saldo(self):
        """Getter - acesso controlado ao saldo"""
        return self.__saldo

    @saldo.setter
    def saldo(self, valor):
        """Setter - validação ao definir saldo"""
        if valor >= 0:
            self.__saldo = valor

conta = ContaBancaria("João", 1000)
conta.depositar(500)
print(conta.saldo)                       # 1500
```

### 6.4 Polimorfismo

Mesma interface, comportamentos diferentes:

```python
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
```

### 6.5 Métodos Especiais (Dunder Methods)

```python
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
        """Retorna comprimento (distância da origem)"""
        return int((self.x**2 + self.y**2)**0.5)

p1 = Ponto(3, 4)
p2 = Ponto(1, 2)
p3 = p1 + p2
print(p3)                               # Ponto(4, 6)
print(p1 == p2)                         # False
```

---

## Capítulo 7: Manipulação de Arquivos

### 7.1 Leitura de Arquivos

```python
# Modo 'r' - leitura (padrão)
# Usar 'with' garante fechamento automático

# Ler todo o conteúdo
with open('arquivo.txt', 'r', encoding='utf-8') as arquivo:
    conteudo = arquivo.read()
    print(conteudo)

# Ler uma linha
with open('arquivo.txt', 'r', encoding='utf-8') as arquivo:
    linha = arquivo.readline()

# Ler todas as linhas em lista
with open('arquivo.txt', 'r', encoding='utf-8') as arquivo:
    linhas = arquivo.readlines()
    for linha in linhas:
        print(linha.strip())

# Iterar linha por linha
with open('arquivo.txt', 'r', encoding='utf-8') as arquivo:
    for linha in arquivo:
        print(linha.strip())
```

### 7.2 Escrita em Arquivos

```python
# Modo 'w' - escrita (sobrescreve)
with open('saida.txt', 'w', encoding='utf-8') as arquivo:
    arquivo.write("Primeira linha\n")
    arquivo.write("Segunda linha\n")

# Modo 'a' - append (adiciona ao final)
with open('saida.txt', 'a', encoding='utf-8') as arquivo:
    arquivo.write("Linha adicional\n")

# Escrever múltiplas linhas
linhas = ["Linha 1\n", "Linha 2\n", "Linha 3\n"]
with open('saida.txt', 'w', encoding='utf-8') as arquivo:
    arquivo.writelines(linhas)
```

### 7.3 Trabalhando com JSON

```python
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

# Conversão entre JSON e string
json_string = json.dumps(dados, indent=2)
dados_de_string = json.loads(json_string)
```

### 7.4 Trabalhando com CSV

```python
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
```

---

## Capítulo 8: Tratamento de Exceções

### 8.1 Try-Except Básico

```python
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
```

### 8.2 Try-Except-Else-Finally

```python
try:
    arquivo = open('arquivo.txt', 'r')
    conteudo = arquivo.read()
except FileNotFoundError:
    print("Arquivo não encontrado!")
else:
    # Executado se NÃO houver exceção
    print("Arquivo lido com sucesso!")
finally:
    # SEMPRE executado
    print("Finalizando operação...")
    if 'arquivo' in locals():
        arquivo.close()
```

### 8.3 Levantando Exceções

```python
def calcular_raiz_quadrada(numero):
    if numero < 0:
        raise ValueError("Número não pode ser negativo")
    return numero ** 0.5

try:
    resultado = calcular_raiz_quadrada(-4)
except ValueError as e:
    print(f"Erro: {e}")
```

### 8.4 Exceções Personalizadas

```python
class SaldoInsuficienteError(Exception):
    """Exceção customizada"""
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
```

---

## Capítulo 9: Módulos e Pacotes

### 9.1 Importando Módulos

```python
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
```

### 9.2 Módulos Úteis da Biblioteca Padrão

#### 9.2.1 datetime - Datas e Horas

```python
from datetime import datetime, date, time, timedelta

agora = datetime.now()
hoje = date.today()
hora_atual = datetime.now().time()
amanha = hoje + timedelta(days=1)

# Formatação
print(agora.strftime("%d/%m/%Y %H:%M:%S"))
```

#### 9.2.2 random - Números Aleatórios

```python
import random

numero_aleatorio = random.randint(1, 100)
decimal_aleatorio = random.random()
escolha = random.choice(['maçã', 'banana', 'laranja'])

numeros = [1, 2, 3, 4, 5]
random.shuffle(numeros)
```

#### 9.2.3 os - Sistema Operacional

```python
import os

diretorio_atual = os.getcwd()
os.makedirs('nova_pasta', exist_ok=True)
arquivos = os.listdir('.')
caminho = os.path.join('pasta', 'arquivo.txt')
existe = os.path.exists('arquivo.txt')
```

#### 9.2.4 collections - Estruturas de Dados

```python
from collections import Counter, defaultdict, namedtuple

# Counter
palavras = ['python', 'java', 'python', 'c++', 'python']
contador = Counter(palavras)
print(contador.most_common(2))    # [('python', 3), ('java', 1)]

# defaultdict
dd = defaultdict(int)
dd['contador'] += 1

# namedtuple
Ponto = namedtuple('Ponto', ['x', 'y'])
p = Ponto(10, 20)
print(p.x, p.y)
```

---

## Capítulo 10: Compreensões Avançadas

### 10.1 List Comprehension

```python
# Sintaxe: [expressão for item in iterável if condição]

quadrados = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

pares = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

maiusculas = [palavra.upper() for palavra in ['python', 'java', 'c++']]
# ['PYTHON', 'JAVA', 'C++']

# Aninhada
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
achatada = [num for linha in matriz for num in linha]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# If-else
resultado = [x if x % 2 == 0 else -x for x in range(10)]
# [0, -1, 2, -3, 4, -5, 6, -7, 8, -9]
```

### 10.2 Dictionary Comprehension

```python
quadrados_dict = {x: x**2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Invertendo chave-valor
original = {'a': 1, 'b': 2, 'c': 3}
invertido = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}

# Com condição
pares_dict = {x: x**2 for x in range(10) if x % 2 == 0}
```

### 10.3 Set Comprehension

```python
quadrados_set = {x**2 for x in range(-5, 6)}
# {0, 1, 4, 9, 16, 25} - sem duplicatas
```

### 10.4 Generator Expression

```python
# Similar a list comprehension, mas usa () e é lazy (avalia sob demanda)
quadrados_gen = (x**2 for x in range(1000000))

print(next(quadrados_gen))    # 0
print(next(quadrados_gen))    # 1

# Uso com funções
soma = sum(x**2 for x in range(100))
```

---

## Capítulo 11: Geradores e Iteradores

### 11.1 Funções Geradoras

```python
def contador(maximo):
    """Gerador simples que conta até o máximo"""
    n = 0
    while n < maximo:
        yield n                      # Pausa e retorna o valor
        n += 1

for num in contador(5):
    print(num)                       # 0, 1, 2, 3, 4

# Fibonacci
def fibonacci(n):
    """Gera os primeiros n números de Fibonacci"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for fib in fibonacci(10):
    print(fib, end=' ')              # 0 1 1 2 3 5 8 13 21 34
```

### 11.2 Iteradores Personalizados

```python
class ContagemRegressiva:
    """Iterador customizado"""
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
    print(num)                       # 5, 4, 3, 2, 1
```

### 11.3 itertools - Ferramentas de Iteração

```python
import itertools

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
```

---

## Capítulo 12: Expressões Regulares

### 12.1 Funções Básicas

```python
import re

texto = "Python é incrível! Python versão 3.11"

# search - encontra primeira ocorrência
match = re.search(r'Python', texto)
if match:
    print(match.group())             # Python
    print(match.start())             # posição inicial

# findall - encontra todas
ocorrencias = re.findall(r'Python', texto)
print(ocorrencias)                   # ['Python', 'Python']

# finditer - retorna iterador
for match in re.finditer(r'Python', texto):
    print(match.group(), match.start())

# match - verifica se começa com padrão
match = re.match(r'Python', texto)

# fullmatch - verifica se string inteira corresponde
match = re.fullmatch(r'Python', 'Python')
```

### 12.2 Padrões Comuns

| Padrão  | Significado                    |
| ------- | ------------------------------ |
| `.`     | Qualquer caractere (exceto \n) |
| `^`     | Início da string               |
| `$`     | Fim da string                  |
| `*`     | 0 ou mais repetições           |
| `+`     | 1 ou mais repetições           |
| `?`     | 0 ou 1 repetição               |
| `{n}`   | Exatamente n repetições        |
| `{n,}`  | n ou mais repetições           |
| `{n,m}` | Entre n e m repetições         |
| `[]`    | Conjunto de caracteres         |
| `\|`    | OU                             |
| `()`    | Grupo de captura               |
| `\`     | Escape                         |

```python
# Exemplos práticos
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
telefone_pattern = r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}'
cpf_pattern = r'\d{3}\.\d{3}\.\d{3}-\d{2}'

# Validar email
email = "usuario@exemplo.com"
if re.match(email_pattern, email):
    print("Email válido!")
```

### 12.3 Grupos e Substituição

```python
# Grupos de captura
texto = "João tem 25 anos e Maria tem 30 anos"
pattern = r'(\w+) tem (\d+) anos'

for match in re.finditer(pattern, texto):
    nome = match.group(1)
    idade = match.group(2)
    print(f"{nome}: {idade}")

# sub - substituir
novo_texto = re.sub(r'\d+', 'XX', texto)
# João tem XX anos e Maria tem XX anos

# Substituição com função
def duplicar_numero(match):
    return str(int(match.group()) * 2)

resultado = re.sub(r'\d+', duplicar_numero, "Tenho 10 maçãs e 5 laranjas")
# Tenho 20 maçãs e 10 laranjas

# split - dividir por padrão
partes = re.split(r'[,;]', "maçã,banana;laranja")
# ['maçã', 'banana', 'laranja']
```

### 12.4 Flags

```python
texto_multi = """Primeira linha
Segunda linha
Terceira linha"""

# re.IGNORECASE ou re.I - ignorar maiúsculas/minúsculas
matches = re.findall(r'python', "Python PYTHON python", re.I)

# re.MULTILINE ou re.M - ^ e $ funcionam em cada linha
linhas = re.findall(r'^.*linha$', texto_multi, re.M)

# re.DOTALL ou re.S - . corresponde a qualquer caractere, incluindo \n
conteudo = re.search(r'Primeira.*Terceira', texto_multi, re.S)
```

---

## Capítulo 13: Programação Funcional

### 13.1 Map, Filter, Reduce

```python
# map - aplica função a cada elemento
numeros = [1, 2, 3, 4, 5]
quadrados = list(map(lambda x: x**2, numeros))
# [1, 4, 9, 16, 25]

# filter - filtra elementos
pares = list(filter(lambda x: x % 2 == 0, numeros))
# [2, 4]

# reduce - reduz iterável a um único valor
from functools import reduce

produto = reduce(lambda x, y: x * y, numeros)
# 120 (1 * 2 * 3 * 4 * 5)
```

### 13.2 Funções de Alta Ordem

```python
def aplicar_operacao(funcao, lista):
    """Função que recebe outra função como argumento"""
    return [funcao(x) for x in lista]

def quadrado(x):
    return x ** 2

resultado = aplicar_operacao(quadrado, [1, 2, 3, 4])
# [1, 4, 9, 16]

# Retornando funções
def criar_multiplicador(n):
    def multiplicar(x):
        return x * n
    return multiplicar

dobro = criar_multiplicador(2)
triplo = criar_multiplicador(3)

print(dobro(5))                      # 10
print(triplo(5))                     # 15
```

### 13.3 Closures

```python
def contador():
    """Closure - função interna acessa variável externa"""
    count = 0

    def incrementar():
        nonlocal count
        count += 1
        return count

    return incrementar

meu_contador = contador()
print(meu_contador())                # 1
print(meu_contador())                # 2
print(meu_contador())                # 3
```

### 13.4 Partial Functions

```python
from functools import partial

def potencia(base, expoente):
    return base ** expoente

# Criar função com argumento pré-definido
quadrado = partial(potencia, expoente=2)
cubo = partial(potencia, expoente=3)

print(quadrado(5))                   # 25
print(cubo(5))                       # 125
```

---

## Capítulo 14: Context Managers

### 14.1 Usando with

```python
# Garante fechamento automático do arquivo
with open('arquivo.txt', 'r') as f:
    conteudo = f.read()
# Arquivo fechado automaticamente
```

### 14.2 Context Managers com Classes

```python
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
        return False

with GerenciadorArquivo('teste.txt', 'w') as f:
    f.write('Testando context manager')
```

### 14.3 Context Managers com Decoradores

```python
from contextlib import contextmanager

@contextmanager
def gerenciador_simples():
    print("Entrando no contexto")
    try:
        yield "Recurso"
    finally:
        print("Saindo do contexto")

with gerenciador_simples() as recurso:
    print(f"Usando {recurso}")
```

---

## Capítulo 15: Multithreading e Multiprocessing

### 15.1 Threading

```python
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

# Aguardar conclusão
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
        with lock:
            contador += 1
```

### 15.2 Multiprocessing

```python
from multiprocessing import Process, Pool
import time

def worker(numero):
    """Função em processo separado"""
    print(f"Processo {numero} iniciado")
    time.sleep(1)
    return numero ** 2

if __name__ == '__main__':
    # Criar processos
    processos = []
    for i in range(5):
        p = Process(target=worker, args=(i,))
        processos.append(p)
        p.start()

    for p in processos:
        p.join()

    # Pool de processos
    with Pool(processes=4) as pool:
        resultados = pool.map(worker, range(10))
        print(resultados)
```

---

## Capítulo 16: Tópicos Avançados

### 16.1 Type Hints

```python
def saudacao(nome: str, idade: int) -> str:
    """Função com type hints"""
    return f"Olá, {nome}! Você tem {idade} anos."

from typing import List, Dict, Tuple, Optional, Union, Any

def processar_lista(numeros: List[int]) -> List[int]:
    return [n * 2 for n in numeros]

def obter_dados() -> Dict[str, Any]:
    return {"nome": "João", "idade": 30, "ativo": True}

def buscar_usuario(id: int) -> Optional[str]:
    """Retorna nome ou None"""
    return "João" if id == 1 else None
```

### 16.2 Dataclasses

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Pessoa:
    """Classe de dados - gera __init__, __repr__ automaticamente"""
    nome: str
    idade: int
    email: str = "não informado"
    hobbies: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.idade < 0:
            raise ValueError("Idade não pode ser negativa")

pessoa = Pessoa("João", 30, hobbies=["leitura", "programação"])
```

### 16.3 Enums

```python
from enum import Enum, auto

class Status(Enum):
    PENDENTE = 1
    EM_ANDAMENTO = 2
    CONCLUIDO = 3
    CANCELADO = 4

class Cor(Enum):
    VERMELHO = auto()
    VERDE = auto()
    AZUL = auto()

status = Status.PENDENTE
print(status.name)                   # PENDENTE
print(status.value)                  # 1
```

### 16.4 Properties

```python
class Circulo:
    def __init__(self, raio):
        self._raio = raio

    @property
    def raio(self):
        """Getter"""
        return self._raio

    @raio.setter
    def raio(self, valor):
        """Setter com validação"""
        if valor < 0:
            raise ValueError("Raio não pode ser negativo")
        self._raio = valor

    @property
    def area(self):
        """Propriedade calculada"""
        import math
        return math.pi * self._raio ** 2

c = Circulo(5)
print(c.area)
```

### 16.5 Metaclasses

```python
class SingletonMeta(type):
    """Metaclasse para padrão Singleton"""
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
print(s1 is s2)                      # True - mesma instância
```

### 16.6 Descriptors

```python
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
```

---

## Capítulo 17: Boas Práticas e Padrões

### 17.1 PEP 8 - Guia de Estilo

- ✅ Use **4 espaços** para indentação (não tabs)
- ✅ Linhas com **máximo 79 caracteres**
- ✅ **Duas linhas em branco** entre definições de classes/funções
- ✅ **Uma linha em branco** entre métodos de uma classe
- ✅ Imports agrupados: **biblioteca padrão → terceiros → locais**
- ✅ `snake_case` para variáveis e funções
- ✅ `PascalCase` para classes
- ✅ `UPPER_CASE` para constantes

### 17.2 Docstrings

```python
def calcular_area_retangulo(largura, altura):
    """
    Calcula a área de um retângulo.

    Args:
        largura (float): Largura do retângulo em metros.
        altura (float): Altura do retângulo em metros.

    Returns:
        float: A área do retângulo em metros quadrados.

    Raises:
        ValueError: Se dimensões forem negativas.

    Examples:
        >>> calcular_area_retangulo(5, 3)
        15.0
    """
    if largura < 0 or altura < 0:
        raise ValueError("Dimensões não podem ser negativas")
    return largura * altura
```

### 17.3 List vs Generator

```python
# Use list quando precisar iterar múltiplas vezes
quadrados_lista = [x**2 for x in range(1000)]

# Use generator para economizar memória
quadrados_gen = (x**2 for x in range(1000000))
```

### 17.4 Enumerate e Zip

```python
# RUIM - usar range(len())
frutas = ['maçã', 'banana', 'laranja']
for i in range(len(frutas)):
    print(f"{i}: {frutas[i]}")

# BOM - usar enumerate
for i, fruta in enumerate(frutas):
    print(f"{i}: {fruta}")

# BOM - usar zip para múltiplas listas
nomes = ['João', 'Maria', 'Pedro']
idades = [25, 30, 35]
for nome, idade in zip(nomes, idades):
    print(f"{nome}: {idade}")
```

### 17.5 Context Managers para Recursos

```python
# BOM - usar 'with' para garantir fechamento
with open('arquivo.txt', 'r') as f:
    dados = f.read()

# RUIM - pode não fechar se houver exceção
f = open('arquivo.txt', 'r')
dados = f.read()
f.close()
```

---

## Capítulo 18: Análise e Ciência de Dados

> **Nota:** Requires `numpy`, `pandas`, `matplotlib`, `scikit-learn`

### 18.1 NumPy - Computação Numérica

```python
import numpy as np

# Criar arrays
array_1d = np.array([1, 2, 3, 4, 5])
array_2d = np.array([[1, 2, 3], [4, 5, 6]])
array_zeros = np.zeros((3, 3))
array_ones = np.ones((2, 4))
array_range = np.arange(0, 10, 2)
array_linspace = np.linspace(0, 1, 5)

# Operações
soma_elementos = np.sum(array_1d)
media = np.mean(array_1d)
desvio_padrao = np.std(array_1d)
maximo = np.max(array_1d)
minimo = np.min(array_1d)

# Operações elemento a elemento
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
soma = arr1 + arr2
produto = arr1 * arr2

# Reshape
array_original = np.array([1, 2, 3, 4, 5, 6])
matriz = array_original.reshape(2, 3)
achatado = matriz.flatten()
```

### 18.2 Pandas - Manipulação de Dados

```python
import pandas as pd

# Criar DataFrame
dados = {
    'nome': ['João', 'Maria', 'Pedro'],
    'idade': [25, 30, 35],
    'salario': [3000, 3500, 4000]
}
df = pd.DataFrame(dados)

# Informações
print(df.head())
print(df.info())
print(df.describe())

# Seleção
nomes = df['nome']
colunas = df[['nome', 'idade']]

# Filtro
maiores_30 = df[df['idade'] > 30]

# Operações
df['categoria'] = df['idade'].apply(lambda x: 'Senior' if x > 30 else 'Junior')

# Agregação
media_idade = df['idade'].mean()
por_categoria = df.groupby('categoria')['salario'].mean()

# Leitura e escrita
df_csv = pd.read_csv('dados.csv')
df.to_csv('saida.csv', index=False)
```

### 18.3 Matplotlib - Visualização

```python
import matplotlib.pyplot as plt

# Gráfico de linhas
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
plt.plot(x, y, marker='o')
plt.title('Gráfico de Linhas')
plt.show()

# Gráfico de barras
nomes = ['A', 'B', 'C', 'D']
valores = [10, 24, 36, 18]
plt.bar(nomes, valores)
plt.title('Gráfico de Barras')
plt.show()

# Histograma
dados = np.random.randn(1000)
plt.hist(dados, bins=30)
plt.title('Histograma')
plt.show()

# Scatter plot
x_scatter = np.random.randn(100)
y_scatter = np.random.randn(100)
plt.scatter(x_scatter, y_scatter)
plt.title('Scatter Plot')
plt.show()
```

---

## 📚 Recursos Adicionais

- 🔗 [Documentação Oficial do Python](https://docs.python.org/pt-br/3/)
- 📖 [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- 🎓 [Real Python](https://realpython.com/)
- 💻 [GeeksforGeeks Python](https://www.geeksforgeeks.org/python-programming-language/)

---

✅ **Manual completo e formatado para GitHub!** 🚀
