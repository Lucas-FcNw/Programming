"""
SPGraph - Interface Interativa com Streamlit
=============================================
Sistema de análise de vulnerabilidade territorial da rede de saúde
de São Paulo, utilizando modelagem por grafos.

Uso:
    streamlit run src/app.py
"""

import sys
from pathlib import Path
import xml.etree.ElementTree as ET
import unicodedata

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Adicionar a raiz do projeto ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.grafo import GrafoSP
from src.metricas import MetricasAcessibilidade
from src.vulnerabilidade import AnaliseVulnerabilidade

# ============================================================================
# Configuração da Página
# ============================================================================

st.set_page_config(
    page_title="SPGraph - Vulnerabilidade da Rede de Saúde",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
# Constantes
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
# Funções Utilitárias
# ============================================================================


def normalizar_nome(valor: str) -> str:
    texto = str(valor).strip().upper()
    texto = "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )
    return texto


def hex_para_rgba(cor_hex: str, alpha: float) -> str:
    cor = cor_hex.lstrip("#")
    if len(cor) != 6:
        return f"rgba(120,120,120,{alpha})"
    r = int(cor[0:2], 16)
    g = int(cor[2:4], 16)
    b = int(cor[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def area_anel(anel: list[tuple[float, float]]) -> float:
    """Área assinada aproximada de anel (lon/lat)."""
    if len(anel) < 3:
        return 0.0
    a = 0.0
    for i in range(len(anel) - 1):
        x1, y1 = anel[i]
        x2, y2 = anel[i + 1]
        a += (x1 * y2) - (x2 * y1)
    return a / 2.0


def ponto_em_poligono(x: float, y: float, poligono: list[tuple[float, float]]) -> bool:
    """Teste simples de ponto no polígono (ray casting)."""
    dentro = False
    n = len(poligono)
    if n < 3:
        return False
    j = n - 1
    for i in range(n):
        xi, yi = poligono[i]
        xj, yj = poligono[j]
        cond = ((yi > y) != (yj > y))
        if cond:
            x_inter = (xj - xi) * (y - yi) / ((yj - yi) if (yj - yi) != 0 else 1e-12) + xi
            if x < x_inter:
                dentro = not dentro
        j = i
    return dentro


def ponto_representativo_anel(anel: list[tuple[float, float]]) -> tuple[float, float]:
    """Retorna ponto representativo preferencialmente dentro do anel."""
    if len(anel) < 3:
        return (0.0, 0.0)

    a = area_anel(anel)
    if abs(a) < 1e-12:
        return anel[len(anel) // 2]

    cx_num = 0.0
    cy_num = 0.0
    for i in range(len(anel) - 1):
        x1, y1 = anel[i]
        x2, y2 = anel[i + 1]
        cross = (x1 * y2) - (x2 * y1)
        cx_num += (x1 + x2) * cross
        cy_num += (y1 + y2) * cross

    cx = cx_num / (6.0 * a)
    cy = cy_num / (6.0 * a)

    if ponto_em_poligono(cx, cy, anel):
        return (cx, cy)

    return anel[len(anel) // 2]


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


@st.cache_resource
def carregar_vulnerabilidade(_grafo):
    """Inicializa o analisador de vulnerabilidade."""
    return AnaliseVulnerabilidade(_grafo)


@st.cache_data
def carregar_poligonos_kml(caminho_kml: Path) -> dict[str, list[list[tuple[float, float]]]]:
    """Carrega polígonos distritais a partir de KML."""
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
            if not txt:
                continue

            pontos: list[tuple[float, float]] = []
            for token in txt.replace("\n", " ").split():
                partes = token.split(",")
                if len(partes) < 2:
                    continue
                try:
                    lon = float(partes[0])
                    lat = float(partes[1])
                    pontos.append((lon, lat))
                except ValueError:
                    continue

            if len(pontos) < 3:
                continue

            n = len(pontos)
            passo = 1
            if n > 2000:
                passo = 8
            elif n > 1000:
                passo = 6
            elif n > 600:
                passo = 4
            elif n > 300:
                passo = 3
            elif n > 150:
                passo = 2

            simplificado = pontos[::passo]
            if simplificado[0] != simplificado[-1]:
                simplificado.append(simplificado[0])

            aneis.append(simplificado)

        if aneis:
            poligonos[nome_norm] = aneis

    return poligonos


# ============================================================================
# Mapa Base (reutilizado em múltiplas abas)
# ============================================================================

def construir_mapa(
    grafo,
    poligonos_kml,
    distrito_id: int,
    ids_destaque: set[int] | None = None,
    cor_destaque: str = "#e74c3c",
    ids_removidos: set[int] | None = None,
    componentes: list[dict] | None = None,
    modo: str = "cidade_inteira",
    titulo: str = "Mapa de São Paulo",
    altura: int = 600,
) -> go.Figure:
    """
    Constrói o mapa de São Paulo com polígonos distritais e grafo.

    Args:
        grafo: instância de GrafoSP
        poligonos_kml: polígonos do KML
        distrito_id: distrito selecionado (amarelo)
        ids_destaque: distritos a destacar (ex: articulações)
        cor_destaque: cor para distritos destacados
        ids_removidos: distritos removidos (cinza hachurado)
        componentes: lista de componentes pós-falha para colorir
        modo: "cidade_inteira" ou "foco_local"
        titulo: título do mapa
        altura: altura do gráfico em pixels
    """
    fig = go.Figure()

    if ids_destaque is None:
        ids_destaque = set()
    if ids_removidos is None:
        ids_removidos = set()

    ids_por_nome_norm = {
        normalizar_nome(info["nome"]): did
        for did, info in grafo.distritos.items()
    }

    # Mapa de componente para cor
    cor_componente: dict[int, str] = {}
    cores_componentes = [
        "#2ecc71", "#3498db", "#e74c3c", "#f39c12", "#9b59b6",
        "#1abc9c", "#e67e22", "#34495e", "#16a085", "#c0392b",
    ]
    if componentes:
        for i, comp in enumerate(componentes):
            cor = cores_componentes[i % len(cores_componentes)]
            for did in comp.get("distritos_ids", []):
                cor_componente[did] = cor

    # Plotar polígonos
    zonas_legenda: set[str] = set()
    all_poly_lons: list[float] = []
    all_poly_lats: list[float] = []
    ponto_label_por_id: dict[int, tuple[float, float]] = {}
    bounds_por_id: dict[int, tuple[float, float, float, float]] = {}

    for nome_norm, aneis in poligonos_kml.items():
        did = ids_por_nome_norm.get(nome_norm)
        if did is None:
            continue
        if did not in grafo.distritos:
            continue

        info_d = grafo.distritos[did]
        zona = info_d["zona"]
        cor_zona = CORES_ZONA.get(zona, "#999999")
        selecionado = did == distrito_id

        anel_principal = max(aneis, key=lambda r: abs(area_anel(r)))
        ponto_x, ponto_y = ponto_representativo_anel(anel_principal)
        ponto_label_por_id[did] = (ponto_x, ponto_y)
        xs_princ = [p[0] for p in anel_principal]
        ys_princ = [p[1] for p in anel_principal]
        bounds_por_id[did] = (min(xs_princ), max(xs_princ), min(ys_princ), max(ys_princ))

        # Determinar cor do polígono
        if did in ids_removidos:
            fill_cor = "rgba(100,100,100,0.5)"
            line_cor = "#333333"
            line_w = 2.0
        elif selecionado:
            fill_cor = hex_para_rgba("#f1c40f", 0.4)
            line_cor = "#7c5600"
            line_w = 2.6
        elif did in ids_destaque:
            fill_cor = hex_para_rgba(cor_destaque, 0.45)
            line_cor = cor_destaque
            line_w = 2.2
        elif did in cor_componente:
            fill_cor = hex_para_rgba(cor_componente[did], 0.35)
            line_cor = cor_componente[did]
            line_w = 1.5
        else:
            fill_cor = hex_para_rgba(cor_zona, 0.25)
            line_cor = hex_para_rgba(cor_zona, 0.8)
            line_w = 1.0

        for idx_anel, anel in enumerate(aneis):
            xs = [p[0] for p in anel]
            ys = [p[1] for p in anel]
            all_poly_lons.extend(xs)
            all_poly_lats.extend(ys)

            show = zona not in zonas_legenda and idx_anel == 0
            fig.add_trace(go.Scattergl(
                x=xs, y=ys,
                mode="lines",
                fill="toself",
                fillcolor=fill_cor,
                line=dict(color=line_cor, width=line_w),
                customdata=[[did, info_d["nome"], zona]] * len(xs),
                hovertemplate="<b>%{customdata[1]}</b><br>Zona: %{customdata[2]}<extra></extra>",
                name=f"Zona {zona}",
                legendgroup=f"zona_{zona}",
                showlegend=show,
            ))

        zonas_legenda.add(zona)

    # Garantir ponto representativo para todos os distritos
    for did in grafo.G.nodes():
        if did not in ponto_label_por_id:
            ponto_label_por_id[did] = (grafo.distritos[did]["lon"], grafo.distritos[did]["lat"])

    # Arestas do grafo
    edge_x: list[float | None] = []
    edge_y: list[float | None] = []
    for u, v in grafo.G.edges():
        if u in ponto_label_por_id and v in ponto_label_por_id:
            xu, yu = ponto_label_por_id[u]
            xv, yv = ponto_label_por_id[v]
            edge_x.extend([xu, xv, None])
            edge_y.extend([yu, yv, None])

    fig.add_trace(go.Scattergl(
        x=edge_x, y=edge_y,
        mode="lines",
        line=dict(color="rgba(55,65,81,0.4)", width=0.8),
        hoverinfo="skip",
        name="Conexões",
        showlegend=True,
    ))

    # Vértices
    vx, vy, vcustom, vcores, vsizes = [], [], [], [], []
    for did in grafo.G.nodes():
        px_v, py_v = ponto_label_por_id[did]
        dno = grafo.distritos[did]
        vx.append(px_v)
        vy.append(py_v)
        vcustom.append([did, dno["nome"], dno["zona"]])

        if did in ids_removidos:
            vcores.append("#333333")
            vsizes.append(5)
        elif did in ids_destaque:
            vcores.append(cor_destaque)
            vsizes.append(10)
        elif did == distrito_id:
            vcores.append("#f1c40f")
            vsizes.append(9)
        else:
            vcores.append(CORES_ZONA.get(dno["zona"], "#9ca3af"))
            vsizes.append(6)

    fig.add_trace(go.Scattergl(
        x=vx, y=vy,
        mode="markers",
        marker=dict(size=vsizes, color=vcores, line=dict(width=0.7, color="#1f2937"), opacity=0.95),
        customdata=vcustom,
        hovertemplate="<b>%{customdata[1]}</b><br>Zona: %{customdata[2]}<extra></extra>",
        name="Distritos",
        showlegend=True,
    ))

    # Zoom
    if modo == "foco_local":
        ids_foco = [distrito_id] + list(grafo.G.neighbors(distrito_id))
        xs_zoom, ys_zoom = [], []
        for did_f in ids_foco:
            if did_f in bounds_por_id:
                xmin, xmax, ymin, ymax = bounds_por_id[did_f]
                xs_zoom.extend([xmin, xmax])
                ys_zoom.extend([ymin, ymax])
            elif did_f in ponto_label_por_id:
                xs_zoom.append(ponto_label_por_id[did_f][0])
                ys_zoom.append(ponto_label_por_id[did_f][1])
        margem_lon = max(0.03, (max(xs_zoom) - min(xs_zoom)) * 0.45) if xs_zoom else 0.05
        margem_lat = max(0.02, (max(ys_zoom) - min(ys_zoom)) * 0.45) if ys_zoom else 0.04
    else:
        xs_zoom = all_poly_lons if all_poly_lons else [grafo.distritos[n]["lon"] for n in grafo.G.nodes()]
        ys_zoom = all_poly_lats if all_poly_lats else [grafo.distritos[n]["lat"] for n in grafo.G.nodes()]
        span_lon = max(xs_zoom) - min(xs_zoom)
        span_lat = max(ys_zoom) - min(ys_zoom)
        margem_lon = max(0.05, span_lon * 0.08)
        margem_lat = max(0.04, span_lat * 0.08)

    lat_media = float(np.mean(ys_zoom)) if ys_zoom else -23.55
    fator_geo = float(1.0 / np.cos(np.deg2rad(lat_media)))

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=0, r=0, t=40, b=0),
        title=titulo,
        title_font=dict(size=16, color="#111827"),
        font=dict(color="#111827"),
        legend=dict(orientation="h", yanchor="top", y=1.02, xanchor="left", x=0.0),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        hoverlabel=dict(bgcolor="#ffffff", font_color="#111827"),
        xaxis=dict(
            showgrid=False, zeroline=False, showticklabels=False,
            range=[min(xs_zoom) - margem_lon, max(xs_zoom) + margem_lon],
        ),
        yaxis=dict(
            showgrid=False, zeroline=False, showticklabels=False,
            scaleanchor="x", scaleratio=fator_geo,
            range=[min(ys_zoom) - margem_lat, max(ys_zoom) + margem_lat],
        ),
        dragmode=False,
        height=altura,
    )
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)

    return fig


# ============================================================================
# Verificar dados
# ============================================================================

data_dir = Path(__file__).resolve().parent.parent / "data"
if not (data_dir / "ubs_vertices.json").exists() and not (data_dir / "distritos.json").exists():
    st.error("⚠️ Arquivos de dados não encontrados!")
    st.info("Execute: `python gerar_dados.py`")
    st.stop()

# Carregar dados
grafo = carregar_grafo()
metricas = carregar_metricas(grafo)
vuln = carregar_vulnerabilidade(grafo)
kml_path = data_dir / "São Paulo.kml"
poligonos_kml = carregar_poligonos_kml(kml_path)

# ============================================================================
# Sidebar
# ============================================================================

st.sidebar.markdown("# 🏙️ SPGraph")
st.sidebar.markdown("**Vulnerabilidade da Rede de Saúde**")
st.sidebar.markdown("---")

# Seleção de distrito
nomes = grafo.get_nomes_ordenados()
opcoes_distrito = {nome: did for did, nome in nomes}

if "distrito_id" not in st.session_state:
    st.session_state["distrito_id"] = next(iter(opcoes_distrito.values()))

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

# Estatísticas
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Estatísticas do Grafo")
stats = grafo.estatisticas()
st.sidebar.metric("Vértices (Distritos)", stats["num_vertices"])
st.sidebar.metric("Arestas (Conexões)", stats["num_arestas"])
st.sidebar.metric("Grau Médio", stats["grau_medio"])
st.sidebar.metric("Densidade", stats["densidade"])
st.sidebar.metric("Conexo", "✅ Sim" if stats["eh_conexo"] else "❌ Não")

# ============================================================================
# Cabeçalho
# ============================================================================

st.markdown(
    '<div class="main-header">SPGraph — Vulnerabilidade da Rede de Saúde</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">'
    'Análise estrutural por grafos · 96 distritos de São Paulo · ODS 10 — Redução das Desigualdades'
    '</div>',
    unsafe_allow_html=True,
)

# ============================================================================
# Abas
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ Visão Geral",
    "🔴 Pontos Críticos",
    "💥 Simulação de Falha",
    "📊 Cobertura",
    "ℹ️ Sobre",
])

# ============================================================================
# Tab 1: Visão Geral
# ============================================================================

with tab1:
    st.subheader("Grafo dos Distritos de São Paulo")

    col_grafo, col_info = st.columns([3, 1])

    with col_grafo:
        modo_mapa = st.radio(
            "Visualização",
            options=["Cidade inteira", "Foco local"],
            horizontal=True,
            key="modo_mapa_t1",
        )

        fig = construir_mapa(
            grafo, poligonos_kml, distrito_id,
            modo="foco_local" if modo_mapa == "Foco local" else "cidade_inteira",
            titulo=f"Mapa Distrital — {modo_mapa}",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown("### 📋 Distrito Selecionado")
        d = grafo.distritos[distrito_id]
        st.markdown(f"**{d['nome']}**")
        st.markdown(f"📍 Zona: **{d['zona']}**")
        st.markdown(f"👥 População: **{d['populacao']:,}**".replace(",", "."))
        st.markdown(f"🔗 Conexões: **{grafo.G.degree(distrito_id)}**")

        st.markdown("---")
        st.markdown("### 🏛️ Serviços Locais")
        servicos_local = grafo.contar_servicos_distrito(distrito_id)
        if servicos_local:
            for tipo, qtd in sorted(servicos_local.items()):
                st.markdown(f"- {NOMES_SERVICO.get(tipo, tipo)}: **{qtd}**")
        else:
            st.warning("Nenhum serviço neste distrito")

        st.markdown("---")
        st.markdown("### 🏘️ Vizinhos")
        vizinhos = list(grafo.G.neighbors(distrito_id))
        for v in sorted(vizinhos, key=lambda x: grafo.get_nome(x)):
            peso = grafo.G[distrito_id][v]["weight"]
            st.markdown(f"• {grafo.get_nome(v)} ({peso:.1f} km)")


# ============================================================================
# Tab 2: Pontos Críticos
# ============================================================================

with tab2:
    st.subheader(f"Pontos Críticos da Rede — {NOMES_SERVICO.get(tipo_servico, tipo_servico)}")

    st.markdown("""
    > **Vértices de articulação** são distritos cuja remoção **fragmenta** o grafo em pedaços desconectados.
    > **Pontes** são conexões cuja remoção **isola** regiões inteiras.
    > Identificados pelo **algoritmo de Tarjan** (DFS com low-link values).
    """)

    # Articulações
    articulacoes = vuln.vertices_articulacao(tipo_servico)
    ids_articulacao = {a["distrito_id"] for a in articulacoes}

    col_mapa_art, col_dados_art = st.columns([2, 1])

    with col_mapa_art:
        fig_art = construir_mapa(
            grafo, poligonos_kml, distrito_id,
            ids_destaque=ids_articulacao,
            cor_destaque="#e74c3c",
            titulo=f"Vértices de Articulação ({len(articulacoes)} encontrados)",
            altura=550,
        )
        st.plotly_chart(fig_art, use_container_width=True)

    with col_dados_art:
        st.markdown(f"### 🔴 {len(articulacoes)} Vértices de Articulação")

        if articulacoes:
            for a in articulacoes:
                servico_txt = "✅ Tem serviço" if a["tem_servico"] else "❌ Sem serviço"
                st.markdown(
                    f"**{a['distrito']}** ({a['zona']})\n\n"
                    f"👥 Pop: {a['populacao']:,} · 🔗 Grau: {a['grau']} · {servico_txt}".replace(",", ".")
                )
                st.markdown("---")
        else:
            st.success("Nenhum vértice de articulação encontrado — a rede é robusta!")

    # Pontes
    st.markdown("---")
    st.subheader("🌉 Pontes Críticas")

    pontes = vuln.pontes_criticas()

    if pontes:
        st.markdown(f"**{len(pontes)} ponte(s)** encontrada(s) — arestas cuja remoção fragmenta o grafo.")
        df_pontes = pd.DataFrame(pontes)
        df_pontes_display = df_pontes[["distrito1", "distrito2", "distancia_km", "pop_lado_menor", "pop_lado_maior"]].copy()
        df_pontes_display.columns = ["Distrito A", "Distrito B", "Distância (km)", "Pop. Lado Menor", "Pop. Lado Maior"]
        st.dataframe(df_pontes_display, use_container_width=True, hide_index=True)
    else:
        st.success("Nenhuma ponte crítica — todas as conexões têm caminhos alternativos.")


# ============================================================================
# Tab 3: Simulação de Falha (ABA CENTRAL)
# ============================================================================

with tab3:
    st.subheader(f"💥 Simulação de Falha — {NOMES_SERVICO.get(tipo_servico, tipo_servico)}")

    st.markdown("""
    > Selecione distritos para **simular seu fechamento** e veja o impacto na rede de saúde.
    > O sistema remove os nós do grafo, recalcula componentes conexas e mede a fragmentação.
    """)

    # Seletor de distritos a remover
    nomes_todos = grafo.get_nomes_ordenados()
    opcoes_remover = {nome: did for did, nome in nomes_todos}

    distritos_para_remover = st.multiselect(
        "🗑️ Selecione distritos para simular fechamento",
        options=list(opcoes_remover.keys()),
        default=[],
        help="Selecione 1 ou mais distritos. O sistema simulará a remoção deles do grafo.",
    )

    ids_remover = [opcoes_remover[n] for n in distritos_para_remover]

    if ids_remover:
        with st.spinner("Simulando fechamento e recalculando rede..."):
            resultado = vuln.simular_fechamento(ids_remover, tipo_servico)
            componentes = vuln.componentes_pos_falha(ids_remover, tipo_servico)

        # Métricas de impacto
        st.markdown("### 📊 Impacto da Remoção")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            delta_comp = resultado["componentes_depois"] - resultado["componentes_antes"]
            st.metric(
                "🧩 Componentes Conexas",
                resultado["componentes_depois"],
                delta=f"+{delta_comp}" if delta_comp > 0 else "0",
                delta_color="inverse",
            )
        with col2:
            st.metric(
                "🚫 Distritos Sem Acesso",
                resultado["distritos_sem_acesso_depois"],
                delta=f"+{len(resultado['novos_sem_acesso'])}" if resultado["novos_sem_acesso"] else "0",
                delta_color="inverse",
            )
        with col3:
            st.metric(
                "👥 Pop. Removida",
                f"{resultado['pop_removida']:,}".replace(",", "."),
            )
        with col4:
            st.metric(
                "📏 Δ Distância Média",
                f"{resultado['aumento_medio_distancia']:+.2f} km",
                delta_color="inverse",
            )

        st.markdown("---")

        # Mapa antes vs depois
        col_antes, col_depois = st.columns(2)

        with col_antes:
            st.markdown("#### 🟢 ANTES da remoção")
            fig_antes = construir_mapa(
                grafo, poligonos_kml, distrito_id,
                ids_destaque=set(ids_remover),
                cor_destaque="#f39c12",
                titulo="Grafo Original",
                altura=450,
            )
            st.plotly_chart(fig_antes, use_container_width=True)

        with col_depois:
            st.markdown("#### 🔴 DEPOIS da remoção")
            # Construir grafo pós-falha para o mapa
            grafo_pos = grafo.copiar_sem_nos(set(ids_remover))
            fig_depois = construir_mapa(
                grafo_pos, poligonos_kml, distrito_id,
                ids_removidos=set(ids_remover),
                componentes=componentes,
                titulo=f"Grafo Pós-Falha ({len(componentes)} componentes)",
                altura=450,
            )
            st.plotly_chart(fig_depois, use_container_width=True)

        # Detalhes das componentes
        st.markdown("---")
        st.markdown("### 🧩 Componentes Conexas Resultantes")

        for comp in componentes:
            status = "🔴 **ISOLADA** (sem serviço)" if comp["isolada"] else "🟢 Coberta"
            with st.expander(
                f"Componente {comp['componente_id']} — "
                f"{comp['num_distritos']} distritos · "
                f"Pop: {comp['populacao']:,} · {status}".replace(",", "."),
                expanded=comp["isolada"],
            ):
                st.markdown(f"**Distritos:** {', '.join(comp['nomes'])}")
                st.markdown(f"**Possui serviço:** {'Sim' if comp['tem_servico'] else '❌ NÃO'}")
                st.markdown(f"**Distritos com serviço na componente:** {comp['num_distritos_com_servico']}")

        # Distritos com aumento de distância
        if resultado["distritos_com_aumento"]:
            st.markdown("---")
            st.markdown("### 📈 Distritos com Aumento de Distância")

            dados_aumento = list(resultado["distritos_com_aumento"].values())
            df_aumento = pd.DataFrame(dados_aumento)
            df_aumento.columns = ["Distrito", "Zona", "População", "Dist. Antes (km)", "Dist. Depois (km)", "Aumento (km)"]
            st.dataframe(df_aumento, use_container_width=True, hide_index=True)

    else:
        st.info("👆 Selecione distritos acima para simular o fechamento e ver o impacto na rede.")

        # Sugestão: mostrar os distritos mais críticos
        st.markdown("---")
        st.markdown("### 💡 Sugestão: Distritos mais críticos para simular")
        arts = vuln.vertices_articulacao(tipo_servico)
        if arts:
            st.markdown("Estes são **vértices de articulação** — sua remoção fragmenta o grafo:")
            for a in arts[:5]:
                st.markdown(f"- **{a['distrito']}** (zona {a['zona']}, grau {a['grau']})")


# ============================================================================
# Tab 4: Cobertura (adaptada do original)
# ============================================================================

with tab4:
    st.subheader(f"Ranking de Cobertura — {NOMES_SERVICO.get(tipo_servico, tipo_servico)}")

    ranking_df = metricas.ranking(tipo_servico)
    media = metricas.media_cidade(tipo_servico)

    # Métricas resumo
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📏 Dist. Ref. Média", f"{media['media_distancia']:.1f} km")
    with col2:
        st.metric("⭐ Índice Médio", f"{media['score_medio']:.0f}/100")
    with col3:
        st.metric("📐 Mediana", f"{media['mediana_distancia']:.1f} km")
    with col4:
        st.metric("✅ Melhor", f"{media['melhor_distancia']:.1f} km")
    with col5:
        st.metric("❌ Pior", f"{media['pior_distancia']:.1f} km")

    st.markdown("---")

    col_top, col_bottom = st.columns(2)

    with col_top:
        st.markdown("#### ✅ Top 10 — Melhor Cobertura")
        top10 = ranking_df.head(10)
        fig_top = px.bar(
            top10, x="distrito", y="score", color="zona",
            color_discrete_map=CORES_ZONA,
            title="Distritos com melhor cobertura",
            labels={"score": "Score", "distrito": "Distrito", "zona": "Zona"},
        )
        fig_top.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_top, use_container_width=True)

    with col_bottom:
        st.markdown("#### ❌ Top 10 — Menor Cobertura")
        bottom10 = ranking_df.tail(10).sort_values("score", ascending=True)
        fig_bottom = px.bar(
            bottom10, x="distrito", y="score", color="zona",
            color_discrete_map=CORES_ZONA,
            title="Distritos com menor cobertura",
            labels={"score": "Score", "distrito": "Distrito", "zona": "Zona"},
        )
        fig_bottom.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_bottom, use_container_width=True)

    # Dispersão
    st.markdown("---")
    st.markdown("#### 📈 População vs. Cobertura")
    fig_scatter = px.scatter(
        ranking_df, x="populacao", y="score", color="zona",
        color_discrete_map=CORES_ZONA, size="populacao",
        hover_name="distrito",
        title=f"Relação população × cobertura ({tipo_servico})",
        labels={"populacao": "População", "score": "Índice de Cobertura", "zona": "Zona"},
    )
    fig_scatter.add_hline(
        y=media["score_medio"], line_dash="dash", line_color="red",
        annotation_text=f"Média: {media['score_medio']:.0f}",
    )
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Tabela completa
    st.markdown("---")
    st.markdown("#### 📋 Ranking Completo")
    ranking_display = ranking_df.copy()
    ranking_display.columns = [
        "Posição", "ID", "Distrito", "Zona",
        "População", "Distância Ref. (km)", "Índice",
    ]
    st.dataframe(
        ranking_display[["Posição", "Distrito", "Zona", "População", "Distância Ref. (km)", "Índice"]],
        use_container_width=True, hide_index=True, height=400,
    )


# ============================================================================
# Tab 5: Sobre
# ============================================================================

with tab5:
    st.subheader("Sobre o Projeto")

    col_about1, col_about2 = st.columns(2)

    with col_about1:
        st.markdown("""
        ### 🏙️ SPGraph

        Sistema interativo que modela a cidade de São Paulo como um **grafo**
        para analisar a **vulnerabilidade estrutural** da rede de saúde pública.

        ### 🎯 Objetivo

        Identificar **pontos críticos** na rede de UBS, UPA e hospitais SUS
        cujo fechamento comprometeria o acesso da população a serviços de saúde,
        utilizando **algoritmos clássicos de teoria dos grafos**.

        ### 🌍 ODS 10 — Redução das Desigualdades

        A desigualdade urbana se manifesta no acesso desigual a serviços de saúde.
        O projeto identifica regiões vulneráveis e simula cenários de falha
        para subsidiar decisões de planejamento urbano.
        """)

    with col_about2:
        st.markdown("""
        ### 📐 Modelagem em Grafos

        - **Vértices:** 96 distritos administrativos de São Paulo
        - **Arestas:** Adjacências geográficas (calculadas via KML)
        - **Peso:** Distância Haversine entre centróides (km)
        - **Tipo:** Grafo não direcionado e ponderado

        ### 🔬 Algoritmos Implementados

        - **Tarjan:** Vértices de articulação e pontes
        - **BFS/DFS:** Componentes conexas pós-falha
        - **Dijkstra:** Distâncias mínimas e serviço mais próximo
        - **Simulação de falha:** Remoção de nós com recálculo completo
        - **Ranking de criticidade:** Score composto por impacto

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
    | Visualização | Plotly |
    | Dados | JSON, CSV, KML |

    ### 👥 Equipe

    | Nome | RA |
    |---|---|
    | Lucas Fernandes | 10419400 |
    | Lendy Naiara Pacheco | 10428525 |
    | Anna Luiza Santos | 10417401 |
    """)
