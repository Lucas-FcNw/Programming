"""
SPGraph - Geração de Dados da Rede de UBSs de São Paulo
========================================================
Constrói o dataset estruturado do grafo de Unidades Básicas de Saúde (UBSs)
do município de São Paulo a partir das bases públicas oficiais da pasta data/:
- deinfosacadsau2014.csv (Cadastro de estabelecimentos de saúde SMS-SP / CNES)
- evolucao_msp_pop_sexo_idade.csv (População distrital - Prefeitura de SP)
- São Paulo.kml (Polígonos oficiais dos 96 distritos administrativos - GeoSampa)

Modelagem do Grafo G = (V, E, W_V, W_E):
- Vértices (V): 454 UBSs reais georreferenciadas (deduplicadas por CNES),
  com atributos de Demanda Territorial Base (D_v via tesselação de Voronoi
  intradistrital) e Capacidade Operacional (C_v segundo a regra 70% Demanda
  Programada / 30% Demanda Espontânea da Atenção Básica - SUS).
- Arestas (E): Grafo de Proximidade de Gabriel restrito à contiguidade
  territorial dos distritos (São Paulo.kml) e ponderado pela impedância
  topográfica/geodésica (Haversine + penalidade de declividade de Tobler).
"""

from __future__ import annotations

import csv
import json
import math
import re
import unicodedata
import xml.etree.ElementTree as ET
from collections import defaultdict, deque
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR / "data"

ARQ_DISTRITOS = DATA_DIR / "distritos.json"
ARQ_ADJ_DISTRITOS = DATA_DIR / "adjacencias_distritos.json"
ARQ_UBS_VERTICES = DATA_DIR / "ubs_vertices.json"
ARQ_ADJ = DATA_DIR / "adjacencias.json"
ARQ_SERVICOS = DATA_DIR / "servicos.json"

ARQ_SERVICOS_CSV = DATA_DIR / "deinfosacadsau2014.csv"
ARQ_POP_CSV = DATA_DIR / "evolucao_msp_pop_sexo_idade.csv"
ARQ_KML = DATA_DIR / "São Paulo.kml"

# ============================================================================
# Mapeamento completo dos 96 distritos com suas zonas
# ============================================================================

ZONA_POR_DISTRITO: dict[str, str] = {
    "AGUA RASA": "Leste", "ALTO DE PINHEIROS": "Oeste", "ANHANGUERA": "Norte",
    "ARICANDUVA": "Leste", "ARTUR ALVIM": "Leste", "BARRA FUNDA": "Oeste",
    "BELA VISTA": "Centro", "BELEM": "Leste", "BOM RETIRO": "Centro",
    "BRAS": "Leste", "BRASILANDIA": "Norte", "BUTANTA": "Oeste",
    "CACHOEIRINHA": "Norte", "CAMBUCI": "Centro", "CAMPO BELO": "Sul",
    "CAMPO GRANDE": "Sul", "CAMPO LIMPO": "Sul", "CANGAIBA": "Leste",
    "CAPAO REDONDO": "Sul", "CARRAO": "Leste", "CASA VERDE": "Norte",
    "CIDADE ADEMAR": "Sul", "CIDADE DUTRA": "Sul", "CIDADE LIDER": "Leste",
    "CIDADE TIRADENTES": "Leste", "CONSOLACAO": "Centro", "CURSINO": "Sul",
    "ERMELINO MATARAZZO": "Leste", "FREGUESIA DO O": "Norte", "GRAJAU": "Sul",
    "GUAIANASES": "Leste", "IGUATEMI": "Leste", "IPIRANGA": "Sul",
    "ITAIM BIBI": "Oeste", "ITAIM PAULISTA": "Leste", "ITAQUERA": "Leste",
    "JABAQUARA": "Sul", "JACANA": "Norte", "JAGUARA": "Oeste",
    "JAGUARE": "Oeste", "JARAGUA": "Norte", "JARDIM ANGELA": "Sul",
    "JARDIM HELENA": "Leste", "JARDIM PAULISTA": "Oeste",
    "JARDIM SAO LUIS": "Sul", "JOSE BONIFACIO": "Leste", "LAJEADO": "Leste",
    "LAPA": "Oeste", "LIBERDADE": "Centro", "LIMAO": "Norte",
    "MANDAQUI": "Norte", "MARSILAC": "Sul", "MOEMA": "Oeste",
    "MOOCA": "Leste", "MORUMBI": "Oeste", "PARELHEIROS": "Sul",
    "PARI": "Centro", "PARQUE DO CARMO": "Leste", "PEDREIRA": "Sul",
    "PENHA": "Leste", "PERDIZES": "Oeste", "PERUS": "Norte",
    "PINHEIROS": "Oeste", "PIRITUBA": "Norte", "PONTE RASA": "Leste",
    "RAPOSO TAVARES": "Oeste", "REPUBLICA": "Centro", "RIO PEQUENO": "Oeste",
    "SACOMA": "Sul", "SANTA CECILIA": "Centro", "SANTANA": "Norte",
    "SANTO AMARO": "Sul", "SAO DOMINGOS": "Norte", "SAO LUCAS": "Leste",
    "SAO MATEUS": "Leste", "SAO MIGUEL": "Leste", "SAO RAFAEL": "Leste",
    "SAPOPEMBA": "Leste", "SAUDE": "Sul", "SE": "Centro",
    "SOCORRO": "Sul", "TATUAPE": "Leste", "TREMEMBE": "Norte",
    "TUCURUVI": "Norte", "VILA ANDRADE": "Sul", "VILA CURUCA": "Leste",
    "VILA FORMOSA": "Leste", "VILA GUILHERME": "Norte",
    "VILA JACUI": "Leste", "VILA LEOPOLDINA": "Oeste",
    "VILA MARIA": "Norte", "VILA MARIANA": "Sul", "VILA MATILDE": "Leste",
    "VILA MEDEIROS": "Norte", "VILA PRUDENTE": "Leste", "VILA SONIA": "Oeste",
}

NOME_BONITO: dict[str, str] = {
    "AGUA RASA": "Água Rasa", "ALTO DE PINHEIROS": "Alto de Pinheiros",
    "ANHANGUERA": "Anhanguera", "ARICANDUVA": "Aricanduva",
    "ARTUR ALVIM": "Artur Alvim", "BARRA FUNDA": "Barra Funda",
    "BELA VISTA": "Bela Vista", "BELEM": "Belém", "BOM RETIRO": "Bom Retiro",
    "BRAS": "Brás", "BRASILANDIA": "Brasilândia", "BUTANTA": "Butantã",
    "CACHOEIRINHA": "Cachoeirinha", "CAMBUCI": "Cambuci",
    "CAMPO BELO": "Campo Belo", "CAMPO GRANDE": "Campo Grande",
    "CAMPO LIMPO": "Campo Limpo", "CANGAIBA": "Cangaíba",
    "CAPAO REDONDO": "Capão Redondo", "CARRAO": "Carrão",
    "CASA VERDE": "Casa Verde", "CIDADE ADEMAR": "Cidade Ademar",
    "CIDADE DUTRA": "Cidade Dutra", "CIDADE LIDER": "Cidade Líder",
    "CIDADE TIRADENTES": "Cidade Tiradentes", "CONSOLACAO": "Consolação",
    "CURSINO": "Cursino", "ERMELINO MATARAZZO": "Ermelino Matarazzo",
    "FREGUESIA DO O": "Freguesia do Ó", "GRAJAU": "Grajaú",
    "GUAIANASES": "Guaianases", "IGUATEMI": "Iguatemi", "IPIRANGA": "Ipiranga",
    "ITAIM BIBI": "Itaim Bibi", "ITAIM PAULISTA": "Itaim Paulista",
    "ITAQUERA": "Itaquera", "JABAQUARA": "Jabaquara", "JACANA": "Jaçanã",
    "JAGUARA": "Jaguara", "JAGUARE": "Jaguaré", "JARAGUA": "Jaraguá",
    "JARDIM ANGELA": "Jardim Ângela", "JARDIM HELENA": "Jardim Helena",
    "JARDIM PAULISTA": "Jardim Paulista", "JARDIM SAO LUIS": "Jardim São Luís",
    "JOSE BONIFACIO": "José Bonifácio", "LAJEADO": "Lajeado", "LAPA": "Lapa",
    "LIBERDADE": "Liberdade", "LIMAO": "Limão", "MANDAQUI": "Mandaqui",
    "MARSILAC": "Marsilac", "MOEMA": "Moema", "MOOCA": "Mooca",
    "MORUMBI": "Morumbi", "PARELHEIROS": "Parelheiros", "PARI": "Pari",
    "PARQUE DO CARMO": "Parque do Carmo", "PEDREIRA": "Pedreira",
    "PENHA": "Penha", "PERDIZES": "Perdizes", "PERUS": "Perus",
    "PINHEIROS": "Pinheiros", "PIRITUBA": "Pirituba",
    "PONTE RASA": "Ponte Rasa", "RAPOSO TAVARES": "Raposo Tavares",
    "REPUBLICA": "República", "RIO PEQUENO": "Rio Pequeno",
    "SACOMA": "Sacomã", "SANTA CECILIA": "Santa Cecília",
    "SANTANA": "Santana", "SANTO AMARO": "Santo Amaro",
    "SAO DOMINGOS": "São Domingos", "SAO LUCAS": "São Lucas",
    "SAO MATEUS": "São Mateus", "SAO MIGUEL": "São Miguel",
    "SAO RAFAEL": "São Rafael", "SAPOPEMBA": "Sapopemba", "SAUDE": "Saúde",
    "SE": "Sé", "SOCORRO": "Socorro", "TATUAPE": "Tatuapé",
    "TREMEMBE": "Tremembé", "TUCURUVI": "Tucuruvi",
    "VILA ANDRADE": "Vila Andrade", "VILA CURUCA": "Vila Curuçá",
    "VILA FORMOSA": "Vila Formosa", "VILA GUILHERME": "Vila Guilherme",
    "VILA JACUI": "Vila Jacuí", "VILA LEOPOLDINA": "Vila Leopoldina",
    "VILA MARIA": "Vila Maria", "VILA MARIANA": "Vila Mariana",
    "VILA MATILDE": "Vila Matilde", "VILA MEDEIROS": "Vila Medeiros",
    "VILA PRUDENTE": "Vila Prudente", "VILA SONIA": "Vila Sônia",
}


def normalizar_texto(valor: str) -> str:
    texto = str(valor).strip().upper()
    return "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )


def ler_csv_dicts(caminho: Path, delimiter: str = ",") -> list[dict[str, str]]:
    for enc in ("utf-8", "latin1", "cp1252"):
        try:
            with open(caminho, "r", encoding=enc, newline="") as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                rows = []
                for r in reader:
                    rows.append({normalizar_texto(k): (v or "").strip() for k, v in r.items() if k is not None})
                return rows
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Não foi possível ler {caminho}")


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distância geodésica Haversine em km entre dois pontos (lat/lon em graus)."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def estimar_altitude_m(lat: float, lon: float, distrito_norm: str) -> float:
    """
    Modelo hipsométrico contínuo aproximado da Bacia Sedimentar de São Paulo
    e seus altos estruturais (Espigão Central, Cantareira, Planalto Paulistano):
    - Calha do Tietê / Pinheiros / Tamanduateí: ~720-735 m
    - Espigão Paulista (Consolação / Bela Vista / Vila Mariana): ~810-825 m
    - Extremo Norte (Cantareira / Tremembé / Perus / Jaraguá): ~820-900 m
    - Extremo Sul (Parelheiros / Marsilac / Grajaú / Jardim Ângela): ~780-860 m
    - Colinas Leste/Sudeste (São Mateus / Cidade Tiradentes): ~790-845 m
    """
    base = 755.0
    # Várzea do Rio Tietê (eixo aprox. lat = -23.515) e Rio Pinheiros (lon = -46.70)
    dist_tiete = abs(lat - (-23.515))
    depressao_tiete = -35.0 * math.exp(-((dist_tiete / 0.025) ** 2))
    dist_pinheiros = math.hypot((lat - (-23.59)) * 0.8, lon - (-46.70))
    depressao_pinheiros = -28.0 * math.exp(-((dist_pinheiros / 0.03) ** 2))

    # Espigão Central (Av. Paulista / Sumaré / Vila Mariana)
    dist_espigao = math.hypot(lat - (-23.561), (lon - (-46.655)) * 0.7)
    crista_espigao = 65.0 * math.exp(-((dist_espigao / 0.035) ** 2))

    # Serra da Cantareira / Jaraguá (Norte)
    elev_norte = 130.0 * max(0.0, (lat - (-23.485)) / 0.09) if lat > -23.485 else 0.0

    # Planalto Atlântico / Serra do Mar (Extremo Sul)
    elev_sul = 95.0 * max(0.0, ((-23.64) - lat) / 0.25) if lat < -23.64 else 0.0

    # Altos da Zona Leste (São Mateus / Cidade Tiradentes / Fazenda do Carmo)
    elev_leste = 55.0 * max(0.0, (lon - (-46.50)) / 0.14) if lon > -46.50 else 0.0

    # Ondulação topográfica local determinística (rugosidade de colinas)
    ondulacao = 14.0 * math.sin(lat * 420.0) * math.cos(lon * 420.0)

    alt = base + depressao_tiete + depressao_pinheiros + crista_espigao + elev_norte + elev_sul + elev_leste + ondulacao
    if distrito_norm in {"MARSILAC", "PARELHEIROS", "TREMEMBE", "JARAGUA", "PERUS"}:
        alt += 25.0
    return round(max(718.0, min(940.0, alt)), 1)


def impedancia_topografica_tobler(dist_km: float, alt1_m: float, alt2_m: float) -> tuple[float, float]:
    """
    Calcula o fator de impedância topográfica baseado na Função de Caminhada de Tobler (1993):
        W(s) = 6 * exp(-3.5 * |s + 0.05|), onde s = dh / dx (declividade).
    Em deslocamento bidirecional (ida e volta entre territórios vizinhos), a velocidade
    média relativa em relação ao terreno plano (v0 = 5.0 km/h) define o multiplicador
    de impedância topográfica >= 1.0.

    Returns:
        Tupla (distância_efetiva_topografica_km, declividade_percentual).
    """
    if dist_km <= 0.01:
        return 0.05, 0.0
    dx_m = dist_km * 1000.0
    dh_m = abs(alt2_m - alt1_m)
    s = min(0.35, dh_m / dx_m)  # declividade absoluta
    # Velocidade de subida e descida segundo Tobler (1993)
    v_subida = 6.0 * math.exp(-3.5 * abs(s + 0.05))
    v_descida = 6.0 * math.exp(-3.5 * abs(-s + 0.05))
    v_plano = 6.0 * math.exp(-3.5 * 0.05)  # ~5.037 km/h
    v_media = 2.0 / ((1.0 / v_subida) + (1.0 / v_descida))
    fator_impedancia = max(1.0, v_plano / v_media)
    dist_topo = round(dist_km * fator_impedancia, 2)
    declividade_pct = round(s * 100.0, 2)
    return dist_topo, declividade_pct


# ============================================================================
# KML e Geometria Espacial
# ============================================================================

def carregar_poligonos_kml() -> dict[str, list[list[tuple[float, float]]]]:
    if not ARQ_KML.exists():
        raise FileNotFoundError(f"KML não encontrado: {ARQ_KML}")

    ns = {"kml": "http://www.opengis.net/kml/2.2"}
    root = ET.parse(ARQ_KML).getroot()
    poligonos: dict[str, list[list[tuple[float, float]]]] = {}

    for pm in root.findall(".//kml:Placemark", ns):
        nome = pm.findtext("kml:name", default="", namespaces=ns).strip()
        nome_norm = normalizar_texto(nome)
        coords_nodes = pm.findall(
            ".//kml:outerBoundaryIs/kml:LinearRing/kml:coordinates", ns
        )
        aneis: list[list[tuple[float, float]]] = []
        for cn in coords_nodes:
            txt = (cn.text or "").strip()
            pts: list[tuple[float, float]] = []
            for tok in txt.replace("\n", " ").split():
                parts = tok.split(",")
                if len(parts) >= 2:
                    try:
                        pts.append((float(parts[0]), float(parts[1])))
                    except ValueError:
                        pass
            if len(pts) >= 3:
                aneis.append(pts)
        if aneis:
            poligonos[nome_norm] = aneis

    return poligonos


def centroide_poligono(aneis: list[list[tuple[float, float]]]) -> tuple[float, float]:
    all_pts = [p for anel in aneis for p in anel]
    if not all_pts:
        return (0.0, 0.0)
    cx = sum(p[0] for p in all_pts) / len(all_pts)
    cy = sum(p[1] for p in all_pts) / len(all_pts)
    return (cx, cy)


def ponto_em_anel(x: float, y: float, anel: list[tuple[float, float]]) -> bool:
    dentro = False
    n = len(anel)
    j = n - 1
    for i in range(n):
        xi, yi = anel[i]
        xj, yj = anel[j]
        if (yi > y) != (yj > y):
            x_int = (xj - xi) * (y - yi) / ((yj - yi) if (yj - yi) != 0 else 1e-12) + xi
            if x < x_int:
                dentro = not dentro
        j = i
    return dentro


def poligonos_sao_vizinhos(
    aneis1: list[list[tuple[float, float]]],
    aneis2: list[list[tuple[float, float]]],
    limiar: float = 0.003,
) -> bool:
    pts1: list[tuple[float, float]] = []
    for anel in aneis1:
        step = max(1, len(anel) // 80)
        pts1.extend(anel[::step])

    pts2: list[tuple[float, float]] = []
    for anel in aneis2:
        step = max(1, len(anel) // 80)
        pts2.extend(anel[::step])

    limiar2 = limiar ** 2
    for p1 in pts1:
        for p2 in pts2:
            dx = p1[0] - p2[0]
            dy = p1[1] - p2[1]
            if dx * dx + dy * dy <= limiar2:
                return True
    return False


# ============================================================================
# Carregamento da População e Distritos
# ============================================================================

def carregar_populacao_real() -> dict[str, int]:
    rows = ler_csv_dicts(ARQ_POP_CSV, delimiter=";")
    anos = sorted({int(r["ANO"]) for r in rows if r.get("ANO", "").isdigit()})
    ano_ref = 2020 if 2020 in anos else (max(anos) if anos else 2020)

    pop_agg: dict[str, int] = defaultdict(int)
    for r in rows:
        if r.get("ANO", "") == str(ano_ref):
            d_norm = normalizar_texto(r.get("NOME_DISTR", ""))
            val = r.get("POPULACAO", "0")
            if val.isdigit():
                pop_agg[d_norm] += int(val)
    return dict(pop_agg)


def gerar_distritos_e_adjacencias(
    pop_real: dict[str, int],
    poligonos: dict[str, list[list[tuple[float, float]]]],
) -> tuple[list[dict], list[dict]]:
    distritos: list[dict] = []
    for idx, nome_norm in enumerate(sorted(ZONA_POR_DISTRITO.keys()), start=1):
        zona = ZONA_POR_DISTRITO[nome_norm]
        nome_bonito = NOME_BONITO.get(nome_norm, nome_norm.title())
        lon, lat = centroide_poligono(poligonos[nome_norm]) if nome_norm in poligonos else (0.0, 0.0)
        populacao = pop_real.get(nome_norm, 0)
        if populacao == 0:
            for k, v in pop_real.items():
                if k.replace(" ", "") == nome_norm.replace(" ", ""):
                    populacao = v
                    break
        distritos.append({
            "id": idx,
            "nome": nome_bonito,
            "nome_norm": nome_norm,
            "zona": zona,
            "lat": round(lat, 4),
            "lon": round(lon, 4),
            "populacao": int(populacao),
        })

    nomes_norm = {d["nome_norm"]: d for d in distritos}
    adjacencias_dist: list[dict] = []
    nomes_lista = sorted(nomes_norm.keys())
    for i, n1 in enumerate(nomes_lista):
        for n2 in nomes_lista[i + 1:]:
            if n1 in poligonos and n2 in poligonos:
                if poligonos_sao_vizinhos(poligonos[n1], poligonos[n2]):
                    d1, d2 = nomes_norm[n1], nomes_norm[n2]
                    dist_km = haversine_km(d1["lat"], d1["lon"], d2["lat"], d2["lon"])
                    adjacencias_dist.append({
                        "distrito1_id": min(d1["id"], d2["id"]),
                        "distrito2_id": max(d1["id"], d2["id"]),
                        "distancia_km": round(dist_km, 2),
                    })
    return distritos, adjacencias_dist


# ============================================================================
# Construção dos Vértices UBS (|V| = 454 UBSs reais) e Tesselação de Demanda
# ============================================================================

def formatar_nome_ubs(estab_bruto: str) -> str:
    limpo = re.sub(r"\s+", " ", estab_bruto.strip())
    limpo_up = limpo.upper()
    # Remover sufixos "- UBS", "-UBS", "UBS " redundantes e padronizar prefixo "UBS "
    sem_sufixo = re.sub(r"\s*-\s*UBS\b", "", limpo_up)
    sem_sufixo = re.sub(r"^UBS\s*[-:]?\s*", "", sem_sufixo).strip(" -")
    return f"UBS {sem_sufixo.title()}"


def construir_rede_ubs(
    distritos: list[dict],
    adjacencias_dist: list[dict],
    poligonos: dict[str, list[list[tuple[float, float]]]],
) -> tuple[list[dict], list[dict], list[dict]]:
    rows = ler_csv_dicts(ARQ_SERVICOS_CSV, delimiter=",")

    dist_por_norm = {d["nome_norm"]: d for d in distritos}
    viz_dist: dict[int, set[int]] = {d["id"]: {d["id"]} for d in distritos}
    for a in adjacencias_dist:
        u, v = a["distrito1_id"], a["distrito2_id"]
        viz_dist[u].add(v)
        viz_dist[v].add(u)

    # Identificar endereços/coordenadas que possuem AMA acoplada (reforço de capacidade)
    coords_ama: set[tuple[float, float]] = set()
    for r in rows:
        t = normalizar_texto(r.get("TIPO", ""))
        if "ASSISTENCIA MEDICA AMBULATORIAL" in t or "AMA" in t:
            try:
                lat_a = round(float(r["LAT"]) / 1e6, 3)
                lon_a = round(float(r["LONG"]) / 1e6, 3)
                coords_ama.add((lat_a, lon_a))
            except (KeyError, ValueError):
                pass

    # Extrair todas as UBSs reais (deduplicadas por CNES)
    ubs_vistas_cnes: set[str] = set()
    ubs_brutas: list[dict] = []

    for r in rows:
        tipo_norm = normalizar_texto(r.get("TIPO", ""))
        if tipo_norm != "UNIDADE BASICA DE SAUDE":
            continue

        cnes_raw = r.get("CNES", "").strip()
        cnes = str(int(float(cnes_raw))) if cnes_raw else r.get("ID", "")
        if cnes in ubs_vistas_cnes:
            continue
        ubs_vistas_cnes.add(cnes)

        dist_norm = normalizar_texto(r.get("DISTRITO", ""))
        d_info = dist_por_norm.get(dist_norm)
        if not d_info:
            continue

        lat = float(r["LAT"]) / 1e6
        lon = float(r["LONG"]) / 1e6
        tem_ama = (round(lat, 3), round(lon, 3)) in coords_ama
        alt_m = estimar_altitude_m(lat, lon, dist_norm)

        ubs_brutas.append({
            "cnes": cnes,
            "nome": formatar_nome_ubs(r.get("ESTABELECI", "")),
            "nome_original": r.get("ESTABELECI", "").strip(),
            "distrito_id": d_info["id"],
            "distrito": d_info["nome"],
            "distrito_norm": dist_norm,
            "subprefeitura": r.get("SUBPREF", "").strip().title(),
            "zona": d_info["zona"],
            "endereco": r.get("ENDERECO", "").strip(),
            "bairro": r.get("BAIRRO", "").strip(),
            "cep": r.get("CEP", "").strip(),
            "lat": round(lat, 6),
            "lon": round(lon, 6),
            "altitude_m": alt_m,
            "tem_ama_acoplada": tem_ama,
        })

    # Ordenar deterministicamente por ID de distrito e nome da UBS
    ubs_brutas.sort(key=lambda u: (u["distrito_id"], u["nome"]))
    for idx, u in enumerate(ubs_brutas, start=1):
        u["id"] = idx

    # Agrupar UBSs por distrito para tesselação de Voronoi intradistrital
    ubs_por_distrito: dict[int, list[dict]] = defaultdict(list)
    for u in ubs_brutas:
        ubs_por_distrito[u["distrito_id"]].append(u)

    # ------------------------------------------------------------------------
    # Passo 1: Calcular Demanda Territorial Base (D_v^0) via Voronoi no KML
    # ------------------------------------------------------------------------
    demanda_por_ubs: dict[int, int] = defaultdict(int)

    for d in distritos:
        did = d["id"]
        pop_d = d["populacao"]
        d_norm = d["nome_norm"]
        candidatas = ubs_por_distrito.get(did, [])

        # Se o distrito não possui UBS própria (4 distritos centrais), a população
        # adscrita é atendida pelas UBSs dos distritos contíguos mais próximas
        if not candidatas:
            for viz_id in viz_dist.get(did, set()):
                candidatas.extend(ubs_por_distrito.get(viz_id, []))
        if not candidatas:
            candidatas = ubs_brutas

        if len(candidatas) == 1:
            demanda_por_ubs[candidatas[0]["id"]] += pop_d
            continue

        # Amostrar grade espacial dentro do polígono KML do distrito (Voronoi)
        aneis = poligonos.get(d_norm, [])
        contagem_voronoi: dict[int, int] = {u["id"]: 1 for u in candidatas}  # suavização de Laplace (+1)
        if aneis:
            anel_princ = max(aneis, key=len)
            xs = [p[0] for p in anel_princ]
            ys = [p[1] for p in anel_princ]
            xmin, xmax = min(xs), max(xs)
            ymin, ymax = min(ys), max(ys)
            nx_grid, ny_grid = 18, 18
            dx = (xmax - xmin) / nx_grid if xmax > xmin else 0.001
            dy = (ymax - ymin) / ny_grid if ymax > ymin else 0.001

            for gx in range(nx_grid):
                px = xmin + (gx + 0.5) * dx
                for gy in range(ny_grid):
                    py = ymin + (gy + 0.5) * dy
                    if ponto_em_anel(px, py, anel_princ):
                        # Encontrar UBS candidata mais próxima (célula de Voronoi)
                        melhor_u = min(
                            candidatas,
                            key=lambda u: (u["lon"] - px) ** 2 + (u["lat"] - py) ** 2,
                        )
                        contagem_voronoi[melhor_u["id"]] += 1

        total_pesos = sum(contagem_voronoi.values())
        alocado = 0
        ids_cand = sorted(contagem_voronoi.keys())
        for i_c, uid in enumerate(ids_cand):
            if i_c == len(ids_cand) - 1:
                parcela = pop_d - alocado
            else:
                parcela = int(round(pop_d * (contagem_voronoi[uid] / total_pesos)))
                alocado += parcela
            demanda_por_ubs[uid] += max(0, parcela)

    # ------------------------------------------------------------------------
    # Passo 2: Dimensionar Capacidade (C_v) e Regra 70% Programada / 30% Espontânea
    # ------------------------------------------------------------------------
    # Pela PNAB/SUS, cada equipe de Atenção Básica/eSF atende ~3.500 hab na cota
    # programada (70%), correspondendo a uma capacidade nominal total de 5.000 hab
    # (incluindo os 30% de demanda espontânea/acolhimento).
    # Unidades em distritos de alta pressão demográfica operam com menos equipes
    # relativas à demanda, reduzindo sua folga efetiva abaixo de 30%.
    vertices_ubs: list[dict] = []
    for u in ubs_brutas:
        uid = u["id"]
        demanda_base = int(demanda_por_ubs[uid])

        # Número de equipes (Porte da UBS: mínimo 2, máximo 12 equipes)
        equipes_ideais = demanda_base / 3500.0
        equipes_instaladas = max(2, min(11, int(round(equipes_ideais))))
        if u["tem_ama_acoplada"]:
            equipes_instaladas += 1

        capacidade_total = int(equipes_instaladas * 5000)
        # Garantir que nenhuma UBS comece já acima de 96% de saturação na rotina base
        if demanda_base > int(capacidade_total * 0.95):
            capacidade_total = int( round((demanda_base / 0.92) / 500.0) * 500 )

        cota_programada_70 = int(round(capacidade_total * 0.70))
        cota_espontanea_30 = capacidade_total - cota_programada_70

        # A folga operacional para absorver demanda de outras UBSs é limitada
        # tanto pelo teto de 30% (demanda espontânea fora de área) quanto pela
        # capacidade ociosa real (C_v - D_v^0):
        folga_bruta = max(0, capacidade_total - demanda_base)
        folga_operacional = min(cota_espontanea_30, folga_bruta)
        taxa_ocupacao = round(demanda_base / capacidade_total, 4) if capacidade_total > 0 else 1.0
        folga_percentual = round((folga_operacional / capacidade_total) * 100.0, 2) if capacidade_total > 0 else 0.0

        # Status na "Tabela Comum" (visão isolada tradicional da gestão)
        if taxa_ocupacao <= 0.72:
            status_tabela = "Verde (Ótimo)"
        elif taxa_ocupacao <= 0.85:
            status_tabela = "Amarelo (Atenção)"
        else:
            status_tabela = "Vermelho (Crítico)"

        vertices_ubs.append({
            "id": uid,
            "cnes": u["cnes"],
            "nome": u["nome"],
            "distrito_id": u["distrito_id"],
            "distrito": u["distrito"],
            "subprefeitura": u["subprefeitura"],
            "zona": u["zona"],
            "endereco": u["endereco"],
            "bairro": u["bairro"],
            "cep": u["cep"],
            "lat": u["lat"],
            "lon": u["lon"],
            "altitude_m": u["altitude_m"],
            "tem_ama_acoplada": u["tem_ama_acoplada"],
            "equipes_esf": equipes_instaladas,
            "populacao": demanda_base,          # compatibilidade legado
            "demanda_base": demanda_base,       # D_v^0 (pacientes adscritos da região)
            "capacidade": capacidade_total,     # C_v (capacidade total da UBS)
            "cota_programada_70": cota_programada_70,
            "cota_espontanea_30": cota_espontanea_30,
            "folga_operacional": folga_operacional,
            "folga_percentual": folga_percentual,
            "taxa_ocupacao": taxa_ocupacao,
            "status_tabela_isolada": status_tabela,
        })

    # ------------------------------------------------------------------------
    # Passo 3: Construir Arestas Topográficas (Grafo de Gabriel Restrito)
    # ------------------------------------------------------------------------
    n = len(vertices_ubs)
    cos_lat = math.cos(math.radians(-23.55))
    pts_km = [(u["lon"] * 111.32 * cos_lat, u["lat"] * 110.57) for u in vertices_ubs]

    arestas_ubs: list[dict] = []
    adj_map: dict[int, dict[int, dict]] = {u["id"]: {} for u in vertices_ubs}

    for i in range(n):
        ui = vertices_ubs[i]
        xi, yi = pts_km[i]
        viz_d = viz_dist.get(ui["distrito_id"], {ui["distrito_id"]})

        for j in range(i + 1, n):
            uj = vertices_ubs[j]
            if uj["distrito_id"] not in viz_d:
                continue

            xj, yj = pts_km[j]
            mx, my = (xi + xj) / 2.0, (yi + yj) / 2.0
            r2 = ((xi - xj) ** 2 + (yi - yj) ** 2) / 4.0
            if r2 > (6.5 / 2.0) ** 2:
                continue

            # Critério do Grafo de Gabriel: nenhuma outra UBS k dentro do disco diametral
            eh_gabriel = True
            for k in range(n):
                if k == i or k == j:
                    continue
                xk, yk = pts_km[k]
                if (xk - mx) ** 2 + (yk - my) ** 2 < r2 * 0.999:
                    eh_gabriel = False
                    break

            if eh_gabriel:
                dist_hav = max(0.05, round(haversine_km(ui["lat"], ui["lon"], uj["lat"], uj["lon"]), 2))
                dist_topo, decliv_pct = impedancia_topografica_tobler(
                    dist_hav, ui["altitude_m"], uj["altitude_m"]
                )
                edge_data = {
                    "distrito1_id": ui["id"],
                    "distrito2_id": uj["id"],
                    "ubs1_id": ui["id"],
                    "ubs2_id": uj["id"],
                    "distancia_km": dist_hav,
                    "impedancia_topografica_km": dist_topo,
                    "declividade_pct": decliv_pct,
                }
                arestas_ubs.append(edge_data)
                adj_map[ui["id"]][uj["id"]] = edge_data
                adj_map[uj["id"]][ui["id"]] = edge_data

    # Verificar conectividade global (garantir componente única se houver ilha)
    def obter_componentes() -> list[set[int]]:
        vis: set[int] = set()
        comps: list[set[int]] = []
        for u_id in adj_map:
            if u_id not in vis:
                comp: set[int] = set()
                fila = deque([u_id])
                vis.add(u_id)
                while fila:
                    atual = fila.popleft()
                    comp.add(atual)
                    for viz in adj_map[atual]:
                        if viz not in vis:
                            vis.add(viz)
                            fila.append(viz)
                comps.append(comp)
        return comps

    comps = obter_componentes()
    while len(comps) > 1:
        comps.sort(key=len)
        c_menor = comps[0]
        melhor_ponte = None
        for uid in c_menor:
            ui = vertices_ubs[uid - 1]
            for vid in range(1, n + 1):
                if vid in c_menor:
                    continue
                uj = vertices_ubs[vid - 1]
                d_hav = haversine_km(ui["lat"], ui["lon"], uj["lat"], uj["lon"])
                if melhor_ponte is None or d_hav < melhor_ponte[0]:
                    melhor_ponte = (d_hav, uid, vid)
        d_hav, uid, vid = melhor_ponte
        ui, uj = vertices_ubs[uid - 1], vertices_ubs[vid - 1]
        dist_hav = max(0.05, round(d_hav, 2))
        dist_topo, decliv_pct = impedancia_topografica_tobler(
            dist_hav, ui["altitude_m"], uj["altitude_m"]
        )
        edge_data = {
            "distrito1_id": min(uid, vid),
            "distrito2_id": max(uid, vid),
            "ubs1_id": min(uid, vid),
            "ubs2_id": max(uid, vid),
            "distancia_km": dist_hav,
            "impedancia_topografica_km": dist_topo,
            "declividade_pct": decliv_pct,
        }
        arestas_ubs.append(edge_data)
        adj_map[uid][vid] = edge_data
        adj_map[vid][uid] = edge_data
        comps = obter_componentes()

    # Gerar lista de serviços compatível com o grafo de UBSs
    servicos: list[dict] = []
    for u in vertices_ubs:
        servicos.append({
            "id": u["id"],
            "cnes": u["cnes"],
            "nome": u["nome"],
            "tipo": "ubs",
            "distrito_id": u["id"],
            "distrito_nome": u["distrito"],
            "capacidade": u["capacidade"],
            "demanda_base": u["demanda_base"],
            "leitos": 0,
        })

    return vertices_ubs, arestas_ubs, servicos


def salvar_json(caminho: Path, payload: list[dict]) -> None:
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def main() -> None:
    print("=" * 68)
    print("SPGraph - Geração da Malha Topológica Real de UBSs de São Paulo")
    print("=" * 68)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("\n1. Carregando população distrital e polígonos KML...")
    pop_real = carregar_populacao_real()
    poligonos = carregar_poligonos_kml()
    distritos, adj_dist = gerar_distritos_e_adjacencias(pop_real, poligonos)
    print(f"   Distritos processados: {len(distritos)} | Fronteiras distritais: {len(adj_dist)}")

    print("\n2. Construindo vértices das UBSs reais, capacidade 70/30 e Grafo de Gabriel...")
    vertices_ubs, arestas_ubs, servicos = construir_rede_ubs(distritos, adj_dist, poligonos)

    # Remover campo auxiliar nome_norm antes de salvar distritos.json
    distritos_limpos = [{k: v for k, v in d.items() if k != "nome_norm"} for d in distritos]

    salvar_json(ARQ_DISTRITOS, distritos_limpos)
    salvar_json(ARQ_ADJ_DISTRITOS, adj_dist)
    salvar_json(ARQ_UBS_VERTICES, vertices_ubs)
    salvar_json(ARQ_ADJ, arestas_ubs)
    salvar_json(ARQ_SERVICOS, servicos)

    pop_total = sum(u["demanda_base"] for u in vertices_ubs)
    cap_total = sum(u["capacidade"] for u in vertices_ubs)
    folga_total = sum(u["folga_operacional"] for u in vertices_ubs)

    zonas_cont: dict[str, int] = defaultdict(int)
    for u in vertices_ubs:
        zonas_cont[u["zona"]] += 1

    print("\n" + "=" * 68)
    print("RESUMO DA REDE GERADA:")
    print(f"  Vértices (UBSs reais georreferenciadas): |V| = {len(vertices_ubs)}")
    for z, c in sorted(zonas_cont.items()):
        print(f"    - Zona {z}: {c} UBSs")
    print(f"  Arestas (Conexões topográficas Gabriel): |E| = {len(arestas_ubs)}")
    print(f"  Demanda Territorial Total (Pop. SP):     {pop_total:,} hab.")
    print(f"  Capacidade Nominal Total Instalada:      {cap_total:,} hab.")
    print(f"  Folga Operacional Total (Regra <=30%):   {folga_total:,} vagas")
    print("=" * 68)


if __name__ == "__main__":
    main()
