# 5. ANÁLISE ALGORÍTMICA E COMPLEXIDADE COMPUTACIONAL

Modelado o pipeline censitário nos grafos matemáticos, a eficácia do sistema condensa-se no bloco algorítmico responsável pela travessia espacial. O objetivo deste capítulo é comprovar as decisões de arquitetura computacional adotadas no núcleo de buscas, aferindo ciclomática e limites assintóticos do modelo.

## 5.1 Travessia Cega e o Uso Instrumental da BFS

Em avaliações de sanidade topológica, o núcleo foi submetido a varreduras não ponderadas utilizando *Breadth-First Search* (Busca em Largura). 
O escopo principal da BFS não é oferecer rotas para cidadãos, mas auditar o grau separação do modelo.

$$ \text{Complexidade (BFS)} = O(|V| + |E|) $$

Rodando no limite base do problema (origem na *UBS HUMAITÁ* e origem na *UBS MAX PERLMAN*), a transversal BFS validou a conectividade unida (um único bloco conexo) atestando que a rede atinge a integralidade de todos os 71 postos monitorados com tolerância variável de apenas **8 a 12 saltos (níveis de vizinhança lógicos)**. Essa prova de alcance confirma que a ausência de gargalos crônicos topológicos — a malha não é bipartida nem despedaçada internamente. Contudo, em virtude da BFS tratar saltos como custos idênticos independentemente de serem quarteirões ou rodovias, seu papel limitou-se ao rastreio de suporte no ambiente de produção.

## 5.2 O Núcleo Restrito do Algoritmo de Dijkstra

A função de recomendação impõe o cálculo progressivo de distância agregada $w_e$ sobre a lista de adjacência, exigindo o rigor incontornável do **Algoritmo de Dijkstra**. Devido à ausência de arestas de penalidade negativa (distâncias estritamente $\ge 0$), ele assegura a completude do Caminho Mínimo e o ranqueamento ótimo de k-candidatos dentro de raios de restrição.

A implementação clássica disciplinar da literatura ($O(|V|^2)$), operando arrays brutos não ordenados para extração do vértice mínimo a cada ciclo, falharia categoricamente nos testes de web concorrência em instâncias *Cloud*.

**Otimização Estrutural via Min-Heap**
Para esmagar o vetor tempo, injetou-se o suporte das Filas de Prioridade (Heaps Binários), utilizando as rotinas de baixo nível `heapq` nativas da linguagem. O relaxamento progressivo das arestas ($u \rightarrow v$) insere o vizinho no heap acarretando custo algorítmico marginal de reorganização de árvore logarítmica.

$$ \text{Complexidade de Tempo Assintótica} = \mathcal{O}\Big((|V| + |E|) \log |V|\Big) $$

Nesta topologia específica paulistana, a densidade é radicalmente suprimida ($D=0,0865$). Isso implica que o número de arestas ($|E|$) escala linearmente para malhas da periferia, evitando o fatídico quadrado dos nós. Em um hipotético arranjo onde a totalidade das cerca de 470 Unidades fossem absorvidas pelo grafo, e o grau médio subisse para 10 conexões por nó, teríamos as restrições $|V|=470$ e $|E|=4.700$. No pior caso de tráfego profundo, a complexidade iteraria em pouco mais que $5.170 \times 8.87 \approx 45.890$ verificações em loop. Essa quantia, para processadores *multicore* contemporâneos, é tratada como um ruído basal da CPU, viabilizando a paralelização infinita para dezenas de milhares de usuários.

## 5.3 O Mecanismo de Ranqueamento Ponderado

A complexidade de recomendação não cessa ao descobrir a rota mínima. A sub-rotina aciona um filtro duplo:
1.  **Envelopamento Radial:** Ao extrair os caminhos de Dijkstra, a aplicação amputa impiedosamente qualquer vértice onde a rota excede um raio viável aceitável (ex. $R_{max} = 6 km$, re-expandindo a $12 km$ caso seja retornado conjunto nulo de $Candidatos=\emptyset$).
2.  **Subversão Ordenada da Lotação:** Para o arranjo enclausurado em $R_{max}$, as UBSs candidatas sofrem *sort* (ordenação) não por distância, mas ordenando o array ascendente utilizando a matriz censitária $w_v$. O Algoritmo Timsort inerente ao núcleo (com $\mathcal{O}(N \log N)$ em que $N$ é minúsculo devido à poda do raio) ranqueia os postos de saúde empurrando a lotação infernal para o final da fila de sugestão.

### 5.3.1 Avaliação Ciclomática
Para garantir a sanidade técnica, a complexidade ciclomática de McCabe, responsável pelo fluxo de controle do bloco de recomendação, fixou-se em singelos **5 graus (5 nós de bifurcação do controle)**: O laço principal `while` do Heap; o laço `for` inerente à leitura das arestas vizinhas; uma condicional de descarte geométrico do raio ($> R_{max}$); a condicional de relaxamento estrito do custo; e o bloco *catch* nulo. A parcimônia lógica assegura a testabilidade massiva do código sem falsos positivos.
