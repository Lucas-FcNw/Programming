# 🏥 SPGraph — Vulnerabilidades Ocultas e Efeito Cascata na Rede de UBSs de São Paulo

Sistema computacional baseado em **Teoria dos Grafos** para diagnóstico de **fragilidade topológica ("gargalos invisíveis")** e simulação de **colapso em cascata (efeito dominó por sobrecarga)** na malha de **454 Unidades Básicas de Saúde (UBSs)** do município de São Paulo.

---

## 🎯 Pergunta Central do Projeto

> **Se uma UBS colapsar hoje na operação do dia a dia, quem fica totalmente isolado de atendimento e quais UBSs vizinhas vão quebrar junto por sobrecarga?**

Por que uma lista ou planilha comum da gestão pública não resolve isso?
1. **O Ponto Cego ("Gargalo Invisível"):** Na tabela isolada, uma UBS com $70\%$ de ocupação aparece como **Verde (Ótimo)**. Porém, na topologia do grafo, ela pode ser um **Vértice de Articulação** (Tarjan): a única ponte geográfica que liga bairros periféricos ao restante da rede. Se ela cair, parte a rede ao meio. Na malha real de SP, **20 dos 21 vértices de articulação aparentam estar "Verdes" na tabela isolada**.
2. **O Efeito Dominó (Cascata por Sobrecarga):** Pela diretriz organizacional do SUS (*Cadernos de Atenção Básica n. 28*), **70% da capacidade** de uma UBS é comprometida com a **Demanda Programada** dos moradores da própria região, restando no máximo **30% de folga operacional** para **Demanda Espontânea** e pacientes de fora. Quando uma UBS falha e joga sua população para as vizinhas, a vizinha mais próxima estoura sua margem de 30% e colapsa também, iniciando uma reação em cadeia.

---

## 📐 Modelagem em Teoria dos Grafos ($G = (V, E, W_V, W_E)$)

- **Vértices ($|V| = 454$ UBSs reais georreferenciadas):** Extraídas da base oficial CNES / SMS-SP (`data/deinfosacadsau2014.csv`). Cada vértice guarda:
  - `demanda_base` ($D_v^0$): População adscrita estimada por tesselação de Voronoi sobre os polígonos oficiais do GeoSampa (`data/São Paulo.kml`) e população do Censo/MSP (`data/evolucao_msp_pop_sexo_idade.csv`);
  - `capacidade` ($C_v$): Capacidade total instalada da UBS;
  - `cota_programada_70` ($0{,}70 \cdot C_v$) e `folga_operacional` ($F_v \le 0{,}30 \cdot C_v$).
- **Arestas ($|E| = 882$ conexões topográficas locais):** Construídas pelo **Grafo de Proximidade de Gabriel** restrito às fronteiras distritais contíguas do `São Paulo.kml`.
- **Peso das Arestas ($d_{\text{topo}}(u, v)$):** Distância geodésica Haversine ajustada pela **Impedância Topográfica de Declividade** (*Tobler's Hiking Function*, Tobler, 1993).

---

## 🔬 Motores Algorítmicos Implementados

1. **Motor 1 — Caça-Gargalos Estruturais (`src/vulnerabilidade.py`):**
   - **Busca em Profundidade (DFS) + Algoritmo de Tarjan (1972)** em $\mathcal{O}(|V| + |E|)$ com vetores `disc[u]` e `low[u]`;
   - Detecta os **21 Vértices de Articulação** e as **19 Pontes Críticas** da malha de UBSs de São Paulo.
2. **Motor 2 — Movimento da População e Simulação de Cascata em Camadas (`src/vulnerabilidade.py`):**
   - **Divisão Gravitacional da Demanda (Huff, 1963 + 3SFCA de Wan, Zou & Sternberg, 2012 + Stacherl & Sauzet, 2023):**
     $$W_{uv} = \frac{C_v^\alpha \cdot d_{\text{topo}}(u, v)^{-\beta}}{\sum_{z \in N_{\text{ativas}}(u)} C_z^\alpha \cdot d_{\text{topo}}(u, z)^{-\beta}}$$
   - **Propagação em Camadas via Busca em Largura (BFS) (Motter & Lai, 2002; Crucitti et al., 2004; Wang et al., 2008):**
     Dispara um BFS em camadas ($k = 1, 2, \dots$) a partir da UBS desativada. Se a carga transferida $\Delta D_{u \to v} = D_u \cdot W_{uv}$ ultrapassar a folga operacional $F_v \le 30\%$ da vizinha $v$, esta entra em colapso e repassa o excedente para a camada seguinte do BFS.

---

## 🚀 Como Executar

```bash
# 1. Gerar os JSONs das 454 UBSs e 882 arestas topográficas
python3 gerar_dados.py

# 2. Gerar o arquivo padronizado grafo.txt (Tipo 3: 454 vértices, 882 arestas)
python3 gerar_grafo_txt.py

# 3. Executar o Dashboard Interativo Streamlit
streamlit run src/app.py
```

---

## 👥 Equipe
- **Lucas Fernandes de Camargo** — RA 10419400
- **Lendy Naiara Carpio Pacheco** — RA 10428525
- **Anna Luiza Stella Santos** — RA 10417401
