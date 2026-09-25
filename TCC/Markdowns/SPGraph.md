# Projeto

## Nome do Projeto
**SPGraph**

## Nome do Sistema
**A DEFINIR**

---

# Tema

Desenvolvimento de um sistema interativo que modela a cidade de São Paulo como um grafo para analisar desigualdades no acesso a serviços públicos essenciais, em conformidade com a **ODS 10 – Redução das Desigualdades**.

---

# Objetivo Geral

Desenvolver um sistema funcional que utilize modelagem por grafos para analisar e visualizar desigualdades no acesso a serviços públicos nos distritos da cidade de São Paulo.

---

# Objetivos Específicos

- Modelar os distritos como **vértices** de um grafo.
- Modelar conexões geográficas entre distritos como **arestas ponderadas**.
- Implementar algoritmos clássicos de grafos, como **Dijkstra** e **BFS**.
- Calcular métricas de acessibilidade.
- Desenvolver uma interface interativa com foco em usabilidade.
- Realizar avaliação básica de usabilidade conforme princípios de **IHC**.

---

# Justificativa

A desigualdade urbana se manifesta no acesso desigual a serviços como saúde, educação e assistência social. Distritos periféricos tendem a apresentar maior tempo de deslocamento até serviços essenciais quando comparados a regiões centrais.

O projeto busca identificar padrões de acessibilidade, destacar regiões mais isoladas e fornecer uma visualização comparativa entre distritos, contribuindo para a discussão da **ODS 10 – Redução das Desigualdades**.

---

# Modelagem em Teoria dos Grafos

## Estrutura do Grafo

- **Vértices:** distritos administrativos da cidade de São Paulo (96 distritos).
- **Arestas:** conexões entre distritos geograficamente vizinhos.
- **Peso das arestas:** distância estimada entre os centros geográficos dos distritos.

Essa modelagem atende ao requisito mínimo de aproximadamente **70 vértices e 180 arestas**.

## Tipo de Grafo

- Grafo **não direcionado**.
- Grafo **ponderado**.
- Estrutura predominantemente **conexa**.

## Algoritmos Utilizados

- **Dijkstra:** cálculo do menor caminho entre um distrito e o serviço mais próximo.
- **BFS:** análise de conectividade e alcance.
- **Grau do vértice:** identificação de distritos mais conectados.
- **Medidas simples de centralidade.**

---

# Funcionalidades do Sistema

O usuário poderá:

- Selecionar um distrito.
- Escolher o tipo de serviço (UBS, hospital, escola ou CRAS).

Visualizar:

- Distância até o serviço mais próximo.
- Caminho mínimo.
- Ranking de acessibilidade.
- Comparação com a média da cidade.
- Identificação de distritos relativamente isolados.

---

# Parte de Interação Humano-Computador (IHC)

O projeto incluirá:

- Protótipo inicial de baixa fidelidade.
- Implementação funcional do sistema.
- Aplicação de heurísticas de usabilidade (por exemplo, heurísticas de Nielsen).
- Teste com usuários e coleta de feedback.
- Ajustes baseados nos resultados da avaliação.

O foco será:

- Clareza.
- Simplicidade de navegação.
- Feedback imediato ao usuário.
- Organização adequada das informações.

---

# Arquitetura do Sistema

## Camada de Dados

- Coleta de dados públicos da cidade de São Paulo.
- Tratamento e organização em formato estruturado (CSV ou JSON).

## Camada de Processamento

- Construção do grafo.
- Implementação e execução dos algoritmos.

## Camada de Interface

- Entrada de dados pelo usuário.
- Exibição dos resultados e métricas calculadas.

---

# Fontes de Dados

- Portal de Dados Abertos da Prefeitura de São Paulo.
- GeoSampa.
- Dados da SPTrans (caso o projeto seja expandido para considerar mobilidade).

---

# Cronograma Proposto

## Mês 1

- Coleta e tratamento de dados.
- Modelagem do grafo.
- Implementação dos algoritmos.

## Mês 2

- Desenvolvimento da interface.
- Integração entre processamento e interface.

## Mês 3

- Testes de usabilidade.
- Ajustes e refinamentos.
- Documentação e preparação da apresentação.

## Liderado por
 `Lucas Fernandes 10419400`
 `Lendy Naiara Pacheco 10428525`
 `Anna Luiza Santos 10417401`