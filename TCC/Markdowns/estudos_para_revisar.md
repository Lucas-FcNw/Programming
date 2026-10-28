# Estudos Auditados e Verificados — SPGraph (Fragilidade Topológica e Efeito Cascata em UBSs)

Todas as referências abaixo foram verificadas por DOI e auditoria de escopo. As quatro entradas não verificáveis anteriormente presentes no `.bib` (`alzubi2021load`, `silva2023astar`, `chen2024bfs`, `kumar2022dijkstra`) foram **removidas definitivamente** em conformidade com a Regra R1.

---

## 1. Movimento da População e Redistribuição Gravitacional entre UBSs Vizinhas

- [x] **Huff (1963)** — *A probabilistic analysis of shopping center trade areas.* Land Economics, 39(1), 81–90. https://doi.org/10.2307/3144521
  - **O que sustenta:** Formulação probabilística clássica na qual a fração de usuários que se desloca da origem $u$ para o serviço $v$ é proporcional à capacidade/atratividade $C_v^\alpha$ e inversamente proporcional à distância $d_{uv}^\beta$.
- [x] **Wan, Zou & Sternberg (2012)** — *A three-step floating catchment area method for analyzing spatial access to health services.* International Journal of Geographical Information Science, 26(6), 1073–1089. https://doi.org/10.1080/13658816.2011.624987
  - **O que sustenta:** Adapta o peso gravitacional de seleção ($G_{ij}$ / $W_{uv}$) especificamente para **unidades de saúde concorrentes**, demonstrando como a demanda populacional se divide entre clínicas vizinhas segundo a impedância de deslocamento.
- [x] **Stacherl & Sauzet (2023)** — *Gravity models for potential spatial healthcare access measurement: a systematic methodological review.* International Journal of Health Geographics, 22(34), 1–22. https://doi.org/10.1186/s12942-023-00358-z
  - **O que sustenta:** Revisão sistemática PRISMA de 309 estudos empíricos em saúde; comprova que modelos gravitacionais com decaimento por distância integram disponibilidade (capacidade) e acessibilidade (proximidade). PDF disponível em `TCC/PDFs/spatial_healthcare_access.pdf`.
- [x] **McGrail (2012)** — *Spatial accessibility of primary health care utilising the two step floating catchment area method: an assessment of recent improvements.* International Journal of Health Geographics, 11(50), 1–12. https://doi.org/10.1186/1476-072X-11-50
  - **O que sustenta:** Avalia funções de decaimento por distância (*distance decay*) em Atenção Primária à Saúde (APS) em regiões metropolitanas. PDF disponível em `TCC/PDFs/Spatial accessibility.pdf`.

---

## 2. Efeito Cascata (Dominó) por Sobrecarga de Capacidade e Regra 70/30 do SUS

- [x] **Brasil — Ministério da Saúde (2011)** — *Acolhimento à demanda espontânea.* Cadernos de Atenção Básica, n. 28, Vol. I, 56 p.
  - **O que sustenta:** Diretriz operacional de rotina da Atenção Básica no SUS, equilibrando a agenda entre Demanda Programada da população adscrita (~70%) e margem de Acolhimento à Demanda Espontânea (~30%).
- [x] **Motter & Lai (2002)** — *Cascade-based attacks on complex networks.* Physical Review E, 66(6), 065102. https://doi.org/10.1103/PhysRevE.66.065102
  - **O que sustenta:** Modelo seminal de falha em cascata em grafos onde cada vértice possui capacidade máxima $C_v = (1 + \alpha) L_v^0$; a queda de um nó redistribui carga e provoca colapsos sucessivos quando a nova carga supera $C_v$.
- [x] **Crucitti, Latora & Marchiori (2004)** — *Model for cascading failures in complex networks.* Physical Review E, 69(4), 045104. https://doi.org/10.1103/PhysRevE.69.045104
  - **O que sustenta:** Dinâmica passo a passo (em camadas) da propagação de sobrecarga e degradação da eficiência da rede.
- [x] **Wang, Rong, Zhang & Zhang (2008)** — *Attack vulnerability of scale-free networks due to cascading failures.* Physica A, 387(26), 6671–6678. https://doi.org/10.1016/j.physa.2008.08.037
  - **O que sustenta:** Regra de **redistribuição local preferencial de carga** (*local preferential load redistribution*): quando um vértice falha, sua demanda é transferida diretamente para seus vizinhos imediatos no grafo proporcionalmente à capacidade de cada vizinho.

---

## 3. Gargalos Topológicos Invisíveis, Voronoi e Impedância Topográfica

- [x] **Tarjan (1972)** — *Depth-first search and linear graph algorithms.* SIAM J. Comput., 1(2), 146–160. https://doi.org/10.1137/0201010
  - **O que sustenta:** Algoritmo linear $\mathcal{O}(|V| + |E|)$ baseado em DFS (`disc` e `low`) para detecção exata de vértices de articulação e pontes críticas.
- [x] **Rezende, Almeida & Nobre (2000)** — *Diagramas de Voronoi para a definição de áreas de abrangência de hospitais públicos no Município do Rio de Janeiro.* Cadernos de Saúde Pública, 16(2), 467–475. https://doi.org/10.1590/S0102-311X2000000200017
  - **O que sustenta:** Tesselação espacial de Voronoi para estimativa de áreas de abrangência e demanda adscrita de unidades públicas de saúde no Brasil.
- [x] **Tobler (1993)** — *Three presentations on geographical analysis and modeling.* Technical Report 93-1, NCGIA.
  - **O que sustenta:** *Tobler's Hiking Function* para ajuste da impedância de caminhada/deslocamento em função da declividade topográfica ($s = \Delta h / \Delta x$).
