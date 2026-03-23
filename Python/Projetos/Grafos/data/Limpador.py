from pathlib import Path
import unicodedata

import pandas as pd


def normalizar_texto(valor: str) -> str:
    texto = str(valor).strip().upper()
    texto = "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )
    return texto


def peso_unidade(tipo: str) -> int:
    tipo = normalizar_texto(tipo)
    if "HOSPITAL" in tipo:
        return 5
    if "UPA" in tipo:
        return 3
    if "UBS" in tipo:
        return 1
    return 1


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


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    arq_saude = base_dir / "deinfosacadsau2014.csv"
    arq_pop = base_dir / "evolucao_msp_pop_sexo_idade.csv"
    saida = base_dir / "dataset_final.csv"

    # =========================
    # 1. CARREGAR DADOS
    # =========================
    saude = ler_csv_com_fallback(arq_saude)
    pop = ler_csv_com_fallback(arq_pop, sep=";")

    # Normalizar nomes de colunas
    saude.columns = [normalizar_texto(c) for c in saude.columns]
    pop.columns = [normalizar_texto(c) for c in pop.columns]

    # =========================
    # 2. LIMPAR DADOS DE SAÚDE
    # =========================
    # CSV de saúde usa DISTRITO e TIPO
    saude["DISTRITO"] = saude["DISTRITO"].map(normalizar_texto)
    saude["PESO"] = saude["TIPO"].map(peso_unidade)

    capacidade = (
        saude.groupby("DISTRITO", as_index=False)
        .agg(capacidade=("PESO", "sum"), qtd_unidades=("TIPO", "count"))
        .rename(columns={"DISTRITO": "distrito"})
    )

    # =========================
    # 3. LIMPAR POPULAÇÃO
    # =========================
    # CSV de população usa nome_distr e delimitador ';'
    pop["NOME_DISTR"] = pop["NOME_DISTR"].map(normalizar_texto)

    if "ANO" in pop.columns:
        ano_ref = 2020 if (pop["ANO"] == 2020).any() else int(pop["ANO"].max())
        pop = pop.loc[pop["ANO"] == ano_ref].copy()

    pop = (
        pop.groupby("NOME_DISTR", as_index=False)
        .agg(populacao=("POPULACAO", "sum"))
        .rename(columns={"NOME_DISTR": "distrito"})
    )

    # =========================
    # 4. JUNTAR DADOS
    # =========================
    df = pd.merge(capacidade, pop, on="distrito", how="inner")

    # =========================
    # 5. CRIAR INDICADORES
    # =========================
    df["cobertura"] = df["capacidade"] / df["populacao"]
    df["pressao"] = df["populacao"] / df["qtd_unidades"].replace(0, pd.NA)

    # =========================
    # 6. RESULTADO FINAL
    # =========================
    df = df.sort_values(by="cobertura", ascending=True)
    df.to_csv(saida, index=False)

    print(f"✅ Dataset gerado: {saida}")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()