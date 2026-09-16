"""
SPGraph - Geração de dados (todos os 96 distritos de SP)
===========================================================
Gera os arquivos JSON do projeto usando os CSV reais da pasta data/:
- deinfosacadsau2014.csv (serviços e leitos)
- evolucao_msp_pop_sexo_idade.csv (população por distrito)
- São Paulo.kml (polígonos distritais para adjacências)

Escopo: TODOS os 96 distritos administrativos de São Paulo.
"""

from __future__ import annotations

import json
import math
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
import re

import pandas as pd

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"

ARQ_DISTRITOS = DATA_DIR / "distritos.json"
ARQ_ADJ = DATA_DIR / "adjacencias.json"
ARQ_SERVICOS_CSV = DATA_DIR / "deinfosacadsau2014.csv"
ARQ_POP_CSV = DATA_DIR / "evolucao_msp_pop_sexo_idade.csv"
ARQ_UBS_MD = DATA_DIR / "Unid_Munic_Saude_Subp.md"
ARQ_UBS_VERTICES = DATA_DIR / "ubs_vertices.json"
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

# Nomes com acentuação correta
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
    texto = "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )
    return texto


def ler_csv_com_fallback(caminho: Path, **kwargs) -> pd.DataFrame:
    encodings = ["utf-8", "latin1", "cp1252"]
    ultimo_erro: UnicodeDecodeError | None = None

    for enc in encodings:
        try:
            return pd.read_csv(caminho, encoding=enc, **kwargs)
        except UnicodeDecodeError as exc:
            ultimo_erro = exc

    raise RuntimeError(
        f"Não foi possível ler {caminho.name} com as codificações testadas: {encodings}"
    ) from ultimo_erro


def mapear_tipo_servico(tipo_bruto: str, classe_bruta: str, estabelecimento_bruto: str) -> str | None:
    t = normalizar_texto(tipo_bruto)
    c = normalizar_texto(classe_bruta)
    e = normalizar_texto(estabelecimento_bruto)

    if "UNIDADE BASICA DE SAUDE" in t or "UBS" in e:
        return "ubs"
    if "UPA" in t or "UPA" in e:
        return "upa"
    if "HOSPITAL" in t or c == "HOSPITAL":
        return "hospital_sus"
    return None


# ============================================================================
# Haversine — distância real entre coordenadas geográficas
# ============================================================================

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distância em km entre dois pontos (lat/lon em graus)."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ============================================================================
# Cálculo de adjacências a partir do KML
# ============================================================================

def carregar_poligonos_kml() -> dict[str, list[list[tuple[float, float]]]]:
    """Carrega polígonos distritais a partir do KML."""
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
    """Calcula centróide médio de um conjunto de anéis (lon, lat)."""
    all_pts = [p for anel in aneis for p in anel]
    if not all_pts:
        return (0.0, 0.0)
    cx = sum(p[0] for p in all_pts) / len(all_pts)
    cy = sum(p[1] for p in all_pts) / len(all_pts)
    return (cx, cy)


def poligonos_sao_vizinhos(
    aneis1: list[list[tuple[float, float]]],
    aneis2: list[list[tuple[float, float]]],
    limiar: float = 0.003,
) -> bool:
    """
    Verifica se dois distritos são vizinhos pela proximidade de suas fronteiras.
    Amostra pontos dos polígonos e verifica se algum par está dentro do limiar.
    limiar em graus (~0.003° ≈ 330m na latitude de SP).
    """
    # Amostrar pontos de cada polígono para eficiência
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


def gerar_adjacencias_kml(
    distritos: list[dict],
    poligonos: dict[str, list[list[tuple[float, float]]]],
) -> list[dict]:
    """
    Gera adjacências entre distritos com base nos polígonos do KML.
    Dois distritos são adjacentes se suas fronteiras estão a ≤ 0.003° (~330m).
    O peso da aresta é a distância Haversine entre centróides.
    """
    nomes_norm = {normalizar_texto(d["nome"]): d for d in distritos}
    adjacencias: list[dict] = []
    pares_vistos: set[tuple[int, int]] = set()

    nomes_lista = sorted(nomes_norm.keys())

    for i, nome1 in enumerate(nomes_lista):
        for nome2 in nomes_lista[i + 1:]:
            if nome1 not in poligonos or nome2 not in poligonos:
                continue

            if poligonos_sao_vizinhos(poligonos[nome1], poligonos[nome2]):
                d1 = nomes_norm[nome1]
                d2 = nomes_norm[nome2]
                id1, id2 = d1["id"], d2["id"]

                par = (min(id1, id2), max(id1, id2))
                if par in pares_vistos:
                    continue
                pares_vistos.add(par)

                dist_km = haversine_km(d1["lat"], d1["lon"], d2["lat"], d2["lon"])

                adjacencias.append({
                    "distrito1_id": par[0],
                    "distrito2_id": par[1],
                    "distancia_km": round(dist_km, 2),
                })

    return adjacencias


# ============================================================================
# Carregamento de dados
# ============================================================================

def carregar_populacao_real() -> dict[str, int]:
    pop = ler_csv_com_fallback(ARQ_POP_CSV, sep=";")
    pop.columns = [normalizar_texto(c) for c in pop.columns]

    pop["NOME_DISTR"] = pop["NOME_DISTR"].map(normalizar_texto)

    if "ANO" in pop.columns:
        ano_ref = 2020 if (pop["ANO"] == 2020).any() else int(pop["ANO"].max())
        pop = pop.loc[pop["ANO"] == ano_ref].copy()

    pop_agg = (
        pop.groupby("NOME_DISTR", as_index=False)
        .agg(populacao=("POPULACAO", "sum"))
    )

    return {
        row["NOME_DISTR"]: int(row["populacao"])
        for _, row in pop_agg.iterrows()
    }


def gerar_distritos_completos(pop_real: dict[str, int]) -> list[dict]:
    """
    Gera a lista de 96 distritos com dados do KML (centróide) e CSV (população).
    """
    poligonos = carregar_poligonos_kml()

    distritos: list[dict] = []
    id_sequencial = 1

    for nome_norm in sorted(ZONA_POR_DISTRITO.keys()):
        zona = ZONA_POR_DISTRITO[nome_norm]
        nome_bonito = NOME_BONITO.get(nome_norm, nome_norm.title())

        # Centróide do polígono KML
        if nome_norm in poligonos:
            lon, lat = centroide_poligono(poligonos[nome_norm])
        else:
            lat, lon = 0.0, 0.0
            print(f"  ⚠️  Sem polígono KML para: {nome_bonito}")

        # População real do CSV
        populacao = pop_real.get(nome_norm, 0)
        if populacao == 0:
            # Tentar variações de nome
            for k, v in pop_real.items():
                if k.replace(" ", "") == nome_norm.replace(" ", ""):
                    populacao = v
                    break

        distritos.append({
            "id": id_sequencial,
            "nome": nome_bonito,
            "zona": zona,
            "lat": round(lat, 4),
            "lon": round(lon, 4),
            "populacao": int(populacao),
        })
        id_sequencial += 1

    return distritos


def gerar_servicos_reais(ids_por_nome_norm: dict[str, int]) -> list[dict]:
    saude = ler_csv_com_fallback(ARQ_SERVICOS_CSV)
    saude.columns = [normalizar_texto(c) for c in saude.columns]

    saude["DISTRITO"] = saude["DISTRITO"].map(normalizar_texto)
    saude["TIPO_GRUPO"] = saude.apply(
        lambda row: mapear_tipo_servico(row["TIPO"], row["CLASSE"], row["ESTABELECI"]),
        axis=1,
    )

    saude = saude[saude["TIPO_GRUPO"].notna()].copy()
    saude = saude[saude["DISTRITO"].isin(ids_por_nome_norm)].copy()

    servicos: list[dict] = []
    vistos: set[tuple[int, str, str]] = set()

    for row in saude.itertuples(index=False):
        did = ids_por_nome_norm[getattr(row, "DISTRITO")]
        nome = str(getattr(row, "ESTABELECI", "")).strip()
        tipo = str(getattr(row, "TIPO_GRUPO"))

        if not nome:
            nome = f"{tipo.upper()}_{did}"

        chave = (did, tipo, normalizar_texto(nome))
        if chave in vistos:
            continue
        vistos.add(chave)

        leitos_bruto = getattr(row, "LEITOS", 0)

        leitos = 0
        if pd.notna(leitos_bruto):
            try:
                leitos = int(float(leitos_bruto))
            except (TypeError, ValueError):
                leitos = 0

        servicos.append({
            "id": len(servicos) + 1,
            "nome": nome,
            "tipo": tipo,
            "distrito_id": did,
            "leitos": max(0, leitos),
        })

    return servicos


def extrair_ubs_por_subprefeitura(caminho_md: Path) -> list[dict]:
    if not caminho_md.exists():
        raise FileNotFoundError(
            f"Arquivo de UBS não encontrado: {caminho_md}. "
            "Salve o MD em data/ antes de gerar os dados."
        )

    linhas = caminho_md.read_text(encoding="utf-8", errors="ignore").splitlines()
    ubs: list[dict] = []
    vistos: set[str] = set()
    subprefeitura_atual = "N/D"

    for ln in linhas:
        raw = ln.strip()
        if not raw:
            continue

        if raw.upper().startswith("## SUBPREFEITURAS"):
            continue

        if raw.upper().startswith("## SUBPREFEITURA"):
            texto = raw.lstrip("#").strip()
            texto = re.sub(r"^SUBPREFEITURA\s+DE\s+", "", texto, flags=re.I)
            texto = re.sub(r"^SUBPREFEITURA\s+DA\s+", "", texto, flags=re.I)
            texto = re.sub(r"^SUBPREFEITURA\s+DO\s+", "", texto, flags=re.I)
            subprefeitura_atual = texto.strip()
            continue

        match_ubs = re.match(r"^(##\s*)?UBS\s+(.+)$", raw, flags=re.I)
        if not match_ubs:
            continue

        nome_ubs = match_ubs.group(2).strip()
        if not nome_ubs:
            continue

        if "UNIDADE BASICA DE SAUDE" in normalizar_texto(nome_ubs):
            continue

        chave = normalizar_texto(nome_ubs)
        if chave in vistos:
            continue
        vistos.add(chave)

        ubs.append({
            "nome": f"UBS {nome_ubs}",
            "subprefeitura": subprefeitura_atual,
        })

    return ubs


def gerar_vertices_ubs(distritos: list[dict]) -> list[dict]:
    ubs_lista = extrair_ubs_por_subprefeitura(ARQ_UBS_MD)
    distritos_ordenados = sorted(distritos, key=lambda d: int(d["id"]))

    if len(ubs_lista) < len(distritos_ordenados):
        print(
            f"  ⚠️  UBSs encontradas ({len(ubs_lista)}) < distritos ({len(distritos_ordenados)}). "
            f"Distritos excedentes usarão nome genérico."
        )

    vertices = []
    for i, d in enumerate(distritos_ordenados):
        if i < len(ubs_lista):
            u = ubs_lista[i]
            nome_ubs = u["nome"]
            subpref = u["subprefeitura"]
        else:
            nome_ubs = f"UBS {d['nome']}"
            subpref = "N/D"

        vertices.append({
            "id": int(d["id"]),
            "nome": nome_ubs,
            "zona": d["zona"],
            "lat": float(d["lat"]),
            "lon": float(d["lon"]),
            "populacao": int(d["populacao"]),
            "subprefeitura": subpref,
        })
    return vertices


def salvar_json(caminho: Path, payload: list[dict]) -> None:
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


# ============================================================================
# Main
# ============================================================================

def main() -> None:
    print("=" * 60)
    print("SPGraph - Geração de dados (96 distritos de SP)")
    print("=" * 60)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 1. População real
    print("\n📊 Carregando população real...")
    pop_real = carregar_populacao_real()
    print(f"   Distritos com população: {len(pop_real)}")

    # 2. Gerar distritos completos (96)
    print("\n🏙️  Gerando distritos...")
    distritos = gerar_distritos_completos(pop_real)
    print(f"   Distritos gerados: {len(distritos)}")

    # 3. Calcular adjacências a partir do KML
    print("\n🔗 Calculando adjacências a partir do KML...")
    poligonos = carregar_poligonos_kml()
    adjacencias = gerar_adjacencias_kml(distritos, poligonos)
    print(f"   Adjacências calculadas: {len(adjacencias)}")

    # 4. Serviços reais
    print("\n🏥 Carregando serviços de saúde...")
    ids_por_nome_norm = {normalizar_texto(d["nome"]): d["id"] for d in distritos}
    servicos = gerar_servicos_reais(ids_por_nome_norm)

    # 5. Vértices UBS
    print("\n📍 Gerando vértices UBS...")
    vertices_ubs = gerar_vertices_ubs(distritos)

    # 6. Salvar tudo
    print("\n💾 Salvando arquivos...")
    salvar_json(ARQ_DISTRITOS, distritos)
    salvar_json(ARQ_ADJ, adjacencias)
    salvar_json(DATA_DIR / "servicos.json", servicos)
    salvar_json(ARQ_UBS_VERTICES, vertices_ubs)

    # Resumo
    contagem: dict[str, int] = {}
    for s in servicos:
        contagem[s["tipo"]] = contagem.get(s["tipo"], 0) + 1

    zonas_contagem: dict[str, int] = {}
    for d in distritos:
        zonas_contagem[d["zona"]] = zonas_contagem.get(d["zona"], 0) + 1

    print(f"\n{'=' * 60}")
    print("✅ Resumo")
    print(f"   Distritos (vértices): {len(distritos)}")
    for z, c in sorted(zonas_contagem.items()):
        print(f"     {z}: {c}")
    print(f"   Adjacências (arestas): {len(adjacencias)}")
    print(f"   Serviços totais: {len(servicos)}")
    print(f"     Hospital SUS: {contagem.get('hospital_sus', 0)}")
    print(f"     UPA:          {contagem.get('upa', 0)}")
    print(f"     UBS:          {contagem.get('ubs', 0)}")
    print(f"   Vértices UBS: {len(vertices_ubs)}")
    print(f"{'=' * 60}")

    # Validações
    assert len(distritos) == 96, f"Esperado 96 distritos, obteve {len(distritos)}"
    print("\n✅ Validação: 96 distritos — OK")


if __name__ == "__main__":
    main()
