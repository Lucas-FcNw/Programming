"""
SPGraph - Interface Interativa com Streamlit
=============================================
Sistema de análise territorial de acesso à saúde nas UBSs
de São Paulo, utilizando modelagem por grafos.

Uso:
    streamlit run app.py
"""

import sys
from pathlib import Path
import xml.etree.ElementTree as ET
import unicodedata

import streamlit as st
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

    # fallback robusto: ponto de um vértice (sempre no contorno do distrito)
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


@st.cache_data
def carregar_poligonos_kml(caminho_kml: Path) -> dict[str, list[list[tuple[float, float]]]]:
    """Carrega polígonos distritais a partir de KML (nome -> lista de anéis)."""
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

            # Simplificação leve para reduzir custo de renderização
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
# Verificar se os dados existem
# ============================================================================

data_dir = Path(__file__).resolve().parent.parent / "data"
if not (data_dir / "ubs_vertices.json").exists():
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

# Seleção de UBS
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
    "📍 Selecione a UBS",
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
st.sidebar.metric("Vértices (UBSs)", stats["num_vertices"])
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
    'Rede de UBSs com distâncias baseadas em adjacência distrital · ODS 10 — Redução das Desigualdades'
    '</div>',
    unsafe_allow_html=True
)

# Abas
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Visão Geral",
    "📍 Análise da UBS",
    "📊 Cobertura",
    "ℹ️ Sobre"
])

# ============================================================================
# Tab 1: Visão Geral do Grafo
# ============================================================================

with tab1:
    st.subheader("Grafo das UBSs de São Paulo")

    col_grafo, col_info = st.columns([3, 1])

    with col_grafo:
        if "modo_mapa" not in st.session_state:
            st.session_state["modo_mapa"] = "Foco local"

        modo_mapa = st.radio(
            "Visualização",
            options=["Foco local", "Cidade inteira"],
            horizontal=True,
            key="modo_mapa",
            help="Foco local: zoom automático no distrito e vizinhos. Cidade inteira: visão completa de São Paulo.",
        )

        kml_path = data_dir / "São Paulo.kml"
        poligonos_kml = carregar_poligonos_kml(kml_path)

        # Mapa interativo distrital (KML da cidade, sem fundo de ruas)
        fig_map = go.Figure()

        ids_por_nome_norm = {
            normalizar_nome(info["nome"]): did
            for did, info in grafo.distritos.items()
        }

        # Plotar polígonos por distrito com cor por zona
        zonas_legenda = set()
        all_poly_lons: list[float] = []
        all_poly_lats: list[float] = []
        ponto_label_por_id: dict[int, tuple[float, float]] = {}
        bounds_por_id: dict[int, tuple[float, float, float, float]] = {}
        for nome_norm, aneis in poligonos_kml.items():
            did = ids_por_nome_norm.get(nome_norm)
            if did is None:
                continue

            info_d = grafo.distritos[did]
            zona = info_d["zona"]
            cor_zona = CORES_ZONA.get(zona, "#999999")
            selecionado = did == distrito_id

            # Geometria principal para labels/zoom
            anel_principal = max(aneis, key=lambda r: abs(area_anel(r)))
            ponto_x, ponto_y = ponto_representativo_anel(anel_principal)
            ponto_label_por_id[did] = (ponto_x, ponto_y)
            xs_princ = [p[0] for p in anel_principal]
            ys_princ = [p[1] for p in anel_principal]
            bounds_por_id[did] = (min(xs_princ), max(xs_princ), min(ys_princ), max(ys_princ))

            for idx_anel, anel in enumerate(aneis):
                xs = [p[0] for p in anel]
                ys = [p[1] for p in anel]
                all_poly_lons.extend(xs)
                all_poly_lats.extend(ys)

                fig_map.add_trace(go.Scattergl(
                    x=xs,
                    y=ys,
                    mode="lines",
                    fill="toself",
                    fillcolor=hex_para_rgba("#f1c40f" if selecionado else cor_zona, 0.35 if selecionado else 0.28),
                    line=dict(
                        color="#7c5600" if selecionado else hex_para_rgba(cor_zona, 1.0),
                        width=2.6 if selecionado else 1.2,
                    ),
                    customdata=[[did, info_d["nome"], zona]] * len(xs),
                    hovertemplate="<b>%{customdata[1]}</b><br>Zona: %{customdata[2]}<extra></extra>",
                    name=f"Zona {zona}",
                    legendgroup=f"zona_{zona}",
                    showlegend=(zona not in zonas_legenda and idx_anel == 0),
                ))

            zonas_legenda.add(zona)

        # Garantir ponto representativo para todos os distritos (fallback)
        for did in grafo.G.nodes():
            if did not in ponto_label_por_id:
                ponto_label_por_id[did] = (grafo.distritos[did]["lon"], grafo.distritos[did]["lat"])

        # Estrutura do grafo (arestas + vértices)
        edge_x: list[float | None] = []
        edge_y: list[float | None] = []
        for u, v in grafo.G.edges():
            xu, yu = ponto_label_por_id[u]
            xv, yv = ponto_label_por_id[v]
            edge_x.extend([xu, xv, None])
            edge_y.extend([yu, yv, None])

        fig_map.add_trace(go.Scattergl(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(color="rgba(55,65,81,0.45)", width=1.0),
            hoverinfo="skip",
            name="Conexões do grafo",
            showlegend=True,
        ))

        vx, vy, vcustom, vcores = [], [], [], []
        for did in grafo.G.nodes():
            px_v, py_v = ponto_label_por_id[did]
            dno = grafo.distritos[did]
            vx.append(px_v)
            vy.append(py_v)
            vcustom.append([did, dno["nome"], dno["zona"]])
            vcores.append("#f1c40f" if did == distrito_id else CORES_ZONA.get(dno["zona"], "#9ca3af"))

        fig_map.add_trace(go.Scattergl(
            x=vx,
            y=vy,
            mode="markers",
            marker=dict(size=7, color=vcores, line=dict(width=0.8, color="#1f2937"), opacity=0.95),
            customdata=vcustom,
            hovertemplate="<b>%{customdata[1]}</b><br>Zona: %{customdata[2]}<extra></extra>",
            name="Vértices (distritos)",
            showlegend=True,
        ))

        # Região de foco (selecionado + vizinhos)
        ids_foco = [distrito_id] + list(grafo.G.neighbors(distrito_id))
        xs_texto = [ponto_label_por_id.get(i, (grafo.distritos[i]["lon"], grafo.distritos[i]["lat"]))[0] for i in ids_foco]
        ys_texto = [ponto_label_por_id.get(i, (grafo.distritos[i]["lon"], grafo.distritos[i]["lat"]))[1] for i in ids_foco]

        # Zoom conforme modo selecionado
        todos_lons = [grafo.distritos[n]["lon"] for n in grafo.G.nodes()]
        todos_lats = [grafo.distritos[n]["lat"] for n in grafo.G.nodes()]

        if modo_mapa == "Cidade inteira":
            xs_zoom = all_poly_lons if all_poly_lons else todos_lons
            ys_zoom = all_poly_lats if all_poly_lats else todos_lats
            span_lon = max(xs_zoom) - min(xs_zoom)
            span_lat = max(ys_zoom) - min(ys_zoom)
            margem_lon = max(0.05, span_lon * 0.08)
            margem_lat = max(0.04, span_lat * 0.08)
            titulo_mapa = "Mapa Distrital de São Paulo — visão completa"
        else:
            xs_zoom = []
            ys_zoom = []
            for did_f in ids_foco:
                if did_f in bounds_por_id:
                    xmin, xmax, ymin, ymax = bounds_por_id[did_f]
                    xs_zoom.extend([xmin, xmax])
                    ys_zoom.extend([ymin, ymax])
                else:
                    xs_zoom.append(grafo.distritos[did_f]["lon"])
                    ys_zoom.append(grafo.distritos[did_f]["lat"])
            margem_lon = max(0.03, (max(xs_zoom) - min(xs_zoom)) * 0.45 if len(xs_zoom) > 1 else 0.05)
            margem_lat = max(0.02, (max(ys_zoom) - min(ys_zoom)) * 0.45 if len(ys_zoom) > 1 else 0.04)
            titulo_mapa = f"Mapa base (distritos) — foco em {distrito_selecionado_nome}"

        # Labels: cidade inteira -> só selecionado; foco local -> selecionado + vizinhos
        ids_labels = [distrito_id] if modo_mapa == "Cidade inteira" else ids_foco
        for did_lbl in ids_labels:
            d_lbl = grafo.distritos[did_lbl]
            px_lbl, py_lbl = ponto_label_por_id.get(did_lbl, (d_lbl["lon"], d_lbl["lat"]))
            fig_map.add_annotation(
                x=px_lbl,
                y=py_lbl,
                text=f"<b>{d_lbl['nome']}</b>",
                showarrow=False,
                font=dict(size=11 if did_lbl != distrito_id else 12, color="#111827"),
                align="center",
                bgcolor="rgba(255,255,255,0.92)",
                bordercolor="#6b7280",
                borderwidth=1,
                borderpad=3,
                opacity=1,
            )

        # Correção de proporção geográfica (lat/lon)
        lat_media = float(np.mean(ys_zoom)) if ys_zoom else -23.55
        fator_geo = float(1.0 / np.cos(np.deg2rad(lat_media)))

        fig_map.update_layout(
            template="plotly_white",
            margin=dict(l=0, r=0, t=40, b=0),
            title=titulo_mapa,
            title_font=dict(size=18, color="#111827"),
            font=dict(color="#111827"),
            legend=dict(orientation="h", yanchor="top", y=1.02, xanchor="left", x=0.0),
            legend_font=dict(color="#111827"),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            hoverlabel=dict(bgcolor="#ffffff", font_color="#111827"),
            xaxis=dict(
                title="",
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                range=[min(xs_zoom) - margem_lon, max(xs_zoom) + margem_lon],
            ),
            yaxis=dict(
                title="",
                showgrid=False,
                zeroline=False,
                scaleanchor="x",
                scaleratio=fator_geo,
                showticklabels=False,
                range=[min(ys_zoom) - margem_lat, max(ys_zoom) + margem_lat],
            ),
            dragmode=False,
            height=650,
        )

        # Bloquear arraste/zoom manual (zoom é guiado pelo clique no distrito)
        fig_map.update_xaxes(fixedrange=True)
        fig_map.update_yaxes(fixedrange=True)

        evento = st.plotly_chart(
            fig_map,
            width="stretch",
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
            st.dataframe(df_vizinhos, width="stretch", hide_index=True)

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
    st.plotly_chart(fig_bfs, width="stretch")


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
        st.plotly_chart(fig_top, width="stretch")

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
        st.plotly_chart(fig_bottom, width="stretch")

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
            width="stretch",
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
    st.plotly_chart(fig_scatter, width="stretch")

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
        width="stretch",
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
