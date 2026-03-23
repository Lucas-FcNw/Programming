"""
SPGraph - Interface Interativa com Streamlit
=============================================
Sistema de análise territorial de acesso à saúde nos distritos
de São Paulo, utilizando modelagem por grafos.

Uso:
    streamlit run app.py
"""

import sys
from pathlib import Path

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Adicionar a raiz do projeto ao path (para permitir import src.*)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.grafo import GrafoSP
from src.metricas import MetricasAcessibilidade

# ============================================================================
# Configuração da Página
# ============================================================================

st.set_page_config(
    page_title="SPGraph - Saúde Territorial",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: bold;
        color: #1f4e79;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# Cores por Zona
# ============================================================================

CORES_ZONA = {
    "Centro": "#e74c3c",
    "Norte": "#3498db",
    "Sul": "#2ecc71",
    "Leste": "#f39c12",
    "Oeste": "#9b59b6",
}

NOMES_SERVICO = {
    "hospital_sus": "🏥 Hospital (SUS)",
    "upa": "🚑 UPA",
    "ubs": "🏨 UBS",
}

# ============================================================================
# Cache de Dados
# ============================================================================

@st.cache_resource
def carregar_grafo():
    """Carrega e constrói o grafo (executado apenas uma vez)."""
    data_dir = Path(__file__).resolve().parent.parent / "data"
    return GrafoSP(data_dir=data_dir)


@st.cache_resource
def carregar_metricas(_grafo):
    """Inicializa o calculador de métricas."""
    return MetricasAcessibilidade(_grafo)


# ============================================================================
# Verificar se os dados existem
# ============================================================================

data_dir = Path(__file__).resolve().parent.parent / "data"
if not (data_dir / "distritos.json").exists():
    st.error("⚠️ Arquivos de dados não encontrados!")
    st.info(
        "Execute o script de geração de dados primeiro:\n\n"
        "```bash\npython gerar_dados.py\n```"
    )
    st.stop()

# Carregar dados
grafo = carregar_grafo()
metricas = carregar_metricas(grafo)

# ============================================================================
# Sidebar
# ============================================================================

st.sidebar.markdown("# 🏙️ SPGraph")
st.sidebar.markdown("**Análise Territorial de Saúde**")
st.sidebar.markdown("---")

# Seleção de distrito
nomes = grafo.get_nomes_ordenados()
opcoes_distrito = {nome: did for did, nome in nomes}

if "distrito_id" not in st.session_state:
    st.session_state["distrito_id"] = (
        opcoes_distrito.get("Sé", next(iter(opcoes_distrito.values())))
    )

nomes_lista = list(opcoes_distrito.keys())
nome_atual = grafo.get_nome(st.session_state["distrito_id"])
index_atual = nomes_lista.index(nome_atual) if nome_atual in nomes_lista else 0

distrito_selecionado_nome = st.sidebar.selectbox(
    "📍 Selecione o Distrito",
    options=nomes_lista,
    index=index_atual,
)
distrito_id = opcoes_distrito[distrito_selecionado_nome]
st.session_state["distrito_id"] = distrito_id

# Seleção de tipo de serviço
tipos_disponiveis = set(grafo.get_tipos_servico())
tipos_servico = [t for t in ["ubs", "upa", "hospital_sus"] if t in tipos_disponiveis]
if not tipos_servico:
    tipos_servico = sorted(tipos_disponiveis)

tipo_servico = st.sidebar.selectbox(
    "🏥 Tipo de Serviço",
    options=tipos_servico,
    format_func=lambda x: NOMES_SERVICO.get(x, str(x)),
)

# Estatísticas do grafo na sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Estatísticas do Grafo")
stats = grafo.estatisticas()
st.sidebar.metric("Vértices (Distritos)", stats["num_vertices"])
st.sidebar.metric("Arestas (Conexões)", stats["num_arestas"])
st.sidebar.metric("Grau Médio", stats["grau_medio"])
st.sidebar.metric("Densidade", stats["densidade"])
st.sidebar.metric("Conexo", "✅ Sim" if stats["eh_conexo"] else "❌ Não")

# ============================================================================
# Conteúdo Principal
# ============================================================================

st.markdown('<div class="main-header">SPGraph — Saúde Territorial em São Paulo</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">'
    'Análise de desigualdades no acesso a UBS, UPA e hospitais SUS por distrito · ODS 10 — Redução das Desigualdades'
    '</div>',
    unsafe_allow_html=True
)

# Abas
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Visão Geral",
    "📍 Análise Distrital",
    "📊 Cobertura",
    "ℹ️ Sobre"
])

# ============================================================================
# Tab 1: Visão Geral do Grafo
# ============================================================================

with tab1:
    st.subheader("Grafo dos Distritos de São Paulo")

    col_grafo, col_info = st.columns([3, 1])

    with col_grafo:
        # Mapa interativo com base cartográfica
        fig_map = go.Figure()

        # Arestas (linhas)
        for u, v, data in grafo.G.edges(data=True):
            lon_u, lat_u = grafo.distritos[u]["lon"], grafo.distritos[u]["lat"]
            lon_v, lat_v = grafo.distritos[v]["lon"], grafo.distritos[v]["lat"]
            fig_map.add_trace(go.Scattermap(
                lon=[lon_u, lon_v],
                lat=[lat_u, lat_v],
                mode="lines",
                line=dict(width=1, color="rgba(120,120,120,0.45)"),
                hoverinfo="skip",
                showlegend=False,
            ))

        # Nós (distritos)
        pops = [grafo.distritos[n]["populacao"] for n in grafo.G.nodes()]
        max_pop = max(pops) if pops else 1

        lons, lats, nomes_nos, cores_nos, tamanhos, custom = [], [], [], [], [], []
        for n in grafo.G.nodes():
            dno = grafo.distritos[n]
            lons.append(dno["lon"])
            lats.append(dno["lat"])
            nomes_nos.append(dno["nome"])
            cores_nos.append("gold" if n == distrito_id else CORES_ZONA.get(dno["zona"], "#999"))
            tamanhos.append(max(8, (dno["populacao"] / max_pop) * 24))
            custom.append([n, dno["nome"]])

        fig_map.add_trace(go.Scattermap(
            lon=lons,
            lat=lats,
            mode="markers",
            marker=dict(size=tamanhos, color=cores_nos, opacity=0.9),
            text=nomes_nos,
            customdata=custom,
            hovertemplate="<b>%{text}</b><br>ID: %{customdata[0]}<extra></extra>",
            name="Distritos",
        ))

        fig_map.update_layout(
            map=dict(
                style="open-street-map",
                center=dict(lat=-23.55, lon=-46.63),
                zoom=10,
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            title=f"Mapa Interativo dos Distritos — {distrito_selecionado_nome} selecionado",
            legend=dict(orientation="h", yanchor="bottom", y=0.01, xanchor="left", x=0.01),
            height=650,
        )

        evento = st.plotly_chart(
            fig_map,
            use_container_width=True,
            key="mapa_interativo_sp",
            on_select="rerun",
            selection_mode="points",
        )

        # Clique no mapa atualiza distrito selecionado
        pontos = []
        if evento is not None:
            if isinstance(evento, dict):
                pontos = evento.get("selection", {}).get("points", [])
            elif hasattr(evento, "selection") and hasattr(evento.selection, "points"):
                pontos = evento.selection.points

        if pontos:
            p = pontos[-1]
            customdata = p.get("customdata") if isinstance(p, dict) else getattr(p, "customdata", None)
            if customdata and len(customdata) >= 1:
                novo_id = int(customdata[0])
                if novo_id != st.session_state.get("distrito_id"):
                    st.session_state["distrito_id"] = novo_id
                    st.rerun()

    with col_info:
        st.markdown("### 📋 Distrito Selecionado")
        d = grafo.distritos[distrito_id]
        st.markdown(f"**{d['nome']}**")
        st.markdown(f"📍 Zona: **{d['zona']}**")
        st.markdown(f"👥 População: **{d['populacao']:,}**".replace(",", "."))
        st.markdown(f"🌐 Lat: {d['lat']:.4f} | Lon: {d['lon']:.4f}")

        grau = grafo.G.degree(distrito_id)
        st.markdown(f"🔗 Conexões: **{grau}**")

        # Serviços no distrito
        st.markdown("---")
        st.markdown("### 🏛️ Serviços Locais")
        servicos_local = grafo.contar_servicos_distrito(distrito_id)
        qtd_tipo = int(servicos_local.get(tipo_servico, 0))
        st.markdown(f"**Selecionado ({NOMES_SERVICO.get(tipo_servico, tipo_servico)}):** {qtd_tipo}")

        if servicos_local:
            st.markdown("**Todos os serviços no distrito:**")
            for tipo, qtd in sorted(servicos_local.items()):
                st.markdown(f"- {NOMES_SERVICO.get(tipo, tipo)}: **{qtd}**")
        else:
            st.warning("Nenhum serviço neste distrito")

        # Vizinhos
        st.markdown("---")
        st.markdown("### 🏘️ Distritos Vizinhos")
        vizinhos = list(grafo.G.neighbors(distrito_id))
        for v in sorted(vizinhos, key=lambda x: grafo.get_nome(x)):
            peso = grafo.G[distrito_id][v]["weight"]
            st.markdown(f"• {grafo.get_nome(v)} ({peso:.1f} km)")


# ============================================================================
# Tab 2: Análise Distrital
# ============================================================================

with tab2:
    st.subheader(f"Análise Distrital: {distrito_selecionado_nome} · {NOMES_SERVICO.get(tipo_servico, tipo_servico)}")

    # Referência territorial de cobertura
    servico, distancia, caminho = grafo.servico_mais_proximo(
        distrito_id, tipo_servico
    )
    comparacao = metricas.comparar_com_media(distrito_id, tipo_servico)

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📏 Distância de Referência",
            f"{comparacao['distancia_km']:.1f} km",
            delta=f"{comparacao['diferenca_distancia']:+.1f} km vs média da cidade",
            delta_color="inverse",
        )
    with col2:
        st.metric(
            "⭐ Índice de Cobertura",
            f"{comparacao['score']:.0f}/100",
            delta=f"{comparacao['diferenca_score']:+.1f} vs média",
        )
    with col3:
        st.metric(
            "🏆 Posição no Ranking",
            f"{comparacao['posicao_ranking']}º",
            delta=f"de {comparacao['total_distritos']}",
            delta_color="off",
        )
    with col4:
        cor_class = {
            "Acima da média": "🟢",
            "Na média": "🟡",
            "Abaixo da média": "🔴",
        }
        st.metric(
            "📊 Situação Relativa",
            f"{cor_class.get(comparacao['classificacao'], '')} {comparacao['classificacao']}",
        )

    st.markdown("---")

    col_contexto, col_vizinhos = st.columns(2)

    with col_contexto:
        st.markdown("#### 🧭 Contexto do Distrito")
        if servico:
            st.markdown(f"**Referência de cobertura:** {servico['nome']}")
            st.markdown(f"**Tipo:** {NOMES_SERVICO.get(servico['tipo'], servico['tipo'])}")
            st.markdown(f"**Distrito de referência:** {grafo.get_nome(servico['distrito_id'])}")

        if distancia == 0:
            st.success("✅ O distrito possui este serviço localmente.")
        else:
            st.info(f"Distância inter-distrital estimada até a referência: **{distancia:.1f} km**")

        st.markdown("---")
        st.markdown("#### 📊 Comparação com a Cidade")
        st.markdown(f"Média da cidade: **{comparacao['media_distancia_cidade']:.1f} km**")
        st.markdown(f"Índice médio de cobertura: **{comparacao['score_medio_cidade']:.0f}/100**")

    with col_vizinhos:
        st.markdown("#### 🏘️ Comparação com Distritos Vizinhos")
        vizinhos = sorted(list(grafo.G.neighbors(distrito_id)), key=lambda x: grafo.get_nome(x))

        if not vizinhos:
            st.info("Sem distritos vizinhos cadastrados para comparação.")
        else:
            dados_vizinhos = []
            for vid in vizinhos:
                comp_v = metricas.comparar_com_media(vid, tipo_servico)
                dados_vizinhos.append({
                    "Distrito": grafo.get_nome(vid),
                    "Zona": grafo.distritos[vid]["zona"],
                    "Índice": comp_v["score"],
                    "Distância Ref. (km)": comp_v["distancia_km"],
                })

            df_vizinhos = pd.DataFrame(dados_vizinhos).sort_values("Índice", ascending=False)
            st.dataframe(df_vizinhos, use_container_width=True, hide_index=True)

            media_vizinhos = float(df_vizinhos["Índice"].mean())
            delta_vizinhos = comparacao["score"] - media_vizinhos
            st.metric(
                "Diferença vs média dos vizinhos",
                f"{delta_vizinhos:+.1f}",
                delta=f"Índice do distrito: {comparacao['score']:.1f}",
                delta_color="normal",
            )

    # Gráfico de BFS
    st.markdown("---")
    st.markdown("#### 🔍 Análise BFS — Alcance por Profundidade")

    bfs_result = grafo.bfs(distrito_id, max_profundidade=5)

    # Contar nós por profundidade
    por_profundidade = {}
    for nid, prof in bfs_result.items():
        if prof not in por_profundidade:
            por_profundidade[prof] = 0
        por_profundidade[prof] += 1

    df_bfs = pd.DataFrame([
        {"Profundidade (saltos)": k, "Distritos Alcançáveis": v}
        for k, v in sorted(por_profundidade.items())
    ])

    fig_bfs = px.bar(
        df_bfs,
        x="Profundidade (saltos)",
        y="Distritos Alcançáveis",
        title=f"Distritos alcançáveis a partir de {distrito_selecionado_nome}",
        color="Distritos Alcançáveis",
        color_continuous_scale="Blues",
    )
    fig_bfs.update_layout(height=350)
    st.plotly_chart(fig_bfs, use_container_width=True)


# ============================================================================
# Tab 3: Ranking
# ============================================================================

with tab3:
    st.subheader(f"Ranking de Cobertura Territorial — {NOMES_SERVICO.get(tipo_servico, tipo_servico)}")

    ranking_df = metricas.ranking(tipo_servico)
    media = metricas.media_cidade(tipo_servico)

    # Métricas resumo
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📏 Distância Ref. Média", f"{media['media_distancia']:.1f} km")
    with col2:
        st.metric("⭐ Índice Médio", f"{media['score_medio']:.0f}/100")
    with col3:
        st.metric("📐 Mediana", f"{media['mediana_distancia']:.1f} km")
    with col4:
        st.metric("✅ Melhor", f"{media['melhor_distancia']:.1f} km")
    with col5:
        st.metric("❌ Pior", f"{media['pior_distancia']:.1f} km")

    st.markdown("---")

    # Top 10 mais acessíveis e menos acessíveis
    col_top, col_bottom = st.columns(2)

    with col_top:
        st.markdown("#### ✅ Top 10 — Melhor Cobertura")
        top10 = ranking_df.head(10)

        fig_top = px.bar(
            top10,
            x="distrito",
            y="score",
            color="zona",
            color_discrete_map=CORES_ZONA,
            title="Distritos com melhor cobertura territorial",
            labels={"score": "Score", "distrito": "Distrito", "zona": "Zona"},
        )
        fig_top.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_top, use_container_width=True)

    with col_bottom:
        st.markdown("#### ❌ Top 10 — Menor Cobertura")
        bottom10 = ranking_df.tail(10).sort_values("score", ascending=True)

        fig_bottom = px.bar(
            bottom10,
            x="distrito",
            y="score",
            color="zona",
            color_discrete_map=CORES_ZONA,
            title="Distritos com menor cobertura territorial",
            labels={"score": "Score", "distrito": "Distrito", "zona": "Zona"},
        )
        fig_bottom.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_bottom, use_container_width=True)

    # Distritos com baixa cobertura
    st.markdown("---")
    st.markdown("#### 🚨 Distritos com Menor Cobertura")
    st.markdown("Distritos no top 20% com maior distância de referência territorial.")

    isolados = metricas.distritos_isolados(tipo_servico, percentil=0.8)
    if isolados:
        df_isolados = pd.DataFrame(isolados)
        df_isolados.columns = [
            "ID", "Distrito", "Zona", "População",
            "Distância de Referência (km)", "Índice"
        ]
        st.dataframe(
            df_isolados[["Distrito", "Zona", "População", "Distância de Referência (km)", "Índice"]],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Todos os distritos têm acesso razoável.")

    # Gráfico de dispersão: População vs Score
    st.markdown("---")
    st.markdown("#### 📈 População vs. Cobertura Territorial")

    fig_scatter = px.scatter(
        ranking_df,
        x="populacao",
        y="score",
        color="zona",
        color_discrete_map=CORES_ZONA,
        size="populacao",
        hover_name="distrito",
        title=f"Relação entre população e índice de cobertura ({tipo_servico})",
        labels={
            "populacao": "População",
            "score": "Índice de Cobertura",
            "zona": "Zona"
        },
    )
    fig_scatter.add_hline(
        y=media["score_medio"],
        line_dash="dash",
        line_color="red",
        annotation_text=f"Média: {media['score_medio']:.0f}",
    )
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Tabela completa
    st.markdown("---")
    st.markdown("#### 📋 Ranking Completo")

    # Destacar distrito selecionado
    ranking_display = ranking_df.copy()
    ranking_display.columns = [
        "Posição", "ID", "Distrito", "Zona",
        "População", "Distância de Referência (km)", "Índice"
    ]

    st.dataframe(
        ranking_display[["Posição", "Distrito", "Zona", "População",
                         "Distância de Referência (km)", "Índice"]],
        use_container_width=True,
        hide_index=True,
        height=400,
    )


# ============================================================================
# Tab 4: Sobre
# ============================================================================

with tab4:
    st.subheader("Sobre o Projeto")

    col_about1, col_about2 = st.columns(2)

    with col_about1:
        st.markdown("""
        ### 🏙️ SPGraph

        Sistema interativo que modela a cidade de São Paulo como um **grafo**
        para analisar desigualdades territoriais no acesso à saúde.

        ### 🎯 Objetivo

        Desenvolver um sistema funcional que utilize **modelagem por grafos**
        para analisar e visualizar desigualdades no acesso a **UBS, UPA e hospitais SUS**
        nos distritos da cidade de São Paulo.

        ### 🌍 ODS 10 — Redução das Desigualdades

        A desigualdade urbana se manifesta no acesso desigual a serviços de saúde.
        Distritos periféricos tendem a apresentar menor cobertura relativa
        de UBS, UPA e hospitais SUS quando comparados a regiões centrais.

        O projeto busca identificar padrões de cobertura territorial, destacar
        regiões com menor acesso e fornecer uma visualização comparativa
        entre distritos.
        """)

    with col_about2:
        st.markdown("""
        ### 📐 Modelagem em Grafos

        - **Vértices:** Distritos administrativos de São Paulo
        - **Arestas:** Conexões entre distritos geograficamente vizinhos
        - **Peso:** Distância estimada entre centros geográficos (km)
        - **Tipo:** Grafo não direcionado e ponderado

        ### 🔬 Algoritmos Implementados

        - **Distâncias ponderadas:** Indicador inter-distrital de cobertura
        - **BFS:** Busca em largura para análise de alcance
        - **Centralidade de Grau:** Identificação de distritos mais conectados
        - **Centralidade de Proximidade:** Eficiência territorial de acesso
        - **Centralidade de Intermediação:** Importância como ponto de passagem

        ### 🏛️ Serviços Analisados

        - 🏥 **Hospitais (SUS)** — Rede hospitalar pública
        - 🚑 **UPA** — Unidades de Pronto Atendimento
        - 🏨 **UBS** — Unidades Básicas de Saúde
        """)

    st.markdown("---")

    st.markdown("""
    ### 🛠️ Tecnologias

    | Componente | Tecnologia |
    |---|---|
    | Linguagem | Python 3.11+ |
    | Grafos | NetworkX |
    | Interface | Streamlit |
    | Visualização | Matplotlib + Plotly |
    | Dados | JSON |

    ### 👥 Equipe

    | Nome | RA |
    |---|---|
    | Lucas Fernandes | 10419400 |
    | Lendy Naiara Pacheco | 10428525 |
    | Anna Luiza Santos | 10417401 |
    """)
