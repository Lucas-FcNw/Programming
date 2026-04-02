# Relatório Técnico — Projeto Parte 2 (Teoria dos Grafos)

Universidade Presbiteriana Mackenzie  
Faculdade de Computação e Informática  
Disciplina: Teoria dos Grafos — Turma 6G  
Professor: Dr. Ivan Carlos Alcântara de Oliveira

---

## 1. Dados do grupo

- Lucas Fernandes de Camargo — RA 10419400
- Lendy Naiara Carpio Pacheco — RA 10428525
- Anna Luiza Stella Santos — RA 10417401

## 2. Título provisório da aplicação

**SPGraph — Análise de Acesso Territorial a Serviços de Saúde em São Paulo**

## 3. Introdução

Este projeto modela um problema real de acesso a serviços de saúde por distritos da cidade de São Paulo utilizando Teoria dos Grafos. O objetivo desta parte da disciplina é consolidar:

1. a modelagem do problema em arquivo `grafo.txt` no formato exigido;
2. a implementação de uma aplicação em Python com menu de operações (`a` até `j`);
3. validação de conexidade e estrutura do grafo.

A aplicação foi desenvolvida em **lista de adjacência**, com suporte a pesos em vértices e arestas, conforme tipo de grafo informado no arquivo.

## 4. Definição do problema real e modelagem

### 4.1 Problema

Existe desigualdade territorial no acesso a serviços de saúde. Distritos com baixa conectividade territorial ou maior distância entre regiões tendem a apresentar piores condições de acesso.

### 4.2 Elementos de modelagem

- **Vértices**: distritos administrativos de São Paulo.
- **Arestas**: relações de adjacência geográfica entre distritos.
- **Peso de vértice**: população do distrito.
- **Peso de aresta**: distância estimada (km) entre distritos adjacentes.

### 4.3 Tipo de grafo utilizado

No arquivo [grafo.txt](grafo.txt), o tipo definido é:

- **Tipo 3**: grafo **não orientado** com **peso em vértices e arestas**.

## 5. Estudo de caso com dados reais

Bases reais utilizadas na preparação do grafo:

- `deinfosacadsau2014.csv` (unidades de saúde e leitos)
- `evolucao_msp_pop_sexo_idade.csv` (população por distrito)

Recorte territorial aplicado para viabilidade de entrega (grupo de 3 alunos):

- zonas mantidas: **Leste, Norte e Sul**

Resultado final do grafo modelado:

- **71 vértices**
- **215 arestas**

Atendimento aos mínimos do enunciado:

- vértices: $71 \ge 70$ ✅
- arestas: $215 \ge 180$ ✅

## 6. Visualizações técnicas do grafo (geradas por código)

As figuras abaixo foram geradas automaticamente a partir do [grafo.txt](grafo.txt) pelo script [gerar_figuras_relatorio.py](gerar_figuras_relatorio.py).

### 6.1 Visão geral da rede

![Visão geral](figuras/01_visao_geral_grafo.png)

### 6.2 Distribuição de grau

![Histograma de graus](figuras/02_histograma_graus.png)

### 6.3 Matriz de adjacência

![Matriz de adjacência](figuras/03_matriz_adjacencia.png)

## 7. Métricas estruturais do grafo

Fonte: [figuras/metricas.json](figuras/metricas.json)

- Tipo: 3 (não orientado, ponderado em vértices e arestas)
- Número de vértices: 71
- Número de arestas: 215
- Grau médio: 6.06
- Grau máximo: 11
- Grau mínimo: 1
- Densidade: 0.0865
- Conexidade: **conexo** (1 componente)

### 7.1 Vértices de maior grau (Top 10)

1. Belém (id 6) — grau 11
2. Mooca (id 52) — grau 11
3. Penha (id 58) — grau 11
4. Tatuapé (id 79) — grau 11
5. Água Rasa (id 1) — grau 10
6. Carrão (id 19) — grau 10
7. Mandaqui (id 49) — grau 10
8. Vila Formosa (id 84) — grau 10
9. Vila Guilherme (id 85) — grau 10
10. Vila Maria (id 88) — grau 10

## 8. Implementação da aplicação com menu (itens a-j)

Arquivo-fonte principal: [projeto_grafo_menu.py](projeto_grafo_menu.py)

Itens implementados conforme enunciado:

- `a)` Ler dados do arquivo `grafo.txt`
- `b)` Gravar dados no arquivo `grafo.txt`
- `c)` Inserir vértice
- `d)` Inserir aresta
- `e)` Remover vértice
- `f)` Remover aresta
- `g)` Mostrar conteúdo do arquivo
- `h)` Mostrar grafo (lista de adjacência)
- `i)` Apresentar conexidade do grafo e reduzido
- `j)` Encerrar aplicação

Além disso, o cabeçalho do código contém integrantes, síntese do arquivo e histórico de alterações.

## 9. Testes de execução (2 testes por opção)

Evidência consolidada em: [evidencias/testes_menu.txt](evidencias/testes_menu.txt)

Cobertura registrada:

- `a1`, `a2`
- `b1`, `b2`
- `c1`, `c2`
- `d1`, `d2`
- `e1`, `e2`
- `f1`, `f2`
- `g1`, `g2`
- `h1`, `h2`
- `i1`, `i2` (inclui teste direcionado e reduzido)
- `j1`, `j2`

Arquivos auxiliares de evidência:

- [evidencias/teste_i2_direcionado.txt](evidencias/teste_i2_direcionado.txt)
- [evidencias/validacao_grafo.txt](evidencias/validacao_grafo.txt)
- [evidencias/roteiro_prints.txt](evidencias/roteiro_prints.txt)

## 10. ODS contemplados e justificativa

### ODS 3 — Saúde e Bem-Estar
O modelo analisa estrutura territorial de acesso à saúde, usando conectividade e distância como base de comparação.

### ODS 10 — Redução das Desigualdades
A análise em grafo ajuda a identificar diferenças entre regiões e possíveis áreas com maior vulnerabilidade de acesso.

### ODS 11 — Cidades e Comunidades Sustentáveis
A visualização e os indicadores estruturais apoiam decisões de organização territorial de serviços públicos.

## 11. Apêndice — GitHub

Repositório público:

- https://github.com/Lucas-FcNw/Programming

Caminho da entrega:

- `Python/Projetos/Grafos/entrega_parte2`

## 12. Conclusão

A entrega da Parte 2 foi consolidada com foco estrito no enunciado da disciplina: modelagem formal em `grafo.txt`, aplicação funcional em Python com menu completo `a-j`, verificação de conexidade e documentação técnica. Os requisitos mínimos de tamanho do grafo foram atendidos com margem e os testes operacionais foram registrados.
