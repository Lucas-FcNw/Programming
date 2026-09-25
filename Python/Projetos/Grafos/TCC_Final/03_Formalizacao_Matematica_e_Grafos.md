# 3. FORMALIZAÇÃO MATEMÁTICA E TOPOLOGIA DE GRAFOS

A transposição de um problema geográfico de saúde metropolitana para as ciências da computação demanda a supressão de detalhes físicos irrelevantes e a cristalização matemática das restrições espaciais. Este capítulo destrincha a modelagem exata desenvolvida para o município de São Paulo, provando estruturalmente que a rede montada suporta a aplicação de algoritmos complexos.

## 3.1 Modelagem Formal do Sistema

A infraestrutura territorial de atendimento não agendado foi abstraída mediante um grafo conexo e não direcionado. Diferindo-se dos grafos acadêmicos teóricos unidimensionais, a exigência do problema forçou a adoção de uma estrutura com **ponderação dupla mista** na ordem de $G = (V, E, w_v, w_e)$.

*   $V$ consolida o conjunto rigoroso de vértices, onde cada $v \in V$ materializa uma Unidade Básica de Saúde. No recorte final consolidado do estudo, o modelo fechou em uma ordem restritiva de $|V| = 71$ vértices (englobando as unidades críticas de alta movimentação da macrorregião expandida do projeto original).
*   $E \subseteq V \times V$ constitui o conjunto de arestas. A aresta denotada por $\{u, v\}$ é computada no sistema apenas se as UBSs subjacentes forem passíveis de conexão territorial fluida, culminando em um tamanho total inicial de $|E| = 215$ arestas. A inexistência de direção na aresta ($(u, v) \equiv (v, u)$) valida o princípio do trajeto bidirecional viário padrão.

### 3.1.1 O Fator de Pressão Demográfica (O Peso do Vértice, $w_v$)

A subversão arquitetural deste projeto repousa na função injetora que determina o estresse do destino: $w_v: V \rightarrow \mathbb{R}^+$.
Tradicionalmente, vértices na logística representam meros cruzamentos vazios. Aqui, o peso $w_v(v)$ equivale estritamente à **população residente estimada na Área de Abrangência da UBS (AAUBS)**. 

A exploração empírica dos dados gerou anomalias topológicas gritantes que justificam a necessidade do roteamento. Constatou-se que a variância do peso habitacional não se conforma a uma distribuição normal justa:
- O Limite Inferior (Menor Peso): $w_{v(min)} = 8.919$ cidadãos, correspondente ao vértice isolado da UBS *WALTER ELIAS, DR - CASA VERDE BAIXA*.
- O Limite Superior (Maior Peso): $w_{v(max)} = 79.792$ cidadãos, flagrado no nó *CAMBUCI-UBS*.
- Com uma média ($\bar{x}$) repousando em $35.759$ habitantes, o sistema demonstra empiricamente o estrangulamento invisível. Um indivíduo próximo ao *Cambuci* disputa o chão do posto médico contra quase $80$ mil vizinhos.

### 3.1.2 A Métrica de Distância Viária (O Peso da Aresta, $w_e$)

A função $w_e: E \rightarrow \mathbb{R}^+$ determina o custo da transição territorial entre o par $\{u, v\}$, expresso objetivamente em quilômetros lineares ou geocodificados.
Os limites observados ($min\{w_e\} = 0.01$ km entre as UBSs *Água Rasa* e *Mooca*; $max\{w_e\} = 3.67$ km isolando a *Chácara Cruzeiro do Sul* e a *Vila Nova Manchester*) atestam um somatório integral da rede que perpassa $530.02$ quilômetros em arestas lógicas. O algoritmo operará para manter o desvio penalizador sempre o mais próximo possível das medianas radiais.

## 3.2 Análise Topológica, Coesão e Euleriana

Para garantir que o cálculo logístico flua através do software, é mister realizar o crivo topológico extraído das funções primárias do modelo implementado em memória.

### 3.2.1 Densidade da Rede ($D$)

Em cenários metropolitanos, é inaceitável que um grafo de saúde seja densamente conectado — uma UBS da Zona Norte não detém aresta direta para o extremo da Zona Leste. A prova matemática da esparsidade da rede é calculada determinando-se a densidade $D$:

$$D = \frac{2|E|}{|V|(|V| - 1)} = \frac{2 \times 215}{71 \times 70} = \frac{430}{4.970} \approx 0,0865$$

A densidade de apenas $8,65\%$ (extrema esparsidade) é o indicador matemático que validou a decisão de **engenharia de software** de rejeitar sumariamente a alocação de grafos via *Matriz de Adjacência* ($O(|V|^2)$ no uso de RAM). Toda a estrutura foi programada utilizando **Listas de Adjacência**, prevenindo o desperdício colossal de matrizes repletas de vetores de peso nulo (zeros).

### 3.2.2 Centralidade, Grau e Propriedades Radiais

A observância da centralidade no espaço intraurbano expõe onde a gestão de tráfego é viável. A excentricidade $\epsilon(v)$ mediu o afastamento sistêmico, provando a robustez da conectividade:
*   **Diâmetro Ponderado:** $\max_{v \in V} \epsilon(v) = 36.87$ km. Este número expressa que, caso a via expressa demande cruzar todo o modelo da UBS *V. Nova Jaguare* até *Paraisópolis*, incorrer-se-á em no máximo 36 km lógicos na rede gerada.
*   **Raio Ponderado e o Centro do Grafo:** O valor $\min_{v \in V} \epsilon(v) = 18.65$ km fixou o centro absoluto estrutural do grafo: o vértice correspondente à *SE - NASF/UBS*. Sob a ótica do planejamento do SUS, unidades móveis de contenção (Ambulâncias base) devotadas a este nó deteriam a latência mecânica média ótima para atingir qualquer outro ponto de colapso do sistema modelado.

A função de grau $\deg(v) = |N(v)|$, onde $N(v)$ exprime os vizinhos, corroborou a variação do tecido de saúde metropolitano. O grau médio situou-se em saudáveis $6,06$ alternativas primárias por nó. O ápice de conectividade ($\deg=12$) aglomerou-se em torno do nó *22 (ILZA WELTMAN HUTZLER DRA-UBS)*. Simultaneamente, periferias geográficas geraram vértices com meras duas arestas (ex: *MAX PERLMAN*, *PARAÍSOPOLIS*), ratificando bolsões perigosos onde falhas operacionais da unidade não fornecem margem algorítmica para escapes radiais do paciente.

### 3.2.3 Análise de Percurso Euleriano

As indagações de viabilidade logística contemplaram a busca euleriana. O grafo conexo acusou a presença maciça de $34$ vértices de grau ímpar. Pelos dogmas estruturais, a presença de múltiplos graus ímpares ($>2$) inviabiliza determinantemente a formulação de um Circuito ou Trilha Euleriana. Essa propriedade exclui a viabilidade de utilizar algoritmos de patrulhamento único que transitem por todas as rotas sem repetições — validando que o modelo é exímio para roteamento descentralizado "ponto a ponto", mas inapropriado (ou seja, de custo exponenciado em NP) caso o objetivo governamental migrasse para a geração de rotas logísticas para Caminhões de Coleta de Resíduos Hospitalares varrendo toda a rede municipal sem recortes setoriais.
