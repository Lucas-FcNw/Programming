Impactos da descentralização nos
sistemas de saúde no estado de
São Paulo, Brasil
Impacts of decentralization in health systems in the
state of São Paulo, Brazil

Daniel Okita Uehara1, Pedro Lucas Rosa1, Matheus Cardoso Moraes1, Renato Cesar Sato1

1 Universidade Federal de São Paulo, São Paulo, SP, Brasil.

DOI: 10.31744/einstein_journal/2021GS5914

RESUMO

❚
Objetivo: Avaliar um modelo de p-medianas para acessibilidade de serviços de saúde com base
na descentralização e na alocação ideal de Unidades Básicas de Saúde no estado de São Paulo,
Brasil. Métodos:  Por meio  de dados geográficos das Unidades Básica de Saúde do estado de
São Paulo, possíveis alocações de suporte e suprimento foram simuladas em uma abordagem
randomizada. Em seguida, uma série de restrições foi imposta ao sistema, simulando possíveis
cenários, e os resultados foram verificados por disposição geográfica. Resultados: Dado um
número  de  instalações  desejadas,  dez  como  restrição,  a  abordagem  p-mediana  alocou  três
nas proximidades da capital, área de maior concertação de Unidades Básica de Saúde, e as
demais foram distribuídas a oeste. Uma segunda rodada de testes avaliou exclusivamente a
influência dos custos fixos, variando de 71 posições ótimas, com custo fixo unitário, até seis
unidades, para um custo 300 vezes maior. Isso foi relevante no processo de tomada de decisão,
pois abrangeu cenários em que apenas o número de instalações finais era conhecido e em que
apenas o orçamento estava especificado. Um terceiro conjunto de simulações contemplou uma
mistura dos casos anteriores. Conclusão: A abordagem p-mediana foi capaz de otimizar uma
ampla gama de cenários, com média de tempo de execução abaixo de 2 horas e 30 minutos,
considerando um conjunto de dados com mais de 4.000 posições. Apesar de suas deficiências,
considerando distâncias euclidianas, o método é simples, mas poderoso para ser considerado
como uma ferramenta para o tomador de decisão em relação à distribuição de recursos e de
instalações em grandes áreas e alto número de locais considerados.

Descritores:  Acesso  aos  serviços  de  saúde;  Equidade  em  Saúde;  Localizações  geográficas;
Instalações de saúde; Alocação de recursos para a atenção à saúde

ABSTRACT

❚
Objective:  To  evaluate  a  p-median  model  for  health  care  services  accessibility  based  on
decentralization  and  optimal  allocation  of  Primary  Health  Care  Units  in  the  State  of  São  Paulo,
Brazil.  Methods:  Using  geographical  data  of  Primary  Health  Care  Units  located  in  the  State  of
São  Paulo,  potential  support  and  supply  facility  allocations  were  simulated  by  means  of  a
random  approach.  Several  constraints  were  then  imposed  on  the  system  to  simulate  different
scenarios.  Results  were  assessed  according  to  geographic  disposition.  Results:  Using  a  fixed
number of supply facilities, ten as a constraint, the p-median approach allocated three facilities
near  the  state  capital  (the  area  with  the  highest  concentration  of  Primary  Health  Care  Units),
while remaining facilities were spread throughout the west of the state. A second round of tests
assessed the impact of fixed costs alone on optimization, ranging from 71 optimal locations with
a fixed unit cost to six optimal locations at a cost 300-fold higher. This finding was relevant to
decision-making, since it encompassed scenarios in which only the final number of facilities or
only the budget was known. A third set of simulations contemplates an intermediate scenario.

1

Como citar este artigo:
Uehara DO, Rosa PL, Moraes MC, Sato RC.
Impactos da descentralização nos sistemas de
saúde no estado de São Paulo, Brasil. einstein
(São Paulo). 2021;19:eGS5914.

Autor correspondente:
Daniel Okita Uehara
Avenida Cesare Mansueto Giulio Lattes, 1.201
Eugênio de Mello
CEP: 12247-014 – São José dos Campos,
SP, Brasil
Tel.: (11) 96494-4763
E-mail: douehara@gmail.com

Data de submissão:
12/6/2020

Data de aceite:
15/12/2020

Conflitos de interesse:
não há.

Copyright 2021

Esta obra está licenciada sob
uma Licença Creative Commons
Atribuição 4.0 Internacional.

GESTÃO E ECONOMIA EM SAÚDEISSN: 1679-4508 | e-ISSN: 2317-6385Publicação Oficial do Instituto Israelita  de Ensino e Pesquisa Albert Einsteineinstein (São Paulo). 2021;19:1-6

Conclusion:  The  p-median  approach  was  capable  of  optimizing  a
wide range of scenarios with an average running time of less than 2
hours and 30 minutes while considering a large dataset of more than
4,000 locations. In spite of some shortcomings, such as estimation of
Euclidean distances, the method is simple yet powerful enough to be
considered a useful tool to assist decision makers in the distribution
of  resources,  and  facilities  across  large  areas  with  high  number  of
locations to be supplied.

Keywords: Health services accessibility; Health equity; Geographic
locations; Health facility; Health care rationing

INTRODUÇÃO

❚
Redes  descentralizadas  de  serviços  de  saúde  abrem  a
possibilidade  de  cobertura  para  indivíduos  que  vivem
na periferia das cidades e que, de outra forma, não po-
deriam acessá-las,(1-5) além de ajudar a reduzir a super-
lotação em grandes hospitais. Entretanto, a necessidade
de abastecer essas infraestruturas com bens de consu-
mo e equipamentos médicos se traduz em custos mais
elevados.  As  consequências  de  decisões  equivocadas
quanto  à  alocação  de  novas  unidades  vão  muito  além
de custos elevados, podendo incluir taxas mais altas de
mortalidade e morbidade.(6-8) Esses impactos são dura-
douros,(9,10)  por  serem  onerosos  e  difíceis  de  reverter.
Decisões deliberadas quanto à localização de unidades
de saúde devem ser baseadas em análises abrangentes
prévias do cenário em questão.

Cirino et al.,(11) compararam a real alocação de hos-
pitais em Santa Catarina com uma simulação feita em-
pregando-se o modelo de p-medianas para auxiliar na
tomada de decisão quanto à construção de novas uni-
dades em regiões com cobertura limitada. O modelo de
p-medianas também pode ser empregado na solução de
diversos problemas em várias áreas de pesquisa, como a
distribuição de candidatos de acordo com a pontuação
ideal no vestibular,(12,13) o agrupamento de dados(14,15) e
diversos  outros  estudos,  conforme  demonstrado  por
Farahani et al.,(16,17) e Karatas et al.(18)

A  expansão  de  estruturas  descentralizadas  resulta
em  uma  rede  de  cuidados  de  saúde  que  pode  conter
milhares de unidades a serem abastecidas e integradas
em uma grande área. Quando combinada com fatores,
como  custos  de  implementação,  a  seleção  de  espaços
otimizados se torna uma questão matemática. A solu-
ção  desse  problema,  em  geral,  está  fora  da  alçada  do
responsável pela tomada de decisão, que não possui as
ferramentas necessárias para solucioná-lo. O desenvol-
vimento de novas ferramentas de otimização que possam
ser  executadas  em  computadores  pessoais  padrão  in-
troduz  uma  nova  abordagem  do  problema,  permitindo

a  obtenção  de  uma  solução  mais  confiável  e  possibili-
tando lidar com um grande número de limitações e dados.
Unidades  descentralizadas  podem  prestar  serviços
(armazenagem  e  distribuição  de  recursos)  para  uni-
dades de saúde. Esta pesquisa foi baseada em Unidades
Básicas de Saúde (UBS), um projeto de infraestrutura
social  criado  pelo  governo  brasileiro  para  expandir  o
acesso aos cuidados de saúde por meio da prestação de
serviços  gratuitos  em  diversas  especialidades  médicas.
Neste  estudo,  foram  consideradas  limitações  como  o
alinhamento da distribuição de recursos para unidades
de  saúde  e  a  melhoria  da  qualidade  dos  serviços  para
oferecer cuidados de saúde melhores para a população.

OBJETIVO

❚
Avaliar um modelo de p-medianas para acessibilidade
de serviços de saúde com base na descentralização e na
alocação ideal de Unidades Básicas de Saúde no estado
de São Paulo, Brasil.

MÉTODOS

implementado  na

❚
O  modelo  descrito  neste  artigo  foi  implementado
em  um  notebook  com  as  seguintes  configurações:
processador Intel® Core™ i5 de sexta geração, 8 GB de
RAM e sistema operacional Windows 10. O algoritmo
foi
linguagem  de  programação
Python 3.7.1, empregando-se o Jupyter Notebook como
ambiente  de  programação  e  os  programas  Anaconda
Navigator  e  Gurobi™  versão  8.1.1  (licença  para  fins
acadêmicos).(19)  Este  estudo  foi  realizado  no  Instituto
de  Ciência  e  Tecnologia  da  Universidade  Federal  de
São Paulo (UNIFESP).

O  objetivo  deste  estudo  foi  criar  um  modelo  que
levasse em conta as limitações e os custos. A localiza-
ção de cada UBS do estado de São Paulo determinada
de acordo com as coordenadas de latitude e longitude
foi utilizada para gerar um conjunto de dados sintético,
incluindo  todas  as  possíveis  localizações  de  unidades.
Finalmente, o modelo foi otimizado por meio de uma
abordagem de p-medianas para diferentes cenários de
limitações, e os resultados foram comparados.

Dada a abordagem selecionada, o projeto foi isen-
to  de  revisão  ética.  A  fim  de  otimizar  a  distribuição
das  unidades,  o  modelo  matemático  levou  em  conta
os  custos da seleção de uma determinada localização,
pois quanto maior a distância da UBS, maior o custo do
transporte. Foram empregadas as seguintes definições:
i para localização das unidades de saúde existentes e j
para possíveis localizações para instalação de novas uni-
dades. A distância entre esses dois pontos pode, então,

2

Uehara DO, Rosa PL, Moraes MC, Sato RCeinstein (São Paulo). 2021;19:1-6

ser calculada. Uma abordagem euclidiana(20) foi repre-
sentada pela equação 1.

Equação 1

A distância dij entre a UBS i e a unidade j pode ser
associada aos gastos com transporte a fim de incorporar
o número de entregas ao longo do tempo. Dessa forma,
a variável custo (vij) pode ser considerada diretamente
proporcional  aos  custos  do  transporte  e  às  distâncias
envolvidas, sendo estimada empregando-se a função α,
conforme a equação 2.

Equação 2

Os custos gerados pelo transporte foram definidos
conforme  a  equação  2.  Para  calcular  o  custo  total,  o
número  de  vezes  que  cada  UBS  usa  a  unidade  de  dis-
tribuição deve ser considerado, uma vez que a demanda
pode variar entre as localidades. O custo total foi defini-
do como yij, e o custo associado ao custo fixo e à instala-
ção de cada unidade foi definido como fj. Uma variável
binária xij, geralmente conhecida como parâmetro p, foi
usada para representar as melhores alocações, conven-
cionando-se que a localização ideal é igual a um e a lo-
calização não ideal é igual a zero. Dessa forma, o número
total desejado de unidades otimizadas pode ser controlado.
Assim, o custo total é descrito pela equação 3.

Equação 3

A  fim  de  diminuir  o  tamanho  do  conjunto  de
dados  e,  consequentemente,  o  tempo  de  resposta  du-
rante  o  processo  de  otimização  do  modelo,  os  dados
empregados neste estudo foram limitados ao estado de
São Paulo. O conjunto de dados consistiu em um banco
de  dados  que  continha  as  coordenadas  geográficas
(latitude e longitude) de 4.771 UBS listadas no registro
na data da última atualização.(21)

No que se refere à possível alocação de unidades, a
melhor alternativa para dar continuidade ao projeto foi
criar  simulações  com  dados  aleatórios.  As  simulações
geraram dados com distribuição gaussiana para garan-
tir um número mais significativo de possíveis alocações
de unidades.

Finalmente, usando-se os conjuntos de dados descri-
tos,  o  modelo  foi  otimizado  e  comparado  nas  seguintes
situações: dados gerados sem e com correção dos discre-
pantes (outliers), empregando-se o parâmetro p como úni-
ca limitação e utilizando os custos como única limitação.
O mapa mostra a localização otimizada e seus resultados.

RESULTADOS

❚
No primeiro teste, a variável fj, que representava o cus-
to fixo associado à implementação de uma unidade na
localidade j, foi definida como um valor unitário para
todas as localidades possíveis. A variável que represen-
tava o custo do transporte entre a UBS e uma unidade
também foi definida como um valor unitário, enquanto
a variável p foi ajustada para dez (isto é, o processo de
otimização  foi  limitado  aos  dez  pontos  mais  altos).  O
objetivo  foi  determinar  a  alocação  ideal  das  unidades
com base nas distâncias mínimas, sem considerar os fa-
tores financeiros.

As  localizações  ideais  determinadas  pelo  modelo  e
as respectivas latitude e longitude foram plotadas em um
mapa base como pontos verdes (Figura 1). O processo de
otimização levou em torno de 2 horas e 9 minutos.

UBS: Unidade Básica de Saúde.
Figura 1. Alocação ideal de unidades considerando-se p=10

Neste  estudo,  três  das  dez  localizações  ideais  en-
contradas  ficavam  próximas  da  capital  do  estado,  que
era a área com a maior concentração de UBS do estado.
As  unidades  restantes  encontravam-se  esparsamente
distribuídas em áreas distantes da capital, enfatizando
a complexidade desse tipo de tarefa.

Uma vez que o objetivo era minimizar as distâncias
entre  as  UBS  e  as  unidades,  foi  criada  uma  segunda
simulação,  desconsiderando  a  variável  p,  que,  no  mo-
delo anterior, representava a limitação que restringia o
número máximo de unidades a serem alocadas. Assim,
empregando-se  o  custo  fixo  fj  como  valor  unitário  in-
dependentemente da localização, o processo, que levou
em torno de 2 horas e 11 minutos para ser completado,
retornou uma variável que continha um conjunto de 71
localidades ideais para o modelo, o qual foi expresso na
figura 2A.

3

Impactos da descentralização nos sistemas de saúde no estado de São Paulo, Brasileinstein (São Paulo). 2021;19:1-6

A

B

UBS: Unidade Básica de Saúde.
Figura 2. Alocações ideais de unidades: (A) Sem a limitação imposta pela variável p; (B) Considerando-se p=1

Os  resultados  obtidos  reforçaram  a  importância
que a atribuição de um valor para a variável p teve no
modelo que excluiu os custos de instalação. Com base
nesse  princípio,  uma  terceira  simulação  foi  realizada,
mais  uma  vez  atribuindo  um  valor  à  variável  p.  Desta
vez, o valor atribuído foi p=1, de tal forma que apenas
a localização ideal para instalação de uma unidade que
servisse todo o estado de São Paulo fosse determinada.
O resultado dessa simulação, cujo tempo de processa-
mento foi de 2 horas e 31 minutos, pode ser visualizado
na figura 2B.

Na  figura  2B,  um  ponto  verde  pode  ser  visualiza-
do  na  Região  Metropolitana  de  Campinas,  a  segunda
maior cidade do estado de São Paulo. Dada a geografia
do  estado,  a  localização  dessa  unidade,  inicialmente,
satisfez  o  objetivo  de  minimizar  as  distâncias  médias
entre a UBS e a unidade. A proximidade da capital do
estado (aproximadamente 100km de distância), onde a
concentração de UBS era mais alta, foi considerada e

representou  a  minimização  das  distâncias  relativas  às
UBS localizadas no oeste do estado.

Controlando-se o valor dos custos fixos associados à
instalação de uma unidade naquela localidade e empre-
gando-se valores 100 ou 300 vezes mais altos do que o
empregado nas simulações anteriores, novas simulações
foram geradas. Esses processos de simulação levaram 2
horas e 11 minutos e 2 horas e 20 minutos para serem
completados, respectivamente, e os resultados obtidos
podem ser visualizados na figura 3.

Os resultados da última simulação mostraram que
a atribuição de um custo fj por si só também agiu como
fator limitante no modelo, uma vez que restringiu o nú-
mero de unidades no processo de otimização mostrado
na figura 3, de 11 para seis. Esse achado se revestiu de
grande  importância  na  tomada  de  decisão,  pois  pôde
fornecer informações relevantes aos tomadores de deci-
são quanto ao orçamento disponível e ao custo de cada
unidade.  Nessas  condições,  o  modelo  pôde  ser  capaz

A

B

UBS: Unidade Básica de Saúde.
Figura 3. Alocações ideais com custo fixo de (A) fj. = 100 e (B) fj = 300

4

Uehara DO, Rosa PL, Moraes MC, Sato RCeinstein (São Paulo). 2021;19:1-6de  continuar  a  minimizar  os  custos  envolvidos.  Uma
situação intermediária, em que o número de unidades
e o custo fixo fossem conhecidos, também poderia ser
simulada empregando-se o método proposto, uma vez
que ambos os fatores limitantes poderiam ser determi-
nados simultaneamente.

Dessa  forma,  três  cenários  de  tomada  de  decisão
puderam ser definidos. No primeiro, o responsável pela
tomada  de  decisão  partiu  de  um  orçamento  limitado
quanto ao número de unidades, e o modelo interpretou
isso com base no parâmetro p, com alocação do número
ideal (“n desejado”) de unidades. No segundo, somente
o custo fixo de cada espaço foi conhecido, e o modelo
interpretou isso como a variável custo fj, considerando
apenas  o  número  máximo  de  unidades  que  operaram
com esse custo. Dessa forma, o custo do investimento
inicial em serviços pôde ser compensado pela economia
gerada a longo prazo, por meio da redução dos custos
variáveis ao longo do tempo. O terceiro cenário corres-
pondeu a uma situação intermediária em que o número
máximo  de  unidades  era  conhecido  e,  consequente-
mente, as despesas podiam ser estimadas.

médicos  sensíveis,  como  aparelhos  para  tomografia  por
emissão  de  pósitrons  (PET)  e  ressonância  magnética
(RM),  disponíveis  para  uso  geral  em  poucas  unidades,
devido ao seu alto custo,(23,27) também pode ser modelada.
Além  disso,  os  inúmeros  fatores  que  podem  in-
fluenciar nos custos da instalação de uma unidade em
um  determinado  local  não  foram  considerados  neste
estudo. Exemplos de tais fatores incluem questões eco-
nômicas  (disponibilidade  local  de  pessoal  qualificado
e concorrên cia por esse tipo de mão de obra com ou-
tras  empresas),  políticas  (incentivos  fiscais  destinados
a atrair novas empresas) e ambientais. Todos esses fa-
tores  constituem  parâmetros  a  serem  incluídos  no  al-
goritmo em estudos futuros.

A  minimização  das  distâncias  médias  entre  a  de-
manda (no caso, a UBS) e as unidades também foi le-
vada  em  conta  no  modelo.  Entretanto,  o  modelo  em-
pregou a minimização da distância euclidiana entre os
pontos, sem considerar a ausência de rotas diferentes.
Entre cada dois pontos, foi obtida uma distância eucli-
diana  ideal,  que  pode  ser  divergente,  dada  a  falta  de
uma via direta de conexão.

DISCUSSÃO

❚
A prestação de cuidados de saúde consiste em estratégias
preventivas  de  baixo  custo  voltadas  para  uma  grande
proporção da população.(22) O número crescente de es-
tudos investigando a localização otimizada de unidades
de saúde deu origem a colaborações importantes entre
os profissionais na abordagem dessa questão.(22,23)

A  ampla  gama  de  fatores  limitantes  considerados
na  avaliação  de  métodos  baseados  em  otimização  de
p-medianas  demonstra  a  flexibilidade  do  modelo,  que
também foi destacada em outras áreas de pesquisa.(24,25)
O tempo necessário para execução das simulações em
um notebook padrão, levando em conta uma quantida-
de considerável de localidades, foi de, aproximadamente,
2 horas e 20 minutos. São Paulo é o estado mais popu-
loso e com maior número de UBS do Brasil. O tempo
de execução em questão foi considerado aceitável, uma
vez que, via de regra, as alocações não são selecionadas
em 1 dia, e sim depois de dias de análise.

Outro ponto importante foi a necessidade de simu-
lação de possíveis localizações neste estudo, o que nem
sempre ocorre em aplicações reais. As coordenadas das
possíveis localizações foram consideradas nas situações
simuladas no modelo, reduzindo o efeito da introdução
de dados aleatórios sobre a dinâmica do sistema.(26)

A unidade de abastecimento considerada neste estudo
não restringe a generalização do modelo desse problema
aos cuidados de saúde. A distribuição de equipamentos

CONCLUSÃO

❚
Este estudo permitiu o desenvolvimento de um modelo
de simulação para auxiliar na tomada de decisão refe-
rente  à  alocação  de  instalações,  aqui  definidas  como
unidades de prestação de serviços para Unidades Básicas
de Saúde no estado de São Paulo. Este trabalho de pes-
quisa  tentou  mostrar  a  importância  da  alocação  ade-
quada de unidades de saúde, a qual apresenta impacto
direto na qualidade de vida da população.

Os resultados obtidos por meio dos algoritmos im-
plementados sugerem que o método proposto oferece
soluções satisfatórias para o problema da alocação de
unidades de saúde a um baixo custo computacional. A
implementação da visualização geoespacial possibilitada
pelo uso das bibliotecas da linguagem de programação
Python também foi fundamental para a compreensão e
a análise dos achados.

Entretanto,  a  falta  de  um  conjunto  real  de  possí-
veis  localizações  de  unidades  limitou  os  resultados  da
simulação e impediu a estimativa da aplicabilidade do mo-
delo. Considerando-se a implementação do algoritmo e a
possibilidade de visualização geoespacial das diferentes
simulações realizadas, o modelo proposto foi conside-
rado  uma  ferramenta  útil  para  o  processo  de  tomada
de  decisões  relacionadas  ao  sistema  de  saúde.  Ainda
assim, o algoritmo precisa ser ajustado de acordo com
as variáveis consideradas e as potenciais limitações de-
tectadas em simulações anteriores.

5

Impactos da descentralização nos sistemas de saúde no estado de São Paulo, Brasileinstein (São Paulo). 2021;19:1-6

Novos estudos se fazem necessários para abordar a
deficiências do modelo, incluindo o uso de novos con-
juntos  de  dados,  o  ajuste  do  modelo  considerando  a
minimização  das  distâncias  e  as  rotas  existentes  entre
os pontos (ou seja, a distância não euclidiana) e a ava-
liação das demandas de cada unidade, de acordo com o
respectivo tamanho e a capacidade de serviço.

CONTRIBUIÇÃO DOS AUTORES

❚
Daniel Okita Uehara: atuou ativamente no planejamento
da  pesquisa,  coleta  de  dados,  bem  como  nas  análises
computacionais dos dados, assim como na redação do
artigo.  Pedro  Lucas  Rosa:  atuou  ativamente  na  orga-
nização e ajuste dos resultados, bem como na redação
do  artigo.  Matheus  Cardoso  Moraes:  participou  na
interpretação  e  análise  dos  dados  obtidos  e  redação
do artigo. Renato Cesar Sato: orientador do trabalho,
atuou  no  planejamento  do  estudo,  orientou  a  coleta
de  dados  e  as  análises  computacionais,  bem  como  na
análise dos dados e redação do artigo.

INFORMAÇÃO DOS AUTORES

❚
Uehara DO: http://orcid.org/0000-0002-9824-370X
Rosa PL: http://orcid.org/0000-0002-0375-9472
Moraes MC: http://orcid.org/0000-0002-6019-6653
Sato RC: http://orcid.org/0000-0002-9902-9086

REFERÊNCIAS

❚
1.  Escobar-Lemmon  MC.  Executives,  legislatures,  and  decentralization.  Policy

Stud J. 2006;34(2):245-63.

2.  Mokrini  A,  Boulaksil  Y,  Berrado  A.  Modelling  facility  location  problems  in
emerging  markets:  The  case  of  the  public  healthcare  sector  in  Morocco.
OSCM Publications. 2019;12(2):100-11.

3.  Shah  A,  Thompson  T,  Zou  HF.  Decentralizing  the  public  sector:  the  impact
of  decentralization  on  service  delivery,  corruption,  fiscal  management  and
growth  in  developing  and  emerging  market  economies:  a  synthesis  of
empirical evidence. CESifo DICE Report. 2004;2(1):10-4.

4.  Abimbola S, Baatiema L, Bigdeli M. The impacts of decentralization on health
system equity, efficiency and resilience: a realist synthesis of the evidence.
Health Policy Plan. 2019;34(8):605-17. Review.

5.  Alizadeh R, Nishi T. Hybrid set covering and dynamic modular covering location
problem: application to an emergency humanitarian logistics problem. J Appl
Sci. 2020;10(20):7110.

7.  Daskin  MS,  Dean  LK.  Location  of  health  care  facilities.  In:  Brandeau  ML,
Saintfort F, Pierskalla WP. Operations research and health care: a handbook of
methods and applications. Boston: Kluwer Academic Publishers; 2005. p. 43-76.

8.  Sharma B, Ramkumar M, Subramanian N, Malhotra B. Dynamic temporary
blood facility location-allocation during and post-disaster periods. Ann Oper
Res. 2019;283(1):705-36.

9.  Snyder  LV.  Facility
200;38(7):547-64.

location  under  uncertainty:  a  review.

IIE  Trans.

10.  Correia I, Saldanha-da-Gama F. Facility location under uncertainty. In: Laporte
G, Nickel S, Gama FS. Location science. 2nd ed. Springer; 2019. p. 177-203.

11.  Cirino S, Gonçalves LA, Gonçalves MB, Cursi ES,  Coelho AS. Avaliação de
acessibilidade  geográfica  em  sistemas  de  saúde  hierarquizados  usando
o  modelo  de  p-medianas:  aplicação  em  Santa  Catarina,  Brasil.  Cad  Saude
Publica. 2016;32:(4):e00172614.

12.  Correa ES, Steiner MT, Freitas AA, Carnieri C. A genetic algorithm for solving a
capacitated p-median problem. Numerical Algorithms. 2004;35(2-4):373-88.

13.  Blanco V. Ordered p-median problems with neighbourhoods. J Comput Optim

Appl. 2019;73(2):603-45.

14.  Köhn HF, Steinley D, Brusco MJ. The p-median model as a tool for clustering

psychological data. Psychol Methods. 2010;15(1):87-95.

15.  Benati  S,  García  S,  Puerto  J.  Mixed  integer  linear  programming  and  heuristic
methods for feature selection in clustering. J Oper Res Soc. 2018;69(9):1379-95.

16.  Farahani  RZ,  SteadieSeifi  M,  Asgari  N.  Multiple  criteria  facility  location
problems: a survey. Applied Mathematical Modelling. 2010;34(7):1689-709.

17.  Farahani RZ, Asgari N, Heidari N, Hosseininia M, Goh M. Covering problems

in facility location: a review. Comput Ind Eng. 2012;62(1):368-407.

18.	 Karatas	M,	Yakıcı	E.	An	iterative	solution	approach	to	a	multi-objective	facility

location problem. Appl Soft Comput. 2018;62:272-87.

19.  Gurobi optimizer reference manual. Version 9.0. Oregon: Gurobi Optimization

LLC; 2020. p. 935.

20.  Linden R. Técnicas de agrupamento. Rev Sistemas Infor FSMA. 2009;4:18-36.

21.  Brasil. Ministério da Saúde. Portal Brasileiro de Dados Abertos. Distribuição
Unidades Básicas de Saúde em funcionamento - UBS. Brasília (DF): Ministério
da  Saúde;  2020  [citado  2020  Out  28].  Disponível  em:  http://dados.gov.br/
dataset/ubs_funcionamento

22.  Almeida  JF,  Pinto  LR,  Conceição  SV,  Campos  FC.  Medical  centers  location
and  specialists’  allocation:  a  healthcare  planning  case  study.  Production.
2019;29:e20190006.

23.  Ahmadi-Javid A, Seyedi P, Syam SS. A survey of healthcare facility location.

Comput Oper Res. 2017;79:223-63.

24.	 Karatas	 M,	 Yakıcı	 E.	 An	 analysis	 of	 p-median	 location	 problem:	 effects	 of
backup  service  level  and  demand  assignment  policy.  Eur  J  Oper  Res.
2018;272(1):207-18.

25.  Badri-Koohi B, Tavakkoli-Moghaddam R, Asghari M. Optimizing number and
locations  of  alternative-fuel  stations  using  a  multi-criteria  approach.  Eng
Technol Appl Sci Res. 2019;9(1):3715-20.

26.  Farahani RZ, Fallah S, Ruiz R, Hosseini S, Asgari N. OR models in urban service
facility location: a critical review of applications and future developments. Eur
J Oper Res. 2019;276(1):1-27.

6.  Cetin E, Sarul LS. A blood bank location model: a multiobjective approach. Eur

27.  Seger  MJ.  Medical  imaging  centers  in  central  Indiana:  optimal  location

J Pure Appl Math. 2009;2(1):112-24.

allocation analyses [thesis]. Indiana: Indiana University; 2016.

6

Uehara DO, Rosa PL, Moraes MC, Sato RCeinstein (São Paulo). 2021;19:1-6


