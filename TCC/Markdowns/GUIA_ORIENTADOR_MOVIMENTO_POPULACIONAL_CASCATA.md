# Guia para Reunião com o Orientador — Movimento da População, Gargalos Invisíveis e Efeito Cascata nas UBSs de São Paulo

> **Objetivo deste documento:** Responder de forma matemática, algorítmica e com literatura científica verificada (fora de cenários pandêmicos) à pergunta central do projeto:
> *"Quando uma UBS colapsa no dia a dia, como prever para quais UBSs vizinhas a população se desloca (sem chutar divisão igualitária de 50%/50% ou 25% para cada), respeitando a regra operacional de 70% Demanda Programada / 30% Demanda Espontânea do SUS, e como simular os gargalos invisíveis e o efeito cascata no grafo?"*

---

## 1. Visão Geral da Nova Modelagem do Grafo ($G = (V, E, W_V, W_E)$)

Em vez de agrupar a cidade em 96 distritos genéricos (o que esconderia as vulnerabilidades locais entre postos de saúde), o sistema modela diretamente a **malha real das Unidades Básicas de Saúde (UBSs)** do município de São Paulo:

* **Vértices ($|V| = 454$ UBSs reais georreferenciadas):** Extraídas da base oficial do CNES / Secretaria Municipal da Saúde de São Paulo (`deinfosacadsau2014.csv`). Cada vértice $v \in V$ armazena:
  1. **Demanda Base Territorial ($D_v^0$):** População adscrita da sua Área de Abrangência (estimada por tesselação espacial de Voronoi dentro dos polígonos oficiais do GeoSampa — `São Paulo.kml`, método de Rezende, Almeida e Nobre, 2000).
  2. **Capacidade Total Instalada ($C_v$):** Dimensionada pelo número de equipes de Saúde da Família (eSF) e reforço assistencial (AMA acoplada).
  3. **Cota Programada ($70\%$ de $C_v$) e Cota de Demanda Espontânea ($\le 30\%$ de $C_v$):** Em conformidade com as diretrizes de rotina da Atenção Básica no SUS (BRASIL, 2011).
* **Arestas ($|E| = 882$ conexões topográficas locais):** Construídas por um **Grafo de Proximidade de Gabriel** restrito às fronteiras distritais contíguas do `São Paulo.kml`. Duas UBSs $(u, v)$ só possuem conexão direta se seus territórios de atendimento são adjacentes na mesma região e não existe outra UBS intermediária no caminho.
* **Peso das Arestas ($w(u, v) = d_{\text{topo}}(u, v)$):** Distância geodésica Haversine ajustada pela **Impedância Topográfica de Declividade** segundo a *Função de Caminhada de Tobler* (TOBLER, 1993), penalizando trajetos com forte desnível altimétrico (ladeiras/morros).

---

## 2. Como Responder à Pergunta do Professor: "Como Calcular o Movimento da População?"

**Por que não podemos dividir igualmente ($1/k$, ex.: 25% para cada uma de 4 UBSs vizinhas)?**
Na vida real, o cidadão cujo posto de saúde fechou temporariamente (por reforma predial, falta de médicos, queda de energia ou alagamento) **não sorteia um posto vizinho ao acaso**. Ele sofre forte influência de dois fatores físicos e operacionais:
1. **Atrito Espacial e Topográfico ($d_{\text{topo}}(u, v)$):** Uma UBS vizinha a $700\text{ metros}$ no plano absorve muito mais pacientes do que outra a $2{,}7\text{ km}$ ou após uma subida íngreme.
2. **Porte / Capacidade da Unidade Destino ($C_v$):** Unidades de maior porte atraem maior proporção do fluxo do que unidades pequenas.

A literatura científica resolve esse problema exato combinando **três modelos clássicos** (todos voltados para operação de rotina, sem depender de cenários de pandemia):

### 2.1. O Limite da Rotina no SUS: Regra 70% Demanda Programada / 30% Demanda Espontânea
Segundo as diretrizes do Ministério da Saúde no *Caderno de Atenção Básica n. 28 — Acolhimento à Demanda Espontânea* (BRASIL, 2011), a agenda cotidiana de uma UBS é dividida entre:
* **70% para Demanda Programada:** Consultas agendadas e cuidado continuado exclusivo dos moradores adscritos da própria região da UBS (pré-natal, puericultura, hipertensos, diabéticos).
* **30% para Demanda Espontânea / Acolhimento:** Margem operacional destinada a queixas agudas do dia e ao acolhimento de usuários desassistidos fora da sua área de abrangência.

Matematicamente, portanto, uma UBS vizinha $v$ **não pode ceder 100% da sua capacidade** para socorrer uma UBS caída $u$. Sua **Folga Operacional Máxima ($F_v$)** disponível para absorver transbordo externo sem entrar em colapso é:

$$F_v = \max\!\Big(0,\; \min\!\big(0{,}30 \cdot C_v,\; C_v - D_v^0\big)\Big)$$

Se uma UBS vizinha já estiver com alta pressão local (por exemplo, $D_v^0 = 0{,}88 \cdot C_v$), sua folga real não é de 30%, mas de apenas **12%** ($C_v - D_v^0$).

---

### 2.2. A Divisão do Fluxo entre as Vizinhas: Modelo Gravitacional Probabilístico de Huff (1963) e 3SFCA (Wan et al., 2012)
Para calcular qual fração $W_{uv} \in [0, 1]$ da demanda desassistida da UBS $u$ vai para cada UBS vizinha ativa $v \in N_{\text{ativas}}(u)$, utiliza-se a formulação gravitacional de **Huff (1963)** adaptada para competição entre unidades de atenção primária pelo método **3SFCA (*Three-Step Floating Catchment Area*, WAN; ZOU; STERNBERG, 2012)** e revisada sistematicamente por **Stacherl e Sauzet (2023)**:

$$W_{uv} = \frac{C_v^\alpha \cdot d_{\text{topo}}(u, v)^{-\beta}}{\sum_{z \in N_{\text{ativas}}(u)} C_z^\alpha \cdot d_{\text{topo}}(u, z)^{-\beta}}$$

Onde:
* $C_v$: Capacidade instalada (porte) da UBS vizinha $v$;
* $d_{\text{topo}}(u, v)$: Impedância topográfica em km da aresta $(u, v)$ (distância Haversine corrigida pela função de declividade de Tobler, 1993);
* $\alpha = 1{,}0$: Parâmetro de elasticidade da capacidade/atratividade;
* $\beta = 2{,}0$: Coeficiente de decaimento por distância (*distance decay*, padrão gravitacional urbano validado por McGrail, 2012 e Wan et al., 2012).

A quantidade de pacientes transferidos pela aresta $(u, v)$ é então:

$$\Delta D_{u \to v} = D_{\text{transbordo}}(u) \cdot W_{uv}$$

---

### 2.3. Caso Real no Centro de São Paulo (`UBS República` — ID 328, conectada a 4 vizinhas)
Para demonstrar ao professor com **dados reais executados no nosso sistema**, veja o que acontece quando desativamos a **`UBS República` (ID = 328, Zona Centro)**, que possui demanda base $D_{328}^0 = 69.304$ habitantes e está conectada a exatamente **4 UBSs vizinhas**:

| UBS Vizinha Conectada | Distância ($d_{\text{topo}}$) | Capacidade ($C_v$) | Folga Real $\le 30\%$ ($F_v$) | Divisão Ingênua (25% p/ cada) | Colapsa nos 25%? | **Modelo Gravitacional (Huff / 3SFCA)** | **Colapsa no Gravitacional?** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. UBS Humaitá - Dr. João A. Lage** (Bela Vista) | **$0{,}75\text{ km}$** | $60.000$ | $18.000$ vagas | $25{,}0\%$ ($17.326$) | Não | **65,91% ($45.678$ hab.)** | **SIM! (+27.678 exced.)** |
| **2. UBS Sé** (Sé) | **$1{,}21\text{ km}$** | $45.000$ | $13.500$ vagas | $25{,}0\%$ ($17.326$) | Sim | **18,99% ($13.161$ hab.)** | Absorve ($99{,}2\%$ ocup.) |
| **3. UBS Dr. Humberto Pascali** (Santa Cecília) | **$2{,}39\text{ km}$** | $94.000$ | $7.684$ vagas | $25{,}0\%$ ($17.326$) | Sim | **10,08% ($6.986$ hab.)** | Absorve ($99{,}3\%$ ocup.) |
| **4. UBS Dr. Octávio A. Rodovalho** (Bom Retiro) | **$2{,}71\text{ km}$** | $60.000$ | $18.000$ vagas | $25{,}0\%$ ($17.326$) | Não | **5,01% ($3.472$ hab.)** | Absorve ($75{,}8\%$ ocup.) |

**O que esse caso real prova para a banca:**
1. Se usássemos a **divisão ingênua de 25%**, diríamos que a `UBS Humaitá` (a apenas $750\text{ m}$ da República) receberia $17.326$ pacientes e **não colapsaria** (pois tem $18.000$ vagas de folga), enquanto a `UBS Bom Retiro` (a $2{,}71\text{ km}$ de distância) receberia os mesmos $17.326$ pacientes!
2. Com o **Modelo Gravitacional (Huff / 3SFCA)**, a proximidade física de $750\text{ m}$ faz com que **65,91% ($45.678$ pacientes)** caminhem para a `UBS Humaitá`. Ela absorve seus $18.000$ de folga máxima (30%) e **entra em colapso na Camada 1 do BFS**!
3. **Efeito Dominó na Camada 2 do BFS:** Os **$27.678$ pacientes excedentes** que não conseguiram vaga na `UBS Humaitá` seguem pelo grafo na Camada 2 do BFS para a vizinha seguinte na Bela Vista: a **`UBS Armando Darienzo - N. Sra. do Brasil`** (a $0{,}98\text{ km}$), que tinha apenas $10.723$ vagas de folga e **também entra em colapso em cascata**!

---

## 3. Os "Gargalos Invisíveis": Tabela Estática da Gestão vs. Topologia do Grafo (Algoritmo de Tarjan)

Executando o **Algoritmo de Tarjan (1972)** via Busca em Profundidade (DFS) em $\mathcal{O}(|V| + |E|)$ sobre as 454 UBSs e 882 arestas de São Paulo, o sistema detectou **21 Vértices de Articulação** e **19 Pontes Críticas**.

O resultado mais expressivo do trabalho é que **20 dos 21 Vértices de Articulação aparecem como "Verde (Ótimo)" numa tabela isolada comum** (pois operam a cerca de 70% de ocupação local), mas no grafo são **pontos únicos de falha**:

| ID | UBS (Vértice de Articulação - Tarjan) | Distrito / Zona | Status na Tabela Comum (Isolada) | O que acontece no Grafo se ela cair hoje? |
| :---: | :--- | :--- | :---: | :--- |
| **399** | **UBS Jd. Fontalis** | Tremembé (Norte) | **Verde (Ótimo)** | Parte a rede e isola **2 UBSs** periféricas (**129.805 hab.**) na Serra da Cantareira |
| **20** | **UBS Humaitá - Dr. João A. Lage** | Bela Vista (Centro) | **Verde (Ótimo)** | Isola **1 UBS** (**124.777 hab.**) e rompe a ponte central Bela Vista–República |
| **209** | **UBS Jd. Aracati** | Jardim Ângela (Sul) | **Verde (Ótimo)** | Parte o corredor da Guarapiranga e isola **4 UBSs** (**80.453 hab.**) |
| **6** | **UBS Morada do Sol** | Anhanguera (Norte) | **Verde (Ótimo)** | Isola **3 UBSs** (**64.300 hab.** — Pq. Anhanguera, Morro Doce e Jd. Rosinha) |
| **223** | **UBS Vila Calu** | Jardim Ângela (Sul) | **Verde (Ótimo)** | Isola **3 UBSs** (**60.339 hab.**) no fundo do Jardim Ângela |
| **98** | **UBS Jd. Icaraí I (Quintana)** | Cidade Dutra (Sul) | **Verde (Ótimo)** | Isola **1 UBS** (**50.782 hab.** — UBS Dr. Sérgio Chaddad) às margens da Billings |
| **270** | **UBS Colônia** | Parelheiros (Sul) | **Verde (Ótimo)** | Isola **4 UBSs** (**47.549 hab.** — Nova América, Marsilac, Vera Poty e Barragem) |

---

## 4. Referências Acadêmicas Verificadas (ABNT NBR 6023:2018)

1. **BONDY, J. A.; MURTY, U. S. R.** *Graph theory*. New York: Springer, 2008.
2. **BRASIL. Ministério da Saúde.** Secretaria de Atenção à Saúde. Departamento de Atenção Básica. *Acolhimento à demanda espontânea*. Brasília: Ministério da Saúde, 2011. v. 1, 56 p. (Cadernos de Atenção Básica, n. 28).
3. **CRUCITTI, P.; LATORA, V.; MARCHIORI, M.** Model for cascading failures in complex networks. *Physical Review E*, v. 69, n. 4, p. 045104, 2004. DOI: `https://doi.org/10.1103/PhysRevE.69.045104`.
4. **DIJKSTRA, E. W.** A note on two problems in connexion with graphs. *Numerische Mathematik*, v. 1, n. 1, p. 269–271, 1959. DOI: `https://doi.org/10.1007/BF01386390`.
5. **HUFF, D. L.** A probabilistic analysis of shopping center trade areas. *Land Economics*, v. 39, n. 1, p. 81–90, 1963. DOI: `https://doi.org/10.2307/3144521`.
6. **McGRAIL, M. R.** Spatial accessibility of primary health care utilising the two step floating catchment area method: an assessment of recent improvements. *International Journal of Health Geographics*, v. 11, n. 50, p. 1–12, 2012. DOI: `https://doi.org/10.1186/1476-072X-11-50`.
7. **MOTTER, A. E.; LAI, Y.-C.** Cascade-based attacks on complex networks. *Physical Review E*, v. 66, n. 6, p. 065102, 2002. DOI: `https://doi.org/10.1103/PhysRevE.66.065102`.
8. **REZENDE, F. A. V. S.; ALMEIDA, R. M. V. R.; NOBRE, F. F.** Diagramas de Voronoi para a definição de áreas de abrangência de hospitais públicos no Município do Rio de Janeiro. *Cadernos de Saúde Pública*, v. 16, n. 2, p. 467–475, 2000. DOI: `https://doi.org/10.1590/S0102-311X2000000200017`.
9. **STACHERL, B.; SAUZET, O.** Gravity models for potential spatial healthcare access measurement: a systematic methodological review. *International Journal of Health Geographics*, v. 22, n. 34, p. 1–22, 2023. DOI: `https://doi.org/10.1186/s12942-023-00358-z`.
10. **TARJAN, R. E.** Depth-first search and linear graph algorithms. *SIAM Journal on Computing*, v. 1, n. 2, p. 146–160, 1972. DOI: `https://doi.org/10.1137/0201010`.
11. **TOBLER, W.** Three presentations on geographical analysis and modeling: non-isotropic geographic modeling; speculations on the geometry of geography; and global spatial analysis. *Technical Report 93-1*, National Center for Geographic Information and Analysis (NCGIA), University of California, Santa Barbara, 1993.
12. **WAN, N.; ZOU, B.; STERNBERG, T.** A three-step floating catchment area method for analyzing spatial access to health services. *International Journal of Geographical Information Science*, v. 26, n. 6, p. 1073–1089, 2012. DOI: `https://doi.org/10.1080/13658816.2011.624987`.
13. **WANG, J.-W.; RONG, L.-L.; ZHANG, L.; ZHANG, Z.** Attack vulnerability of scale-free networks due to cascading failures. *Physica A: Statistical Mechanics and its Applications*, v. 387, n. 26, p. 6671–6678, 2008. DOI: `https://doi.org/10.1016/j.physa.2008.08.037`.

