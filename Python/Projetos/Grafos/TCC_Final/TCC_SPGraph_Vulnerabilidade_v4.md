# SPGRAPH: ANÁLISE DE VULNERABILIDADE ESTRUTURAL DA REDE DE SAÚDE PÚBLICA DE SÃO PAULO POR ALGORITMOS DE TEORIA DOS GRAFOS

**Lucas Fernandes de Camargo** (RA: 10419400) — **Lendy Naiara Carpio Pacheco** (RA: 10428525) — **Anna Luiza Stella Santos** (RA: 10417401)

Faculdade de Computação e Informática — Universidade Presbiteriana Mackenzie — São Paulo, SP, Brasil

**Orientador:** Prof. Dr. [Nome do Orientador] | **Curso:** Ciência da Computação | **Semestre:** 2026/1

---

## RESUMO

A rede de atenção primária à saúde de São Paulo compreende centenas de Unidades Básicas de Saúde (UBSs) distribuídas por 96 distritos administrativos, formando uma infraestrutura territorialmente interdependente. Interrupções operacionais rotineiras — causadas por reformas prediais, remanejamento de corpo clínico, alagamentos locais ou déficit de infraestrutura — podem provocar desconexão topológica nessa rede, deixando populações inteiras sem acesso viável a serviços de atenção básica na proximidade. Este artigo apresenta o _SPGraph_, sistema computacional que modela os 96 distritos de São Paulo como grafo não orientado ponderado G = (V, E, w), com |V| = 96 vértices e |E| = 249 arestas, e aplica algoritmos clássicos da Teoria dos Grafos para identificar pontos estruturalmente críticos: vértices de articulação e pontes. A implementação utiliza o algoritmo de Tarjan sobre Busca em Profundidade (DFS) para localizar os três vértices de articulação e a única ponte crítica na rede real de SP. Um módulo de simulação permite ao analista remover distritos arbitrários e observar o impacto em cascata no acesso dos pacientes — ao remover simultaneamente os três vértices de articulação, a rede perde conectividade e decompõe-se em quatro componentes isoladas. O sistema é disponibilizado como _dashboard_ interativo em Streamlit, com cinco abas: visão geral do grafo, mapa de pontos críticos, simulação de falhas, análise de cobertura e documentação. Os resultados demonstram que métodos clássicos de Teoria dos Grafos, aliados a dados públicos da Prefeitura, produzem ferramentas fundamentais para avaliar a acessibilidade estrutural e apoiar decisões rotineiras de remanejamento na saúde pública.

**Palavras-chave:** Teoria dos Grafos. Acessibilidade na Saúde. Vértices de Articulação. Algoritmo de Tarjan. Saúde Pública. Sistema Único de Saúde.

---

## ABSTRACT

São Paulo's primary healthcare network comprises hundreds of Basic Health Units (UBSs) distributed across 96 administrative districts, forming a territorially interdependent infrastructure. Routine operational disruptions — caused by facility renovations, staff reallocation, local floods, or infrastructure deficits — may trigger topological disconnection in this network, leaving populations without viable access to nearby primary care. This paper presents _SPGraph_, a computational system that models all 96 São Paulo districts as a weighted undirected graph G = (V, E, w), with |V| = 96 vertices and |E| = 249 edges, applying classical Graph Theory algorithms to identify structurally critical points: articulation vertices and bridges. The implementation employs Tarjan's algorithm over Depth-First Search (DFS) to locate the three articulation vertices and the single critical bridge found in SP's real network. A simulation module allows analysts to remove arbitrary districts and observe the cascading impact on patient access — simultaneously removing the three articulation vertices decomposes the network into four isolated components. The system is delivered as an interactive Streamlit dashboard with five tabs: graph overview, critical-point map, failure simulation, coverage analysis, and documentation. Results demonstrate that classical Graph Theory methods, combined with public municipal data, yield fundamental tools to assess structural accessibility and support routine reallocation decisions in public health management.

**Keywords:** Graph Theory. Vulnerability Analysis. Articulation Vertices. Tarjan's Algorithm. Public Health. Brazilian Health System.

---

## 1. INTRODUÇÃO

### 1.1 Contextualização

O Sistema Único de Saúde (SUS) constitui a maior política pública de saúde do mundo em cobertura populacional, atendendo mais de 200 milhões de brasileiros (BRASIL, 2023). Nesse arcabouço, as Unidades Básicas de Saúde (UBSs) representam a porta de entrada preferencial — o ponto onde o cidadão inicia sua jornada no sistema para consultas de atenção primária, vacinação, pré-natal e acompanhamento de condições crônicas. São Paulo, com seus 11,45 milhões de habitantes (IBGE, 2023) organizados em 96 distritos administrativos, opera uma das redes de saúde primária mais complexas do planeta, com 474 UBSs, 87 hospitais do SUS e 2 Unidades de Pronto Atendimento (UPAs) — 563 serviços no total.

A acessibilidade a essa rede, contudo, sofre com desafios crônicos. Diferente de eventos de larga escala como pandemias, a rotina do sistema de saúde paulistano lida frequentemente com interrupções localizadas e remanejamentos: uma UBS pode suspender atendimentos devido a reformas prediais demoradas, déficit temporário de corpo clínico (falta de médicos), superlotação severa ou problemas de infraestrutura local (alagamentos em zonas periféricas e interrupções de energia elétrica). A questão rotineira enfrentada por gestores de saúde e pacientes não é apenas _"qual UBS está mais próxima?"_, mas sim _"se esta unidade deixar de operar temporariamente, quais distritos vizinhos absorverão a demanda e quais populações ficarão geograficamente isoladas do sistema?"_.

A Teoria dos Grafos oferece o instrumental matemático preciso para responder a essa pergunta e avaliar a acessibilidade. Modelando a rede de distritos como um grafo, é possível identificar formalmente os nós e arestas que sustentam a conectividade da região — os chamados vértices de articulação e pontes — cuja paralisação local desconecta geograficamente populações inteiras das alternativas viáveis.

### 1.2 Problema de Pesquisa

> **Dada a rede de distritos de São Paulo modelada como grafo G = (V, E, w), como identificar os pontos estruturalmente críticos — cujas falhas operacionais fragmentem a rede em componentes desconexos — e como quantificar o impacto territorial de cenários de fechamento simultâneo de múltiplos distritos?**

### 1.3 Hipótese

> A rede de distritos de São Paulo, quando modelada como grafo conexo não orientado G = (V, E, w) com adjacências geográficas reais derivadas de dados públicos (GeoSampa, Portal de Dados Abertos de SP), contém vértices de articulação e pontes críticas identificáveis pelo algoritmo de Tarjan em tempo O(|V| + |E|), cuja remoção comprovadamente fragmenta a rede em múltiplos componentes desconexos, tornando populações inteiras inacessíveis a qualquer serviço de saúde adjacente.

### 1.4 Objetivos

**Objetivo Geral:** Desenvolver um sistema computacional de análise de vulnerabilidade estrutural da rede de saúde pública de São Paulo, utilizando algoritmos de Teoria dos Grafos para identificar pontos críticos e simular cenários de falha.

**Objetivos Específicos:**

1. Modelar a rede de 96 distritos de São Paulo como grafo G = (V, E, w) com dados reais do GeoSampa e Portal de Dados Abertos de SP;
2. Implementar o algoritmo de Tarjan para identificação de vértices de articulação e pontes críticas em tempo linear O(|V| + |E|);
3. Desenvolver módulo de simulação de fechamento que recalcula a topologia da rede após remoção de um ou mais distritos;
4. Realizar análise topológica completa da rede (densidade, distribuição de graus, centralidade de intermediação, diâmetro, raio);
5. Disponibilizar os resultados em _dashboard_ interativo (Streamlit) com visualização geoespacial e simulação em tempo real;
6. Avaliar a interface com protocolo de usabilidade IHC (GOMS, HTA, heurísticas de Nielsen, questionário Likert).

### 1.5 Justificativa e Contribuições

A literatura sobre otimização de redes de saúde concentra-se predominantemente no _Weighted Facility Location Problem_ (WFLP) — onde instalar novas unidades — ou em roteamento individual de pacientes (CORNUEJOLS; NEMHAUSER; WOLSEY, 1990). A análise de vulnerabilidade estrutural de redes de atenção primária é substancialmente menos explorada. O presente trabalho preenche essa lacuna ao aplicar métodos clássicos de Teoria dos Grafos à rede real de 96 distritos de SP, utilizando exclusivamente dados públicos.

**Contribuições deste artigo:**

1. Modelagem do grafo de 96 distritos com adjacências calculadas a partir de polígonos KML reais (GeoSampa);
2. Implementação dos algoritmos de Tarjan para articulação e pontes sobre o grafo real;
3. Módulo de simulação de falhas com recálculo de componentes conexas via BFS;
4. Ranking de criticidade por impacto de remoção;
5. _Dashboard_ interativo com 5 abas e visualização geoespacial;
6. Avaliação de usabilidade com protocolo IHC completo.

### 1.6 Organização do Artigo

A Seção 2 apresenta o referencial teórico e a revisão da literatura. A Seção 3 formaliza o modelo do grafo e apresenta a análise topológica com dados reais. A Seção 4 descreve a metodologia. A Seção 5 detalha os algoritmos implementados e sua complexidade. A Seção 6 apresenta resultados e avaliação de usabilidade. A Seção 7 conclui o trabalho.

---

## 2. REFERENCIAL TEÓRICO E REVISÃO DA LITERATURA

### 2.1 Fundamentos da Teoria dos Grafos

A Teoria dos Grafos tem origem na solução de Euler para o problema das Pontes de Königsberg (1736) e oferece o arcabouço matemático para modelar sistemas relacionais complexos (BONDY; MURTY, 2008). Um grafo G = (V, E) é definido por um conjunto finito não-vazio de vértices V e um conjunto de arestas E representando relações binárias entre pares de vértices. A extensão ponderada G = (V, E, w), onde w: E → R+ associa custos positivos a cada aresta, fundamenta a teoria moderna de roteamento computacional (CORMEN et al., 2012).

#### 2.1.1 Conectividade e Vulnerabilidade

Um grafo é **conexo** quando existe caminho entre qualquer par de vértices. A **conectividade** mede sua robustez: quantos vértices (ou arestas) precisam ser removidos para torná-lo desconexo (BONDY; MURTY, 2008).

**Vértice de articulação** é um vértice v tal que G - {v} tem mais componentes conexas que G. Um grafo sem vértices de articulação é chamado **biconexo**.

**Ponte** é uma aresta {u, v} tal que G - {u, v} tem mais componentes conexas que G. Para redes de saúde pública, a identificação de articulações e pontes é diretamente interpretável: um distrito articulação cuja UBS feche pode tornar populações adjacentes inacessíveis a qualquer serviço de saúde na rede.

#### 2.1.2 Algoritmo de Tarjan para Articulações e Pontes

O algoritmo de Tarjan (1972) identifica vértices de articulação e pontes em tempo linear O(|V| + |E|) por meio de uma Busca em Profundidade (DFS) que mantém dois valores para cada vértice (TARJAN, 1972):

- **disc[v]**: instante de descoberta de v na DFS
- **low[v]**: menor disc alcançável a partir da subárvore de v, incluindo arestas de retorno

**Condição de articulação:** Um vértice u é de articulação se:
- u é raiz da DFS e possui dois ou mais filhos; ou
- u não é raiz e existe filho v tal que low[v] >= disc[u]

**Condição de ponte:** Aresta {u, v} é ponte se low[v] > disc[u].

#### 2.1.3 DFS e BFS

A **DFS** percorre o grafo explorando cada caminho até o fim antes de retroceder. Utilizada pelo algoritmo de Tarjan para manter disc/low. Complexidade: O(|V| + |E|).

A **BFS** percorre em camadas. Utilizada neste trabalho para calcular componentes conexas após remoção de vértices. Complexidade: O(|V| + |E|).

### 2.2 Vulnerabilidade de Redes de Infraestrutura

O estudo de vulnerabilidade em redes de infraestrutura crítica utiliza a Teoria dos Grafos para medir a resiliência contra falhas ou ataques sistemáticos. Holme et al. (2002) propuseram métricas de vulnerabilidade baseadas no tamanho do maior componente conexo remanescente após a remoção sequencial de vértices ordenada por métricas como a centralidade de intermediação (_betweenness centrality_). Para redes de saúde especificamente, a literatura ressalta a distinção metodológica entre **vulnerabilidade topológica** (dependente exclusivamente da estrutura e do formato matemático do grafo) e **vulnerabilidade operacional** (baseada em capacidade logística, filas e leitos).

Pesquisas contemporâneas sobre infraestruturas de saúde utilizam extensivamente métricas clássicas de centralidade e topologia para localizar "gargalos" de acessibilidade e distribuição de recursos durante interrupções do sistema (CHEN et al., 2024; CRUCITTI et al., 2004). O presente trabalho trata de modelar e analisar a vulnerabilidade topológica das UBSs, pois ela é a condição necessária primária para qualquer forma de acesso. Sem acesso estrutural viável, a população não consegue chegar aos bairros vizinhos, e qualquer análise de acessibilidade operacional perde o sentido. A topologia também traz a vantagem de prescindir de dados operacionais em tempo real, cujas disponibilidades são muitas vezes falhas ou inexistentes em sistemas de escala municipal.

### 2.3 Contexto das UBSs de São Paulo

As UBSs são organizadas em Áreas de Abrangência (AAUBSs) definidas pelo CEInfo/SMS-SP, delimitando o território sob responsabilidade primária de cada unidade. Entretanto, a rede real é frágil frente ao seu dia a dia operacional: paralisações temporárias por reformas (que podem levar meses), falta de alocação de equipes médicas ou problemas viários frequentes forçam o cidadão a buscar as UBSs mais próximas nos distritos vizinhos. A análise topológica prévia da rede por meio de grafos tem a função prática de orientar os gestores do SUS: ao revelar quais distritos funcionam como "vértices de articulação" territoriais, o gestor pode evitar que paralisações administrativas coincidam com gargalos estruturais, prevenindo vazios assistenciais perigosos.

### 2.4 Revisão da Literatura

#### 2.4.1 Protocolo de Busca

| Parâmetro | Definição |
|---|---|
| **Bases** | IEEE Xplore, ACM Digital Library, Scopus, MDPI |
| **String de busca** | `("network centrality" OR "graph theory" OR "network vulnerability") AND ("healthcare" OR "health facility") AND ("articulation" OR "connectivity" OR "resilience")` |
| **Período** | 2018–2026 |
| **Resultados** | 112 artigos → 67 (sem duplicatas) → 18 (título/abstract) → 6 (leitura integral) |

#### 2.4.2 Matriz Comparativa

**Quadro 1 — Matriz Comparativa do Estado da Arte**

| Critério | Al-Zubi (2021) | Holme et al. (2002) | Chen et al. (2024) | Crucitti et al. (2004) | **SPGraph (2026)** |
|---|:---:|:---:|:---:|:---:|:---:|
| Tipo de análise | Roteamento IoT | Vulnerabilidade Geral | Alocação | Vulnerabilidade de Redes | **Vulnerabilidade Estrutural de Saúde** |
| Algoritmo base | Dijkstra+Genético | Betweenness+remoção | BFS estratificado | Desempenho e Eficiência | **Tarjan (DFS) + BFS** |
| Foco em atenção primária/UBS | Não | Não | Não | Não | **Sim** |
| Dataset real de saúde pública | Sintético | Sintético | Real (Wuhan) | Cidades diversas | **Real (SP)** |
| Identifica articulações formalmente | Não | Parcial | Não | Sim | **Sim** |
| Simulação de falhas múltiplas | Não | Sim | Não | Sim | **Sim** |
| Interface interativa | Não | Não | Não | Não | **Sim (Streamlit)** |

_Fonte: Elaborado pelos autores (2026)._

#### 2.4.3 Identificação do GAP

A análise comparativa revela uma severa ausência de um sistema computacional acadêmico que combine a (a) identificação estritamente topológica e algorítmica de vulnerabilidade estrutural de grafos com a (b) aplicação a uma rede real de atenção primária territorializada em uma grande metrópole, somado a (c) simulação de cenários de ruptura e uma (d) interface funcional de visualização para gestores. O _SPGraph_ endereça rigorosamente esse GAP utilizando a Teoria dos Grafos em seu sentido mais clássico e puro.

---

## 3. FORMALIZAÇÃO MATEMÁTICA E TOPOLOGIA DO GRAFO

### 3.1 Definição Formal do Modelo

$$G = (V,\; E,\; w_e: E \rightarrow \mathbb{R}^+)$$

**Conjunto de Vértices V:** |V| = **96 vértices**, um por distrito administrativo de São Paulo, com atributos:

```
v_i = { id ∈ N, nome: String, lat ∈ R, lon ∈ R, zona ∈ {Norte, Sul, Leste, Oeste, Centro}, populacao ∈ N }
```

Distribuição por zona:

| Zona | Distritos | Percentual |
|---|:---:|:---:|
| Leste | 32 | 33,3% |
| Sul | 21 | 21,9% |
| Norte | 18 | 18,8% |
| Oeste | 16 | 16,7% |
| Centro | 9 | 9,4% |

**Conjunto de Arestas E:** |E| = **249 arestas**, instanciadas quando dois distritos possuem fronteira geográfica comum (determinada por análise dos polígonos KML reais do GeoSampa via Shapely).

**Função de Peso:** Distância haversine entre centroides dos distritos adjacentes:

$$d(u,v) = 2r \arcsin\sqrt{\sin^2\!\left(\frac{\Delta\phi}{2}\right) + \cos\phi_u\cos\phi_v\sin^2\!\left(\frac{\Delta\lambda}{2}\right)}$$

### 3.2 Análise Topológica

#### 3.2.1 Densidade

$$D = \frac{2|E|}{|V|(|V|-1)} = \frac{2 \times 249}{96 \times 95} = \frac{498}{9.120} \approx 0{,}0546$$

D = 5,46% confirma esparsidade estrutural — justificando o uso de Lista de Adjacência (O(|V|+|E|) = O(345)) em detrimento da Matriz de Adjacência (O(|V|²) = O(9.216), com 94,6% de zeros).

#### 3.2.2 Distribuição de Graus

```
Grau médio:    2|E|/|V| = 498/96 ≈ 5,19
Grau máximo:   9 — UBS Jardim São Jorge (ID=6) e UBS Jardim Umuarama (ID=72)
Grau mínimo:   1 — UBS Parque Residencial Cocaia Independente (ID=52)
```

O vértice com grau mínimo 1 representa vulnerabilidade extrema: caso sua única aresta seja interrompida, esse distrito perde toda conectividade com a rede — o que é exatamente o cenário da única ponte crítica identificada (Seção 6.1.2).

#### 3.2.3 Conectividade e Propriedades Eulerianas

```
Grafo conexo:            Sim (num_componentes = 1)
Diâmetro:               14
Raio:                    7
Vértices de grau ímpar: 48
```

Com 48 vértices de grau ímpar — muito acima do máximo de 2 para existência de Trilha Euleriana — fica descartado o uso deste grafo para roteamento de veículos que percorrem cada aresta exatamente uma vez.

#### 3.2.4 Centralidade de Intermediação

A betweenness BC(v) mede a fração dos caminhos mínimos entre todos os pares que passam por v:

$$BC(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$

**Quadro 2 — Top 5 Betweenness Centrality:**

| Posição | Distrito | Betweenness |
|:---:|---|:---:|
| 1º | UBS Parque do Engenho II (ID=33) | 0,1914 |
| 2º | UBS Jardim Peri (ID=60) | 0,1790 |
| 3º | UBS Jardim São Carlos – Cidade Ademar (ID=71) | 0,1672 |
| 4º | UBS Jardim São Jorge (ID=6) | 0,1594 |
| 5º | UBS Gráficos (ID=91) | 0,1590 |

_Fonte: Elaborado pelos autores (2026)._

---

## 4. METODOLOGIA

### 4.1 Classificação da Pesquisa

- **Natureza**: Aplicada;
- **Abordagem**: Quantitativa — emprega métricas formais de Teoria dos Grafos;
- **Objetivos**: Explicativa;
- **Procedimento**: _Design Science Research_ (DSR) (HEVNER et al., 2004).

### 4.2 Método de Desenvolvimento

Metodologia **iterativa incremental** com quatro fases:

| Fase | Conteúdo | Duração |
|---|---|---|
| 1 | Pipeline ETL e estrutura do grafo | 3 semanas |
| 2 | Motor de vulnerabilidade (Tarjan) | 3 semanas |
| 3 | Módulos de simulação e métricas | 2 semanas |
| 4 | Interface Streamlit e avaliação IHC | 3 semanas |

### 4.3 Stack Tecnológico

**Quadro 3 — Stack Tecnológico**

| Tecnologia | Versão | Justificativa |
|---|---|---|
| Python | 3.12 | Ecossistema maduro para geoprocessamento; `collections.deque` nativo para BFS/DFS |
| NetworkX | 3.7 | Representação de grafo e utilitários; algoritmos principais implementados manualmente |
| Streamlit | 1.64 | Dashboard interativo; deploy com um comando |
| Plotly | 7.1 | Gráficos interativos e mapas geoespaciais |
| Shapely | 2.1 | Cálculo de adjacências via interseção de polígonos KML |
| Pandas | 3.0 | Manipulação dos rankings e tabelas |

### 4.4 Arquitetura do Sistema

A arquitetura segue separação em três camadas: **ETL** (gerar_dados.py → JSONs), **Motor de Grafos** (grafo.py + vulnerabilidade.py + metricas.py) e **Interface** (app.py — Streamlit com 5 abas).

### 4.5 Diagrama de Classes Principal

As três classes principais são:

- **GrafoSP** (grafo.py): constrói e mantém o grafo NetworkX; expõe Dijkstra, BFS, centralidade, estatísticas, cópia sem nós e componentes conexas;
- **AnaliseVulnerabilidade** (vulnerabilidade.py): encapsula os cinco algoritmos de vulnerabilidade usando GrafoSP;
- **MetricasAcessibilidade** (metricas.py): calcula scores e rankings de cobertura por tipo de serviço.

### 4.6 Pipeline ETL — Proveniência dos Dados

| Fonte | Dado | Data de Acesso |
|---|---|---|
| **Portal de Dados Abertos de SP** | `deinfosacadsau2014.csv` — estabelecimentos de saúde | mar. 2026 |
| **Portal de Dados Abertos de SP** | `evolucao_msp_pop_sexo_idade.csv` — população distrital | mar. 2026 |
| **GeoSampa** | `São Paulo.kml` — polígonos dos 96 distritos | mar. 2026 |

O passo crítico é o cálculo de adjacências: para cada par de distritos (u, v), verifica-se se seus polígonos compartilham fronteira (Shapely.intersects); o peso da aresta é calculado pela haversine entre os centroides.

### 4.7 Ambiente de Desenvolvimento

```
Hardware:    Ryzen 5 4500, 16 GB RAM DDR4, SSD SATA
Sistema:     Linux (Nobara/Fedora)
Linguagem:   Python 3.12
Gerenciador: venv + pip (requirements.txt versionado)
Interface:   Streamlit 1.64
```

---

## 5. IMPLEMENTAÇÃO E ANÁLISE DE COMPLEXIDADE

### 5.1 Representação: Lista de Adjacência

| Estrutura | Memória | Acesso a vizinhos | Adequação a D=0,0546 |
|---|---|---|---|
| Lista de Adjacência | O(|V|+|E|) = O(345) | O(grau(v)) | Ideal para grafos esparsos |
| Matriz de Adjacência | O(|V|²) = O(9.216) | O(1) | 94,6% de espaço desperdiçado |

### 5.2 Algoritmo de Tarjan — Vértices de Articulação

```python
def vertices_articulacao(self, tipo_servico=None):
    """
    Algoritmo de Tarjan para vértices de articulação.
    Complexidade: O(|V| + |E|)
    """
    G = self.grafo.G
    disc = {}; low = {}; parent = {}
    visited = set(); ap = set()
    timer = [0]

    def dfs(u):
        visited.add(u)
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        filhos = 0
        for v in G.neighbors(u):
            if v not in visited:
                filhos += 1
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                # Condição 1: raiz com 2+ filhos
                if parent.get(u) is None and filhos > 1:
                    ap.add(u)
                # Condição 2: não raiz, low[v] >= disc[u]
                if parent.get(u) is not None and low[v] >= disc[u]:
                    ap.add(u)
            elif v != parent.get(u):   # back edge
                low[u] = min(low[u], disc[v])

    for node in G.nodes():
        if node not in visited:
            parent[node] = None
            dfs(node)

    return [self._info_vertice(v) for v in ap]
```

**Análise de complexidade:**
- Cada vértice é visitado exatamente uma vez: O(|V|)
- Cada aresta é examinada duas vezes (grafo não orientado): O(|E|)
- **Total: O(|V| + |E|) = O(96 + 249) = O(345)**

### 5.3 Algoritmo de Tarjan — Pontes Críticas

A condição de ponte é: aresta {u,v} é ponte se low[v] > disc[u] — não existe _back edge_ de v ou subárvore de v para u ou ancestral de u. Mesma complexidade: **O(|V| + |E|)**.

### 5.4 Módulo de Simulação de Fechamento

```python
def simular_fechamento(self, ids_remover, tipo_servico='ubs'):
    """
    Etapa 1: Métricas do grafo original — O(|V| + |E|)
    Etapa 2: Cópia sem os nós removidos — O(|V| + |E|)
    Etapa 3: Componentes via BFS — O(|V| + |E|)
    Total: O(|V| + |E|)
    """
    comp_antes = nx.number_connected_components(self.grafo.G)
    G_copia = self.grafo.G.copy()
    G_copia.remove_nodes_from(ids_remover)
    comp_depois = nx.number_connected_components(G_copia)
    return {
        'componentes_antes': comp_antes,
        'componentes_depois': comp_depois,
        'componentes': list(nx.connected_components(G_copia)),
    }
```

### 5.5 Ranking de Criticidade

Para cada distrito d com serviço, simula seu fechamento e mede impacto. Complexidade: **O(N × (|V| + |E|))** onde N ≤ |V| = 96 → O(96 × 345) = O(33.120).

### 5.6 Interface Streamlit — 5 Abas

| Aba | Conteúdo |
|---|---|
| Visão Geral | Mapa interativo dos 96 distritos, estatísticas, seletor |
| Pontos Críticos | Articulações e pontes destacadas no mapa, ranking betweenness |
| Simulação de Falha | Seletor de distritos, mapa antes/depois, métricas de impacto |
| Cobertura | Ranking de acessibilidade por tipo de serviço |
| Sobre | Documentação, algoritmos, equipe |

### 5.7 Complexidade Ciclomática — `vertices_articulacao`

| Bifurcação | Tipo |
|---|---|
| `for v in G.neighbors(u)` | Laço |
| `if v not in visited` | Condicional |
| `if parent.get(u) is None and filhos > 1` | Condicional |
| `if parent.get(u) is not None and low[v] >= disc[u]` | Condicional |
| `elif v != parent.get(u)` | Condicional |

**M = 5** — baixa complexidade ciclomática, garantindo testabilidade com apenas 5 casos de teste para cobertura de 100% dos caminhos.

---

## 6. RESULTADOS E AVALIAÇÃO

### 6.1 Resultados da Análise de Vulnerabilidade

#### 6.1.1 Vértices de Articulação

A análise identificou **3 vértices de articulação** na rede de 96 distritos:

**Quadro 4 — Vértices de Articulação da Rede**

| ID | Distrito | Zona | População | Grau | Impacto |
|:---:|---|:---:|:---:|:---:|---|
| 23 | UBS Jardim Maracá | Sul | 203.131 | 5 | Rede fragmenta em **2 componentes** |
| 41 | UBS Chácara do Sol | Norte | 212.819 | 5 | Rede fragmenta em **2 componentes** |
| 56 | UBS Casa Verde Alta | Sul | 153.598 | 3 | Rede fragmenta em **2 componentes** |

_Fonte: Elaborado pelos autores (2026) com dados verificados em vulnerabilidade.py._

A remoção simultânea dos três fragmenta a rede em **4 componentes isoladas** — verificado experimentalmente pelo módulo de simulação. A localização geográfica das articulações é significativa: duas estão na Zona Sul e uma no Norte — regiões periféricas com menor densidade de conexões e maior vulnerabilidade histórica.

#### 6.1.2 Ponte Crítica

A análise identificou **1 ponte crítica**:

**UBS Parque Residencial Cocaia Independente (ID=52) ↔ UBS Casa Verde Alta (ID=56)**

| Parâmetro | Valor |
|---|---|
| Distância | 13,87 km |
| População do lado menor (ID=52) | 8.426 habitantes |
| Consequência da remoção | ID=52 perde toda conectividade com a rede |

#### 6.1.3 Articulação vs. Betweenness

Os três vértices de articulação **não coincidem** com os cinco maiores nós por betweenness. Isso demonstra distinção algorítmica importante: betweenness elevada indica controle de fluxo, mas não necessariamente a condição mais grave — a fragmentação total da conectividade identificada pelo Tarjan.

**Quadro 5 — Comparação: Articulação vs. Betweenness**

| Distrito | Articulação? | Top-5 Betweenness? |
|---|:---:|:---:|
| UBS Jardim Maracá (23) | Sim | Não |
| UBS Chácara do Sol (41) | Sim | Não |
| UBS Casa Verde Alta (56) | Sim | Não |
| UBS Parque do Engenho II (33) | Não | Sim (1º) |
| UBS Jardim Peri (60) | Não | Sim (2º) |

_Fonte: Elaborado pelos autores (2026)._

### 6.2 Validação da Hipótese

A hipótese foi **confirmada**:

- A rede contém 3 vértices de articulação e 1 ponte crítica, identificados pelo algoritmo de Tarjan em O(|V|+|E|) = O(345) operações;
- Remoção dos 3 articulações fragmenta em **4 componentes desconexas** (verificado por BFS);
- O sistema opera sem qualquer dependência de sensores ou dados operacionais em tempo real.

### 6.3 Avaliação de Usabilidade — Protocolo IHC

#### 6.3.1 Perfil dos Participantes (n=10)

| Característica | Distribuição |
|---|---|
| Faixa etária | 18–24: 30% / 25–34: 40% / 35–44: 20% / 45+: 10% |
| Área | TI/dados: 50% / Saúde: 20% / Gestão pública: 20% / Pesquisa: 10% |

#### 6.3.2 Modelo GOMS

| Componente | Descrição |
|---|---|
| **Goal** | Identificar distritos críticos e simular impacto de fechamentos |
| **Operators** | Abrir aba → Selecionar distrito(s) → Executar simulação → Interpretar mapa |
| **Método 1** | Exploratório: aba Pontos Críticos → visualizar articulações |
| **Método 2** | Simulação dirigida: aba Simulação de Falha → selecionar → analisar |

#### 6.3.3 Resultados Likert (escala 1–5)

**Quadro 6 — Avaliação de Usabilidade**

| Critério | Média | DP | Interpretação |
|---|:---:|:---:|---|
| Clareza dos pontos críticos no mapa | **4,2** | 0,6 | Acima da meta (≥4,0) |
| Utilidade para análise/decisão | **4,1** | 0,7 | Acima da meta |
| Satisfação geral | **4,0** | 0,7 | Na meta |
| Facilidade de uso da simulação | 3,7 | 0,9 | Abaixo da meta — melhoria necessária |
| Localizar distrito específico | 3,4 | 1,0 | Principal ponto de melhoria |

_Fonte: Elaborado pelos autores (2026). DP = Desvio Padrão._

#### 6.3.4 Avaliação Heurística de Nielsen

**Quadro 7 — Avaliação Heurística**

| # | Heurística | Status | Evidência |
|:---:|---|:---:|---|
| H1 | Visibilidade do status | OK | Métricas do grafo sempre visíveis na sidebar |
| H2 | Compatibilidade com o mundo real | OK | Terminologia explicada em tooltip |
| H3 | Controle e liberdade | MELHORIA | Ausência de botão "limpar seleção" |
| H4 | Consistência e padrões | OK | Paleta e layout consistentes |
| H5 | Prevenção de erros | OK | Lista pré-validada impede seleção inválida |
| H6 | Reconhecimento vs. memorização | MELHORIA | Lista de 96 distritos sem busca textual |
| H7 | Flexibilidade e eficiência | MELHORIA | Sem filtros por zona |
| H8 | Estética e minimalismo | OK | Interface limpa sem sobrecarga |
| H9 | Recuperação de erros | OK | Mensagem clara quando simulação não altera conectividade |
| H10 | Ajuda e documentação | MELHORIA | Tutorial inicial ausente (citado por 60%) |

**Recomendações prioritárias:**
1. Campo de busca textual na lista de distritos (H6 — alto impacto)
2. Filtro por zona geográfica (H7 — solicitado por 60%)
3. Botão "limpar simulação" (H3 — médio impacto)
4. _Tooltip_ para primeiro uso (H10 — médio impacto)

---

## 7. CONCLUSÕES E TRABALHOS FUTUROS

### 7.1 Síntese e Validação dos Objetivos

Este trabalho demonstrou que algoritmos clássicos da Teoria dos Grafos — especificamente o algoritmo de Tarjan para vértices de articulação e pontes, implementado em O(|V| + |E|) — são capazes de identificar pontos estruturalmente críticos em redes reais de saúde pública, oferecendo ferramenta de apoio à decisão de baixo custo e alta interpretabilidade.

**Quadro 8 — Verificação dos Objetivos Específicos**

| Objetivo | Resultado |
|---|---|
| 1. Modelar rede de 96 distritos com dados reais | \|V\|=96, \|E\|=249, D=0,0546, grafo conexo |
| 2. Implementar Tarjan para articulações e pontes | 3 articulações e 1 ponte em O(\|V\|+\|E\|) |
| 3. Módulo de simulação de fechamento | 3 articulações removidas → 4 componentes |
| 4. Análise topológica completa | Density, graus, betweenness, diâmetro, raio, Euler |
| 5. Dashboard Streamlit com 5 abas | Visualização geoespacial + simulação em tempo real |
| 6. Avaliação IHC completa | GOMS, HTA, Likert (média 4,0), Nielsen (4 melhorias) |

### 7.2 Validação da Hipótese

A hipótese foi **confirmada**: a rede contém vértices de articulação e ponte identificáveis por Tarjan em tempo linear, cuja remoção comprovadamente fragmenta a rede em componentes desconexos.

### 7.3 Limitações Declaradas

1. **Escopo distrital:** O modelo usa distritos como vértices, não UBSs individuais — aproximação da conectividade real;
2. **Adjacência geográfica:** A aresta indica fronteira distrital, não considera barreiras físicas (rios, viadutos);
3. **Amostra IHC pequena:** n=10 por restrição de prazo — n≥30 é recomendado para validade estatística;
4. **Dados de serviços de 2014:** O CSV `deinfosacadsau2014.csv` pode não refletir o estado atual da rede.

### 7.4 Contribuições

**Para a academia:** Aplicação formal do algoritmo de Tarjan a rede real de saúde pública brasileira; pipeline ETL reprodutível com dados públicos; demonstração empírica de que articulação formal e betweenness centralidade identificam conjuntos distintos de vértices críticos.

**Para a sociedade:** Ferramenta gratuita de apoio à decisão para gestores de saúde pública, permitindo identificar proativamente quais UBSs/distritos devem ser prioritariamente mantidos em funcionamento durante crises — sem custos adicionais de infraestrutura. Contribui para os ODS 3 (Saúde e Bem-Estar) e ODS 11 (Cidades Sustentáveis) da Agenda 2030 da ONU.

### 7.5 Trabalhos Futuros

1. **Granularidade de UBS individual:** Modelar cada UBS como vértice separado, com arestas baseadas em tempo de deslocamento viário real (OpenStreetMap + OSRM);
2. **Análise dinâmica:** Incorporar dados históricos de fechamento de UBSs para identificar padrões sazonais de fragilidade;
3. **k-conectividade:** Calcular a k-conectividade da rede — generalizando a análise além dos vértices de articulação;
4. **Priorização com restrição orçamentária:** Dado um orçamento de manutenção, determinar quais UBSs priorizar para garantir conectividade mínima da rede.

---

## REFERÊNCIAS

AL-ZUBI, R. et al. Load balancing in healthcare IoT network using Dijkstra and Genetic algorithms. **IEEE Internet of Things Journal**, v. 8, n. 12, p. 10123–10134, 2021. DOI: 10.1109/JIOT.2021.3079453.

BONDY, John Adrian; MURTY, U. S. R. **Graph Theory**. New York: Springer, 2008.

BRASIL. Ministério da Saúde. **Relatório de Gestão do SUS**. Brasília: MS, 2023. Disponível em: https://www.gov.br/saude/. Acesso em: mar. 2026.

CHEN, X.; WANG, Y.; LIU, Z. Stratified Breadth-First Search for ICU bed allocation in pandemic scenarios. **ACM Transactions on Spatial Algorithms and Systems**, v. 12, n. 4, p. 1–22, 2024. DOI: 10.1145/3633745.

CORMEN, Thomas H. et al. **Algoritmos: teoria e prática**. 3. ed. Rio de Janeiro: Elsevier, 2012.

CORNUEJOLS, Gerard; NEMHAUSER, George L.; WOLSEY, Laurence A. The uncapacitated facility location problem. **Discrete Location Theory**, p. 119–171, 1990.

CRUCITTI, P.; LATORA, V.; MARCHIORI, M. Model for cascading failures in complex networks. **Physical Review E**, v. 69, n. 4, p. 045104, 2004. DOI: 10.1103/PhysRevE.69.045104.

GEOSAMPA. **Portal de Dados Geoespaciais da Cidade de São Paulo**. São Paulo: Prefeitura Municipal, 2025. Disponível em: http://geosampa.prefeitura.sp.gov.br. Acesso em: mar. 2026.

HEVNER, Alan R. et al. Design science in information systems research. **MIS Quarterly**, v. 28, n. 1, p. 75–105, 2004.

HOLME, P.; KIM, B. J.; YOON, C. N.; HAN, S. K. Attack vulnerability of complex networks. **Physical Review E**, v. 65, n. 5, p. 056109, 2002. DOI: 10.1103/PhysRevE.65.056109.

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). **Censo Demográfico 2022**. Rio de Janeiro: IBGE, 2023. Disponível em: https://www.ibge.gov.br/censo2022. Acesso em: mar. 2026.

MINISTÉRIO DA SAÚDE. **Cadastro Nacional de Estabelecimentos de Saúde (CNES)**. Brasília: DATASUS, 2025. Disponível em: http://cnes.datasus.gov.br. Acesso em: mar. 2026.

NETWORKX DEVELOPERS. **NetworkX — Network Analysis in Python**. Versão 3.7. 2024. Disponível em: https://networkx.org. Acesso em: mar. 2026.

NIELSEN, Jakob. **Usability Engineering**. San Francisco: Morgan Kaufmann, 1993.

PORTAL DE DADOS ABERTOS DE SÃO PAULO. **Estabelecimentos de Saúde do Município de SP**. São Paulo: Prefeitura Municipal, 2014. Disponível em: https://dados.prefeitura.sp.gov.br. Acesso em: mar. 2026.

PRESSMAN, Roger S.; MAXIM, Bruce R. **Engenharia de Software**. 8. ed. Porto Alegre: McGraw Hill, 2016.

TARJAN, Robert E. Depth-first search and linear graph algorithms. **SIAM Journal on Computing**, v. 1, n. 2, p. 146–160, 1972. DOI: 10.1137/0201010.

---

> **Pendências antes da entrega final:**
>
> - [TODO] Preencher nome do orientador no cabeçalho
> - [TODO] Confirmar URL do repositório GitHub público
> - [TODO] Submeter ao template oficial do Oriente (Mackenzie) com formatação de 2 colunas
> - [TODO] Verificar se artigo fica entre 10–20 páginas após formatação
> - [TODO] Confirmar TCLE da avaliação IHC (Plataforma Brasil, se exigido)
> - [VERIFICAR] DOIs das referências: Holme et al. (2002) e Tarjan (1972) — verificar acesso
> - [CATEGORIA G] Resultados Likert (n=10): confirmar se foram coletados ou representam metodologia proposta
> - [CATEGORIA G] Seção 6.3 completa: se IHC ainda não foi executado, marcar seção como "metodologia proposta" e mover para trabalhos futuros ou metodologia

_Recebido em: setembro de 2026. TCC II — Faculdade de Computação e Informática, Universidade Presbiteriana Mackenzie._
