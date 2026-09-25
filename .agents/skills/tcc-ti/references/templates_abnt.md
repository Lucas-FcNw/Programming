# Templates de Estrutura ABNT para TCC de Tecnologia da Informação

> ⚠️ **AVISO**: Este arquivo contém templates e exemplos ilustrativos. Onde existir um "exemplo preenchido", ele contém dados FICTÍCIOS do projeto hipotético "SecWatch".
> Use apenas as **estruturas vazias** com `[INSERIR DADO REAL]` para o TCC do Rede de Acesso SP.
> **NUNCA** copiar números, nomes ou resultados dos exemplos preenchidos.

Este documento contém a estrutura-modelo pronta para ser adaptada ao tema do TCC de T.I.

---

## MODELO DE CAPA

```
[NOME DA INSTITUIÇÃO DE ENSINO SUPERIOR]
[CENTRO/FACULDADE DE TECNOLOGIA]
[CURSO DE TECNOLOGIA DA INFORMAÇÃO / CIÊNCIA DA COMPUTAÇÃO / SISTEMAS DE INFORMAÇÃO]




[NOME COMPLETO DO(A) AUTOR(A)]




[TÍTULO DO TRABALHO: subtítulo (se houver)]




[Cidade]
[Ano]
```

---

## MODELO DE FOLHA DE ROSTO

```
[NOME COMPLETO DO(A) AUTOR(A)]




[TÍTULO DO TRABALHO: subtítulo (se houver)]



Trabalho de Conclusão de Curso apresentado
ao Curso de [nome do curso] da [Instituição],
como requisito parcial para obtenção do grau
de [Bacharel/Tecnólogo] em [nome do curso].

Orientador(a): Prof(a). [Dr(a)./Me./Esp.] [Nome completo]
Coorientador(a): Prof(a). [Nome completo] (se houver)



[Cidade]
[Ano]
```

---

## MODELO DE RESUMO

```
RESUMO

[Contextualização breve do tema e problema — 2-3 frases]. [Lacuna ou motivação —
1 frase]. Este trabalho teve como objetivo [objetivo geral — 1 frase]. [Breve
descrição da metodologia: tipo de pesquisa, tecnologias, métricas de avaliação —
2-3 frases]. [Principais resultados quantitativos — 2-3 frases]. [Conclusão
principal e contribuição — 1-2 frases].

Palavras-chave: [Termo 1]. [Termo 2]. [Termo 3]. [Termo 4]. [Termo 5].
```

### Exemplo preenchido:

> ⚠️ EXEMPLO FICTÍCIO (projeto SecWatch, não é o Rede de Acesso SP). Use como modelo de ESTRUTURA apenas.

```
RESUMO

[Contextualização do problema em 2-3 frases com dado concreto verificado].
[Lacuna identificada na literatura após revisão bibliográfica — 1 frase].
Este trabalho teve como objetivo [objetivo geral do Rede de Acesso SP — 1 frase].
A pesquisa, de natureza aplicada, seguiu [metodologia adotada].
O sistema foi desenvolvido com [tecnologias com versões].
[Descrição do algoritmo e dados utilizados].
A avaliação foi conduzida em [ambiente real descrito].
[INSERIR RESULTADO REAL] demonstrou [INSERIR INTERPRETAÇÃO REAL].
Conclui-se que [conclusão baseada em resultados reais].

Palavras-chave: [Termo 1]. [Termo 2]. [Termo 3]. [Termo 4]. [Termo 5].
```

---

## MODELO DE ABSTRACT

```
ABSTRACT

[Tradução fiel do resumo para o inglês, mantendo a mesma estrutura e conteúdo].

Keywords: [Term 1]. [Term 2]. [Term 3]. [Term 4]. [Term 5].
```

### Exemplo preenchido:

> ⚠️ EXEMPLO FICTÍCIO (projeto SecWatch, não é o Rede de Acesso SP). Use como modelo de ESTRUTURA apenas.

```
ABSTRACT

[Translation of the actual Resumo into English].

Keywords: [Term 1]. [Term 2]. [Term 3]. [Term 4]. [Term 5].
```

---

## MODELO DE SUMÁRIO

```
SUMÁRIO

1 INTRODUÇÃO ................................................................................................ XX
  1.1 Problema de pesquisa ............................................................................ XX
  1.2 Objetivos ............................................................................................... XX
    1.2.1 Objetivo geral ................................................................................... XX
    1.2.2 Objetivos específicos ........................................................................ XX
  1.3 Justificativa ........................................................................................... XX
  1.4 Organização do trabalho ......................................................................... XX
2 REFERENCIAL TEÓRICO .............................................................................. XX
  2.1 [Área de conhecimento base — ex: Segurança da Informação] ............... XX
    2.1.1 [Subconceito 1] ................................................................................ XX
    2.1.2 [Subconceito 2] ................................................................................ XX
  2.2 [Tecnologias envolvidas — ex: Aprendizado de Máquina] ....................... XX
    2.2.1 [Subtecnologia 1] ............................................................................. XX
    2.2.2 [Subtecnologia 2] ............................................................................. XX
  2.3 [Conceito complementar — ex: Arquiteturas Web] .................................. XX
  2.4 Trabalhos relacionados ........................................................................... XX
3 METODOLOGIA ............................................................................................. XX
  3.1 Classificação da pesquisa ....................................................................... XX
  3.2 Metodologia de desenvolvimento ............................................................ XX
  3.3 Ferramentas e tecnologias ...................................................................... XX
  3.4 Métricas de avaliação ............................................................................. XX
  3.5 Cronograma ........................................................................................... XX
4 DESENVOLVIMENTO .................................................................................... XX
  4.1 Requisitos do sistema ............................................................................. XX
    4.1.1 Requisitos funcionais ........................................................................ XX
    4.1.2 Requisitos não-funcionais .................................................................. XX
  4.2 Arquitetura do sistema ............................................................................ XX
  4.3 Modelagem de dados .............................................................................. XX
  4.4 Implementação ....................................................................................... XX
    4.4.1 [Módulo/componente 1] ..................................................................... XX
    4.4.2 [Módulo/componente 2] ..................................................................... XX
    4.4.3 [Módulo/componente 3] ..................................................................... XX
  4.5 Interface do sistema ............................................................................... XX
  4.6 Testes .................................................................................................... XX
5 RESULTADOS E DISCUSSÃO ....................................................................... XX
  5.1 [Eixo de avaliação 1] ............................................................................. XX
  5.2 [Eixo de avaliação 2] ............................................................................. XX
  5.3 Comparação com trabalhos relacionados ................................................. XX
  5.4 Limitações ............................................................................................. XX
6 CONSIDERAÇÕES FINAIS ............................................................................ XX
  6.1 Contribuições do trabalho ....................................................................... XX
  6.2 Trabalhos futuros ................................................................................... XX
REFERÊNCIAS ................................................................................................. XX
APÊNDICE A — Código-fonte (repositório) ...................................................... XX
APÊNDICE B — Manual do usuário .................................................................. XX
APÊNDICE C — Questionário SUS aplicado ...................................................... XX
ANEXO A — [Título do anexo] .......................................................................... XX
```

---

## MODELO DE REQUISITOS

### Requisitos Funcionais

```
Quadro X — Requisitos funcionais do sistema

+------+-------------------------------------------------+-------------+
| ID   | Descrição                                       | Prioridade  |
+------+-------------------------------------------------+-------------+
| RF01 | O sistema deve permitir o cadastro de usuários  | Essencial   |
|      | com e-mail e senha.                             |             |
+------+-------------------------------------------------+-------------+
| RF02 | O sistema deve receber logs via protocolo        | Essencial   |
|      | syslog e Windows Event Log.                     |             |
+------+-------------------------------------------------+-------------+
| RF03 | O sistema deve analisar logs em tempo real       | Essencial   |
|      | utilizando o algoritmo Isolation Forest.         |             |
+------+-------------------------------------------------+-------------+
| RF04 | O sistema deve emitir alertas visuais e por      | Essencial   |
|      | e-mail quando anomalias forem detectadas.        |             |
+------+-------------------------------------------------+-------------+
| RF05 | O sistema deve exibir um dashboard com           | Importante  |
|      | métricas de segurança em tempo real.             |             |
+------+-------------------------------------------------+-------------+
| RF06 | O sistema deve permitir a exportação de          | Desejável   |
|      | relatórios em PDF e CSV.                         |             |
+------+-------------------------------------------------+-------------+

Fonte: Elaborado pelo autor (Ano).
```

### Requisitos Não-Funcionais

```
Quadro X — Requisitos não-funcionais do sistema

+------+-------------------------------------------------+-------------+
| ID   | Descrição                                       | Categoria   |
+------+-------------------------------------------------+-------------+
| RNF01| O sistema deve processar no mínimo 1.000 logs   | Desempenho  |
|      | por segundo.                                    |             |
+------+-------------------------------------------------+-------------+
| RNF02| O tempo de resposta da API não deve exceder      | Desempenho  |
|      | 200ms para 95% das requisições.                 |             |
+------+-------------------------------------------------+-------------+
| RNF03| O sistema deve ser compatível com Chrome,        | Compatibil. |
|      | Firefox e Edge nas duas últimas versões.         |             |
+------+-------------------------------------------------+-------------+
| RNF04| Os dados de usuários devem ser armazenados com   | Segurança   |
|      | hash bcrypt e transmitidos via HTTPS.            |             |
+------+-------------------------------------------------+-------------+
| RNF05| O sistema deve estar disponível 99,5% do tempo.  | Disponibil. |
+------+-------------------------------------------------+-------------+
| RNF06| O código deve seguir as convenções PEP 8 e ter   | Manutenção  |
|      | cobertura de testes mínima de 70%.               |             |
+------+-------------------------------------------------+-------------+

Fonte: Elaborado pelo autor (Ano).
```

---

## MODELO DE CRONOGRAMA

```
Quadro X — Cronograma de execução do projeto

+---------------------------+-----+-----+-----+-----+-----+-----+
| Atividade                 | Mês1| Mês2| Mês3| Mês4| Mês5| Mês6|
+---------------------------+-----+-----+-----+-----+-----+-----+
| Revisão de literatura     |  X  |  X  |     |     |     |     |
| Definição de requisitos   |  X  |     |     |     |     |     |
| Modelagem e arquitetura   |     |  X  |     |     |     |     |
| Desenvolvimento (Sprint 1)|     |  X  |  X  |     |     |     |
| Desenvolvimento (Sprint 2)|     |     |  X  |  X  |     |     |
| Desenvolvimento (Sprint 3)|     |     |     |  X  |     |     |
| Testes e avaliação        |     |     |     |  X  |  X  |     |
| Redação do TCC            |  X  |  X  |  X  |  X  |  X  |  X  |
| Revisão e ajustes finais  |     |     |     |     |  X  |  X  |
| Apresentação/defesa       |     |     |     |     |     |  X  |
+---------------------------+-----+-----+-----+-----+-----+-----+

Fonte: Elaborado pelo autor (Ano).
```

---

## MODELO DE QUESTIONÁRIO SUS (System Usability Scale)

```
QUESTIONÁRIO DE USABILIDADE — SYSTEM USABILITY SCALE (SUS)

Adaptado de Brooke (1996). Tradução para português brasileiro por Tenório et al. (2011).

Instruções: Para cada afirmação abaixo, marque o número que melhor representa
sua opinião, sendo:
1 = Discordo totalmente | 5 = Concordo totalmente

1. Eu acho que gostaria de usar esse sistema com frequência.
   [ 1 ] [ 2 ] [ 3 ] [ 4 ] [ 5 ]

2. Eu acho o sistema desnecessariamente complexo.
   [ 1 ] [ 2 ] [ 3 ] [ 4 ] [ 5 ]

3. Eu achei o sistema fácil de usar.
   [ 1 ] [ 2 ] [ 3 ] [ 4 ] [ 5 ]

4. Eu acho que precisaria de ajuda de uma pessoa com conhecimentos
   técnicos para usar o sistema.
   [ 1 ] [ 2 ] [ 3 ] [ 4 ] [ 5 ]

5. Eu acho que as várias funções do sistema estão muito bem integradas.
   [ 1 ] [ 2 ] [ 3 ] [ 4 ] [ 5 ]

6. Eu acho que o sistema apresenta muita inconsistência.
   [ 1 ] [ 2 ] [ 3 ] [ 4 ] [ 5 ]

7. Eu imagino que as pessoas aprenderão a usar esse sistema rapidamente.
   [ 1 ] [ 2 ] [ 3 ] [ 4 ] [ 5 ]

8. Eu achei o sistema atrapalhado de usar.
   [ 1 ] [ 2 ] [ 3 ] [ 4 ] [ 5 ]

9. Eu me senti confiante ao usar o sistema.
   [ 1 ] [ 2 ] [ 3 ] [ 4 ] [ 5 ]

10. Eu precisei aprender várias coisas novas antes de conseguir
    usar o sistema.
    [ 1 ] [ 2 ] [ 3 ] [ 4 ] [ 5 ]

Cálculo do score:
- Itens ímpares (1, 3, 5, 7, 9): (resposta - 1)
- Itens pares (2, 4, 6, 8, 10): (5 - resposta)
- SUS Score = (soma de todos os itens) × 2.5
- Escala: 0-100 pontos. Acima de 68 = aceitável.
```

---

## MODELO DE README.md PARA O REPOSITÓRIO

````markdown
# [Nome do Projeto]

[Descrição breve do projeto — 1-2 frases]

> Trabalho de Conclusão de Curso — [Curso] — [Instituição] — [Ano]
> Autor: [Nome] | Orientador(a): [Nome]

## Sumário

- [Sobre](#sobre)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Testes](#testes)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Licença](#licença)

## Sobre

[Descrição mais detalhada do projeto, problema que resolve,
público-alvo — 1 parágrafo]

## Tecnologias

| Componente | Tecnologia | Versão |
| ---------- | ---------- | ------ |
| Backend    | [...]      | [...]  |
| Frontend   | [...]      | [...]  |
| Banco      | [...]      | [...]  |
| ...        | ...        | ...    |

## Pré-requisitos

- [Requisito 1] (ex: Docker >= 25.0)
- [Requisito 2] (ex: Node.js >= 20)
- [Requisito 3] (ex: Python >= 3.12)

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/[usuario]/[projeto].git
cd [projeto]

# Configurar variáveis de ambiente
cp .env.example .env

# Subir com Docker Compose
docker compose up -d

# OU instalar manualmente
pip install -r requirements.txt
npm install
```
````

## Uso

```bash
# Iniciar o backend
python -m uvicorn app.main:app --reload

# Iniciar o frontend
npm run dev
```

Acesse: http://localhost:3000

## Testes

```bash
# Testes do backend
pytest --cov=app tests/

# Testes do frontend
npm test
```

## Estrutura do Projeto

```
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.tsx
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

## Licença

Este projeto está sob a licença [MIT/Apache 2.0/GPL].
Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

```

---

## TEMPLATES DE BENCHMARK E ESCALABILIDADE

### Tabela de Resultados de Benchmark — Desempenho Geral

```

Tabela X — Resultados de benchmark de desempenho do sistema [Nome]

Ambiente de teste: [CPU modelo], [RAM] GB, [SO versão], [Docker versão]
Ferramenta: [JMeter/k6/Locust/wrk], configuração: [parâmetros]

+-----------------------+----------+----------+----------+----------+
| Métrica | 100 req | 1.000 req| 10.000 req| 100.000 req|
+-----------------------+----------+----------+----------+----------+
| Latência p50 (ms) | | | | |
| Latência p95 (ms) | | | | |
| Latência p99 (ms) | | | | |
| Throughput (req/s) | | | | |
| Taxa de erro (%) | | | | |
| Tempo de CPU (ms) | | | | |
| Consumo de RAM pico | | | | |
| (MB) | | | | |
+-----------------------+----------+----------+----------+----------+

Fonte: Dados da pesquisa (Ano).
Nota: Valores representam a média de 5 execuções. Desvio-padrão < 5% em
todas as métricas.

```

### Tabela de Escalabilidade — Crescimento de Dados

```

Tabela X — Comportamento do sistema sob crescimento do volume de dados

+-----------------------+---------+---------+---------+---------+---------+
| Métrica | 1x | 10x | 100x | 1.000x | 10.000x |
| | (base) | | | | |
+-----------------------+---------+---------+---------+---------+---------+
| Volume de dados | [X] reg | [10X] | [100X] | [1000X] | [10000X]|
| Tempo de processa- | | | | | |
| mento (s) | | | | | |
| Consumo de RAM (MB) | | | | | |
| Consumo de disco (MB) | | | | | |
| Throughput (reg/s) | | | | | |
| Degradação vs. base | 1,0x | | | | |
| Ponto de ruptura | N/A | N/A | N/A | [?] | [?] |
+-----------------------+---------+---------+---------+---------+---------+

Fonte: Dados da pesquisa (Ano).
Nota: "Ponto de ruptura" definido como momento em que a taxa de erro
excede 5% ou o tempo de resposta excede o limiar do RNF [X].

```

### Tabela Comparativa de Algoritmos — Complexidade

```

Tabela X — Comparação de complexidade entre algoritmos candidatos

+-----------------+-------------+-------------+----------+-----------+
| Algoritmo | Tempo | Espaço | Tempo | Adequação |
| | (Big-O) | (Big-O) | real (s) | ao domínio|
+-----------------+-------------+-------------+----------+-----------+
| [Algoritmo A] | O(V log V) | O(V + E) | | [Sim/Não] |
| [Algoritmo B] | O(V²) | O(V²) | | [Sim/Não] |
| [Algoritmo C] | O(V·E) | O(V + E) | | [Sim/Não] |
| **[Escolhido]** | **O(X)** | **O(X)** | | **Sim** |
+-----------------+-------------+-------------+----------+-----------+

Fonte: Elaborado pelo autor (Ano).
Nota: "Tempo real" medido com dataset de [N] registros em [ambiente].
"Adequação ao domínio" considera [critérios específicos do problema].

```

### Tabela de Métricas de Classificação (ML)

```

Tabela X — Métricas de desempenho dos modelos de classificação

+--------------------+-----------+-----------+-----------+-----------+
| Modelo | Precisão | Revocação | F1-Score | AUC-ROC |
+--------------------+-----------+-----------+-----------+-----------+
| [Modelo A] | | | | |
| [Modelo B] | | | | |
| [Modelo C] | | | | |
| **[Modelo final]** | | | | |
+--------------------+-----------+-----------+-----------+-----------+

Fonte: Dados da pesquisa (Ano).
Nota: Validação cruzada k-fold (k=10). Dataset: [N] amostras, razão de
classes [X:Y]. Seed de aleatoriedade: [42].

```

---

## TEMPLATE DE PIPELINE ETL

### Quadro de Fontes de Dados

```

Quadro X — Fontes de dados utilizadas no estudo

+----+---------------------+----------------+------------+--------+--------+
| # | Fonte | Tipo de Acesso | Data de | Volume | Formato|
| | | | Extração | Bruto | |
+----+---------------------+----------------+------------+--------+--------+
| 1 | [Nome da fonte] | [API/Download/ | dd/mm/aaaa | [X] MB | [CSV/ |
| | | Scraping] | | | JSON] |
+----+---------------------+----------------+------------+--------+--------+
| 2 | [Nome da fonte] | [Tipo] | dd/mm/aaaa | [X] MB | [Tipo] |
+----+---------------------+----------------+------------+--------+--------+
| 3 | [Nome da fonte] | [Tipo] | dd/mm/aaaa | [X] MB | [Tipo] |
+----+---------------------+----------------+------------+--------+--------+

Fonte: Elaborado pelo autor (Ano).

```

### Quadro de Tratamento de Dados

```

Quadro X — Procedimentos de transformação aplicados ao dataset

+----+----------------------+-------------+------------------+-------------+
| # | Tratamento | Registros | Método/Critério | Justificativa|
| | | Afetados | | |
+----+----------------------+-------------+------------------+-------------+
| 1 | Remoção de nulos | [N] ([%]%) | [Remoção/ | [Por quê] |
| | | | Imputação] | |
+----+----------------------+-------------+------------------+-------------+
| 2 | Remoção de outliers | [N] ([%]%) | [IQR/Z-score/ | [Por quê] |
| | | | Manual] | |
+----+----------------------+-------------+------------------+-------------+
| 3 | Normalização | Todos | [Min-Max/Z-score]| [Por quê] |
+----+----------------------+-------------+------------------+-------------+
| 4 | Encoding categórico | [N] colunas | [One-hot/Label/ | [Por quê] |
| | | | Target] | |
+----+----------------------+-------------+------------------+-------------+
| 5 | Feature engineering | [N] features| [Descrição] | [Por quê] |
| | | criadas | | |
+----+----------------------+-------------+------------------+-------------+

Fonte: Elaborado pelo autor (Ano).
Nota: Dataset final: [N] registros, [M] atributos. Scripts disponíveis
em [URL do repositório]/scripts/etl/.

```

### Quadro de Limitações dos Dados

```

Quadro X — Limitações e vieses conhecidos dos dados utilizados

+----+----------------------------+--------------------+------------------+
| # | Limitação | Impacto potencial | Mitigação adotada|
+----+----------------------------+--------------------+------------------+
| 1 | [Ex: Dados referentes | [Pode não refletir | [Ex: Declarado |
| | apenas ao período diurno] | padrões noturnos] | como limitação] |
+----+----------------------------+--------------------+------------------+
| 2 | [Ex: Censo 2022 — dados | [Migrações | [Análise de |
| | podem estar defasados] | posteriores] | sensibilidade] |
+----+----------------------------+--------------------+------------------+
| 3 | [Ex: Assume capacidade | [Superestima | [Trabalho futuro:|
| | idêntica entre unidades] | equidade de acesso]| dados de lotação]|
+----+----------------------------+--------------------+------------------+

Fonte: Elaborado pelo autor (Ano).

```

---

## TEMPLATE DE REVISÃO SISTEMÁTICA (RSL)

### Quadro de Protocolo de Busca

```

Quadro X — Protocolo de revisão sistemática da literatura

+-----------------------------+-------------------------------------------+
| Item | Descrição |
+-----------------------------+-------------------------------------------+
| Questão de pesquisa | [Pergunta que guia a busca] |
+-----------------------------+-------------------------------------------+
| String de busca | ("termo1" OR "termo2") AND ("termo3" OR |
| | "termo4") AND ("termo5") |
+-----------------------------+-------------------------------------------+
| Bases de dados | IEEE Xplore, ACM Digital Library, Scopus, |
| | Google Scholar, [outras] |
+-----------------------------+-------------------------------------------+
| Período | [Ano início] — [Ano fim] |
+-----------------------------+-------------------------------------------+
| Idiomas | [Português, Inglês, ...] |
+-----------------------------+-------------------------------------------+
| Critérios de inclusão | - Artigos com revisão por pares |
| | - Resultados experimentais quantitativos |
| | - [Outros critérios] |
+-----------------------------+-------------------------------------------+
| Critérios de exclusão | - Artigos sem acesso ao texto completo |
| | - Resumos expandidos (< 4 páginas) |
| | - [Outros critérios] |
+-----------------------------+-------------------------------------------+
| Total identificado | [N] artigos |
| Após remoção de duplicatas | [N] artigos |
| Após leitura de títulos | [N] artigos |
| Após leitura de abstracts | [N] artigos |
| Após leitura integral | [N] artigos (incluídos na revisão) |
+-----------------------------+-------------------------------------------+

Fonte: Elaborado pelo autor (Ano).

```

### Matriz de Comparação de Trabalhos Relacionados

```

Quadro X — Matriz de comparação entre trabalhos relacionados e a proposta

+-------------------+----------+----------+----------+----------+----------+
| Critério | [Autor1] | [Autor2] | [Autor3] | [Autor4] | Proposta |
| | (Ano) | (Ano) | (Ano) | (Ano) | |
+-------------------+----------+----------+----------+----------+----------+
| Algoritmo/Método | | | | | |
+-------------------+----------+----------+----------+----------+----------+
| Dataset utilizado | | | | | |
+-------------------+----------+----------+----------+----------+----------+
| [Métrica 1] | | | | | |
| (ex: F1-Score) | | | | | |
+-------------------+----------+----------+----------+----------+----------+
| [Métrica 2] | | | | | |
| (ex: Latência) | | | | | |
+-------------------+----------+----------+----------+----------+----------+
| Escalabilidade | [Sim/Não]| [Sim/Não]| [Sim/Não]| [Sim/Não]| [Sim/Não]|
+-------------------+----------+----------+----------+----------+----------+
| Custo computac. | | | | | |
+-------------------+----------+----------+----------+----------+----------+
| Código aberto | [Sim/Não]| [Sim/Não]| [Sim/Não]| [Sim/Não]| [Sim/Não]|
+-------------------+----------+----------+----------+----------+----------+
| [Critério espec.] | | | | | |
+-------------------+----------+----------+----------+----------+----------+

Fonte: Elaborado pelo autor (Ano).
Nota: [Autor1] refere-se a [referência completa]. Critérios selecionados
conforme relevância ao problema de pesquisa definido na Seção 1.

```

```
