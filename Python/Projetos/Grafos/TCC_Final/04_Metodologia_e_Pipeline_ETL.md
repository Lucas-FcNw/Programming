# 4. METODOLOGIA E PIPELINE DE ENGENHARIA DE DADOS

O insumo principal da presente pesquisa não reside apenas nos algoritmos clássicos, mas na pureza informacional que carrega a malha matemática. Para alçar o status da Teoria dos Grafos da abstração letárgica rumo a um motor ativo de decisão pública, concebeu-se um pipeline de Engenharia de Dados de extrema responsabilidade arquitetural (ETL – *Extract, Transform and Load*).

Esta pesquisa adota uma abordagem de *Design Science Research* com metodologia estritamente quantitativa, lidando com milhares de polígonos habitacionais da região mais complexa do país.

## 4.1 Proveniência dos Dados Governamentais

O roteamento populacional exigiu o cruzamento transparente e reprodutível de entes federativos distintos, cujas bases operam, tradicionalmente, em silos isolados de banco de dados.

O **Vértice ($V$)** nasceu das diretrizes estaduais e municipais de equipamentos de saúde. Os dados geolocalizados (pontos cartesianos de Latitude e Longitude) das UBSs foram consumidos por via de malhas *Shapefile* e arquivos CSV públicos providos pela plataforma aberta **GeoSampa** da Prefeitura Municipal de São Paulo, bem como complementados pelo Sistema Busca Saúde da SMS. 

O **Peso Nodal ($w_v$)**, o cerne logístico que quantifica a gravidade do estrangulamento da unidade, exigiu fusão profunda de bases poligonais. As delimitações cartográficas em vetor das Áreas de Abrangência (AAUBS 2025 preliminar) foram descarregadas dos repositórios oficiais da Coordenação de Epidemiologia e Informação (CEInfo / SMS-SP). Em paralelo, extraíram-se os Microdados do **Instituto Brasileiro de Geografia e Estatística (IBGE - Censo Demográfico de 2022)**.

## 4.2 Arquitetura de Processamento (ETL e Spatial Joins)

O carregamento das malhas territoriais foi operado via bibliotecas espaciais da linguagem Python, promovendo geoprocessamento programático que descarta processos manuais enviesados. As subfases da higienização englobaram:

1.  **Limpeza Bidimensional de Identificadores**: 
    Equipamentos providos pelo GeoSampa, que eventualmente careciam de códigos unificados, foram pareados ao Cadastro Nacional de Estabelecimentos de Saúde (CNES). Unidades sem referencial físico fixo (ônibus ambulatoriais flutuantes) ou registros obsoletos sem população declarada foram podadas do espaço métrico.
2.  **Mesclagem Geoespacial Avançada (Spatial Join)**: 
    O Censo do IBGE mensura habitantes baseando-se no limite do Setor Censitário. Contudo, o SUS paulistano opera com a malha da AAUBS. Para sincronizar as escalas, scripts Python calcularam intersecções geométricas (*intersect/within*). A variável canônica censitária `V001AAUBS` (Total populacional de residentes fixos) incrustada nos polígonos foi unificada. A contagem sumariada dos setores censitários englobados por um polígono da CEInfo forjou a atribuição definitiva do peso habitacional do vértice. 
3.  **Configuração Restritiva das Arestas**:
    As distâncias ($w_e$) não foram instanciadas cegamente para todas as combinações ($N \times N$) possíveis do sistema (o que geraria lixo topológico atravessando a cidade inteira numa só via). Um limite territorial máximo ($R_{lim}$) determinou que arestas seriam constituídas unicamente se a métrica espacial comprovasse proximidade exequível entre bairros adjacentes (evitando que o sistema tente recomendar uma clínica a 50 km de distância só por ela estar vazia).

## 4.3 Limitações Declaradas da Matriz de Dados

O rigor metodológico exige a declaração de vieses emersos da estatística pública. Assumir a variável `V001AAUBS` como sinônimo irrestrito de lotação teórica implica assumir que:
*   A "capacidade" operacional interna ($C(v)$ - médicos plantonistas por metro quadrado) de todas as UBSs do recorte seja proporcional, o que não pôde ser atestado por inacessibilidade a bases fechadas do NUVIS-AB e e-SUS.
*   Cidadãos na condição de pessoas em situação de rua, bem como a gigantesca parcela flutuante diurna do trânsito laborativo de São Paulo, não constam na variável residente censitária noturna do IBGE, subestimando as regiões centrais em favor das periféricas. 

Estas limitações não invalidam o escopo da modelagem estatística de probabilidade de colapso da fila, mas reiteram o artefato como um preditor direcional estático perante anomalias cartográficas explícitas.
