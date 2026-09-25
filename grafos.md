Rede de Acesso SP

Relatório Técnico - Teoria dos
Grafos

Projeto: Rede de Acesso SP - Saúde Territorial em São Paulo
Tema: Modelagem de UBSs como grafo ponderado para análise de
acesso territorial
Instituição: Universidade Presbiteriana Mackenzie
Faculdade: Faculdade de Computação e Informática
Professor: Prof. Dr. Ivan Carlos Alcântara de Oliveira
Disciplina: Teoria dos Grafos - Turma: 6G
Integrantes: Lucas Fernandes de Camargo, Lendy Naiara Carpio
Pacheco e Anna Luiza Stella Santos

Membros do Projeto

Integrante

Lucas Fernandes de Camargo

Lendy Naiara Carpio Pacheco

Anna Luiza Stella Santos

RA

10419400

10428525

10417401

Links de Entrega

Recurso

Link

Sistema publicado

Rede de Acesso SP - Streamlit

Repositório do projeto

Lucas-FcNw/rede-de-acesso-sp

Vídeo público de apresentação

https://youtu.be/6LAj96dURXc

1. Introdução

A Rede de Acesso SP modela parte da rede de Unidades Básicas de
Saúde (UBSs) do município de São Paulo por meio de um grafo pon-
derado. A proposta é representar UBSs como vértices, conexões terri-
toriais como arestas e utilizar pesos para apoiar análises de acessibili-
dade, pressão populacional e recomendação de unidades com maior
chance relativa de atendimento rápido.

A motivação central do projeto é transformar um problema urbano re-
al em uma estrutura matemática manipulável por algoritmos de
grafos. Em vez de recomendar apenas a UBS mais próxima em linha
reta, o sistema considera um conjunto de UBSs próximas e compara a
pressão populacional associada a cada unidade. Assim, o grafo serve
como base para tomada de decisão dentro de um recorte territorial.

1.1 Problema Real e Situação de Uso

No município de São Paulo, uma pessoa que procura atendimento
básico pode estar próxima de mais de uma UBS. Uma busca orientada
apenas por distância identifica a unidade geometricamente mais per-
to, mas não diferencia territórios atendidos por populações potencial-
mente muito distintas. Para o usuário, isso significa que a alternativa
mais curta não é necessariamente a que apresenta menor demanda
territorial relativa.

O sistema estuda essa situação com dados reais de UBSs e respecti-
vas Áreas de Abrangência (AAUBS). O usuário informa um endereço;
a aplicação restringe a comparação a unidades localizadas em um
raio viável, inicialmente 6 km, expansível até 12 km quando existem
poucas opções, e recomenda a candidata cuja AAUBS possui menor

população residente estimada. Assim, a distância preserva a viabili-
dade do deslocamento e o peso populacional oferece um critério com-
parativo de demanda potencial.

O projeto não informa fila, lotação ou tempo de espera em tempo real.
O indicador ideal incluiria capacidade ou número de equipes por
UBS, mas esse conjunto completo não foi identificado em fonte públi-
ca reprodutível para as unidades analisadas. Essa limitação é declara-
da para impedir que uma estimativa territorial seja interpretada como
garantia operacional.

1.2 Objetivos

O objetivo geral é aplicar Teoria dos Grafos para apoiar a análise de
acesso territorial a UBSs, oferecendo uma recomendação local que
considere distância e demanda territorial potencial.

Os objetivos específicos são:

• modelar UBSs reais como vértices e relações de proximidade co-

mo arestas;

• utilizar pesos nos vértices e nas arestas para representar AAUBS e

distância;

• implementar caminho mínimo com Dijkstra e investigações estru-

turais da rede;

• apresentar os resultados em uma aplicação interativa e em um

menu textual verificável;

• documentar fontes, limitações e resultados de modo reprodutível.

1.3 Objetivos de Desenvolvimento Sustentável

ODS rela-
cionada

Contribuição
do projeto

Justificativa

ODS 3 - Saúde
e Bem-Estar

Apoio informa-
cional para aces-
so a serviços de
atenção básica.

A aplicação organiza UBSs
reais e permite localizar alter-
nativas próximas, oferecendo
informação territorial útil para
o acesso à saúde primária.

ODS 10 - Re-
dução das De-
sigualdades

Evidencia difer-
enças territoriais
de demanda po-
tencial entre

A comparação de população
por AAUBS permite observar
desigualdade espacial na dis-
tribuição da pressão estimada

ODS rela-
cionada

Contribuição
do projeto

Justificativa

áreas de
abrangência.

sobre serviços públicos.

O sistema não resolve isoladamente desigualdades de oferta de
saúde, mas fornece uma representação computacional transparente
para analisar o problema e apoiar discussões de acesso territorial.

2. Modelo Matemático do Grafo

O grafo utilizado pode ser definido formalmente como:

G = (V, E, wV, wE)

Onde:

• V é o conjunto de vértices, representando UBSs.
• E é o conjunto de arestas, representando conexões de proximidade

geográfica entre UBSs.

• wV: V -> R+ é a função de peso dos vértices.
• wE: E -> R+ é a função de peso das arestas.

No arquivo grafo.txt, o tipo do grafo é 3. Pela implementação em
projeto_grafo_menu.py, isso significa:

• grafo não orientado;
• vértices ponderados;
• arestas ponderadas.

Portanto, para qualquer aresta {u, v} pertencente a E, a conexão é
bidirecional:

(u, v) equivale a (v, u)

Isso é coerente com a interpretação territorial, pois a proximidade en-
tre duas UBSs não depende de direção.

2.1 Modelagem Visual do Grafo

A modelagem visual abaixo sintetiza a conversão do problema real
para a estrutura de grafo ponderado utilizada pelo sistema:

Endereço
informado

localização

UBSs candidatas

raio inicial: 6 km

expansão até 12 km

G = (V, E, wV, wE)

vértices e arestas ponderados

UBS A

wE: km

UBS B

wV: população

wV: população

km

km

UBS C

wV: população

AAUBS: área de abrangência

Ranking

menor pressão

territorial

UBS
recomendada

rota no mapa

Diagrama A - Modelagem da recomendação. O endereço delimita as
UBSs candidatas; o grafo registra pesos territoriais e distâncias; a re-
comendação destaca a menor pressão estimada no raio viável.

Na representação:

• cada círculo representa um vértice v pertencente a V, isto é, uma

UBS real;

• o peso interno do vértice, wV(v), corresponde à população resi-

dente estimada na área de abrangência da UBS (AAUBS);

• cada linha representa uma aresta não direcionada {u, v}

pertencente a E;

• o peso da aresta, wE(u, v), corresponde a distância aproximada en-

tre as UBSs;

• o endereço do usuário não é um vértice permanente do grafo: ele

é um ponto de consulta usado para delimitar candidatas próximas;

• a recomendação utiliza o recorte geográfico e escolhe, entre as

UBSs viáveis, a de menor pressão relativa.

2.2 Exemplo Visual de um Subgrafo Real

O trecho abaixo utiliza vértices e arestas presentes no arquivo
grafo.txt. Ele demonstra como as UBSs centrais próximas se conec-
tam por distância:

1 - HUMAITA-UBS

DR. JOAO AZEVEDO LAGE

AAUBS: 39.373 pessoas

2,35 km

2 - CAMBUCI-UBS

AAUBS: 79.792 pessoas

0,75 km

1,54 km

2,72 km

2,12 km

3 - REPUBLICA - UBS

AAUBS: 52.057 pessoas

1,21 km

4 - SE - NASF/UBS

AAUBS: 49.150 pessoas

Diagrama B - Subgrafo real da região central. Os vértices correspon-
dem a UBSs efetivamente presentes nos dados, e as arestas registram suas
distâncias aproximadas.

Esse subgrafo evidencia que duas informações distintas coexistem na
modelagem: a população estimada na área de abrangência de cada
unidade aparece como peso de vértice, enquanto a proximidade espa-
cial entre unidades aparece como peso de aresta.

2.3 Visualização do Grafo Completo Modelado

A figura a seguir foi gerada a partir dos arquivos finais data/
ubs_vertices.json e data/adjacencias.json. Ela representa todos os vér-
tices e arestas do modelo, usando a localização geográfica das UBSs
para o posicionamento visual e a população estimada da AAUBS para
a cor dos vértices.

Figura 1 - Grafo completo da Rede de Acesso SP. Os pontos represen-
tam UBSs, as linhas representam arestas de proximidade e a escala de cor
representa o peso do vértice. A figura cumpre o papel de modelagem visual
do grafo em software de visualização equivalente, mantendo rastreabili-
dade direta com os arquivos executados pela aplicação.

3. Estrutura dos Vértices

Cada vértice representa uma UBS selecionada no recorte do projeto.

No arquivo grafo.txt, cada vértice segue o formato:

id "nome_da_ubs" peso_do_vertice

Exemplo:

12 "PARI - UBS" 18498.00

Neste projeto, o peso do vértice representa a população residente es-
timada na Área de Abrangência da UBS (AAUBS). O valor é asso-
ciado a cada vértice pelo código CNES da unidade, usando a base
pública da SMS-SP/CEInfo organizada a partir do Censo Demográfico
de 2022/IBGE para a versão preliminar AAUBS 2025.

Essa opção substitui o modelo inicial baseado em população distrital,
pois uma UBS é responsável por um território de abrangência especí-
fico e não necessariamente por todo o distrito onde seu endereço se
encontra.

Interpretação do Peso do Vértice

O peso wV(v) pode ser entendido como:

wV(v) = populacao_residente_estimada_na_AAUBS(v)

Essa escolha é importante porque o objetivo do sistema não é apenas
encontrar a UBS geometricamente mais próxima, mas estimar qual
UBS próxima atende um território potencialmente menos populoso.

No recorte final:

• Total de vértices: 71
• Menor peso de vértice: 8919, na WALTER ELIAS,DR- CASA VERDE BAIXA

UBS

• Maior peso de vértice: 79792, na CAMBUCI-UBS
• Peso médio dos vértices: 35759.5
• Mediana dos pesos dos vértices: 31547
• Soma dos pesos dos vértices: 2538925

Limite do Peso Utilizado

O indicador teoricamente mais completo seria:

pressao_ideal(v) = populacao_adscrita(v) /
capacidade_ou_numero_de_equipes(v)

A pesquisa nas fontes oficiais identificou que a SMS-SP disponibiliza
publicamente população residente estimada por AAUBS. Entretanto,
o Documento Norteador do NUVIS-AB informa que dados de popu-
lação cadastrada por equipe e por UBS estão em sistemas de acesso

restrito, como BI de Cadastros do e-SUS e Radar Saúde. Assim, não
foi possível obter, de forma pública e reprodutível, a capacidade ou
número de equipes das 71 UBSs.

Consequentemente, o modelo implementado utiliza:

pressao_estimada(v) = populacao_residente_estimada_na_AAUBS(v)

Essa métrica assume capacidades comparáveis entre UBSs candi-
datas e indica demanda territorial potencial, não fila real, ocu-
pação atual ou garantia de menor tempo de atendimento.

4. Estrutura das Arestas

Cada aresta representa uma conexão de proximidade entre duas UB-
Ss. Como o grafo é não orientado, a aresta indica que as UBSs estão
relacionadas territorialmente, sem sentido único de deslocamento.

No arquivo grafo.txt, cada aresta segue o formato:

id_origem id_destino peso_da_aresta

Exemplo:

1 3 0.75

Neste caso, existe uma conexão entre os vértices 1 e 3, com peso 0.75.

Interpretação do Peso da Aresta

O peso da aresta representa a distância aproximada em quilômetros
entre duas UBSs:

wE(u, v) = distancia_km(u, v)

Essa distância é utilizada nos algoritmos de caminho mínimo, espe-
cialmente Dijkstra. Quanto menor o peso da aresta, mais próxima é a
relação territorial entre as UBSs conectadas.

No recorte final:

• Total de arestas: 215
• Menor peso de aresta: 0.01 km, entre AGUA RASA-UBS e MOOCA - UBS

• Maior peso de aresta: 3.67 km, entre CHACARA CRUZEIRO DO SUL - UBS

e V NOVA MANCHESTER (ARLINDO GENNARI,DR)-UBS

• Peso médio das arestas: 2.47 km
• Mediana dos pesos das arestas: 2.67 km
• Soma dos pesos das arestas: 530.02 km

5. Representação Computacional

O projeto utiliza duas formas principais de representação.

5.1 Arquivo grafo.txt

O arquivo grafo.txt é a representação textual da disciplina. Ele con-
tém:

1. Tipo do grafo.
2. Quantidade de vértices.
3. Lista de vértices.
4. Quantidade de arestas.
5. Lista de arestas.

Essa estrutura permite carregar e salvar o grafo de maneira indepen-
dente da interface visual.

5.2 Lista de Adjacência

No arquivo projeto_grafo_menu.py, a classe GrafoListaAdj armazena o
grafo usando lista de adjacência:

adj[u][v] = peso_da_aresta

Essa representação é adequada para o projeto porque o grafo é relati-
vamente esparso. Um grafo completo com 71 vértices teria:

n(n - 1) / 2 = 71 * 70 / 2 = 2485 arestas

O grafo real possui 215 arestas, muito menos que o máximo possível.
Logo, lista de adjacência é mais eficiente que matriz de adjacência
para percorrer vizinhos e executar algoritmos como BFS e Dijkstra.

6. Propriedades Gerais do Grafo

Com base no grafo final:

Propriedade

Tipo

Orientado

Ponderado nos vértices

Ponderado nas arestas

Número de vértices

Número de arestas

Densidade

Grau mínimo

Grau máximo

Grau médio

Mediana do grau

Componentes conexas

Grafo conexo

6.1 Densidade

Valor

3

Não

Sim

Sim

71

215

0.0865

2

12

6.06

6

1

Sim

A densidade de um grafo simples não orientado é calculada por:

D = 2m / (n(n - 1))

Substituindo os valores:

D = 2 * 215 / (71 * 70)
D = 430 / 4970
D = 0.0865

Isso mostra que o grafo é esparso. Apenas cerca de 8.65% das
conexões possíveis estão presentes. Essa esparsidade é desejável,
pois o projeto não conecta todas as UBSs entre si; ele conecta apenas
UBSs territorialmente próximas.

6.2 Grau dos Vértices

O grau de um vértice em grafo não orientado é a quantidade de
arestas incidentes nele:

grau(v) = |N(v)|

Onde N(v) é o conjunto de vizinhos de v.

Distribuição de graus:

Grau

Quantidade de vértices

2

3

4

5

6

7

8

9

10

11

12

4

9

10

6

12

12

6

4

4

3

1

O maior grau é 12, pertencente ao vértice:

22 - ILZA WELTMAN HUTZLER DRA-UBS

Os vértices com menor grau, igual a 2, são:

49 - NANCY ABRANCHES - UBS CAXINGUI
51 - V NOVA JAGUARE-UBS
64 - MAX PERLMAN (V OLIMPIA)-UBS
71 - PARAISOPOLIS - UBS

Vértices de maior grau tendem a estar em regiões mais bem conec-
tadas dentro do recorte. Vértices de menor grau aparecem como pon-
tos mais periféricos ou menos conectados na estrutura do grafo.

7. Conectividade

O grafo possui apenas uma componente conexa:

numero_de_componentes = 1

Logo, para qualquer par de vértices u e v, existe pelo menos um cam-
inho entre eles.

Formalmente:

para todo u, v pertencentes a V, existe caminho P(u, v)

Essa propriedade é essencial para o projeto, pois garante que algorit-
mos de caminho mínimo consigam comparar trajetos entre quaisquer
UBSs do recorte.

8. Caminhos Mínimos e Dijkstra

O algoritmo de Dijkstra é utilizado para calcular caminhos mínimos
ponderados. Como todas as arestas possuem pesos não negativos, o
algoritmo é adequado para o problema.

O custo de um caminho P é calculado pela soma dos pesos das
arestas:

custo(P) = soma wE(e), para cada e pertencente a P

Assim, o menor caminho entre dois vértices é o caminho cuja soma
das distâncias é mínima.

Na implementação, existem duas versões:

• projeto_grafo_menu.py: implementação manual com fila de priori-

dade usando heapq.

• src/grafo.py: uso de networkx.dijkstra_path e

networkx.dijkstra_path_length.

8.1 Complexidade

Na implementação com heap, a complexidade esperada é:

O((|V| + |E|) log |V|)

Para o grafo final:

|V| = 71
|E| = 215

Essa escala é pequena o suficiente para permitir execução rápida na
interface interativa.

8.2 Diâmetro Ponderado

O diâmetro ponderado é a maior distância mínima entre dois vértices:

diametro(G) = max d(u, v)

No grafo final:

• Diâmetro ponderado: 36.87 km
• Par associado: V NOVA JAGUARE-UBS até PARAISOPOLIS - UBS

Esse resultado mostra o maior afastamento interno do recorte quando
se percorre a rede pelas conexões disponíveis.

8.3 Raio e Centro Ponderado

A excentricidade de um vértice é a maior distância mínima dele até
qualquer outro vértice:

ecc(v) = max d(v, u)

O raio do grafo é:

raio(G) = min ecc(v)

No grafo final:

• Raio ponderado: 18.65 km
• Centro ponderado identificado: SE - NASF/UBS

Isso indica que, dentro da rede modelada, a UBS SE - NASF/UBS é a
mais central considerando distâncias mínimas ponderadas.

9. Busca em Largura (BFS)

A busca em largura é utilizada para explorar o grafo por níveis de viz-
inhança, desconsiderando os pesos das arestas.

A BFS retorna a distância em número de saltos:

nivel(v) = menor número de arestas entre origem e v

No contexto do projeto, BFS é útil para:

• verificar alcance estrutural a partir de uma UBS;
• identificar vizinhos diretos e indiretos;
• analisar a rede por camadas;
• verificar conectividade sem considerar quilometragem.

Diferentemente de Dijkstra, BFS considera cada aresta com custo
uniforme. Por isso, BFS responde quantas conexões separam duas
UBSs, enquanto Dijkstra responde qual é o menor caminho em
quilômetros.

10. Análise Euleriana

Um grafo conexo possui circuito euleriano se todos os vértices pos-
suem grau par. Possui trilha euleriana aberta se exatamente dois vér-
tices possuem grau ímpar.

No grafo final:

• Número de vértices de grau ímpar: 34
• O grafo é conexo: sim
• O grafo é euleriano: não
• O grafo é semieuleriano: não

Como existem mais de dois vértices de grau ímpar, não há circuito
euleriano nem trilha euleriana que percorra todas as arestas exata-
mente uma vez.

Essa conclusão é coerente com a natureza do problema: a rede não
foi criada para representar um percurso único que passe por todas as
conexões, mas sim uma malha de proximidade territorial.

11. Centralidade e Interpretação Territor-
ial

O projeto também calcula centralidade de proximidade. A centrali-
dade de proximidade mede o quanto um vértice está próximo dos de-
mais em termos de distância na rede.

Uma forma conceitual da métrica é:

C(v) = (n - 1) / soma d(v, u)

Vértices com maior centralidade tendem a estar em posições mais es-
tratégicas dentro do grafo, pois alcançam outras UBSs com menor
custo médio.

No sistema, essa informação aparece associada a análise de cobertu-
ra, junto com:

• quantidade de conexões;
• população estimada da área de abrangência;
• comparação com AAUBSs vizinhas;
• índice territorial relativo;
• classificação de pressão territorial.

12. Métricas de Cobertura Territorial

A métrica principal do projeto é a pressão territorial estimada:

pressao_estimada(v) = populacao_residente_estimada_na_AAUBS(v)

Quanto menor a população de abrangência, menor a demanda poten-
cial relativa sob a hipótese de capacidade semelhante. Essa métrica
foi escolhida porque o objetivo do sistema é comparar UBSs próximas
com granularidade melhor do que a população distrital, sem alegar
informação de fila em tempo real.

Como indicador auxiliar, é calculada a unidade por 10 mil pessoas na
própria AAUBS:

unidade_por_10_mil_AAUBS = (1 / populacao_AAUBS) * 10000

O número de UBSs no distrito continua disponível apenas como infor-
mação contextual e não entra no peso do vértice.

12.1 Score de Cobertura

O score de cobertura normaliza a pressão para uma escala de 0 a 100:

score = ((maior_pressao - pressao) / (maior_pressao - menor_pressao))

* 100

Interpretação:

• 100: melhor cobertura relativa no recorte;
• 0: pior cobertura relativa no recorte;
• valores intermediários: cobertura proporcional dentro do intervalo

observado.

13. Recomendação de UBS

A recomendação no sistema combina duas ideias:

1. Restrição geográfica: considerar UBSs próximas ao endereço in-

formado.

2. Pressão territorial estimada: ordenar ou destacar UBSs com

menor população em sua área de abrangência.

Assim, a recomendação não é uma simples busca da menor distância.
O sistema evita indicar uma UBS muito distante apenas por ter mel-
hor score global. A decisão é feita dentro de um raio aceitável, prior-
izando unidades próximas com maior chance relativa de atendimento
rápido.

Conceitualmente, para um endereço x, o sistema busca um conjunto
candidato:

C(x) = {v pertencente a V | distancia(x, v) <= raio}

Depois avalia os candidatos por critérios como:

• distância até o endereço;
• população estimada da AAUBS;
• quantidade de UBSs no distrito, somente como contexto;

• score de cobertura;
• conexões no grafo.

Essa abordagem é mais adequada ao problema real, pois usuários
normalmente procuram uma UBS viável territorialmente, mas podem
se beneficiar de uma recomendação que considere sobrecarga relati-
va.

14. Fontes, Links e Tratamento dos Dados

O projeto utiliza dados públicos e dados derivados:

• unidades e serviços de saúde da Prefeitura de São Paulo/SMS;
• população residente estimada por AAUBS a partir da SMS-SP/CE-

Info e Censo 2022/IBGE;

• população distrital mantida apenas como contexto a partir de TAB-

NET/SMS-SP, IBGE e Fundação SEADE;

• limites territoriais e bases geográficas do GeoSampa;
• adjacências geradas pelo projeto a partir da proximidade geográfi-

ca das UBSs.

14.1 Links das Fontes de Dados

As fontes abaixo foram consultadas para obter ou validar os dados
utilizados. Os links receberam rótulos curtos para manter a diagra-
mação legível na versão em PDF.

1. Unidades Básicas de Saúde, endereços e informações insti-

tucionais.
Fonte: Prefeitura de São Paulo - Secretaria Municipal da Saúde.
Link: Serviços de Saúde do Município

2. Consulta pública de UBSs próximas por endereço.

Fonte: Busca Saúde - Prefeitura de São Paulo.
Link: Busca Saúde

3. Áreas de abrangência das UBSs e referência territorial da

atenção básica.
Fonte: Secretaria Municipal da Saúde - CEInfo.
Link: Página oficial das AAUBS

4. População residente estimada por AAUBS, vinculada pelo

CNES.
Fonte: SMS-SP/CEInfo - AAUBS 2025 preliminar, Censo 2022/
IBGE.
Variável utilizada: V001AAUBS - Total de pessoas.
Link: Dados oficiais AAUBS 2025

5. Restrição de dados cadastrais por equipe ou UBS.
Fonte: SMS-SP - Documento Norteador NUVIS-AB.
Link: Quadro de territorialização 2025

6. Limites territoriais e bases cartográficas.

Fonte: GeoSampa - Mapa Digital da Cidade de São Paulo.
Link: Download GeoSampa

7. Metadados das camadas geográficas.

Fonte: GeoSampa - Catálogo de Metadados Geográficos.
Link: Catálogo GeoSampa

8. População por distrito, subprefeitura e regiões de saúde.
Fonte: TABNET/SMS-SP, com fontes IBGE e Fundação SEADE.
Link: TABNET População

14.2 Rastreabilidade da Fonte Aplicada ao Peso

Item
metodológico

Base efetiva-
mente aplica-
da ao peso dos
vértices

Variável ex-
traída

Registro utilizado no projeto

Dados sociodemográficos por Área de Abrangência
de UBS (AAUBS 2025 preliminar), SMS-SP/CEIn-
fo, estimados a partir do Censo Demográfico 2022/
IBGE

V001AAUBS - Total de pessoas

Chave de asso-
ciação

CNESAAUBS da base oficial associado ao campo cnes
de cada UBS do projeto

Cobertura da
associação

71 de 71 vértices do grafo foram vinculados a uma
AAUBS

Peso anterior

População do distrito, preservada apenas como in-
formação contextual e não utilizada no peso atual

Limitação de-
clarada

O denominador ideal seria capacidade ou número
de equipes por UBS. Sem fonte pública completa

Item
metodológico

Registro utilizado no projeto

para as 71 unidades, o peso representa demanda
territorial potencial, não fila ou tempo de espera
em tempo real.

Os dados finais estão organizados nos arquivos:

• data/ubs_vertices.json
• data/populacao_aaubs_2025.json
• data/servicos.json
• data/distritos.json
• data/adjacencias.json
• data/Sao Paulo.kml
• grafo.txt

A documentação específica das fontes também está registrada no ar-
quivo FONTES_DADOS.md.

15. Relação com Teoria dos Grafos

O projeto contempla conceitos centrais da disciplina:

Conceito

Aplicação no projeto

Vértice

Aresta

UBS

Conexão territorial entre UBSs próximas

Peso de vértice

População residente estimada na AAUBS

Peso de aresta

Distância aproximada em km

Grau

Caminho

Quantidade de UBSs vizinhas

Sequência de UBSs conectadas

Caminho mínimo

Menor percurso ponderado por distância

Conectividade

Verificação de alcance entre UBSs

BFS

Dijkstra

Exploração por níveis de vizinhança

Menor caminho ponderado

Densidade

Proporção de conexões existentes

Centralidade

Posição relativa da UBS na rede

Conceito

Aplicação no projeto

Grafo euleriano

Verificação estrutural por graus pares

16. Resultados Técnicos Principais

O grafo final apresenta:

• 71 vértices;
• 215 arestas;
• densidade 0.0865;
• grau médio 6.06;
• uma única componente conexa;
• pesos de arestas entre 0.01 km e 3.67 km;
• diâmetro ponderado de 36.87 km;
• raio ponderado de 18.65 km;
• centro ponderado na SE - NASF/UBS;
• não é euleriano;
• não é semieuleriano.

Esses resultados indicam uma rede esparsa, conexa e suficientemente
estruturada para aplicação de algoritmos de busca, caminho mínimo
e análise de cobertura.

17. Testes de Execução das Opções do
Menu

Os testes foram executados em 25/05/2026 por meio do programa tex-
tual projeto_grafo_menu.py, carregando o arquivo final grafo.txt. As
operações que alteram o grafo foram realizadas somente em memória
e gravadas em arquivos temporários, preservando o arquivo oficial da
entrega.

17.1 Testes de Regressão das Operações Fundamen-
tais

Foram realizados dois fluxos independentes para validar as opções
herdadas de manipulação e inspeção do grafo.

Fluxo A: carregamento de grafo.txt; gravação da cópia temporária
/tmp/redeasp_grafo_teste_a.txt; inserção do vértice temporário 900; in-
serção e remoção da aresta 1-900, com peso 1.25; remoção do vértice
temporário; exibição do arquivo, da lista de adjacência e da conexi-
dade.

Fluxo B: carregamento de grafo.txt; gravação da cópia temporária
/tmp/redeasp_grafo_teste_b.txt; inserção do vértice temporário 901; in-
serção e remoção da aresta 4-901, com peso 2.10; remoção do vértice
temporário; exibição do arquivo, da lista de adjacência e da conexi-
dade.

Verificação executada
nos dois fluxos

Ler e gravar arquivo

Inserir e remover vértice
temporário

Inserir e remover aresta
temporária

Mostrar arquivo e lista de
adjacência

Analisar conexidade após
as remoções

Resultado observado

Operações concluídas com sucesso; ar-
quivo final preservado

Operações concluídas com sucesso

Operações concluídas com sucesso

Conteúdo apresentado corretamente

Grafo não orientado: CONEXO

Figura 2 - Evidência consolidada dos testes de regressão. As men-
sagens foram obtidas das duas execuções reais do menu, utilizando apenas
vértices e arquivos temporários nas operações de alteração.

17.2 Testes da Opção j - Solução com Dijkstra

A opção j, acrescentada para investigar uma solução ao problema,
utiliza Dijkstra sobre as arestas ponderadas por distância. Foram exe-
cutados dois casos em regiões distintas do recorte.

Teste

Entrada

Centro

Origem 1 - HUMAITA; desti-
no 4 - SE

Caminho
mínimo retor-
nado

Distância

1 -> 4

1.54 km

Oeste/
Sul

Origem 64 - MAX PERLMAN;
destino 71 - PARAISOPOLIS

64 -> 50 -> 53
-> 71

6.41 km

No primeiro caso, o programa também identificou REPUBLICA - UBS co-
mo alternativa mais próxima da origem, a 0.75 km. No segundo caso,
identificou JOSE DE BARROS MAGALDI-UBS, a 1.52 km. Os resultados
demonstram que a investigação calcula caminhos e alternativas no
grafo ponderado, em vez de apenas listar unidades.

17.3 Testes da Opção k - Características do Problema
Modelado

A opção k concentra as técnicas adicionais solicitadas para investigar
características do grafo.

Técnica veri-
ficada

Ordem e
tamanho

Teste com origem 1

Teste com origem 64

71 vértices e 215 arestas

71 vértices e 215 arestas

Densidade

0.0865

Conectividade Conexo

0.0865

Conexo

Grau

mínimo 2, máximo 12,
médio 6.06

mínimo 2, máximo 12,
médio 6.06

Verificação
euleriana

Não euleriano; 34 vér-
tices de grau ímpar

Não euleriano; 34 vér-
tices de grau ímpar

BFS/alcance

71 vértices alcançáveis
em até 8 saltos

71 vértices alcançáveis
em até 12 saltos

Figura 3 - Execução do teste central. Dijkstra foi aplicado de HUMAITA
para SE, seguido das características estruturais e BFS com origem em HU-
MAITA.

Figura 4 - Execução do teste oeste/sul. Dijkstra foi aplicado de MAX
PERLMAN para PARAISOPOLIS, seguido das características estruturais e
BFS com origem em MAX PERLMAN.

17.4 Correspondência entre Menu, Técnicas e Proble-
ma

Opção nova

Técnica da disci-
plina

Papel na solução

j - Investigar
solução com
Dijkstra

Caminho mínimo
em grafo pondera-
do

Mede percursos territoriais
entre UBSs conectadas usan-
do distância como peso das
arestas.

k - Apresentar
características

Grau, densidade,
conexidade, verifi-
cação euleriana e
BFS

Descreve a estrutura da rede
e demonstra que as UBSs per-
manecem alcançáveis no mod-
elo.

18. Conclusão

A Rede de Acesso SP demonstra a aplicação prática de Teoria dos
Grafos em um problema urbano de saúde pública. A modelagem por
grafo permite transformar UBSs e suas relações territoriais em uma
estrutura formal, sobre a qual podem ser aplicados algoritmos clássi-
cos como BFS e Dijkstra.

A escolha de pesos nos vértices e nas arestas amplia a capacidade
analítica do modelo. As arestas ponderadas permitem calcular camin-
hos mínimos por distância, enquanto os vértices ponderados utilizam
população estimada de cada AAUBS para comparar demanda territor-
ial potencial. O sistema não substitui dados operacionais de atendi-
mento ou capacidade, mas oferece um critério público e reproduzível
para recomendação e comparação de unidades próximas.

Do ponto de vista da disciplina, o projeto cobre representação de
grafos, leitura e escrita em arquivo, lista de adjacência, propriedades
estruturais, busca, caminho mínimo, densidade, graus, conectividade,
centralidade e análise euleriana. Do ponto de vista aplicado, o sis-
tema mostra como grafos podem apoiar decisões em cenários reais de
desigualdade territorial e acesso a serviços públicos.

Apêndice A - Links de Entrega

Entrega

Endereço

Repositório público do
projeto

https://github.com/Lucas-FcNw/rede-de-
acesso-sp

Aplicação publicada

https://redeasp.streamlit.app/

Vídeo público no
YouTube

https://youtu.be/6LAj96dURXc

O repositório público deve incluir este relatório atualizado, o arquivo
grafo.txt, os códigos-fonte e os recursos visuais referenciados neste
documento.


