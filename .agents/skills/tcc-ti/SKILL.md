---
name: "TCC Tecnologia da Informação"
description: "Skill para elaboração completa de Trabalho de Conclusão de Curso (TCC) em Tecnologia da Informação (T.I.), com verificação antiplágio, autenticidade, linguagem acadêmica de alta qualidade, originalidade, código-fonte funcional, uso rigoroso de fontes primárias verificáveis e conformidade com normas ABNT. Acionada quando o usuário solicitar criação, revisão ou auxílio em TCC de Tecnologia da Informação, Ciência da Computação, Sistemas de Informação, Engenharia de Software ou áreas correlatas."
---

# TCC de Tecnologia da Informação — Guia de Elaboração (v4)

> **Projeto de referência desta skill**: **SPGraph** — modelo baseado em Teoria dos Grafos para identificação de vulnerabilidades topológicas ocultas ("gargalos invisíveis" via algoritmo de Tarjan) e simulação de efeito cascata por sobrecarga operacional (via Busca em Largura — BFS acoplada ao Modelo Gravitacional de Huff/3SFCA e à regra de 70% Demanda Programada / 30% Demanda Espontânea do SUS) na malha de 454 Unidades Básicas de Saúde (UBSs) de São Paulo.
>
> Esta skill é especializada nesse projeto. Ela não deve ser transformada em skill genérica de TCC.

---

## PARTE I — REGRAS ABSOLUTAS

---

### REGRA DE OURO — FIDELIDADE À IMPLEMENTAÇÃO REAL

A skill existe para documentar cientificamente o projeto que realmente existe. Ela não deve reconstruir o projeto segundo uma arquitetura idealizada apenas porque essa arquitetura seria academicamente mais sofisticada.

**Ordem obrigatória de operação:**

1. Identificar como o projeto realmente funciona.
2. Identificar como os dados realmente são processados.
3. Identificar quais algoritmos realmente estão implementados.
4. Identificar quais resultados realmente foram obtidos.
5. Somente então escrever ou propor adequações textuais.

**A skill NÃO PODE, em nenhuma circunstância:**

- Inventar componentes do sistema.
- Presumir que existe uma API, banco, grafo viário, malha OSM, heap, estrutura de dados ou biblioteca que não esteja comprovadamente presente no código ou documentação.
- Transformar uma arquitetura desejável em uma arquitetura existente.
- Substituir silenciosamente o algoritmo implementado por outro.
- Alterar silenciosamente a metodologia.
- Atribuir ao sistema uma capacidade que não esteja demonstrada.
- Converter uma hipótese metodológica em fato.
- Converter uma proposta futura em funcionalidade existente.

**Quando houver divergência** entre o que o TCC afirma, o que o código faz, o que os dados demonstram e o que a metodologia pretende, a skill deve interromper a redação definitiva daquele ponto e sinalizar assim:

```
DIVERGÊNCIA IDENTIFICADA:
O texto/metodologia afirma [X], porém a implementação/documentação disponível demonstra [Y].
Decisão necessária: manter Y e documentá-lo corretamente, ou alterar a implementação para X.
```

A skill não pode decidir sozinha qual alternativa adotar quando isso modificar o projeto.

---

### R1 — NUNCA INVENTAR REFERÊNCIAS BIBLIOGRÁFICAS

É expressamente proibido criar, sintetizar, deduzir ou completar referências bibliográficas.

Nenhum dos seguintes elementos pode ser inventado ou preenchido por inferência:
- Autor(es)
- Título do trabalho
- Periódico, conferência ou livro
- Volume, número, páginas
- DOI, ISBN, URL, ISSN
- Ano de publicação

Se um DOI informado não corresponder ao artigo, descartar a referência. Não "corrigir" uma referência inventando os dados que faltam.

Se uma referência não puder ser verificada por meio de busca real, ela não pode ser usada.

Quando a ferramenta disponível permitir pesquisa na internet, a literatura deve ser pesquisada antes da redação do referencial teórico.

---

### R2 — NUNCA INVENTAR RESULTADOS EXPERIMENTAIS

É expressamente proibido inventar ou estimar como resultados reais qualquer dos seguintes tipos de dado:
- Benchmarks (latência, throughput, p50/p95/p99)
- Quantidade de requisições, usuários ou participantes
- Respostas de questionários (SUS, escalas Likert)
- Médias, medianas, desvios-padrão, percentis
- Percentuais de ganho, redução ou melhoria
- Resultados de testes de escalabilidade ou carga
- Resultados de usabilidade
- Tempo de execução de algoritmos
- Qualquer número que dependa de experimento não realizado

Se o dado não estiver disponível:
1. Descrever a metodologia de como o dado seria obtido; ou
2. Marcar como `[RESULTADO PENDENTE: descrever como será coletado]`.

Nunca preencher com valores plausíveis.

---

### R3 — TEXTO EXISTENTE NÃO É EVIDÊNCIA

A presença de uma afirmação em uma versão anterior do TCC não comprova sua veracidade.

Um número escrito no TCC não deve ser automaticamente considerado real. Exemplos de valores que exigem auditoria de origem:

- `|V| = 71`
- `|E| = 215`
- 100.000 requisições
- p95 = 110 ms
- 97,8% de redução
- SUS = 78,5
- quantidade de participantes
- quantidade de UBSs
- quantidade de setores censitários
- população total
- qualquer percentual

**Pergunta obrigatória:** "De onde veio esse valor?"

Origens aceitáveis:
- Código verificável
- Dataset
- Documentação formal do projeto
- Arquivo de configuração
- Execução reproduzível
- Resultado experimental realmente executado
- Fonte bibliográfica verificável

Se não houver origem rastreável, classificar como **G — Proveniência incompleta** (ver Seção 2).

---

### R4 — NUNCA USAR EXEMPLOS DA SKILL COMO DADOS DO PROJETO

Os arquivos em `references/` contêm exemplos estruturais com placeholders e material de estilo. Eles são exclusivamente materiais de aprendizado de estrutura e estilo acadêmico.

Nenhuma referência encontrada exclusivamente em arquivo de exemplo pode ser automaticamente adicionada à bibliografia. Ela precisa passar pela mesma verificação bibliográfica de qualquer outra referência.

Nenhum número, resultado, autor, dado ou metodologia presente em arquivos de exemplo pode ser copiado, adaptado ou utilizado como dado do Rede de Acesso SP.

---

### R5 — NUNCA PRESUMIR A ESTRUTURA DO GRAFO

A skill deve primeiro descobrir, pelo código e documentação:

- O que representa um vértice.
- O que representa uma aresta.
- Como as arestas são construídas.
- Qual é o peso da aresta.
- Se o grafo é direcionado ou não direcionado.
- Se os pesos representam distância, tempo, custo ou outra variável.
- Se existe ou não malha viária.
- Se existe ou não OpenStreetMap.
- Se o grafo contém UBSs, setores censitários, ou outra estrutura.

É proibido escrever "grafo viário" sem evidência de que o código representa vias reais.

É proibido confundir:
- Distância geodésica (haversine entre coordenadas)
- Distância euclidiana
- Distância entre centroides
- Distância pela malha viária
- Distância de caminhada
- Distância de carro

Cada conceito é diferente. Usar o que realmente está implementado.

---

### R6 — PROPORCIONALIDADE DAS CONCLUSÕES

A força de uma conclusão deve ser proporcional à força da evidência que a sustenta.

| Se o sistema faz... | Dizer... | Não dizer... |
|---|---|---|
| Calcula distância entre pontos | "calcula acessibilidade/proximidade" | "garante atendimento mais rápido" |
| Usa população como proxy | "incorpora indicador de demanda potencial" | "identifica UBSs sobrecarregadas" |
| Implementou um método | "o método foi implementado" | "o método demonstrou superioridade" |
| Não executou comparação | "não há baseline comparativo nesta versão" | "o método é superior à alternativa" |

---

### R7 — POPULAÇÃO NÃO É CAPACIDADE

A população da Área de Abrangência da UBS (AAUBS) deve ser tratada como **proxy de demanda territorial potencial**, quando essa for a interpretação metodológica adotada.

Não escrever que população é:
- Capacidade da UBS
- Lotação
- Tamanho da fila
- Número de pacientes aguardando
- Tempo de espera
- Demanda efetivamente observada
- Concorrência efetiva
- Velocidade de atendimento

A menos que exista dado empírico que sustente cada uma dessas afirmações.

Preferir: "a população da área de abrangência é utilizada como proxy de demanda potencial" — e explicar a limitação.

---

### R8 — AUTENTICIDADE ACADÊMICA

O texto deve:
- Ser original.
- Ter linguagem acadêmica natural, sem artificialismo.
- Evitar clichês e expressões formulaicas.
- Evitar repetição estrutural de parágrafos.
- Apresentar raciocínio crítico.
- Distinguir claramente fatos, interpretação e hipótese.
- Não copiar a estrutura frasal das fontes.
- Citar corretamente ideias de terceiros.

A skill não deve tentar enganar ferramentas de detecção de IA. Não usar estratégias baseadas em perplexidade, burstiness ou manipulação de métricas linguísticas. A autenticidade vem do conteúdo, não da manipulação estilística.

Não usar vocabulário rebuscado artificialmente. "Ademais", "outrossim", "à guisa de conclusão" e expressões similares devem aparecer apenas quando naturais ao contexto, não como substituição sistemática de expressões mais diretas.

---

## PARTE II — CONTEXTO INSTITUCIONAL

---

### Seção 0 — FCI MACKENZIE

**ATENÇÃO:** Regras institucionais podem mudar entre semestres. As informações abaixo devem ser tratadas como referência, não como norma permanente. Confirmar no documento oficial vigente disponível no Oriente antes de cada entrega.

Quando não houver confirmação do documento vigente, usar: `[REQUISITO INSTITUCIONAL A CONFIRMAR NO ORIENTE]`

#### 0.1 Formato de Entrega por Fase (a confirmar no Oriente)

| Fase | Produto Final | Tamanho indicativo |
|---|---|---|
| TCC I | Relatório Técnico + Pôster | A confirmar |
| TCC II | Artigo Científico (CC e SI) | Aproximadamente 10–20 páginas |

#### 0.2 Estrutura mínima do Relatório Técnico — TCC I (a confirmar)

1. **Introdução** — contextualização, problema, objetivos, contribuições.
2. **Referencial Teórico** — base conceitual, trabalhos correlatos.
3. **Metodologia** — método, coleta de dados, instrumentos.
4. **Cronograma** — tarefas e prazos para o TCC II.

#### 0.3 Estrutura do Artigo Científico — TCC II (a confirmar no template do Oriente)

1. Título
2. Autores e RAs
3. Resumo (PT) + Palavras-chave
4. Abstract (EN) + Keywords
5. Introdução
6. Referencial Teórico / Revisão de Literatura
7. Metodologia
8. Desenvolvimento / Implementação
9. Resultados e Discussão
10. Conclusão
11. Referências (ABNT NBR 6023)

#### 0.4 Critérios de Avaliação da Banca (a confirmar)

A banca avalia, tipicamente:
- Estrutura e coerência do trabalho
- Consistência metodológica
- Embasamento científico
- Relevância, originalidade e ineditismo
- Apresentação oral e defesa

Fórmula de nota e percentuais: `[CONFIRMAR NO DOCUMENTO OFICIAL VIGENTE]`

#### 0.5 Informações Institucionais

- Portal: ORIENTE (https://mackcloud.mackenzie.br/apps/oriente/)
- Número de integrantes do grupo: `[CONFIRMAR]`
- Frequência de orientação: `[CONFIRMAR COM ORIENTADOR]`
- Contato: fci.pesquisa@mackenzie.br
- TCC envolvendo seres humanos: verificar necessidade de CEP/UPM via Plataforma Brasil

---

## PARTE III — SISTEMA DE CONTROLE DE EVIDÊNCIAS

---

### Seção 1 — Fluxo Obrigatório

A escrita nunca deve preceder a auditoria do projeto e a definição metodológica.

```
PROJETO REAL
    |
    v
1. AUDITORIA DO PROJETO         (Seção 2: o que existe de fato)
    |
    v
2. AUDITORIA ALGORÍTMICA        (Seção 3: o que o algoritmo realmente faz)
    |
    v
3. BUSCA BIBLIOGRÁFICA          (Seção 6: literatura verificável)
    |
    v
4. DEFINIÇÃO DO GAP             (Seção 5B: comparativo, não absoluto)
    |
    v
5. ESCRITA                      (Seção 7: protocolo de 15 passos)
    |
    v
6. AUDITORIA FINAL              (Seção 8: verificação de alucinação)
```

---

### Seção 2 — Classificação de Evidências (A–G)

Antes de afirmar qualquer coisa sobre o projeto, classificar cada informação:

| Categoria | Descrição | Pode ser afirmado como fato? |
|---|---|---|
| **A** — Confirmado no código/dados | Verificável diretamente no código-fonte ou dataset | Sim |
| **B** — Confirmado na documentação | Verificável em documentação formal e confiável do projeto | Sim |
| **C** — Planejado, não executado | Previsto, mas ainda não implementado | Apenas como planejamento ou trabalho futuro |
| **D** — Hipótese | Suposição não verificada empiricamente | Apenas como hipótese explícita |
| **E** — Exemplo ilustrativo | Valor de exemplo, não dado real | Nunca como dado do projeto |
| **F** — Não verificável | Origem desconhecida ou não rastreável | Nunca |
| **G** — Proveniência incompleta | Valor aparentemente real, mas origem não rastreável até evidência original | Não, até confirmar origem |

**Regras de uso:**
- Apenas A e B podem ser apresentados como fatos do projeto.
- C aparece como: "está previsto que...", "a metodologia prevê que...".
- D aparece como: "a hipótese é que...", "assume-se que...", "propõe-se que...".
- E e F nunca aparecem como dado do projeto.
- G exige investigação antes de qualquer afirmação. Enquanto não confirmado, tratar como F.
- É proibido transformar C, D, E, F ou G em resultado experimental.

---

### Seção 2.1 — Matriz de Rastreabilidade

Antes de gerar qualquer seção metodologicamente sensível, construir internamente esta matriz (não exibir ao usuário a menos que solicitado, mas usar como mecanismo de controle):

| Informação | Valor | Categoria | Fonte | Localização (arquivo/linha/dataset) | Pode afirmar? |
|---|---|---|---|---|---|
| Número de UBSs | [?] | [A/B/G] | [código/doc] | [onde] | [Sim/Não] |
| Número de vértices | [?] | [A/B/G] | [código] | [onde] | [Sim/Não] |
| Número de arestas | [?] | [A/B/G] | [código] | [onde] | [Sim/Não] |
| Tipo de distância usada | [?] | [A/B/G] | [código] | [onde] | [Sim/Não] |
| Estrutura de dados do grafo | [?] | [A/B/G] | [código] | [onde] | [Sim/Não] |
| Algoritmo implementado | [?] | [A/B/G] | [código] | [onde] | [Sim/Não] |
| Modelo multicritério | [?] | [A/B/C/D] | [código/doc] | [onde] | [Sim/Não] |
| Tempo de execução | [?] | [A/C] | [experimento] | [quando] | [Sim/Não] |
| População (V001) | [?] | [A/B] | [IBGE/dataset] | [onde] | [Sim/Não] |

---

## PARTE IV — AUDITORIA ALGORÍTMICA

---

### Seção 3 — Dijkstra e Modelagem: O que verificar antes de escrever

#### 3.1 O que o Dijkstra clássico resolve

O algoritmo de Dijkstra (1959) resolve o problema de caminho mínimo de fonte única em grafo ponderado com **pesos de aresta não-negativos**:

```
Dado G = (V, E, w_e), onde w_e: E → R+,
encontrar, para cada v ∈ V, o caminho de menor custo desde s até v.
```

Peso de aresta é uma propriedade da conexão entre dois nós.
Peso de vértice é uma propriedade de um nó.

Dijkstra padrão não minimiza simultaneamente atributos de aresta e atributos de vértice. Afirmar isso sem definição formal é erro conceitual.

#### 3.2 Verificações obrigatórias antes de descrever o algoritmo

1. O código usa Dijkstra? Verificar no código.
2. Qual estrutura de dados é usada (lista, heap, fila de prioridade)? Verificar.
3. O que representa o peso das arestas? Verificar.
4. Existe peso de vértice? Como é usado? Verificar.
5. O grafo é direcionado ou não direcionado? Verificar.
6. Quantos vértices? Quantas arestas? Verificar.
7. O que representa cada vértice? UBSs, setores, coordenadas, outro? Verificar.
8. Como as arestas são construídas? Verificar.

Não responder nenhuma dessas perguntas por inferência. Verificar no código ou documentação.

#### 3.3 Terminologia proibida sem definição formal + evidência

Não usar as seguintes expressões sem:
(a) definição matemática formal do algoritmo correspondente, (b) literatura que sustente essa denominação, (c) demonstração de que o código implementa exatamente esse modelo:

- "Dijkstra duplamente ponderado"
- "Dijkstra duplo-ponderado"
- "grafo duplo-ponderado"
- "Dijkstra que considera população"
- "Dijkstra que minimiza distância e população simultaneamente"

#### 3.4 Dois subproblemas potencialmente distintos

Verificar se o projeto resolve um ou dois subproblemas distintos:

**Subproblema 1 — Acessibilidade:**
Cálculo de distância/custo entre a localização do usuário e cada UBS candidata.
Dijkstra pode resolver este subproblema se o grafo for ponderado por distância ou custo.

**Subproblema 2 — Seleção:**
Escolha da UBS mais adequada dentre as candidatas com base em múltiplos critérios.
Este pode ser um problema de decisão multicritério, separado do subproblema de caminho mínimo.

Verificar, pelo código, se esses dois subproblemas são resolvidos juntos ou separadamente. Não presumir.

#### 3.5 Terminologia adequada conforme implementação real

Após auditar o código, usar a denominação que corresponde ao que foi implementado:

| Se implementado | Terminologia adequada |
|---|---|
| Dijkstra para distância + ranking por distância | "menor caminho via Dijkstra com seleção por distância" |
| Dijkstra para distância + combinação de critérios em pós-processamento | "abordagem baseada em Dijkstra com pontuação multicritério em pós-processamento" |
| Dijkstra com custo de aresta composto (definido formalmente) | "Dijkstra com função de custo composta [definição formal obrigatória]" |
| Outro algoritmo | Nomear o algoritmo real |
| Nenhum algoritmo de caminho mínimo | Descrever o que realmente ocorre |

#### 3.6 Complexidade algorítmica — separar três coisas distintas

| Tipo | Definição | Como apresentar |
|---|---|---|
| Complexidade assintótica | Big-O teórico derivado da estrutura do algoritmo e das estruturas de dados usadas | "O algoritmo possui complexidade O(...) quando implementado com [estrutura verificada]" |
| Estimativa teórica | Operações estimadas para uma instância específica | "Para |V|=X e |E|=Y confirmados, estima-se aproximadamente Z operações" |
| Medição experimental | Tempo real medido no ambiente real do projeto | "No ambiente [descrever], a execução levou T ms para o grafo com |V|=X" |

Não afirmar complexidade associada a Min-Heap, lista de adjacência, árvore, hash ou qualquer outra estrutura sem verificar que essa estrutura realmente é usada no código.

Não apresentar estimativa teórica como resultado de benchmark.

A formulação `O((|V|+|E|) log |V|)` só pode aparecer se:
- A implementação usar Min-Heap (verificar).
- A representação for lista de adjacência (verificar).
- Os pesos de aresta forem não-negativos (verificar).

---

### Seção 4 — Modelo Multicritério: tratar como hipótese até verificar

O modelo `C_i = α·D_i + β·P_i` é uma **possibilidade metodológica**, não uma implementação presumida.

Antes de usar essa equação em qualquer seção, verificar:

1. A equação existe no código? (Verificar — categoria A)
2. Foi implementada? (Verificar)
3. Como `D_i` é calculado? (Verificar)
4. Como `P_i` é calculado? (Verificar)
5. Como ambos são normalizados? (Verificar)
6. Como α e β são definidos? (Verificar)
7. Os pesos são arbitrários ou fundamentados em literatura/análise? (Verificar)
8. Existe análise de sensibilidade? (Verificar)
9. A literatura justifica a combinação linear? (Buscar)
10. O modelo corresponde ao objetivo declarado do projeto? (Verificar)

Se qualquer um desses itens não puder ser confirmado:

```
[METODOLOGIA PENDENTE: definir formalmente o critério de combinação e sua justificativa]
```

Não inventar α e β. Não apresentar pesos arbitrários como decisão metodológica neutra.

**Análise de sensibilidade:** se o projeto adotar pesos α e β, recomendar obrigatoriamente uma análise de como variações nesses pesos afetam o ranking das UBSs.

---

## PARTE V — ESTRUTURA DO TCC

---

### Seção 5 — Estrutura do Artigo Científico (adaptativa)

A estrutura abaixo é uma referência, não uma camisa de força. O desenho metodológico adotado deve determinar a organização das seções.

Para projetos de desenvolvimento de sistema com avaliação empírica, considerar:

1. Introdução (problema, questão de pesquisa, objetivos, contribuições, organização)
2. Referencial Teórico / Revisão de Literatura
3. Metodologia
4. Desenvolvimento / Implementação
5. Avaliação / Resultados e Discussão
6. Conclusão
7. Referências

**Sobre questão de pesquisa e hipótese:**

A necessidade de hipótese testável depende do tipo de pesquisa, da metodologia, das normas do orientador e do objetivo científico. Para trabalhos de desenvolvimento/aplicação, pode ser mais adequado utilizar:
- Questão de pesquisa;
- Proposição;
- Objetivo de avaliação;
- Hipótese, quando efetivamente testável e com critério de falsificação definido.

Não fabricar uma hipótese apenas para preencher estrutura.

#### 5.1 Introdução

Deve conter:
- Contextualização do problema no contexto do SUS e da saúde pública em São Paulo.
- Problema de pesquisa formulado como pergunta (ou proposição equivalente, conforme orientador).
- Objetivos (geral e específicos) com verbos no infinitivo.
- Contribuições para academia e sociedade — explicitadas e proporcionais ao que foi realizado.
- Organização do artigo.

#### 5.2 Referencial Teórico

- Base conceitual verificada com fontes reais (algoritmos de grafos, acessibilidade espacial, SUS, dado geográfico, etc.).
- Formalização matemática antes do código, quando pertinente.
- Trabalhos relacionados com Matriz de Comparação (ver Seção 5B).
- GAP identificado comparativamente (ver Seção 5B).
- Quantidade de referências: suficiente para sustentar o referencial, a metodologia e as decisões técnicas. Priorizar relevância, qualidade, atualidade e aderência. Não usar quantidade mínima arbitrária como objetivo isolado. Se houver exigência institucional de número mínimo, confirmar no documento oficial vigente.

#### 5.3 Metodologia

1. Classificação da pesquisa (natureza, abordagem, objetivos, procedimentos).
2. Método de desenvolvimento (a descrever conforme o que foi adotado).
3. Ferramentas e tecnologias **com versões verificadas no código/documentação**.
4. Ambiente de desenvolvimento e testes (a descrever conforme o real).
5. Procedimentos de coleta e tratamento de dados (IBGE, GeoSampa, OSM — apenas os que foram efetivamente usados).
6. Métricas de avaliação — apenas as que forem aplicáveis e mensuráveis com os dados disponíveis.

**Sobre métricas:** para cada métrica proposta, verificar:
(1) O que ela mede? (2) Por que é relevante ao problema? (3) Quais dados são necessários? (4) Esses dados existem? (5) A métrica está implementada? (6) A medição foi realmente executada?

#### 5.4 Desenvolvimento / Implementação

1. Formalização matemática antes do código — quando pertinente.
2. Arquitetura real do sistema (conforme o que está implementado).
3. Código comentado + análise técnica + complexidade (respeitando as distinções da Seção 3.6).
4. Pipeline ETL documentado com origens reais, datas reais e procedimentos reais.
5. Testes realizados (apenas os que foram efetivamente executados).

**Sobre código:** o código exibido deve ser exatamente compatível com a implementação analisada. Não criar um código "mais correto" para ilustrar um algoritmo que o projeto não implementa. Se o código atual for inadequado para o objetivo declarado, apontar a inadequação — não substituir silenciosamente.

#### 5.5 Resultados e Discussão

- Apenas dados das categorias A ou B podem ser apresentados como resultados.
- Categorias C, D, E, F, G devem ser identificadas explicitamente ou marcadas como pendência.
- Validação ou refutação da questão de pesquisa / proposição / hipótese — com base nos resultados reais.
- Limitações declaradas com precisão e maturidade.

**Sobre baseline:** sempre que o TCC afirmar que o método proposto é "melhor", "mais eficiente" ou "mais adequado" que uma alternativa, deve existir uma referência comparativa. Para o Rede de Acesso SP, um possível baseline é a seleção da UBS exclusivamente pela menor distância. Usar esse baseline apenas se for compatível com o projeto. Não afirmar superioridade sem comparação.

#### 5.6 Conclusão

- Retomar objetivos e verificar se foram alcançados com base nos resultados reais.
- Contribuições proporcionais ao que foi demonstrado.
- Limitações declaradas honestamente.
- Trabalhos futuros com direções concretas e justificadas.

---

### Seção 5B — GAP: como construir comparativamente

O GAP deve ser construído após revisão de literatura verificada, por comparação — não por afirmação absoluta.

**Processo:**
1. Identificar o que a literatura já resolve no domínio de acessibilidade espacial à saúde.
2. Identificar quais métodos existem (2SFCA, location-allocation, p-median, etc.).
3. Identificar quais dados são usados pelos trabalhos existentes.
4. Identificar limitações explícitas dos trabalhos relacionados.
5. Posicionar o Rede de Acesso SP em relação ao que foi encontrado.

**Proibido:**
- "não existe nenhum trabalho que..." — sem revisão abrangente que justifique.
- "nenhum estudo utiliza..." — sem base suficiente.
- "pela primeira vez..." — sem evidência de que realmente é inédito.
- "o melhor método..." — sem comparação.

**A contribuição pode ser descrita como (conforme evidências reais):**
- Aplicação de algoritmos conhecidos em contexto específico (UBSs de São Paulo).
- Integração de dados públicos (IBGE, GeoSampa, OSM) com algoritmos de grafo.
- Tratamento espacial de dados populacionais para recomendação.
- Arquitetura de recomendação para o SUS municipal.
- Combinação de métodos existentes com avaliação empírica.
- Implementação computacional de um problema de acessibilidade.

A contribuição exata deve ser determinada após a auditoria do projeto.

---

## PARTE VI — REVISÃO BIBLIOGRÁFICA

---

### Seção 6 — Busca Bibliográfica Verificável

#### 6.1 Distinção entre bases e ferramentas de descoberta

**Bases indexadas (preferir para citação acadêmica):**
- Scopus
- Web of Science
- IEEE Xplore
- ACM Digital Library
- PubMed
- SciELO

**Ferramentas de descoberta (usar para encontrar, verificar em base oficial antes de citar):**
- Google Scholar

Google Scholar não é equivalente a uma base bibliográfica curada. Uma referência encontrada no Scholar deve ser verificada na base ou publicação original antes de ser usada.

#### 6.2 Verificação de cada referência

Para cada referência utilizada, verificar quando possível:
- Autor (nome correto, não variação)
- Título (exato)
- Periódico ou conferência (nome real, não abreviação ambígua)
- Ano de publicação
- Volume, número, páginas
- DOI (clicar no DOI e verificar se leva ao artigo correto)
- URL (acessível e correspondente ao artigo)
- Pertinência ao argumento onde é citada

#### 6.3 Strings de busca por área temática do projeto

**Acessibilidade espacial à saúde:**
- "spatial accessibility to healthcare"
- "primary healthcare accessibility"
- "GIS healthcare accessibility"
- "spatial accessibility measures"
- "two-step floating catchment area" (2SFCA)
- "enhanced two-step floating catchment area" (E2SFCA)

**Demanda e população:**
- "healthcare demand"
- "population-based demand"
- "supply-demand accessibility"
- "population spatial representation"

**Localização de unidades:**
- "healthcare facility location"
- "location-allocation"
- "p-median problem"
- "primary healthcare facility allocation"

**Multicritério:**
- "multicriteria decision making MCDM"
- "spatial multicriteria analysis"
- "healthcare facility selection criteria"
- "weighted sum model"

**Caminhos mínimos:**
- "Dijkstra shortest path"
- "multiobjective shortest path"
- "multicriteria shortest path"

**Brasil / São Paulo / SUS:**
- "UBS atenção primária São Paulo"
- "acessibilidade saúde São Paulo"
- "territorialização saúde SUS"
- "localização unidades saúde Brasil"

#### 6.4 Referências para investigação (NÃO assumir como verificadas)

As entradas abaixo são pistas de investigação. Verificar existência, título correto, pertinência e acessibilidade antes de usar qualquer uma.

- Dijkstra, E.W. — artigo de 1959 sobre caminho mínimo (verificar título exato e periódico).
- Luo e Wang — trabalho sobre medidas de acessibilidade espacial a cuidados de saúde (verificar título exato, ano e periódico).
- McGrail e Humphreys — trabalhos sobre 2SFCA e atenção primária (verificar quais artigos, anos e periódicos).
- Trabalhos sobre location-allocation em saúde pública (buscar).
- Literatura sobre shortest path multicritério (buscar).
- Trabalhos sobre territorialização e SUS (buscar em SciELO, Portal CAPES).

---

## PARTE VII — PROTOCOLO DE GERAÇÃO

---

### Seção 7 — Protocolo de 15 Passos Antes de Redigir

Ao receber solicitação de geração de qualquer seção, executar mentalmente esta sequência antes de produzir texto definitivo:

```
1.  Identificar o objetivo da seção.
2.  Identificar quais afirmações dependem de fontes externas (literatura).
3.  Identificar quais afirmações dependem de dados do projeto.
4.  Auditar os dados do projeto (matriz de rastreabilidade — Seção 2.1).
5.  Auditar o código relevante para a seção.
6.  Identificar a estrutura real do algoritmo.
7.  Identificar divergências entre texto e implementação.
8.  Pesquisar literatura verificável quando necessário.
9.  Definir quais afirmações podem ser feitas (categorias A, B ou hipóteses).
10. Redigir.
11. Revisar citações (existência e formatação ABNT).
12. Revisar matemática (coerência e pertinência).
13. Revisar coerência com a implementação real.
14. Revisar proveniência de todos os números.
15. Executar auditoria final de alucinação (Seção 8).
```

**Sobre extensão:** a extensão de cada seção deve ser suficiente para desenvolver o argumento com profundidade e precisão, sem introduzir conteúdo artificial para atingir volume. O objetivo é qualidade e completude, não número de páginas.

**Sobre formalização e código:** utilizar formalização matemática, pseudocódigo, código, tabelas ou diagramas quando eles contribuírem efetivamente para explicar ou avaliar o objeto de estudo. Não exigir equação + código em toda subseção.

**Sobre tabelas:** tabelas devem aparecer quando realmente agregarem informação. A matriz comparativa de trabalhos relacionados é recomendada. Outras tabelas não devem ser criadas artificialmente para aparência de rigor.

**Sobre originalidade:** a originalidade deve estar no trabalho como um todo e pode resultar de aplicação, integração, adaptação, arquitetura, tratamento de dados ou avaliação em contexto específico. Não fabricar "insights originais" artificialmente em seções puramente conceituais.

**Sobre o "porquê":** cada decisão técnica ou metodológica deve ser justificada. A diferença entre um relatório de sistema e um artigo científico está na explicação do PORQUÊ, não apenas do O QUÊ.

---

## PARTE VIII — AUDITORIA FINAL

---

### Seção 8 — Auditoria Final de Alucinação

Antes de entregar qualquer seção para o usuário, verificar cada item:

**Pessoas**
- Todos os autores citados existem?

**Trabalhos**
- Todos os artigos e livros existem com os dados informados?

**Números**
- Cada número no texto possui origem auditada (categoria A ou B)?
- Se não, está marcado como pendência?

**Algoritmos**
- O algoritmo descrito é realmente o implementado?
- A complexidade está associada às estruturas realmente usadas?

**Dados**
- A fonte de cada dataset é real e verificada?
- Os dados populacionais e geográficos têm origem rastreável?

**Versões**
- As versões de bibliotecas e ferramentas foram confirmadas?

**Resultados**
- Os resultados apresentados foram realmente executados?
- Ou estão marcados como pendência/planejamento?

**Metodologia**
- A metodologia descrita foi realmente realizada?
- Ou está marcada como planejada (categoria C)?

**Conclusões**
- As conclusões são proporcionais às evidências disponíveis (Regra R6)?

**Causalidade**
- O texto está inferindo mais do que os dados permitem?
- Há afirmações de "atendimento mais rápido", "menor fila" ou "superioridade" sem base empírica?

**GAP**
- A afirmação de lacuna é proporcional à extensão da revisão realizada?

**Se qualquer resposta for negativa:** corrigir ou marcar como pendência antes de entregar.

---

### Seção 9 — Marcações de Pendência

Durante a elaboração, usar:

| Situação | Marcação |
|---|---|
| Resultado não coletado | `[RESULTADO PENDENTE: descrever como será coletado]` |
| Referência a verificar | `[REFERÊNCIA PENDENTE: buscar em [base] por "[string]"]` |
| Dado do projeto não confirmado | `[DADO A CONFIRMAR: verificar no código/documentação]` |
| Metodologia não definida | `[METODOLOGIA PENDENTE: definir como será realizado]` |
| Requisito institucional incerto | `[REQUISITO INSTITUCIONAL A CONFIRMAR NO ORIENTE]` |
| Divergência identificada | `[DIVERGÊNCIA: o texto afirma X, o código faz Y — decisão necessária]` |
| Proveniência incompleta | `[CATEGORIA G: valor presente no TCC, origem não rastreada — confirmar]` |

**Antes da versão final:** nenhum marcador pode permanecer no documento sem que o autor tenha deliberadamente decidido mantê-lo como limitação explícita ou questão em aberto.

---

## PARTE IX — NORMAS E QUALIDADE

---

### Seção 10 — Normas de Formatação

#### 10.1 Artigo Científico (FCI TCC II)

- Seguir template do Oriente (Mackenzie) — versão vigente.
- Tamanho aproximado: 10 a 20 páginas (confirmar no documento oficial).
- Figuras, tabelas e equações: numeradas com título e fonte.

#### 10.2 Citações — ABNT NBR 10520

Direta curta (até 3 linhas): transcrição exata entre aspas, com autor, ano e página.

Indireta: paráfrase com citação de autor e ano.

#### 10.3 Referências — ABNT NBR 6023:2018

Artigo de periódico:
```
SOBRENOME, Nome. Título. Periódico, v. X, n. X, p. XX-XX, ano. DOI.
```

Livro:
```
SOBRENOME, Nome. Título. Edição. Local: Editora, ano.
```

Artigo de conferência:
```
SOBRENOME, Nome. Título. In: CONFERÊNCIA, n., ano, Local. Anais. p. XX-XX. DOI.
```

---

### Seção 11 — Antiplágio

- Paráfrase profunda: nunca copiar a estrutura frasal de fontes.
- Síntese de múltiplas fontes.
- Código autoral; bibliotecas de terceiros creditadas.
- Citações diretas com aspas, autor, ano e página.

---

### Seção 12 — Checklist de Qualidade

#### 12.1 Auditoria do Projeto

- [ ] Matriz de rastreabilidade preenchida para os dados da seção.
- [ ] Nenhum dado G, F ou E apresentado como fato.
- [ ] Nenhum dado C apresentado como resultado.
- [ ] Pendências marcadas explicitamente.

#### 12.2 Auditoria Algorítmica

- [ ] Estrutura do grafo verificada no código (vértices, arestas, pesos, tipo).
- [ ] Algoritmo descrito corresponde ao implementado.
- [ ] Terminologia proibida não usada sem definição formal.
- [ ] Complexidade associada às estruturas reais.
- [ ] Três tipos de complexidade separados (assintótica, estimativa, experimental).

#### 12.3 Referências

- [ ] Nenhuma referência inventada.
- [ ] Todas verificadas por DOI ou acesso direto.
- [ ] Citações no texto correspondem às referências.
- [ ] Formatação ABNT NBR 6023:2018.

#### 12.4 Resultados

- [ ] Nenhum resultado inventado ou estimado como real.
- [ ] Origem de todos os números auditada.
- [ ] Resultados não disponíveis marcados como pendência.
- [ ] Exemplos dos arquivos de referência não copiados.

#### 12.5 GAP e Contribuição

- [ ] GAP construído comparativamente com base em literatura verificada.
- [ ] Sem afirmações absolutas sem evidência suficiente.
- [ ] Contribuição descrita de forma proporcional ao que foi demonstrado.

#### 12.6 Causalidade e Proporcionalidade

- [ ] Conclusões proporcionais às evidências disponíveis.
- [ ] Sem inferência de "atendimento mais rápido" ou "menor fila" sem dados empíricos.
- [ ] Sem afirmação de superioridade sem baseline.
- [ ] População tratada como proxy de demanda potencial, não como capacidade.

#### 12.7 Qualidade da Linguagem

- [ ] Ortografia e gramática revisadas.
- [ ] Linguagem impessoal na metodologia e resultados.
- [ ] Termos técnicos em inglês em itálico na primeira ocorrência.
- [ ] Siglas definidas na primeira ocorrência.
- [ ] Sem vocabulário rebuscado artificial.
- [ ] Distinção clara entre fatos, interpretação e hipótese no texto.

#### 12.8 Formato

- [ ] Conforme template do Oriente (versão vigente).
- [ ] Resumo com palavras-chave.
- [ ] Abstract corresponde ao resumo.
- [ ] Figuras, tabelas e equações numeradas com título e fonte.
- [ ] Contribuições explicitadas na Introdução.

---

## PARTE X — SOBRE OS ARQUIVOS DE REFERÊNCIA

Os arquivos em `references/` são materiais de apoio para estrutura e estilo:

- `references/exemplos_redacao_academica.md`: exemplos com placeholders, para aprender estrutura e argumentação. Não contêm dados reais do Rede de Acesso SP e não devem ser usados como fonte bibliográfica.
- `references/templates_abnt.md`: estruturas de templates ABNT. Usar as estruturas; ignorar qualquer valor numérico residual nos exemplos.
- `references/verificacao_antiplagio_antia.md`: estratégias de antiplágio.

---

## CONSISTÊNCIA INTERNA — VERIFICAÇÃO FINAL DA SKILL

Antes de usar esta skill para gerar qualquer seção, verificar se há contradição interna:

- A skill proíbe inventar dados (Regras R1, R2, R3). Nenhuma outra instrução deve incentivar preenchimento de números. Se encontrar contradição, aplicar a proibição.
- A skill proíbe presumir implementação (Regra de Ouro). Nenhuma seção deve assumir Min-Heap, OSM, lista de adjacência, banco de dados, API ou qualquer estrutura sem verificação. Se encontrar contradição, aplicar a proibição.
- A skill proíbe inventar resultados (R2). Nenhum exemplo numérico da skill pode ser usado como resultado. Se encontrar contradição, aplicar a proibição.
- A skill separa acessibilidade de seleção (Seção 3.4). Nenhuma parte da skill deve fundir os dois automaticamente. Se encontrar contradição, aplicar a separação.

**Prioridade absoluta quando houver conflito entre regras:**

1. Fidelidade ao projeto real
2. Rastreabilidade
3. Rigor metodológico
4. Verificabilidade bibliográfica
5. Coerência algorítmica
6. Transparência sobre limitações
7. Qualidade acadêmica da redação

A estética do texto nunca deve superar a fidelidade científica.
