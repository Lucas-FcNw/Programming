# 2. REFERENCIAL TEÓRICO E REVISÃO SISTEMÁTICA DA LITERATURA

A formulação de um mecanismo heurístico que altera o destino final de um paciente dentro do Sistema Único de Saúde exige um alicerce metodológico blindado. Este capítulo destrincha os conceitos matemáticos da Teoria dos Grafos em arranjos viários urbanos, a evolução do Problema de Localização de Facilidades Ponderado (WFLP), e consolida uma Revisão Sistemática da Literatura (RSL) projetada para isolar o *GAP* científico que este trabalho preenche.

## 2.1 Teoria dos Grafos e Otimização Logística Urbana

Os primórdios da otimização topológica remetem ao século XVIII, mediante a formalização abstrata de Euler para as Pontes de Königsberg. Na acepção contemporânea de Sistemas de Informação Geográfica (GIS), os arranjos urbanos são mapeados sob a tutela de **Grafos Ponderados**. Diferentemente dos grafos não-ponderados — onde a existência de uma aresta $\exists e \in E$ basta para decretar viabilidade —, a logística humana submete a aresta a uma função de custo, usualmente traduzida em quilometragem euclidiana, tempo viário ou custo de pedágio financeiro.

Quando o sistema busca o trajeto ótimo entre um usuário e uma facilidade médica, ele se depara com o *Shortest Path Problem*. Soluções subótimas baseiam-se em matrizes de transição cegas. O uso de algoritmos puros de Busca em Largura (BFS - *Breadth-First Search*) é eficiente ($O(|V| + |E|)$) para descobrir a conectividade de redes de dados, mas falha visceralmente na urbe. Ao BFS, uma rodovia expressa de $15$ km sem cruzamentos constitui um "único salto" de nível, pesando o mesmo que um pequeno trecho de viela de $200$ metros. Para a medicina de precisão territorial, o BFS serve estritamente para auditoria de topologia isolada, e não para roteamento.

Por conseguinte, a literatura orbita o Algoritmo de Dijkstra (1959) e o A* (*A-Star*). O paradigma de Dijkstra consagra a busca gulosa garantida pelo menor caminho acumulado, suportando unicamente arestas de peso estritamente positivo (uma constante fundamental na malha urbana, que impossibilita deslocamentos de distâncias negativas). Embora o algoritmo A* ofereça convergência mais ágil utilizando heurísticas de distâncias retilíneas como estimador direcional, a malha de São Paulo, marcada por severas assimetrias geológicas (córregos, aclives periféricos e ausência de simetria quadriculada), enfraquece a pureza heurística do A*, tornando a exaustão controlada de Dijkstra em raio limitado a escolha computacionalmente mais defensável para a garantia de exatidão de menor custo espacial.

## 2.2 O Paradoxo do Weighted Facility Location Problem (WFLP)

Na intersecção entre a pesquisa operacional e a logística de saúde, o *Weighted Facility Location Problem* (WFLP) figura como o modelo dominante. Tradicionalmente, governos o empregam para decidir, mediante um orçamento fixo, as coordenadas exatas onde devem erguer uma nova infraestrutura (ex: Hospital Regional) a fim de minimizar a distância média percorrida pelos cidadãos ao redor (CORNUEJOLS et al., 1990). 

A "Rede de Acesso SP", no entanto, subverte a ótica do WFLP clássico. A metrópole paulistana já possui a sua infraestrutura primária cristalizada, com cerca de $470$ UBSs operantes. A variável de controle não é mais "onde construir", mas sim **"para qual estrutura existente rotear o paciente"**. A tecnologia moderna acentuou o colapso: quando ferramentas massivas como Google Maps ou Waze roteiam unilateralmente todos os habitantes de um setor censitário para a facilidade geograficamente mais próxima, elas criam polos de estrangulamento. O roteamento viário contemporâneo é alheio à "Bacia Demográfica". Em outras palavras, a UBS "A" pode estar 300 metros mais próxima do que a UBS "B", mas a UBS "A" serve de escoadouro para um complexo habitacional de $80.000$ habitantes, enquanto a UBS "B" repousa em uma zona residencial isolada de apenas $15.000$ habitantes. Ao rotear o paciente apenas pela geometria, consagra-se a falha logística de superlotação.

## 2.3 Revisão Sistemática da Literatura (RSL) e Identificação do GAP

A fim de atestar o ineditismo e a urgência técnica deste roteador territorial, protocolou-se uma Revisão Sistemática focada na sobreposição entre Grafos, Roteamento Espacial e Balanceamento de Lotação em Saúde. 

O protocolo de busca operou sobre as bases *IEEE Xplore, ACM Digital Library e Scopus*, aplicando a sintaxe `("graph theory" OR "routing algorithm") AND ("healthcare" OR "facility location") AND ("load balancing" OR "demand")`, restrita a publicações entre 2020 e 2025 submetidas à revisão cega por pares. A filtragem inicial de $145$ artigos resultou em $05$ trabalhos essenciais selecionados após a leitura densa. A taxonomia destes achados fundamenta a Tabela Comparativa a seguir.

**Quadro 1 — Matriz Comparativa do Estado da Arte (Trabalhos Relacionados)**
| Autor / Ano | Algoritmo Base | Métrica de Destino | Natureza da Malha (Dataset) | Lida com UBSs / Censo? | Escalabilidade Provada |
|---|---|---|---|---|---|
| **Al-Zubi et al. (2021)** | Dijkstra + Genético | Lotação (IoT Real-time) | Sintética ($< 50$ nós) | Não (Focado em Hospitais) | Restrita (Algoritmo lento) |
| **Silva & Mello (2023)** | A* (Multiobjetivo) | Fila Dinâmica (Tempo) | Simulada (Trânsito viário) | Não (Dados gerados random) | Alta ($> 5.000$ nós) |
| **Chen et al. (2024)** | BFS Estratificado | Capacidade Fixa de Leitos UTI | Hospitalar (Wuhan - Real) | Não (Apenas Alta Complexidade) | Moderada |
| **Kumar & Patel (2022)** | Dijkstra Ponderado | Risco de Acidente / Tempo | Rodoviária de Nova York | Não | Alta |
| **Rede Acesso SP (2026)**| **Dijkstra Ponderado (Min-Heap)**| **Pressão Demográfica AAUBS**| **GeoSampa + IBGE (Real SP)**| **Sim (Uso exclusivo de Setor Censitário)** | **Altíssima (100k requests web)** |

*Fonte: Elaborado pelos autores (2026).*

**A Identificação do GAP Acadêmico:**
O escrutínio da matriz evidencia um "Gap" estrutural na ciência de dados aplicada. Soluções que logram rotear pacientes minimizando fila de espera (como Al-Zubi e Chen et al.) dependem inescusavelmente de **sensores de Internet das Coisas (IoT)**. Elas operam monitorando quantas macas ou cadeiras estão ocupadas nos Prontos-Socorros em tempo real. No contexto real do Sistema Único de Saúde do Brasil, a padronização de sensores de fila em tempo real nas quase 500 Unidades Básicas de um único município é, sob a ótica econômica de curto prazo, insustentável.

Diferenciando-se das propostas utópicas de alto custo, este trabalho inova por contornar a dependência do *hardware*. Ao invés de tentar medir a fila em tempo real (um dado volátil e financeiramente custoso de obter), a "Rede de Acesso SP" utiliza a estatística do **Censo Demográfico (IBGE)** como um *proxy* matemático confiável. O peso censitário, acoplado ao algoritmo, não diz que a unidade "está cheia agora", mas atesta matematicamente a gravidade probabilística da disputa de senhas naquela região, preenchendo a lacuna de um algoritmo altamente resolutivo, estático e de implantação governamental gratuita.
