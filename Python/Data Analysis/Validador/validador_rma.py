"""
VALIDADOR DE POLÍTICAS DE CRÉDITO
===================================
Valida regras implementadas em notebooks PySpark contra gabaritos (RMA).

Compatível com: Windows, Linux, Databricks.
Fontes suportadas: Parquet local, JDBC (BD), Databricks Tables, FICO.

Uso:
  # Execução local com parquet:
  python validador_rma.py --notebook ./notebooks/regras.ipynb --input ./dados/input --rma ./dados/rma

  # Execução com BD via JDBC:
  python validador_rma.py --notebook ./notebooks/regras.ipynb --fonte jdbc \\
      --jdbc-url "jdbc:oracle:thin:@host:1521:ORCL" \\
      --tabela-input "SCHEMA.INPUT" --tabela-rma "SCHEMA.RMA" \\
      --usuario user --senha pass

  # Execução com Databricks:
  python validador_rma.py --notebook ./notebooks/regras.ipynb --fonte databricks \\
      --catalog catalogo --schema credito \\
      --tabela-input clientes --tabela-rma rma_clientes

  # Execução com FICO:
  python validador_rma.py --notebook ./notebooks/regras.ipynb --fonte fico \\
      --fico-endpoint "https://fico.empresa.com/api/v1" \\
      --tabela-input scores --tabela-rma rma_scores --fico-token "Bearer xxx"
"""

from __future__ import annotations

import argparse
import os
import re
import sys

# Adiciona diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import nbformat
from pyspark.sql import functions as F
from pyspark.sql.types import (
    IntegerType, StringType, DoubleType, BooleanType
)

from config import (
    Config, FonteDados, TipoFonte,
    config_local_parquet, config_databricks, config_jdbc, config_fico,
)


# ═══════════════════════════════════════════════════════════════
#  Leitor de Notebooks
# ═══════════════════════════════════════════════════════════════

def varrer_notebook(caminho_nb: str) -> list[dict]:
    """
    Lê o notebook e extrai as regras (withColumn).
    Aceita caminhos locais e também notebooks já baixados de outras fontes.
    """
    if not os.path.exists(caminho_nb):
        print(f"[ERRO] Notebook não encontrado em {caminho_nb}")
        return []

    with open(caminho_nb, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    politicas = []
    regex_regra = r"\.withColumn\s*\(\s*[\"'](.*?)[\"']"

    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue

        codigo = cell.source
        if not codigo.strip():
            continue

        for match in re.finditer(regex_regra, codigo):
            # Verifica se a linha está comentada
            texto_antes = codigo[: match.start()]
            linha_atual = texto_antes.split("\n")[-1]
            if "#" in linha_atual:
                continue

            politicas.append({
                "id": len(politicas) + 1,
                "nome": match.group(1),
                "codigo": codigo,
                "celula": i + 1,
            })

    return politicas


# ═══════════════════════════════════════════════════════════════
#  Validação Regra a Regra
# ═══════════════════════════════════════════════════════════════

def executar_validacao(spark, politica: dict, df_input, df_rma,
                       prefixo_rma: str, chave_primaria: str):
    """Valida uma regra do notebook contra o gabarito RMA."""
    print(f"[TESTE] Validando Regra: {politica['nome']} ... ", end="")

    df_local = df_input.alias("df_input")
    ctx = {
        "spark": spark,
        "F": F,
        "df": df_local,
        "IntegerType": IntegerType,
        "StringType": StringType,
        "DoubleType": DoubleType,
        "BooleanType": BooleanType,
    }

    try:
        exec(politica["codigo"], {**globals()}, ctx)
        df_resultado = ctx.get("df")

        if politica["nome"] not in df_resultado.columns:
            print("[ERRO] Coluna não criada após execução.")
            return

        col_calc = politica["nome"]
        col_rma = f"{prefixo_rma}{col_calc}"

        if col_rma not in df_rma.columns:
            print("[PULAR] Sem gabarito no RMA para esta coluna.")
            return

        df_compare = (
            df_resultado.select(chave_primaria, F.col(col_calc).alias("vlr_calc"))
            .join(
                df_rma.select(chave_primaria, F.col(col_rma).alias("vlr_rma")),
                on=chave_primaria,
            )
        )

        df_divergente = df_compare.filter(
            (F.col("vlr_calc") != F.col("vlr_rma"))
            | (F.col("vlr_calc").isNull() & F.col("vlr_rma").isNotNull())
            | (F.col("vlr_calc").isNotNull() & F.col("vlr_rma").isNull())
        )

        total_erros = df_divergente.count()

        if total_erros == 0:
            print("[SUCESSO] OK")
        else:
            print("[FALHA] DIVERGÊNCIA ENCONTRADA")
            print(f"   -> Encontrados {total_erros} erros. Amostra:")
            df_divergente.show(5)

    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha na execução do código: {e}")


# ═══════════════════════════════════════════════════════════════
#  Pipeline Principal
# ═══════════════════════════════════════════════════════════════

def main(cfg: Config | None = None):
    """
    Executa a validação completa.

    Args:
        cfg: Config já montada. Se None, monta a partir dos args da CLI.
    """
    print("\n╔══════════════════════════════════════════════╗")
    print("║   VALIDADOR DE POLÍTICAS DE CRÉDITO          ║")
    print("╚══════════════════════════════════════════════╝\n")

    # ─── Config ───
    if cfg is None:
        cfg = _config_via_cli()

    print(cfg.resumo())
    print()

    # ─── Spark ───
    spark = cfg.iniciar_spark()

    # ─── Dados ───
    try:
        if cfg.fonte_input is None or cfg.fonte_rma is None:
            print("[ERRO] Fontes de dados (input e rma) não configuradas.")
            return
        df_input = cfg.carregar_dados(spark, cfg.fonte_input)
        df_rma = cfg.carregar_dados(spark, cfg.fonte_rma)
    except Exception as e:
        print(f"[ERRO] Falha ao carregar dados: {e}")
        return

    # ─── Regras do Notebook ───
    if not cfg.caminho_notebook:
        print("[ERRO] Caminho do notebook não informado.")
        return

    politicas = varrer_notebook(cfg.caminho_notebook)

    if not politicas:
        print("[AVISO] Nenhuma regra encontrada (Verifique se o notebook está salvo).")
        return

    print(f"\n[INFO] Testando {len(politicas)} políticas...\n")

    # ─── Execução ───
    for p in politicas:
        executar_validacao(
            spark, p, df_input, df_rma,
            prefixo_rma=cfg.prefixo_rma,
            chave_primaria=cfg.chave_primaria,
        )

    print("\n--- FIM DA VALIDAÇÃO ---")


# ═══════════════════════════════════════════════════════════════
#  CLI (Linha de Comando)
# ═══════════════════════════════════════════════════════════════

def _config_via_cli() -> Config:
    """Monta Config a partir de argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Validador de Políticas de Crédito PySpark",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Local com parquet
  python validador_rma.py --notebook nb.ipynb --input ./dados/input --rma ./dados/rma

  # BD via JDBC (Oracle)
  python validador_rma.py --notebook nb.ipynb --fonte jdbc \\
    --jdbc-url "jdbc:oracle:thin:@host:1521:DB" \\
    --tabela-input SCHEMA.INPUT --tabela-rma SCHEMA.RMA \\
    --usuario user --senha pass

  # Databricks
  python validador_rma.py --notebook nb.ipynb --fonte databricks \\
    --catalog cat --schema sch --tabela-input tbl --tabela-rma rma

  # FICO
  python validador_rma.py --notebook nb.ipynb --fonte fico \\
    --fico-endpoint https://fico.corp/api --tabela-input scores --tabela-rma rma
        """,
    )

    # Geral
    parser.add_argument("--notebook", required=True, help="Caminho do notebook (.ipynb)")
    parser.add_argument("--fonte", choices=["parquet", "jdbc", "databricks", "fico"],
                        default="parquet", help="Tipo de fonte de dados (default: parquet)")
    parser.add_argument("--prefixo-rma", default="rma_", help="Prefixo das colunas RMA")
    parser.add_argument("--chave-primaria", default="id_cliente", help="Coluna chave primária")
    parser.add_argument("--java-home", default="", help="JAVA_HOME (opcional)")

    # Parquet
    parser.add_argument("--input", default="./dados/mock_input", help="Caminho parquet input")
    parser.add_argument("--rma", default="./dados/mock_rma", help="Caminho parquet RMA")

    # JDBC
    parser.add_argument("--jdbc-url", default="", help="URL JDBC (ex: jdbc:oracle:thin:@host:1521:DB)")
    parser.add_argument("--tabela-input", default="", help="Tabela de input (BD/Databricks/FICO)")
    parser.add_argument("--tabela-rma", default="", help="Tabela RMA (BD/Databricks/FICO)")
    parser.add_argument("--usuario", default="", help="Usuário JDBC")
    parser.add_argument("--senha", default="", help="Senha JDBC")
    parser.add_argument("--driver", default="", help="Classe do driver JDBC")

    # Databricks
    parser.add_argument("--catalog", default="", help="Catálogo Databricks (Unity Catalog)")
    parser.add_argument("--schema", default="", help="Schema Databricks")

    # FICO
    parser.add_argument("--fico-endpoint", default="", help="URL da API FICO")
    parser.add_argument("--fico-token", default="", help="Token de autenticação FICO")

    args = parser.parse_args()

    # Monta Config conforme fonte escolhida
    if args.fonte == "parquet":
        return config_local_parquet(
            caminho_notebook=args.notebook,
            caminho_input=args.input,
            caminho_rma=args.rma,
            prefixo_rma=args.prefixo_rma,
            chave_primaria=args.chave_primaria,
            java_home=args.java_home,
        )
    elif args.fonte == "jdbc":
        return config_jdbc(
            caminho_notebook=args.notebook,
            jdbc_url=args.jdbc_url,
            tabela_input=args.tabela_input,
            tabela_rma=args.tabela_rma,
            usuario=args.usuario,
            senha=args.senha,
            driver=args.driver,
            prefixo_rma=args.prefixo_rma,
            chave_primaria=args.chave_primaria,
            java_home=args.java_home,
        )
    elif args.fonte == "databricks":
        return config_databricks(
            caminho_notebook=args.notebook,
            catalog=args.catalog,
            schema=args.schema,
            tabela_input=args.tabela_input,
            tabela_rma=args.tabela_rma,
            prefixo_rma=args.prefixo_rma,
            chave_primaria=args.chave_primaria,
            java_home=args.java_home,
        )
    elif args.fonte == "fico":
        return config_fico(
            caminho_notebook=args.notebook,
            fico_endpoint=args.fico_endpoint,
            tabela_input=args.tabela_input,
            tabela_rma=args.tabela_rma,
            fico_token=args.fico_token,
            prefixo_rma=args.prefixo_rma,
            chave_primaria=args.chave_primaria,
            java_home=args.java_home,
        )

    raise ValueError(f"Fonte desconhecida: {args.fonte}")


if __name__ == "__main__":
    main()