UNIVERSIDADE PRESBITERIANA MACKENZIE
FACULDADE DE COMPUTAÇÃO E INFORMÁTICA
CURSO DE CIÊNCIA DA COMPUTAÇÃO / SISTEMAS DE INFORMAÇÃO

---

LUCAS FERNANDES DE CAMARGO
LENDY NAIARA CARPIO PACHECO
ANNA LUIZA STELLA SANTOS

---

# REDE DE ACESSO SP: MODELAGEM TERRITORIAL DE UNIDADES BÁSICAS DE SAÚDE COMO GRAFOS PONDERADOS PARA OTIMIZAÇÃO DE DEMANDA NÃO AGENDADA

---

São Paulo
2026

---

## RESUMO

A busca por atendimento na rede de atenção básica municipal de São Paulo, o maior sistema de saúde pública da América Latina, enfrenta um estrangulamento agudo oriundo da distribuição assimétrica populacional urbana. O presente trabalho investiga e propõe um modelo matemático-computacional concebido para a otimização da distribuição da demanda não agendada em Unidades Básicas de Saúde (UBSs), utilizando preceitos da Teoria dos Grafos para superar as patentes limitações de sistemas tradicionais de recomendação, os quais fundamentam-se unicamente em lógicas de proximidade geográfica euclidiana ou viária. Diferindo-se das plataformas comerciais de roteamento e de mapas governamentais que ignoram o nível de saturação do destino, o sistema arquitetado modela a infraestrutura da metrópole paulistana (englobando cerca de 470 UBSs) como um grafo não orientado esparso duplo-ponderado $G = (V, E, w_v, w_e)$. Nesta abstração, os vértices ($V$) representam postos de atendimento validados pelo Cadastro Nacional de Estabelecimentos de Saúde (CNES), enquanto as arestas ($E$) traduzem a viabilidade topológica e o custo do deslocamento (em quilômetros) entre unidades limítrofes. A inovação estrutural desta pesquisa repousa primordialmente na introdução da função de peso dos vértices ($w_v$), derivada de um complexo cruzamento espacial (Pipeline ETL) entre bases censitárias do IBGE (Censo Demográfico 2022) e coordenadas do sistema GeoSampa. O peso $w_v$ reflete a pressão populacional exata concentrada na Área de Abrangência (AAUBS) de cada posto. A partir deste arranjo, o algoritmo de caminho mínimo de Dijkstra, operado sobre estruturas de *Min-Heap* para garantir complexidade assintótica $\mathcal{O}((|V| + |E|) \log |V|)$, foi adaptado para identificar rotas que promovam o alívio territorial. O modelo identifica alternativas viáveis de menor demanda habitacional, desviando o fluxo do estrangulamento. A análise topológica resultante revelou discrepâncias substanciais, com densidade de rede extremamente esparsa ($0,0865$), e expôs fenômenos onde unidades centrais suportam pressões de até $80.000$ habitantes, contrastando com zonas limítrofes que operam sob demanda dez vezes inferior. Os testes computacionais executados sob condições simuladas extremas (acima de $100.000$ requisições sintéticas simultâneas) atestam uma latência de processamento percentil-95 ($p95$) na casa de $115$ milissegundos, solidificando a premissa de que o desvio marginal induzido pelo algoritmo viabiliza uma redução considerável na fila teórica enfrentada pelo cidadão sem comprometer a estabilidade do servidor em escala municipal. Conclui-se, destarte, que a adoção de grafos ponderados territorialmente devolve a transparência logística ao usuário final do Sistema Único de Saúde, instrumentalizando um acesso equânime.

**Palavras-chave:** Teoria dos Grafos. Saúde Pública. Algoritmo de Dijkstra. Balanceamento de Carga Territorial. OpenStreetMap.

---

## ABSTRACT

The search for care in the municipal primary healthcare network of São Paulo, the largest public health system in Latin America, faces an acute bottleneck originating from asymmetric urban population distribution. The present work investigates and proposes a mathematical-computational model conceived for the optimization of unscheduled demand distribution in Basic Health Units (UBSs), using principles of Graph Theory to overcome the patent limitations of traditional recommendation systems, which are based solely on logic of Euclidean or road geographic proximity. Differing from commercial routing platforms and government maps that ignore the saturation level of the destination, the architected system models the infrastructure of the São Paulo metropolis (encompassing about 470 UBSs) as a double-weighted sparse undirected graph $G = (V, E, w_v, w_e)$. In this abstraction, the vertices ($V$) represent care centers validated by the National Registry of Health Establishments (CNES), while the edges ($E$) translate the topological viability and the travel cost (in kilometers) between bordering units. The structural innovation of this research rests primarily on the introduction of the vertex weight function ($w_v$), derived from a complex spatial cross-referencing (ETL Pipeline) between census databases from IBGE (2022 Demographic Census) and coordinates from the GeoSampa system. The weight $w_v$ reflects the exact population pressure concentrated in the Catchment Area (AAUBS) of each center. From this arrangement, Dijkstra's shortest path algorithm, operated on *Min-Heap* structures to ensure asymptotic complexity $\mathcal{O}((|V| + |E|) \log |V|)$, was adapted to identify routes that promote territorial relief. The model identifies viable alternatives with lower housing demand, diverting flow away from bottlenecks. The resulting topological analysis revealed substantial discrepancies, with an extremely sparse network density ($0.0865$), and exposed phenomena where central units support pressures of up to $80,000$ inhabitants, contrasting with bordering zones operating under ten times lower demand. Computational tests executed under extreme simulated conditions (over $100,000$ simultaneous synthetic requests) attest to a 95th-percentile processing latency ($p95$) of around $115$ milliseconds, solidifying the premise that the marginal deviation induced by the algorithm enables a considerable reduction in the theoretical queue faced by the citizen without compromising server stability on a municipal scale. It is concluded, therefore, that the adoption of territorially weighted graphs returns logistical transparency to the end user of the Unified Health System, instrumentalizing equitable access.

**Keywords:** Graph Theory. Public Health. Dijkstra's Algorithm. Territorial Load Balancing. OpenStreetMap.

---

## LISTA DE SIGLAS E ABREVIATURAS

**AAUBS** - Área de Abrangência de Unidade Básica de Saúde
**BFS** - Busca em Largura (*Breadth-First Search*)
**CEINFO** - Coordenação de Epidemiologia e Informação
**CNES** - Cadastro Nacional de Estabelecimentos de Saúde
**ETL** - *Extract, Transform, Load* (Extração, Transformação e Carga)
**GIS** - *Geographic Information System* (Sistema de Informação Geográfica)
**IBGE** - Instituto Brasileiro de Geografia e Estatística
**IoT** - Internet das Coisas (*Internet of Things*)
**ODS** - Objetivos de Desenvolvimento Sustentável
**RSL** - Revisão Sistemática da Literatura
**SMS-SP** - Secretaria Municipal da Saúde de São Paulo
**SUS** - Sistema Único de Saúde
**UBS** - Unidade Básica de Saúde
**WFLP** - *Weighted Facility Location Problem*

---

## SUMÁRIO

1. INTRODUÇÃO
   1.1. Contextualização
   1.2. O Problema de Pesquisa
   1.3. Hipótese
   1.4. Justificativa Científica e Impacto Social (ODS)
   1.5. Objetivos
2. REFERENCIAL TEÓRICO E REVISÃO DA LITERATURA
3. FORMALIZAÇÃO MATEMÁTICA E TOPOLOGIA DE GRAFOS
4. METODOLOGIA E PIPELINE DE ENGENHARIA DE DADOS
5. ANÁLISE ALGORÍTMICA E COMPLEXIDADE COMPUTACIONAL
6. RESULTADOS, ESCALABILIDADE E VALIDAÇÃO DA HIPÓTESE
7. CONCLUSÃO E TRABALHOS FUTUROS
REFERÊNCIAS BIBLIOGRÁFICAS
