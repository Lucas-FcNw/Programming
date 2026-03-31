# Relatório Técnico — Projeto 1 de Estrutura de Dados II

## Compressão de Arquivos com o Algoritmo de Huffman

**Aluno:** Lucas  Fernandes de Camargo 10419400, Rafael Lima 10425819
**Disciplina:** Estrutura de Dados II  
**Professor:** Prof. Leonardo takuno
**Data:** 31/03/2026

---

## 1. Resumo

Este projeto implementa, em Java, um compressor/descompressor sem perdas baseado no algoritmo de Huffman. A solução foi desenvolvida com foco em:

- construção de uma fila de prioridades usando **Min-Heap próprio**;
- construção e travessia de **árvore binária de Huffman**;
- compressão e descompressão por linha de comando;
- manipulação de arquivos binários com cabeçalho e dados compactados;
- medição de desempenho com `System.nanoTime()`.

O sistema final gera e executa o arquivo `huffman.jar` com os comandos exigidos no enunciado.

---

## 2. Objetivos Atendidos

- [x] Implementação de Min-Heap com `ArrayList<No>`
- [x] Classe `No` com `Comparable<No>`
- [x] Contagem de frequências com `int[256]`
- [x] Tabela de códigos com `String[256]`
- [x] Compressão e descompressão por CLI
- [x] Geração de arquivo comprimido com cabeçalho
- [x] Reconstrução da árvore na descompressão
- [x] Impressão de etapas no console
- [x] Benchmark em Java com `System.nanoTime()`

---

## 3. Organização do Projeto

```text
Compressão_Huffman/
├── huffman.jar
├── RELATORIO.md
├── Pdf.md
├── src/
│   ├── Main.java
│   ├── HuffmanCodec.java
│   ├── MinHeap.java
│   ├── No.java
│   └── Benchmark.java
└── bench/
  ├── arq_de_teste.txt
    ├── texto_1KB.txt
    ├── texto_100KB.txt
    ├── texto_1MB.txt
    ├── texto_10MB.txt
    ├── repetitivo_1MB.txt
    ├── aleatorio_1MB.txt
    └── codigo_1MB.java
```

---

## 4. Estruturas de Dados e Decisões de Projeto

### 4.1 Classe `No`

Cada nó da árvore armazena:

- `char caractere`
- `int frequencia`
- `No esquerda`
- `No direita`

Também implementa `Comparable<No>` para ordenação por frequência no heap.

### 4.2 Min-Heap Próprio

A classe `MinHeap` foi implementada com `ArrayList<No>`, respeitando o mapeamento:

- filho esquerdo: $2i + 1$
- filho direito: $2i + 2$
- pai: $\lfloor (i-1)/2 \rfloor$

Operações implementadas:

- `inserir(No)`
- `extrairMin()`
- `tamanho()`
- `snapshot()`

Complexidades:

- inserção: $O(\log n)$
- extração do mínimo: $O(\log n)$

### 4.3 Formato do Arquivo Comprimido (`.huff`)

Para permitir reconstrução completa, o arquivo comprimido grava:

1. **MAGIC** (`int`) para validar formato
2. **tamanho original** (`int`)
3. **tabela de frequências** (256 inteiros)
4. **quantidade de bits válidos** do payload
5. **payload compactado** (bytes)

Isso torna a descompressão independente de estado externo.

---

## 5. Fluxo de Compressão

1. Lê arquivo de entrada em bytes.
2. Conta frequências em `int[256]`.
3. Cria um `No` por caractere presente e insere no Min-Heap.
4. Constrói árvore de Huffman removendo os 2 menores nós repetidamente.
5. Gera códigos recursivamente (`0` esquerda, `1` direita).
6. Concatena bits dos caracteres do arquivo.
7. Empacota bits em bytes.
8. Escreve cabeçalho + payload no arquivo de saída.

### Saídas de depuração

A aplicação imprime as etapas pedidas no enunciado:

- ETAPA 1: Tabela de Frequência
- ETAPA 2: Min-Heap inicial
- ETAPA 3: Árvore de Huffman
- ETAPA 4: Tabela de Códigos
- ETAPA 5: Resumo da compressão

---

## 6. Fluxo de Descompressão

1. Valida `MAGIC` do arquivo.
2. Lê tamanho original e frequências.
3. Reconstrói a árvore de Huffman.
4. Lê o fluxo de bits válidos.
5. Faz percurso guiado por bits:
   - `0` -> esquerda
   - `1` -> direita
6. Ao chegar em folha, escreve caractere e volta à raiz.
7. Repete até restaurar exatamente o número de bytes original.

### Tratamento de erro

- arquivo comprimido inválido (assinatura incorreta)
- inconsistência entre bits e tamanho esperado

---

## 7. Execução

### 7.1 Compilar

```bash
javac src/*.java
```

### 7.2 Gerar `huffman.jar`

```bash
jar cfe huffman.jar Main -C src .
```

### 7.3 Comprimir

```bash
java -jar huffman.jar -c <arquivo_original> <arquivo_comprimido>
```

### 7.4 Descomprimir

```bash
java -jar huffman.jar -d <arquivo_comprimido> <arquivo_restaurado>
```

---

## 8. Análises Requeridas

As medições de tempo foram feitas em Java com `System.nanoTime()`, por meio da classe `Benchmark.java`.

### 8.1 Parte 1 — Performance (Tempo)

#### Metodologia

- Foi utilizado o arquivo padrão **`arq_de_teste.txt`** (conforme enunciado) para o cenário de texto comum.
- Também foram gerados arquivos adicionais de teste com tamanhos diferentes.
- Para cada arquivo, mediu-se:
  - tempo de compressão (ms)
  - tempo de descompressão (ms)

#### Resultados

| Arquivo | Tamanho (bytes) | Compressão (ms) | Descompressão (ms) |
|---|---:|---:|---:|
| arq_de_teste.txt | 102.400 | 42,199 | 12,473 |
| texto_1KB.txt | 1.024 | 33,049 | 1,307 |
| texto_100KB.txt | 102.400 | 16,228 | 11,369 |
| texto_1MB.txt | 1.048.576 | 25,297 | 12,514 |
| texto_10MB.txt | 10.485.760 | 187,132 | 89,926 |

#### Discussão

- O tempo cresce com o tamanho de entrada, com tendência aproximadamente linear para arquivos maiores.
- Em tamanhos muito pequenos (1KB), custos fixos (JVM/IO/alocação) distorcem a proporcionalidade.
- Para 10MB, os tempos são significativamente maiores, como esperado pela análise assintótica.

### 8.2 Parte 2 — Taxa de Compressão (Espaço)

A taxa foi calculada por:

$$
\text{Taxa de Compressão} = \left(1 - \frac{\text{Tamanho Comprimido}}{\text{Tamanho Original}}\right) \times 100\%
$$

#### Resultados por tipo de arquivo

| Tipo de arquivo | Exemplo | Tamanho original | Taxa de compressão |
|---|---|---:|---:|
| Texto comum (arquivo padrão) | arq_de_teste.txt | 102.400 bytes | 47,27% |
| Texto comum | texto_1MB.txt | 1.048.576 bytes | 48,19% |
| Código-fonte | codigo_1MB.java | 1.048.576 bytes | 46,56% |
| Muito repetitivo | repetitivo_1MB.txt | 1.048.576 bytes | 87,40% |
| Aleatório | aleatorio_1MB.txt | 1.048.576 bytes | 15,95% |
| Texto muito pequeno | texto_1KB.txt | 1.024 bytes | -52,93% |

#### Discussão

- **Repetitivo comprime muito bem**: baixa entropia e distribuição concentrada de símbolos.
- **Texto comum e código-fonte** apresentam boa compressão: há padrão e redundância léxica/sintática.
- **Aleatório comprime mal**: distribuição próxima do uniforme diminui vantagem de códigos variáveis.
- **Arquivo muito pequeno pode piorar**: overhead do cabeçalho supera o ganho da codificação.

---

## 9. Complexidade Teórica

Seja $n$ o tamanho do arquivo (em bytes) e $\sigma$ o alfabeto (aqui, no máximo 256):

- Contagem de frequência: $O(n)$
- Construção do heap: $O(\sigma \log \sigma)$
- Construção da árvore: $O(\sigma \log \sigma)$
- Codificação do arquivo: $O(n)$
- Descodificação: $O(n)$ (proporcional ao total de bits válidos)

Como $\sigma \le 256$, o custo dominante prático é linear em $n$.

---

## 10. Validação Funcional

Teste de sanidade executado com conteúdo `BANANA`:

- compressão gerada com sucesso;
- descompressão gerada com sucesso;
- comparação com `diff` retornou arquivos idênticos.

Também foi validada execução direta com:

- `java -jar huffman.jar -c ...`
- `java -jar huffman.jar -d ...`

---

## 11. Limitações e Melhorias Futuras

### Limitações atuais

- Cabeçalho grava 256 inteiros sempre (simples, porém não mínimo).
- Implementação trabalha com tabela ASCII estendida (0–255).

### Melhorias futuras

- serialização compacta da árvore em vez da tabela inteira;
- suporte completo a Unicode por codificação em bytes e metadados;
- modo silencioso para benchmarks mais limpos;
- testes automatizados com JUnit;
- interface gráfica opcional.

---

## 12. Conclusão

A implementação em Java cumpre os requisitos centrais do projeto de Huffman:

- estruturas de dados exigidas (Min-Heap + árvore binária),
- compressão/descompressão corretas,
- execução por linha de comando,
- análises de tempo e taxa de compressão.

Os resultados experimentais confirmam o comportamento esperado do algoritmo: melhor desempenho em arquivos com padrões e pior eficiência em conteúdo aleatório ou muito pequeno.

---

## Referências

- CORMEN, T. H. et al. *Algoritmos: Teoria e Prática*. 3ª ed. LTC, 2012.
- Huffman coding (IME-USP): https://www.ime.usp.br/~pf/estruturas-de-dados/aulas/huffman.html
- GeeksforGeeks — Heap: https://www.geeksforgeeks.org/heap-data-structure/
- GeeksforGeeks — Priority Queue em Java: https://www.geeksforgeeks.org/java/priority-queue-in-java/
