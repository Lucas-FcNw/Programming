# Projeto

## Nome do Projeto
**SPGraph — Diagnóstico de Fragilidade Topológica, Gargalos Invisíveis e Efeito Cascata em Redes de UBSs de São Paulo**

---

# Tema

Desenvolvimento de um modelo computacional baseado em Teoria dos Grafos para identificar vulnerabilidades topológicas ocultas ("gargalos invisíveis") e simular o efeito cascata (efeito dominó por sobrecarga operacional) na rede de 454 Unidades Básicas de Saúde (UBSs) do município de São Paulo em cenários de rotina diária.

---

# Pergunta Central de Pesquisa

> **Se uma Unidade Básica de Saúde (UBS) de São Paulo colapsar hoje em sua operação cotidiana (por reforma predial, déficit de médicos, queda de energia ou alagamento), quais comunidades periféricas ficam totalmente isoladas de atendimento e quais UBSs vizinhas quebram juntas em efeito dominó por sobrecarga?**

---

# Objetivo Geral

Desenvolver um sistema computacional baseado em Teoria dos Grafos que modele as 454 UBSs georreferenciadas de São Paulo como uma malha conectada topograficamente, identificando pontos únicos de falha via Algoritmo de Tarjan e simulando o deslocamento populacional e o colapso em cascata via Busca em Largura (BFS) acoplada ao Modelo Gravitacional de Huff/3SFCA e à regra operacional de 70% Demanda Programada / 30% Demanda Espontânea do SUS.

---

# Objetivos Específicos

- Modelar as **454 UBSs reais de São Paulo** (base CNES/SMS-SP) como **vértices ($V$)** dotados de **Demanda Base Territorial ($D_v^0$)** e **Capacidade Instalada ($C_v$)** segundo a regra 70/30 da Atenção Básica.
- Construir as **882 conexões geográficas e topográficas ($E$)** via Grafo de Proximidade de Gabriel restrito às fronteiras distritais (`São Paulo.kml`), ponderadas pela distância geodésica e pela impedância de declividade de Tobler (1993).
- Implementar o **Algoritmo de Tarjan (1972)** sobre Busca em Profundidade (DFS) em $\mathcal{O}(|V| + |E|)$ para detectar os **21 vértices de articulação** ("gargalos invisíveis" que parecem verdes numa planilha isolada, mas partem a rede ao meio) e as **19 pontes críticas**.
- Implementar o motor de **Simulação de Colapso e Efeito Cascata em Camadas via BFS**, redistribuindo a demanda desassistida entre UBSs vizinhas pelo **Modelo Gravitacional Probabilístico de Huff (1963) e 3SFCA (Wan, Zou & Sternberg, 2012)** e verificando o estouro da margem de 30% de demanda espontânea (Motter & Lai, 2002; Wang et al., 2008).
- Comparar o diagnóstico topológico do grafo com a análise tradicional por tabelas/listas estáticas e disponibilizar visualização interativa em Streamlit.

---

# Modelagem em Teoria dos Grafos

## Estrutura do Grafo $G = (V, E, W_V, W_E)$

- **Vértices ($|V| = 454$):** Unidades Básicas de Saúde (UBSs) reais do município de São Paulo.
  - Atributos de cada vértice $v$: Demanda Base ($D_v^0$), Capacidade Total ($C_v$), Cota Programada ($70\%$), Folga Operacional Espontânea ($F_v \le 30\%$), Altitude ($m$) e Status na Tabela Isolada.
- **Arestas ($|E| = 882$):** Conexões diretas de vizinhança territorial (Grafo de Gabriel restrito a distritos contíguos do GeoSampa).
- **Peso das Arestas ($w(u, v) = d_{\text{topo}}(u, v)$):** Impedância topográfica em km (distância Haversine ajustada pela declividade via Função de Tobler).

## Motores Algorítmicos

1. **Caça-Gargalos Estruturais (DFS + Algoritmo de Tarjan):** Detecta em $\mathcal{O}(|V| + |E|)$ os vértices de articulação e pontes que isolam bairros inteiros.
2. **Simulação de Colapso e Cascata em Dominó (BFS em Camadas + Modelo Gravitacional):**
   - Calcula a fração de deslocamento populacional $W_{uv} = \frac{C_v^\alpha \cdot d_{\text{topo}}(u,v)^{-\beta}}{\sum_z C_z^\alpha \cdot d_{\text{topo}}(u,z)^{-\beta}}$ para cada vizinha ativa;
   - Se a demanda transferida $\Delta D_{u \to v}$ ultrapassar a folga operacional $F_v \le 0{,}30 \cdot C_v$, a UBS vizinha entra em colapso e propaga o excedente para a camada seguinte do BFS.

---

# Equipe
- `Lucas Fernandes de Camargo — RA 10419400`
- `Lendy Naiara Carpio Pacheco — RA 10428525`
- `Anna Luiza Stella Santos — RA 10417401`
