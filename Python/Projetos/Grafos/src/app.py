"""
SPGraph - Interface Interativa com Streamlit
============================================
Sistema de diagnóstico de fragilidade topológica, gargalos invisíveis
(Tarjan) e simulação de efeito cascata em dominó (BFS + Modelo Gravitacional
de Huff/3SFCA + Regra 70/30 do SUS) na malha de 454 UBSs de São Paulo.

Uso:
    streamlit run src/app.py
"""

import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.grafo import GrafoSP
from src.metricas import MetricasAcessibilidade
from src.vulnerabilidade import AnaliseVulnerabilidade

st.set_page_config(
    page_title="SPGraph - Fragilidade Topológica e Efeito Cascata (UBSs SP)",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: bold;
        color: #1f4e79;
        margin-bottom: 0.3rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

CORES_ZONA = {
    "Centro": "#e74c3c",
    "Norte": "#3498db",
    "Sul": "#2ecc71",
    "Leste": "#f39c12",
    "Oeste": "#9b59b6",
}


def normalizar_nome(valor: str) -> str:
    texto = str(valor).strip().upper()
    return "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )


def hex_para_rgba(cor_hex: str, alpha: float) -> str:
    cor = cor_hex.lstrip("#")
    if len(cor) != 6:
        return f"rgba(120,120,120,{alpha})"
    r = int(cor[0:2], 16)
    g = int(cor[2:4], 16)
    b = int(cor[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


@st.cache_resource
def carregar_grafo():
    data_dir = Path(__file__).resolve().parent.parent / "data"
    return GrafoSP(data_dir=data_dir)


@st.cache_resource
def carregar_metricas(_grafo):
    return MetricasAcessibilidade(_grafo)


@st.cache_resource
def carregar_vulnerabilidade(_grafo):
    return AnaliseVulnerabilidade(_grafo)


@st.cache_data
def carregar_poligonos_kml(caminho_kml: Path) -> dict[str, list[list[tuple[float, float]]]]:
    if not caminho_kml.exists():
        return {}
    ns = {"kml": "http://www.opengis.net/kml/2.2"}
    root = ET.parse(caminho_kml).getroot()
    poligonos: dict[str, list[list[tuple[float, float]]]] = {}

    for placemark in root.findall(".//kml:Placemark", ns):
        nome = placemark.findtext("kml:name", default="", namespaces=ns)
        nome_norm = normalizar_nome(nome)
        aneis: list[list[tuple[float, float]]] = []
        for coord_node in placemark.findall(
            ".//kml:outerBoundaryIs/kml:LinearRing/kml:coordinates", ns
        ):
            txt = (coord_node.text or "").strip()
            pontos: list[tuple[float, float]] = []
            for token in txt.replace("\n", " ").split():
                partes = token.split(",")
                if len(partes) >= 2:
                    try:
                        pontos.append((float(partes[0]), float(partes[1])))
                    except ValueError:
                        continue
            if len(pontos) >= 3:
                passo = max(1, len(pontos) // 250)
                simplificado = pontos[::passo]
                if simplificado[0] != simplificado[-1]:
                    simplificado.append(simplificado[0])
                aneis.append(simplificado)
        if aneis:
            poligonos[nome_norm] = aneis
    return poligonos


def construir_mapa(
    grafo: GrafoSP,
    poligonos_kml: dict,
    ubs_selecionada_id: int,
    ids_destaque: set[int] | None = None,
    cor_destaque: str = "#e74c3c",
    ids_removidos: set[int] | None = None,
    ids_cascata: set[int] | None = None,
    modo: str = "cidade_inteira",
    titulo: str = "Malha Topológica de UBSs — São Paulo",
    altura: int = 600,
) -> go.Figure:
    fig = go.Figure()
    if ids_destaque is None:
        ids_destaque = set()
    if ids_removidos is None:
        ids_removidos = set()
    if ids_cascata is None:
        ids_cascata = set()

    # Camada de fundo: polígonos dos 96 distritos do KML
    all_lons, all_lats = [], []
    for nome_norm, aneis in poligonos_kml.items():
        for anel in aneis:
            xs = [p[0] for p in anel]
            ys = [p[1] for p in anel]
            all_lons.extend(xs)
            all_lats.extend(ys)
            fig.add_trace(go.Scattergl(
                x=xs, y=ys,
                mode="lines",
                fill="toself",
                fillcolor="rgba(229,231,235,0.25)",
                line=dict(color="rgba(156,163,175,0.45)", width=0.8),
                hoverinfo="skip",
                showlegend=False,
            ))

    # Arestas entre UBSs
    edge_x, edge_y = [], []
    for u, v in grafo.G.edges():
        if u in grafo.distritos and v in grafo.distritos:
            du, dv = grafo.distritos[u], grafo.distritos[v]
            edge_x.extend([du["lon"], dv["lon"], None])
            edge_y.extend([du["lat"], dv["lat"], None])

    fig.add_trace(go.Scattergl(
        x=edge_x, y=edge_y,
        mode="lines",
        line=dict(color="rgba(55,65,81,0.38)", width=0.9),
        hoverinfo="skip",
        name="Arestas Topográficas (Gabriel)",
        showlegend=True,
    ))

    # Vértices (454 UBSs)
    vx, vy, vcustom, vcores, vsizes = [], [], [], [], []
    for uid in grafo.G.nodes():
        u = grafo.distritos[uid]
        vx.append(u["lon"])
        vy.append(u["lat"])
        vcustom.append([
            uid,
            u["nome"],
            u.get("distrito", ""),
            u["zona"],
            u.get("demanda_base", 0),
            u.get("capacidade", 0),
            u.get("folga_operacional", 0),
            u.get("status_tabela_isolada", ""),
        ])

        if uid in ids_removidos:
            vcores.append("#111827")
            vsizes.append(11)
        elif uid in ids_cascata:
            vcores.append("#dc2626")
            vsizes.append(10)
        elif uid in ids_destaque:
            vcores.append(cor_destaque)
            vsizes.append(10)
        elif uid == ubs_selecionada_id:
            vcores.append("#facc15")
            vsizes.append(11)
        else:
            vcores.append(CORES_ZONA.get(u["zona"], "#6b7280"))
            vsizes.append(6)

    fig.add_trace(go.Scattergl(
        x=vx, y=vy,
        mode="markers",
        marker=dict(size=vsizes, color=vcores, line=dict(width=0.8, color="#1f2937"), opacity=0.95),
        customdata=vcustom,
        hovertemplate=(
            "<b>%{customdata[1]}</b> (ID=%{customdata[0]})<br>"
            "Distrito: %{customdata[2]} · Zona: %{customdata[3]}<br>"
            "Demanda Base: %{customdata[4]:,} hab · Capacidade: %{customdata[5]:,}<br>"
            "Folga Espontânea (≤30%): %{customdata[6]:,} vagas<br>"
            "Tabela Isolada: %{customdata[7]}<extra></extra>"
        ),
        name="UBSs (Vértices)",
        showlegend=True,
    ))

    if modo == "foco_local" and ubs_selecionada_id in grafo.distritos:
        ids_foco = [ubs_selecionada_id] + list(grafo.G.neighbors(ubs_selecionada_id))
        xs_zoom = [grafo.distritos[i]["lon"] for i in ids_foco if i in grafo.distritos]
        ys_zoom = [grafo.distritos[i]["lat"] for i in ids_foco if i in grafo.distritos]
        margem_lon = max(0.025, (max(xs_zoom) - min(xs_zoom)) * 0.5)
        margem_lat = max(0.020, (max(ys_zoom) - min(ys_zoom)) * 0.5)
    else:
        xs_zoom = all_lons if all_lons else vx
        ys_zoom = all_lats if all_lats else vy
        margem_lon = 0.04
        margem_lat = 0.03

    lat_media = float(np.mean(ys_zoom)) if ys_zoom else -23.55
    fator_geo = float(1.0 / np.cos(np.deg2rad(lat_media)))

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=0, r=0, t=40, b=0),
        title=titulo,
        height=altura,
        xaxis=dict(
            showgrid=False, zeroline=False, showticklabels=False,
            range=[min(xs_zoom) - margem_lon, max(xs_zoom) + margem_lon],
        ),
        yaxis=dict(
            showgrid=False, zeroline=False, showticklabels=False,
            scaleanchor="x", scaleratio=fator_geo,
            range=[min(ys_zoom) - margem_lat, max(ys_zoom) + margem_lat],
        ),
    )
    return fig


data_dir = Path(__file__).resolve().parent.parent / "data"
grafo = carregar_grafo()
metricas = carregar_metricas(grafo)
vuln = carregar_vulnerabilidade(grafo)
poligonos_kml = carregar_poligonos_kml(data_dir / "São Paulo.kml")

# Sidebar
st.sidebar.markdown("# 🏥 SPGraph — UBSs")
st.sidebar.markdown("**Fragilidade Topológica & Efeito Cascata**")
st.sidebar.markdown("---")

nomes = grafo.get_nomes_ordenados()
opcoes_ubs = {f"{nome} (#{did})": did for did, nome in nomes}
nomes_lista = list(opcoes_ubs.keys())

ubs_sel_label = st.sidebar.selectbox("📍 Selecione uma UBS", options=nomes_lista, index=0)
ubs_id = opcoes_ubs[ubs_sel_label]

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Estatísticas da Malha")
stats = grafo.estatisticas()
st.sidebar.metric("Vértices (UBSs Reais)", stats["num_vertices"])
st.sidebar.metric("Arestas Topográficas", stats["num_arestas"])
st.sidebar.metric("Grau Médio", stats["grau_medio"])
st.sidebar.metric("Demanda Total (SP)", f"{stats['demanda_total']:,}".replace(",", "."))
st.sidebar.metric("Folga Total (Regra ≤30%)", f"{stats['folga_total']:,}".replace(",", "."))

st.markdown(
    '<div class="main-header">SPGraph — Vulnerabilidades Ocultas e Efeito Cascata na Rede de UBSs</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">'
    '454 UBSs georreferenciadas · 882 conexões topográficas · Algoritmo de Tarjan (DFS) · '
    'Simulação de Cascata via BFS + Modelo Gravitacional (Huff / 3SFCA) + Regra 70/30 do SUS'
    '</div>',
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ Malha de UBSs",
    "🔴 Gargalos Invisíveis (Tarjan)",
    "💥 Simulação de Colapso & Cascata (BFS)",
    "⚖️ Divisão Gravitacional vs. Igualitária",
    "ℹ️ Metodologia & Referências",
])

with tab1:
    col_mapa, col_info = st.columns([3, 1])
    with col_mapa:
        modo_m = st.radio("Zoom", ["Cidade inteira", "Foco local na UBS"], horizontal=True)
        fig = construir_mapa(
            grafo, poligonos_kml, ubs_id,
            modo="foco_local" if modo_m == "Foco local na UBS" else "cidade_inteira",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        u = grafo.distritos[ubs_id]
        st.markdown(f"### 🏥 {u['nome']}")
        st.markdown(f"- **CNES:** `{u.get('cnes', 'N/D')}`")
        st.markdown(f"- **Distrito:** {u.get('distrito', '')} ({u['zona']})")
        st.markdown(f"- **Altitude est.:** {u.get('altitude_m', 760)} m")
        st.markdown(f"- **Demanda Base ($D_v^0$):** {u['demanda_base']:,} hab.")
        st.markdown(f"- **Capacidade Total ($C_v$):** {u['capacidade']:,} hab.")
        st.markdown(f"- **Cota Programada (70%):** {u['cota_programada_70']:,} vagas")
        st.markdown(f"- **Folga Espontânea (≤30%):** {u['folga_operacional']:,} vagas ({u['folga_percentual']}%)")
        st.markdown(f"- **Status na Tabela Isolada:** **{u.get('status_tabela_isolada', '')}**")
        st.markdown("---")
        st.markdown("### 🔗 UBSs Vizinhas Conectadas")
        for vid in grafo.G.neighbors(ubs_id):
            aresta = grafo.G[ubs_id][vid]
            st.markdown(
                f"• **{grafo.get_nome(vid)}** — {aresta['weight']:.2f} km "
                f"(topo: {aresta.get('impedancia_topografica_km', aresta['weight']):.2f} km)"
            )

with tab2:
    st.subheader("Caça-Gargalos Estruturais: Vértices de Articulação e Pontes (Algoritmo de Tarjan)")
    st.markdown("""
    > **O Ponto Cego da Tabela Comum ("Gargalo Invisível"):** Na gestão tradicional por listas/planilhas, uma UBS com ocupação equilibrada aparece como **Verde (Ótimo)**. Porém, no grafo topológico, ela pode ser um **Vértice de Articulação**: a única ponte que conecta bairros periféricos ao restante da rede. Se ela cair, parte a rede ao meio!
    """)
    arts = vuln.vertices_articulacao()
    ids_art = {a["ubs_id"] for a in arts}
    col_a1, col_a2 = st.columns([2, 1])
    with col_a1:
        fig_art = construir_mapa(
            grafo, poligonos_kml, ubs_id,
            ids_destaque=ids_art,
            cor_destaque="#e74c3c",
            titulo=f"{len(arts)} Vértices de Articulação Identificados por Tarjan (O(|V|+|E|))",
        )
        st.plotly_chart(fig_art, use_container_width=True)
    with col_a2:
        df_art = pd.DataFrame(arts)[[
            "nome_ubs", "distrito_adm", "zona", "status_tabela_isolada",
            "ubs_isoladas_se_cair", "pop_isolada_se_cair"
        ]]
        df_art.columns = ["UBS", "Distrito", "Zona", "Na Tabela Comum", "UBSs Isoladas", "Pop. Isolada"]
        st.dataframe(df_art, use_container_width=True, hide_index=True, height=520)

    st.markdown("---")
    st.subheader("🌉 Pontes Críticas (Tarjan)")
    df_pontes = pd.DataFrame(vuln.pontes_criticas())
    st.dataframe(df_pontes, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("💥 Simulação de Colapso e Efeito Cascata em Dominó (BFS + Modelo Gravitacional)")
    opcoes_rem = {f"{d['nome']} ({d.get('distrito', '')} - #{did})": did for did, d in grafo.distritos.items()}
    selecionadas = st.multiselect(
        "Selecione uma ou mais UBSs para desativar (Camada 0 do BFS):",
        options=list(opcoes_rem.keys()),
        default=[opcoes_rem[k] for k in list(opcoes_rem.keys()) if opcoes_rem[k] == 328][:1] and [k for k, v in opcoes_rem.items() if v == 328],
    )
    ids_rem = [opcoes_rem[k] for k in selecionadas]

    if ids_rem:
        casc = vuln.simular_cascata_bfs(ids_rem)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("UBSs Desativadas (Gatilho)", casc["num_iniciais"])
        c2.metric("UBSs Derrubadas em Cascata", f"+{casc['num_colapsadas_cascata']}")
        c3.metric("Saltos Máximos no BFS", f"{casc['saltos_maximos_bfs']} camada(s)")
        c4.metric("Demanda Isolada/Sem Vaga", f"{casc['demanda_isolada_sem_atendimento']:,}".replace(",", "."))

        fig_casc = construir_mapa(
            grafo, poligonos_kml, ubs_id,
            ids_removidos=set(ids_rem),
            ids_cascata=set(casc["ids_colapsadas_cascata"]),
            titulo="Propagação Espacial do Colapso (Preto = Falha Inicial | Vermelho = Colapso em Cascata)",
            altura=500,
        )
        st.plotly_chart(fig_casc, use_container_width=True)

        for camada in casc["camadas_bfs"]:
            with st.expander(
                f"Camada BFS {camada['camada']} — "
                f"{camada['num_ubs_atingidas']} UBS(s) vizinhas receberam pacientes · "
                f"{camada['num_novos_colapsos']} novo(s) colapso(s) por estouro dos 30%",
                expanded=True,
            ):
                df_fl = pd.DataFrame(camada["fluxos"])
                st.dataframe(df_fl, use_container_width=True, hide_index=True)

with tab4:
    st.subheader("⚖️ Por que não dividir 25% para cada vizinha? (Modelo Gravitacional vs. Divisão Igualitária)")
    comp = vuln.comparar_divisao_demanda(ubs_id)
    st.markdown(
        f"**UBS analisada:** `{comp['ubs_nome']}` ({comp['distrito']} - {comp['zona']}) · "
        f"**Demanda a redistribuir:** `{comp['demanda_remanejada']:,}` pacientes · "
        f"**Vizinhas conectadas:** `{comp['num_vizinhos']}`"
    )
    df_comp = pd.DataFrame(comp["vizinhos"])[[
        "vizinho_nome", "distrito", "distancia_km", "impedancia_topografica_km",
        "capacidade", "folga_operacional",
        "percentual_divisao_igual", "pacientes_divisao_igual", "colapsa_na_divisao_igual",
        "percentual_gravitacional", "pacientes_modelo_gravitacional", "colapsa_no_gravitacional",
    ]]
    df_comp.columns = [
        "UBS Vizinha", "Distrito", "Dist. (km)", "Imped. Topo (km)",
        "Capacidade Total", "Folga 30% (SUS)",
        "% Igual (1/k)", "Pacientes (1/k)", "Colapsa (1/k)?",
        "% Gravitacional (Huff)", "Pacientes (Huff)", "Colapsa (Huff)?",
    ]
    st.dataframe(df_comp, use_container_width=True, hide_index=True)

with tab5:
    st.subheader("Fundamentação Científica Implementada")
    st.markdown("""
    1. **Regra 70% Demanda Programada / 30% Demanda Espontânea (SUS):** *Cadernos de Atenção Básica n. 28* (Ministério da Saúde, 2011).
    2. **Redistribuição Gravitacional entre UBSs Vizinhas:** Modelo Probabilístico de Huff (1963) e método *Three-Step Floating Catchment Area* (3SFCA) de Wan, Zou & Sternberg (2012), revisado por Stacherl & Sauzet (2023).
    3. **Efeito Cascata por Sobrecarga Local:** Motter & Lai (2002), Crucitti, Latora & Marchiori (2004) e Wang et al. (2008).
    4. **Gargalos Topológicos Invisíveis:** Algoritmo de Tarjan (1972) via Busca em Profundidade (DFS) em $\\mathcal{O}(|V| + |E|)$.
    """)
