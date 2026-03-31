"""
SPGraph - Geração de dados (recorte enxuto + dados reais)
===========================================================
Gera os arquivos JSON do projeto usando os CSV reais da pasta data/:
- deinfosacadsau2014.csv (serviços e leitos)
- evolucao_msp_pop_sexo_idade.csv (população por distrito)

Recorte aplicado para reduzir escopo:
- Mantém apenas zonas: Leste, Norte e Sul
- Exclui zonas: Centro e Oeste
"""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"

ARQ_DISTRITOS = DATA_DIR / "distritos.json"
ARQ_ADJ = DATA_DIR / "adjacencias.json"
ARQ_SERVICOS_CSV = DATA_DIR / "deinfosacadsau2014.csv"
ARQ_POP_CSV = DATA_DIR / "evolucao_msp_pop_sexo_idade.csv"

ZONAS_MANTIDAS = {"Leste", "Norte", "Sul"}


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


def carregar_distritos_base() -> list[dict]:
    if not ARQ_DISTRITOS.exists():
        raise FileNotFoundError(
            f"Arquivo base não encontrado: {ARQ_DISTRITOS}. "
            "Mantenha um distritos.json de referência no diretório data/."
        )

    with open(ARQ_DISTRITOS, "r", encoding="utf-8") as f:
        distritos = json.load(f)

    return distritos


def recortar_distritos_com_populacao(distritos_base: list[dict], pop_real: dict[str, int]) -> list[dict]:
    distritos_saida: list[dict] = []

    for d in distritos_base:
        if d.get("zona") not in ZONAS_MANTIDAS:
            continue

        nome_norm = normalizar_texto(d["nome"])
        populacao = pop_real.get(nome_norm, int(d.get("populacao", 0)))

        distritos_saida.append({
            "id": int(d["id"]),
            "nome": d["nome"],
            "zona": d["zona"],
            "lat": float(d["lat"]),
            "lon": float(d["lon"]),
            "populacao": int(populacao),
        })

    return distritos_saida


def recortar_adjacencias(ids_mantidos: set[int]) -> list[dict]:
    if not ARQ_ADJ.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {ARQ_ADJ}")

    with open(ARQ_ADJ, "r", encoding="utf-8") as f:
        adjacencias_base = json.load(f)

    adj = [
        {
            "distrito1_id": int(a["distrito1_id"]),
            "distrito2_id": int(a["distrito2_id"]),
            "distancia_km": float(a["distancia_km"]),
        }
        for a in adjacencias_base
        if int(a["distrito1_id"]) in ids_mantidos and int(a["distrito2_id"]) in ids_mantidos
    ]

    return adj


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


def salvar_json(caminho: Path, payload: list[dict]) -> None:
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def main() -> None:
    print("=" * 60)
    print("SPGraph - Geração de dados reais com recorte por zonas")
    print("=" * 60)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    distritos_base = carregar_distritos_base()
    pop_real = carregar_populacao_real()

    distritos = recortar_distritos_com_populacao(distritos_base, pop_real)
    ids_mantidos = {d["id"] for d in distritos}
    ids_por_nome_norm = {normalizar_texto(d["nome"]): d["id"] for d in distritos}

    adjacencias = recortar_adjacencias(ids_mantidos)
    servicos = gerar_servicos_reais(ids_por_nome_norm)

    salvar_json(ARQ_DISTRITOS, distritos)
    salvar_json(ARQ_ADJ, adjacencias)
    salvar_json(DATA_DIR / "servicos.json", servicos)

    contagem: dict[str, int] = {}
    for s in servicos:
        contagem[s["tipo"]] = contagem.get(s["tipo"], 0) + 1

    print("\n✅ Arquivos atualizados:")
    print(f"   - {ARQ_DISTRITOS}")
    print(f"   - {ARQ_ADJ}")
    print(f"   - {DATA_DIR / 'servicos.json'}")

    print(f"\n{'=' * 60}")
    print("📊 Resumo do recorte")
    print(f"   Zonas mantidas: {', '.join(sorted(ZONAS_MANTIDAS))}")
    print(f"   Distritos (vértices): {len(distritos)}")
    print(f"   Adjacências (arestas): {len(adjacencias)}")
    print(f"   Serviços totais: {len(servicos)}")
    print(f"   Hospital SUS: {contagem.get('hospital_sus', 0)}")
    print(f"   UPA:          {contagem.get('upa', 0)}")
    print(f"   UBS:          {contagem.get('ubs', 0)}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
