# SPGRAPH: MODELAGEM EM TEORIA DOS GRAFOS PARA IDENTIFICAÇÃO DE GARGALOS TOPOLÓGICOS INVISÍVEIS E EFEITO CASCATA NA REDE DE UBSs DE SÃO PAULO

**Lucas Fernandes de Camargo** (RA: 10419400) — **Lendy Naiara Carpio Pacheco** (RA: 10428525) — **Anna Luiza Stella Santos** (RA: 10417401)

Faculdade de Computação e Informática — Universidade Presbiteriana Mackenzie — São Paulo, SP, Brasil

**Orientador:** Prof. Dr. [Nome do Orientador] | **Curso:** Ciência da Computação | **Semestre:** 2026/1

---

## RESUMO

A gestão tradicional da Atenção Primária à Saúde apoia-se predominantemente em listas e tabelas estáticas que avaliam cada Unidade Básica de Saúde (UBS) de forma isolada, classificando-a apenas pela razão entre demanda local e capacidade instalada. Essa visão tabular possui dois pontos cegos estruturais: (i) o _gargalo invisível_, no qual uma UBS aparenta operar em condição saudável ("verde" na planilha), mas constitui a única ponte topográfica que conecta bairros periféricos ao restante da malha assistencial; e (ii) o _efeito cascata_ (efeito dominó), no qual a paralisação rotineira de uma UBS transfere sua demanda para unidades vizinhas cuja folga operacional para demanda espontânea é limitada pela regra de 70% de demanda programada e 30% de demanda espontânea do Sistema Único de Saúde (SUS), provocando colapsos sucessivos por sobrecarga. Este artigo apresenta o _SPGraph_, um sistema computacional que modela as 454 UBSs georreferenciadas de São Paulo como um grafo ponderado não orientado $G = (V, E, W_V, W_E)$, com $|V| = 454$ vértices e $|E| = 882$ arestas topográficas construídas via Grafo de Proximidade de Gabriel restrito às fronteiras distritais do GeoSampa e ajustadas pela impedância de declividade de Tobler. O sistema integra dois motores algorítmicos: (1) o algoritmo de Tarjan sobre Busca em Profundidade (DFS) em $\mathcal{O}(|V| + |E|)$, que identificou 21 vértices de articulação e 19 pontes críticas na rede real — sendo que 20 dos 21 vértices de articulação figuram como "Verdes (Ótimos)" na tabela isolada; e (2) um simulador de colapso em cascata via Busca em Largura (BFS) em camadas, que redistribui a população desassistida para as UBSs vizinhas segundo o Modelo Gravitacional Probabilístico de Huff e o método _Three-Step Floating Catchment Area_ (3SFCA). Os resultados demonstram que a falha individual de 287 das 454 UBSs (63,2%) desencadeia pelo menos um colapso secundário em cascata nas unidades adjacentes, comprovando a necessidade da análise topológica em grafos como ferramenta complementar ao planejamento em saúde pública.

**Palavras-chave:** Teoria dos Grafos. Unidades Básicas de Saúde. Algoritmo de Tarjan. Falhas em Cascata. Modelo Gravitacional de Huff. Sistema Único de Saúde.

---

## ABSTRACT

Traditional primary healthcare management relies predominantly on static lists and spreadsheets that evaluate each Basic Health Unit (UBS) in isolation, classifying it solely by the ratio between local demand and installed capacity. This tabular perspective suffers from two structural blind spots: (i) the _invisible bottleneck_, where a UBS appears operationally healthy ("green" in a static table) yet acts as the sole topographical bridge linking peripheral neighborhoods to the rest of the healthcare network; and (ii) the _cascading failure_ (domino effect), where a routine disruption at one UBS shifts its demand onto neighboring units whose operational buffer for spontaneous care is bounded by the Brazilian Unified Health System (SUS) 70% scheduled / 30% spontaneous demand rule, triggering successive overload collapses. This paper presents _SPGraph_, a computational system that models all 454 georeferenced UBSs in São Paulo as a weighted undirected graph $G = (V, E, W_V, W_E)$ with $|V| = 454$ vertices and $|E| = 882$ topographical edges built via a Gabriel Proximity Graph constrained by GeoSampa district boundaries and weighted by Tobler's slope impedance. The system integrates two algorithmic engines: (1) Tarjan's algorithm over Depth-First Search (DFS) in $\mathcal{O}(|V| + |E|)$, which identified 21 articulation vertices and 19 critical bridges in São Paulo's real network — 20 of which appear "Green (Optimal)" in an isolated spreadsheet; and (2) a layered Breadth-First Search (BFS) cascading failure simulator that redistributes displaced patients across neighboring UBSs using Huff's Probabilistic Gravity Model and the _Three-Step Floating Catchment Area_ (3SFCA) selection weights. Empirical results show that a single-node failure in 287 of the 454 UBSs (63.2%) triggers at least one secondary cascading collapse among adjacent clinics, demonstrating the value of graph topological diagnostics for public health management.

**Keywords:** Graph Theory. Primary Health Care. Tarjan's Algorithm. Cascading Failures. Huff Gravity Model. Brazilian Health System.

---

## 1. INTRODUÇÃO

### 1.1 Contextualização

As Unidades Básicas de Saúde (UBSs) constituem a porta de entrada preferencial do Sistema Único de Saúde (SUS), responsabilizando-se pelo acompanhamento longitudinal da população adscrita em sua Área de Abrangência (AAUBS) (BRASIL, 2011). No município de São Paulo, uma população de 11,87 milhões de habitantes distribuída em 96 distritos administrativos é assistida por uma malha de 454 UBSs georreferenciadas (PORTAL DE DADOS ABERTOS DE SÃO PAULO, 2014; GEOSAMPA, 2025).

Fora de cenários excepcionais de pandemias ou catástrofes — nos quais as regras operacionais ordinárias são suspensas —, a gestão cotidiana da rede municipal enfrenta interrupções localizadas frequentes: interdições temporárias para reformas prediais, vacância de equipes médicas, quedas de energia ou alagamentos sazonais. Na prática administrativa tradicional, os gestores monitoram essas unidades por meio de relatórios tabulares e planilhas ordenadas. Nessa visão estática, uma UBS cuja demanda territorial ocupe 70% da capacidade instalada é classificada como "verde" (saudável).

Entretanto, uma tabela estática enxerga cada UBS como um ponto isolado e ignora a **malha topológica e geográfica** que conecta as unidades vizinhas. Isso cria dois fenômenos críticos invisíveis às planilhas:
1. **O Gargalo Invisível (Fragilidade Topológica):** Uma UBS pode apresentar indicadores internos ótimos ("verde" na tabela), mas localizar-se no único corredor viário ou topográfico que conecta um conjunto de bairros periféricos ao restante da rede. Na Teoria dos Grafos, esse nó é um **vértice de articulação** (TARJAN, 1972): se ele falhar, parte a rede ao meio e isola populações inteiras.
2. **O Efeito Cascata ou Dominó (Sobrecarga em Cadeia):** De acordo com as diretrizes organizacionais da Atenção Básica no SUS (*Cadernos de Atenção Básica n. 28*, BRASIL, 2011), cerca de **70% da capacidade** de uma UBS é comprometida com a **Demanda Programada** dos moradores da sua própria região (pré-natal, puericultura, crônicos), restando no máximo **30% da capacidade** para **Demanda Espontânea** e acolhimento de pacientes vindos de fora do território. Quando uma UBS colapsa e sua população se desloca para as UBSs vizinhas, uma unidade adjacente que tinha apenas 10% a 30% de folga estoura sua capacidade máxima e entra em colapso, repassando o excedente para a camada seguinte da rede (MOTTER; LAI, 2002; WANG et al., 2008).

### 1.2 Problema de Pesquisa

> **Dada a malha de 454 UBSs do município de São Paulo modelada como um grafo topográfico ponderado $G = (V, E, W_V, W_E)$, se uma UBS colapsar hoje na rotina diária, como determinar matematicamente quais comunidades ficam isoladas por gargalos topológicos, como prever a distribuição desigual do deslocamento populacional entre as UBSs vizinhas (sem assumir divisão igualitária arbitrária) e quais unidades adjacentes entrarão em colapso sucessivo por sobrecarga da margem de 30% de demanda espontânea?**

### 1.3 Proposição Científica

> A modelagem da rede de 454 UBSs de São Paulo como grafo topográfico $G = (V, E, W_V, W_E)$ permite: (i) identificar em tempo linear $\mathcal{O}(|V| + |E|)$, pelo algoritmo de Tarjan, gargalos estruturais invisíveis às tabelas isoladas; e (ii) simular em camadas de Busca em Largura (BFS) o efeito cascata de sobrecarga operacional quando o deslocamento dos pacientes entre UBSs vizinhas é governado pelo Modelo Gravitacional Probabilístico de Huff (1963) e pelos pesos de competição em saúde do método 3SFCA (WAN; ZOU; STERNBERG, 2012), sujeitos ao teto de 30% de demanda espontânea do SUS.

### 1.4 Objetivos

**Objetivo Geral:** Desenvolver um modelo computacional baseado em Teoria dos Grafos para identificar vulnerabilidades topológicas ocultas ("gargalos invisíveis") e simular o efeito cascata de sobrecarga na rede de 454 UBSs de São Paulo.

**Objetivos Específicos:**

1. Construir o grafo $G = (V, E, W_V, W_E)$ com $|V| = 454$ UBSs reais georreferenciadas (CNES/SMS-SP) e $|E| = 882$ arestas topográficas geradas por Grafo de Proximidade de Gabriel restrito às fronteiras distritais do GeoSampa e ponderadas pela impedância de declividade de Tobler (1993);
2. Estimar a demanda territorial base ($D_v^0$) de cada UBS por tesselação espacial de Voronoi (REZENDE; ALMEIDA; NOBRE, 2000) e parametrizar a capacidade ($C_v$) e a folga operacional ($F_v \le 0{,}30 \cdot C_v$) conforme a regra 70/30 da Atenção Básica do SUS;
3. Implementar o algoritmo de Tarjan (1972) via Busca em Profundidade (DFS) para detecção de vértices de articulação e pontes críticas em $\mathcal{O}(|V| + |E|)$, confrontando-os com a classificação de uma tabela isolada;
4. Implementar o motor de simulação de colapso em cascata via Busca em Largura (BFS) em camadas, acoplando a redistribuição gravitacional de demanda (HUFF, 1963; WAN; ZOU; STERNBERG, 2012) ao modelo de sobrecarga local em redes complexas (MOTTER; LAI, 2002; WANG et al., 2008);
5. Disponibilizar os diagnósticos em um _dashboard_ interativo em Streamlit e comparar a divisão gravitacional com a divisão igualitária ingênua ($1/k$).

---

## 2. REFERENCIAL TEÓRICO E TRABALHOS RELACIONADOS

### 2.1 Conectividade em Grafos, Vértices de Articulação e Algoritmo de Tarjan

Seja $G = (V, E)$ um grafo não orientado. Um vértice $v \in V$ é definido como **vértice de articulação** (ou vértice de corte) se a sua remoção $(G - \{v\})$ aumenta o número de componentes conexas do grafo (BONDY; MURTY, 2008). Analogamente, uma aresta $e = \{u, v\} \in E$ é uma **ponte** se $G - \{e\}$ possui mais componentes conexas que $G$.

Tarjan (1972) demonstrou que todos os vértices de articulação e pontes de um grafo podem ser determinados em tempo estritamente linear $\mathcal{O}(|V| + |E|)$ mediante uma única Busca em Profundidade (DFS) que mantém, para cada vértice $u$, o instante de descoberta $\text{disc}[u]$ e o menor índice de descoberta alcançável a partir da subárvore enraizada em $u$ por meio de no máximo uma aresta de retorno, denominado $\text{low}[u]$:

$$\text{low}[u] = \min \begin{cases} \text{disc}[u], \\ \text{low}[v] & \text{para todo filho } v \text{ de } u \text{ na árvore DFS}, \\ \text{disc}[w] & \text{para toda aresta de retorno } (u, w). \end{cases}$$

Um vértice $u$ é de articulação se e somente se: (a) $u$ é raiz da árvore DFS e possui ao menos dois filhos; ou (b) $u$ não é raiz e existe algum filho $v$ na árvore DFS tal que $\text{low}[v] \ge \text{disc}[u]$. Já a aresta $\{u, v\}$ é ponte se e somente se $\text{low}[v] > \text{disc}[u]$ (TARJAN, 1972).

### 2.2 Organização da Atenção Básica no SUS e a Regra 70% / 30%

Diferentemente de unidades de pronto-socorro hospitalar, a UBS opera sob o princípio da territorialização e adscrição de clientela (BRASIL, 2011). Para conciliar o acompanhamento longitudinal dos moradores da sua Área de Abrangência com o atendimento de intercorrências agudas do cotidiano, os protocolos de gestão da agenda na Atenção Básica estruturam a capacidade instalada ($C_v$) em duas faixas operacionais:
- **Demanda Programada ($\approx 70\%$ de $C_v$):** destinada às ações continuadas e agendadas da população adscrita da própria região da UBS;
- **Demanda Espontânea ($\le 30\%$ de $C_v$):** margem operacional reservada ao acolhimento de eventos agudos do dia e ao atendimento eventual de usuários fora de sua área de abrangência (BRASIL, 2011).

Essa restrição institucional é fundamental para a modelagem de vulnerabilidade em cenários de rotina: uma UBS vizinha $v$ não dispõe da totalidade de sua capacidade $C_v$ para absorver pacientes oriundos de uma unidade colapsada $u$, mas apenas da sua **folga operacional efetiva** $F_v = \max(0,\; \min(0{,}30 \cdot C_v,\; C_v - D_v^0))$.

### 2.3 Movimento da População entre UBSs Vizinhas: Modelo Gravitacional de Huff e 3SFCA

Quando uma UBS $u$ suspende seus atendimentos e possui $k \ge 2$ UBSs vizinhas conectadas no grafo, assumir uma divisão uniforme da demanda ($1/k$, como $25\%$ para cada uma de quatro unidades vizinhas) viola a dinâmica espacial do comportamento do usuário de saúde. Em Geografia da Saúde, a escolha de pacientes entre múltiplas unidades concorrentes é modelada por **Modelos de Interação Espacial (Modelos Gravitacionais)** (STACHERL; SAUZET, 2023).

Huff (1963) formulou a probabilidade de um usuário localizado em $u$ deslocar-se até um serviço $v$ como diretamente proporcional à atratividade/porte da unidade de destino ($C_v^\alpha$) e inversamente proporcional a uma função de atrito da distância ($d_{uv}^\beta$). No domínio específico de serviços de saúde, **Wan, Zou e Sternberg (2012)** incorporaram esse mecanismo no método _Three-Step Floating Catchment Area_ (**3SFCA**), definindo o **peso de seleção por competição ($G_{uv}$ ou $W_{uv}$)** entre unidades de saúde próximas. Conforme demonstrado na revisão sistemática de **Stacherl e Sauzet (2023)** e na avaliação de funções de decaimento espacial de **McGrail (2012)**, o peso gravitacional captura simultaneamente a disponibilidade de oferta ($C_v$) e a impedância geográfica ($d_{uv}^{-\beta}$).

Adicionalmente, em cidades com relevo acidentado como São Paulo, a distância horizontal simples não reflete o esforço físico do deslocamento a pé ou por transporte local. **Tobler (1993)** propôs a _Hiking Function_, na qual a velocidade de caminhada decai exponencialmente com a declividade topográfica $s = |\Delta h| / \Delta x$:

$$V(s) = 6 \cdot e^{-3{,}5 \cdot |s + 0{,}05|} \quad (\text{km/h})$$

permitindo ponderar as arestas do grafo pela **impedância topográfica efetiva** $d_{\text{topo}}(u, v)$.

### 2.4 Falhas em Cascata e Redistribuição Local de Carga em Redes Complexas

O fenômeno do "efeito dominó" decorrente de sobrecarga em grafos foi formalizado por **Motter e Lai (2002)**, que definiram a capacidade máxima de cada vértice como $C_v = (1 + \alpha) L_v^0$, onde $L_v^0$ é a carga inicial e $\alpha \ge 0$ é o parâmetro de tolerância. Quando um vértice falha e sua carga é redistribuída, qualquer vértice cuja carga atualizada supere $C_v$ também entra em colapso, gerando uma reação em cadeia. **Crucitti, Latora e Marchiori (2004)** estenderam essa formulação para passos discretos (camadas iterativas de propagação).

Para sistemas físicos e territoriais nos quais a demanda de um nó não salta instantaneamente para o extremo oposto da cidade, mas transborda para a vizinhança imediata, **Wang et al. (2008)** introduziram a **Regra de Redistribuição Preferencial Local de Carga** (_Local Preferential Load Redistribution_): quando o nó $u$ falha, sua carga é distribuída exclusivamente entre seus vizinhos imediatos $v \in N(u)$ proporcionalmente às características dos vizinhos, propagando-se camada a camada na rede.

### 2.5 Comparação de Abordagens na Literatura

**Quadro 1 — Síntese Comparativa de Abordagens Relacionadas**

| Trabalho | Domínio / Escopo | Modelo / Algoritmo Principal | Considera Capacidade e Demanda? | Modela Escolha / Fluxo entre Vizinhos? | Simula Efeito Cascata (Dominó)? | Identifica Articulações (Tarjan)? |
|---|---|---|---|---|---|---|
| **Rezende, Almeida e Nobre (2000)** | Saúde Pública (RJ) | Diagramas de Voronoi para áreas de abrangência | Sim (demanda adscrita) | Apenas vizinho mais próximo | Não | Não |
| **Motter e Lai (2002)**; **Wang et al. (2008)** | Redes Complexas | Capacidade $C_v = (1+\alpha)L_v^0$ e redistribuição local | Sim (carga/capacidade) | Preferencial por grau/capacidade | **Sim** | Não |
| **Wan, Zou e Sternberg (2012)**; **Stacherl e Sauzet (2023)** | Atenção Primária (GIS) | 3SFCA / Modelos Gravitacionais com peso de seleção | Sim (oferta/demanda) | **Sim ($W_{uv}$ gravitacional)** | Não (modelo estático) | Não |
| **Mossoux, Kervyn e Canters (2019)** | Serviços Críticos | Remoção iterativa de segmentos viários | Não | Menor caminho viário | Não | Parcial |
| **Uehara et al. (2021)** | UBSs (Estado de SP) | Otimização por _p-medianas_ | Sim (alocação ótima) | Alocação estática | Não | Não |
| **SPGraph (Proposto, 2026)** | **454 UBSs Reais (Município de SP)** | **Tarjan (DFS) + Cascata em Camadas (BFS) + Huff/3SFCA + Regra 70/30 SUS** | **Sim ($C_v, D_v^0, F_v \le 30\%$)** | **Sim ($W_{uv}$ gravitacional topográfico)** | **Sim (BFS em camadas)** | **Sim (Tarjan $\mathcal{O}(\|V\|+\|E\|)$)** |

_Fonte: Elaborado pelos autores (2026)._

---

## 3. FORMALIZAÇÃO MATEMÁTICA E MODELAGEM DO GRAFO DE UBSs

### 3.1 Definição Formal do Grafo $G = (V, E, W_V, W_E)$

A malha de Atenção Primária à Saúde de São Paulo é modelada como um grafo não orientado duplamente ponderado:

$$G = (V,\; E,\; W_V,\; W_E)$$

1. **Conjunto de Vértices ($V$):** $|V| = 454$ vértices, correspondendo às **454 UBSs georreferenciadas únicas** (deduplicadas por código CNES) presentes na base oficial da Secretaria Municipal da Saúde de São Paulo (`deinfosacadsau2014.csv`). Cada vértice $v \in V$ possui a tupla de atributos:
   $$W_V(v) = \big(D_v^0,\; C_v,\; C_{v,\text{prog}},\; F_v,\; h_v\big)$$
   onde:
   - $D_v^0 \in \mathbb{N}$: **Demanda Territorial Base** (população adscrita da AAUBS), obtida pela partição espacial de Voronoi da população oficial dos distritos (`evolucao_msp_pop_sexo_idade.csv`, totalizando $11.869.660$ habitantes) no interior dos polígonos do GeoSampa (`São Paulo.kml`);
   - $C_v \in \mathbb{N}$: **Capacidade Total Instalada** da UBS, dimensionada pelo porte de Equipes de Saúde da Família ($\text{eSF} \times 5.000$) e presença de AMA acoplada, somando $16.954.500$ vagas nominais na rede;
   - $C_{v,\text{prog}} = 0{,}70 \cdot C_v$: **Cota de Demanda Programada** (70% reservados à população da própria região);
   - $F_v = \max\!\big(0,\; \min(0{,}30 \cdot C_v,\; C_v - D_v^0)\big)$: **Folga Operacional Efetiva** ($\le 30\%$) disponível para absorver demanda espontânea e transbordo de UBSs vizinhas (totalizando $4.190.264$ vagas na cidade);
   - $h_v \in \mathbb{R}^+$: Altitude estimada em metros no relevo da Bacia de São Paulo.

**Quadro 2 — Distribuição das 454 UBSs Reais por Zona Geográfica**

| Zona Geográfica | Quantidade de UBSs ($\|V\|$) | Percentual da Rede |
|---|:---:|:---:|
| **Leste** | 174 | 38,33% |
| **Sul** | 152 | 33,48% |
| **Norte** | 89 | 19,60% |
| **Oeste** | 29 | 6,39% |
| **Centro** | 10 | 2,20% |
| **Total** | **454** | **100,00%** |

_Fonte: Processado pelos autores a partir de `deinfosacadsau2014.csv` (2026)._

2. **Conjunto de Arestas ($E$):** $|E| = 882$ arestas construídas pelo **Grafo de Proximidade de Gabriel** restrito à contiguidade distrital do KML. Dois vértices $u, v \in V$ são conectados por uma aresta $\{u, v\} \in E$ se e somente se pertencem ao mesmo distrito ou a distritos limítrofes em `São Paulo.kml` (evitando conexões artificiais entre zonas distantes ou separadas por represas) e satisfazem a condição geométrica de Gabriel:
   $$d^2(u, v) \le d^2(u, k) + d^2(v, k), \quad \forall k \in V \setminus \{u, v\}$$
   garantindo que só existam conexões entre UBSs imediatamente adjacentes, sem "saltar" sobre uma UBS intermediária $k$.

3. **Peso das Arestas ($W_E$):** Cada aresta $e = \{u, v\} \in E$ recebe a distância geodésica Haversine $d_{\text{hav}}(u, v)$ corrigida pelo fator de declividade topográfica $s_{uv} = |h_u - h_v| / (1000 \cdot d_{\text{hav}}(u, v))$ via função de Tobler (1993):
   $$d_{\text{topo}}(u, v) = d_{\text{hav}}(u, v) \cdot \frac{V(0)}{V_{\text{média}}(s_{uv})}$$

### 3.2 Equação de Redistribuição Gravitacional e Cascata em Camadas (BFS)

Quando uma UBS $u$ falha na camada $k-1$ do BFS com uma carga desassistida $D_{\text{transbordo}}(u)$, o deslocamento populacional para cada vizinha ativa $v \in N_{\text{ativas}}(u)$ na camada $k$ é determinado pelo peso gravitacional de Huff (1963) e 3SFCA (WAN; ZOU; STERNBERG, 2012):

$$W_{uv} = \frac{C_v^\alpha \cdot d_{\text{topo}}(u, v)^{-\beta}}{\sum_{z \in N_{\text{ativas}}(u)} C_z^\alpha \cdot d_{\text{topo}}(u, z)^{-\beta}}, \qquad \Delta D_{u \to v} = D_{\text{transbordo}}(u) \cdot W_{uv}$$

com $\alpha = 1{,}0$ e $\beta = 2{,}0$. A carga total recebida pelo vizinho $v$ na camada $k$ é $\Delta D_v^{(k)} = \sum_{u} \Delta D_{u \to v}$. Confrontando essa carga com a folga operacional restante $F_v^{(k-1)}$ (limitada pelos $30\%$ de demanda espontânea):
- **Caso 1 ($\Delta D_v^{(k)} \le F_v^{(k-1)}$ — Absorção):** A UBS vizinha $v$ absorve integralmente os pacientes, sua folga atualiza-se para $F_v^{(k)} = F_v^{(k-1)} - \Delta D_v^{(k)}$ e a cascata cessa naquele ramo.
- **Caso 2 ($\Delta D_v^{(k)} > F_v^{(k-1)}$ — Colapso em Cascata / Efeito Dominó):** A UBS vizinha $v$ satura sua margem de $30\%$, entra em **colapso por sobrecarga** ($v$ é removida do conjunto de unidades ativas para novos transbordos) e o **excedente não atendido**
  $$E_v^{(k)} = \Delta D_v^{(k)} - F_v^{(k-1)}$$
  é inserido na fila do BFS para ser redistribuído aos vizinhos ativos de $v$ na **Camada $k+1$**!

### 3.3 Propriedades Topológicas da Malha de 454 UBSs

- **Densidade:** $D = \frac{2|E|}{|V|(|V|-1)} = \frac{2 \times 882}{454 \times 453} = \frac{1.764}{205.662} \approx 0{,}0086$ ($0{,}86\%$), confirmando alta esparsidade e justificando a estrutura de Lista de Adjacência ($\mathcal{O}(|V|+|E|) = \mathcal{O}(1.336)$) frente à Matriz de Adjacência ($\mathcal{O}(|V|^2) = \mathcal{O}(206.116)$).
- **Distribuição de Graus:** Grau médio $= 3{,}89$; Grau máximo $= 7$ (`UBS Jd. Paulistano` ID=30, `UBS Jd. República` ID=99 e `UBS Vila das Mercês` ID=340); Grau mínimo $= 1$ (11 UBSs periféricas pendulares).
- **Conectividade, Diâmetro e Raio:** Grafo conexo ($1$ componente conexa); Diâmetro topológico $= 35$ saltos; Raio $= 18$ saltos; Vértices de grau ímpar $= 232$.

---

## 4. RESULTADOS EXPERIMENTAIS E DISCUSSÃO

### 4.1 Detecção de "Gargalos Invisíveis" via Algoritmo de Tarjan

A execução do algoritmo de Tarjan ($\mathcal{O}(|V| + |E|)$) sobre as 454 UBSs e 882 arestas identificou **21 vértices de articulação** e **19 pontes críticas**.

**Quadro 3 — Principais Vértices de Articulação ("Gargalos Invisíveis") Detectados por Tarjan**

| ID | UBS (Vértice de Articulação) | Distrito (Zona) | Grau | Status na Tabela Isolada | UBSs Isoladas se Cair | População Isolada se Cair |
|:---:|---|---|:---:|:---:|:---:|:---:|
| **328** | UBS República | República (Centro) | 4 | Vermelho (Crítico) | 2 UBSs | 163.943 hab. |
| **399** | UBS Jd. Fontalis | Tremembé (Norte) | 5 | **Verde (Ótimo)** | 2 UBSs | 129.805 hab. |
| **20** | UBS Humaitá - Dr. João A. Lage | Bela Vista (Centro) | 2 | **Verde (Ótimo)** | 1 UBS | 124.777 hab. |
| **209** | UBS Jd. Aracati | Jardim Ângela (Sul) | 4 | **Verde (Ótimo)** | 4 UBSs | 80.453 hab. |
| **6** | UBS Morada do Sol | Anhanguera (Norte) | 3 | **Verde (Ótimo)** | 3 UBSs | 64.300 hab. |
| **223** | UBS Vila Calu | Jardim Ângela (Sul) | 3 | **Verde (Ótimo)** | 3 UBSs | 60.339 hab. |
| **98** | UBS Jd. Icaraí I (Quintana) | Cidade Dutra (Sul) | 4 | **Verde (Ótimo)** | 1 UBS | 50.782 hab. |
| **270** | UBS Colônia | Parelheiros (Sul) | 4 | **Verde (Ótimo)** | 4 UBSs | 47.549 hab. |

_Fonte: Resultados experimentais verificados em `src/vulnerabilidade.py` (2026)._

Constata-se que **20 dos 21 vértices de articulação (95,2%) apresentam status "Verde (Ótimo)" quando avaliados isoladamente em uma tabela comum** (pois operam com taxa de ocupação base próxima a 70%). Contudo, topologicamente, são pontos únicos de falha que sustentam corredores geográficos inteiros nos extremos Sul (Parelheiros, Marsilac, Jardim Ângela, Cidade Dutra, Pedreira) e Norte (Anhanguera, Perus, Tremembé).

### 4.2 Validação do Movimento Populacional: Divisão Gravitacional (Huff/3SFCA) vs. Divisão Igualitária ($1/k$)

Para demonstrar a inadequação da divisão uniforme ($25\%$ para cada vizinho quando $\text{grau}=4$), o Quadro 4 apresenta o resultado experimental da desativação da **`UBS República` (ID=328, Zona Centro, $D_{328}^0 = 69.304$ hab.)**, conectada a quatro UBSs vizinhas:

**Quadro 4 — Comparação Real na `UBS República` (ID=328): Divisão Igualitária (25%) vs. Modelo Gravitacional (Huff/3SFCA)**

| UBS Vizinha ($v \in N(328)$) | Distância $d_{\text{topo}}$ | Capacidade ($C_v$) | Folga $\le 30\%$ ($F_v$) | Fluxo Igualitário ($25\%$) | Fluxo Gravitacional ($W_{uv}$) | Pacientes (Huff/3SFCA) | Resultado na Camada 1 do BFS (Gravitacional) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **UBS Humaitá** (Bela Vista) | $0{,}75\text{ km}$ | $60.000$ | $18.000$ | $17.326$ (Não colapsa) | **65,91%** | **45.678 hab.** | **COLAPSA! (Excedente: +27.678 hab.)** |
| **UBS Sé** (Sé) | $1{,}21\text{ km}$ | $45.000$ | $13.500$ | $17.326$ (Colapsa) | **18,99%** | **13.161 hab.** | Absorve ($99{,}2\%$ de ocupação) |
| **UBS Sta. Cecília** (Sta. Cecília) | $2{,}39\text{ km}$ | $94.000$ | $7.684$ | $17.326$ (Colapsa) | **10,08%** | **6.986 hab.** | Absorve ($99{,}3\%$ de ocupação) |
| **UBS Bom Retiro** (Bom Retiro) | $2{,}71\text{ km}$ | $60.000$ | $18.000$ | $17.326$ (Não colapsa) | **5,01%** | **3.472 hab.** | Absorve ($75{,}8\%$ de ocupação) |

_Fonte: Resultados obtidos pelo método `comparar_divisao_demanda(328)` em `src/vulnerabilidade.py` (2026)._

Enquanto a divisão igualitária subestima severamente a pressão sobre a unidade mais próxima (`UBS Humaitá`, a apenas $0{,}75\text{ km}$), o modelo gravitacional revela que **65,91% do fluxo ($45.678$ pacientes)** concentra-se na `UBS Humaitá`, rompendo sua folga de $18.000$ vagas na **Camada 1 do BFS** e disparando, na **Camada 2 do BFS**, o colapso secundário da `UBS Armando Darienzo - N. Sra. do Brasil` (que possuía $10.723$ vagas de folga e recebeu os $27.678$ pacientes excedentes).

### 4.3 Simulação Sistemática do Efeito Cascata em Toda a Rede de São Paulo

Simulando individualmente a falha de cada uma das 454 UBSs da rede via BFS em camadas:
- **287 das 454 UBSs (63,2%)** provocam pelo menos **1 colapso secundário em cascata** nas unidades vizinhas quando falham isoladamente;
- Nos cenários mais severos de pressão demográfica periférica (Quadro 5), a falha de uma única UBS de grande porte chega a derrubar entre **8 e 17 UBSs vizinhas em efeito dominó**, exigindo que o cidadão percorra de **4 a 6 saltos na malha** até encontrar a primeira UBS com vaga disponível na cota de 30%.

**Quadro 5 — Top 6 Gatilhos de Efeito Cascata em Dominó (Simulação BFS + Huff/3SFCA)**

| ID | UBS Desativada (Camada 0) | Distrito (Zona) | Demanda Remanejada | UBSs Derrubadas em Cascata | Profundidade da Cascata (Saltos BFS) |
|:---:|---|---|:---:|:---:|:---:|
| **137** | UBS Chácara Santo Amaro | Grajaú (Sul) | 128.930 hab. | **+17 UBSs** | **6 saltos** |
| **233** | UBS Jd. Souza | Jardim São Luís (Sul) | 95.642 hab. | **+12 UBSs** | **6 saltos** |
| **31** | UBS Jd. Vista Alegre | Brasilândia (Norte) | 116.022 hab. | **+12 UBSs** | **4 saltos** |
| **207** | UBS Cidade Ipava | Jardim Ângela (Sul) | 91.423 hab. | **+11 UBSs** | **6 saltos** |
| **439** | UBS NGA 39 Santa Cruz - PAM | Vila Mariana (Sul) | 133.049 hab. | **+10 UBSs** | **5 saltos** |
| **19** | UBS Armando Darienzo N. Sra. do Brasil | Bela Vista (Centro) | 124.777 hab. | **+8 UBSs** | **6 saltos** |

_Fonte: Simulação executada em `src/vulnerabilidade.py` sobre as 454 UBSs (2026)._

---

## 5. CONCLUSÕES

Este trabalho desenvolveu e validou o _SPGraph_, modelando as **454 UBSs reais de São Paulo** e suas **882 conexões topográficas** para responder quem fica desassistido e quais unidades vizinhas colapsam em efeito dominó quando uma UBS falha no dia a dia.

1. **Superação das listas estáticas ("Gargalos Invisíveis"):** O algoritmo de Tarjan provou que 20 das 21 UBSs que funcionam como vértices de articulação na topologia da cidade aparentam estar "Verdes" em relatórios tabulares isolados, mas sua paralisação secciona o grafo e isola até $129.805$ moradores em uma única falha.
2. **Previsão fundamentada do movimento populacional:** A combinação da regra operacional do SUS (**70% demanda programada / 30% demanda espontânea**) com o **Modelo Gravitacional de Huff (1963) e 3SFCA (WAN; ZOU; STERNBERG, 2012)** eliminou a necessidade de divisões arbitrárias ($1/k$), ponderando rigorosamente a capacidade instalada das vizinhas e a impedância topográfica de deslocamento.
3. **Quantificação do efeito dominó via BFS:** A simulação em camadas demonstrou que 63,2% das UBSs paulistanas desencadeiam sobrecarga crítica em ao menos uma vizinha imediata caso sejam desativadas sem contingência prévia.

---

## REFERÊNCIAS

ALBERT, R.; JEONG, H.; BARABÁSI, A.-L. Error and attack tolerance of complex networks. **Nature**, v. 406, p. 378–382, 2000. DOI: https://doi.org/10.1038/35019019.

BONDY, J. A.; MURTY, U. S. R. **Graph theory**. New York: Springer, 2008.

BRASIL. Ministério da Saúde. Secretaria de Atenção à Saúde. Departamento de Atenção Básica. **Acolhimento à demanda espontânea**. Brasília: Ministério da Saúde, 2011. v. 1, 56 p. (Cadernos de Atenção Básica, n. 28).

CRUCITTI, P.; LATORA, V.; MARCHIORI, M. Model for cascading failures in complex networks. **Physical Review E**, v. 69, n. 4, p. 045104, 2004. DOI: https://doi.org/10.1103/PhysRevE.69.045104.

DIJKSTRA, E. W. A note on two problems in connexion with graphs. **Numerische Mathematik**, v. 1, n. 1, p. 269–271, 1959. DOI: https://doi.org/10.1007/BF01386390.

GEOSAMPA. **Portal de Dados Geoespaciais da Cidade de São Paulo**. São Paulo: Prefeitura Municipal, 2025. Disponível em: http://geosampa.prefeitura.sp.gov.br. Acesso em: mar. 2026.

HUFF, D. L. A probabilistic analysis of shopping center trade areas. **Land Economics**, v. 39, n. 1, p. 81–90, 1963. DOI: https://doi.org/10.2307/3144521.

JANKOWSKI, P.; BROWN, B. Health care accessibility modeling: effects of change in spatial representation of demand for primary health care services. **Quaestiones Geographicae**, v. 33, n. 3, p. 39–53, 2014. DOI: https://doi.org/10.2478/quageo-2013-0028.

LALOU, M.; TAHRAOUI, M. A.; KHEDDOUCI, H. The Critical Node Detection Problem in networks: A survey. **Computer Science Review**, v. 28, p. 92–117, 2018. DOI: https://doi.org/10.1016/j.cosrev.2018.02.002.

McGRAIL, M. R. Spatial accessibility of primary health care utilising the two step floating catchment area method: an assessment of recent improvements. **International Journal of Health Geographics**, v. 11, n. 50, p. 1–12, 2012. DOI: https://doi.org/10.1186/1476-072X-11-50.

MOSSOUX, S.; KERVYN, M.; CANTERS, F. Assessing the impact of road segment obstruction on accessibility of critical services in case of a hazard. **Natural Hazards and Earth System Sciences**, v. 19, p. 1251–1263, 2019. DOI: https://doi.org/10.5194/nhess-19-1251-2019.

MOTTER, A. E.; LAI, Y.-C. Cascade-based attacks on complex networks. **Physical Review E**, v. 66, n. 6, p. 065102, 2002. DOI: https://doi.org/10.1103/PhysRevE.66.065102.

PORTAL DE DADOS ABERTOS DE SÃO PAULO. **Estabelecimentos de Saúde do Município de São Paulo (`deinfosacadsau2014.csv`)**. São Paulo: Prefeitura Municipal, 2014. Disponível em: https://dados.prefeitura.sp.gov.br. Acesso em: mar. 2026.

REZENDE, F. A. V. S.; ALMEIDA, R. M. V. R.; NOBRE, F. F. Diagramas de Voronoi para a definição de áreas de abrangência de hospitais públicos no Município do Rio de Janeiro. **Cadernos de Saúde Pública**, v. 16, n. 2, p. 467–475, 2000. DOI: https://doi.org/10.1590/S0102-311X2000000200017.

STACHERL, B.; SAUZET, O. Gravity models for potential spatial healthcare access measurement: a systematic methodological review. **International Journal of Health Geographics**, v. 22, n. 34, p. 1–22, 2023. DOI: https://doi.org/10.1186/s12942-023-00358-z.

TARJAN, R. E. Depth-first search and linear graph algorithms. **SIAM Journal on Computing**, v. 1, n. 2, p. 146–160, 1972. DOI: https://doi.org/10.1137/0201010.

TOBLER, W. **Three presentations on geographical analysis and modeling: non-isotropic geographic modeling; speculations on the geometry of geography; and global spatial analysis**. Technical Report 93-1. Santa Barbara: National Center for Geographic Information and Analysis (NCGIA), University of California, 1993.

UEHARA, D. O.; ROSA, P. L.; MORAES, M. C.; SATO, R. C. Impacts of decentralization in health systems in the state of São Paulo, Brazil. **einstein (São Paulo)**, v. 19, p. eGS5914, 2021. DOI: https://doi.org/10.31744/einstein_journal/2021GS5914.

WAN, N.; ZOU, B.; STERNBERG, T. A three-step floating catchment area method for analyzing spatial access to health services. **International Journal of Geographical Information Science**, v. 26, n. 6, p. 1073–1089, 2012. DOI: https://doi.org/10.1080/13658816.2011.624987.

WANG, J.-W.; RONG, L.-L.; ZHANG, L.; ZHANG, Z. Attack vulnerability of scale-free networks due to cascading failures. **Physica A: Statistical Mechanics and its Applications**, v. 387, n. 26, p. 6671–6678, 2008. DOI: https://doi.org/10.1016/j.physa.2008.08.037.
