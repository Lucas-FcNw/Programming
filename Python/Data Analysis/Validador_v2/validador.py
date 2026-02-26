"""
Validador de Políticas de Crédito — v2 (Simplificado)

Uso:
  python validador.py                                  → usa notebook padrão da pasta notebooks/
  python validador.py notebooks/regras_credito.ipynb   → caminho relativo
  python validador.py /caminho/absoluto/notebook.ipynb → caminho absoluto
  python validador.py C:\\Users\\...\\regras.ipynb       → caminho Windows
"""

from __future__ import annotations

import os
import sys
import re
import platform
import tempfile
import glob
from datetime import datetime
from typing import Optional

# ═══════════════════════════════════════════════════════════
#  1. CONFIGURAÇÃO DE AMBIENTE (Windows / Linux)
# ═══════════════════════════════════════════════════════════

def _configurar_ambiente():
    """
    Configura JAVA_HOME e HADOOP_HOME automaticamente.
    Resolve no Windows:
      - winutils.exe not found
      - HADOOP_HOME / hadoop.home.dir unset
      - NativeCodeLoader warning
    """
    sistema = platform.system().lower()

    # ── JAVA ──
    if not os.environ.get("JAVA_HOME"):
        if sistema == "windows":
            candidatos = [
                r"C:\Program Files\Java\jdk-17*",
                r"C:\Program Files\Eclipse Adoptium\jdk-17*",
                r"C:\Program Files\Microsoft\jdk-17*",
                r"C:\Program Files\Java\jdk-11*",
            ]
        else:
            candidatos = [
                "/usr/lib/jvm/java-17*",
                "/usr/lib/jvm/java-11*",
                "/usr/local/sdkman/candidates/java/current",
            ]
        for padrao in candidatos:
            matches = glob.glob(padrao)
            if matches:
                os.environ["JAVA_HOME"] = matches[0]
                break

    # ── HADOOP (crítico no Windows) ──
    hadoop_home = os.environ.get("HADOOP_HOME", "")
    winutils_ok = hadoop_home and os.path.isfile(
        os.path.join(hadoop_home, "bin", "winutils.exe")
    )

    if sistema == "windows" and not winutils_ok:
        # Procura em caminhos comuns
        for caminho in [
            os.path.join(os.path.expanduser("~"), "hadoop"),
            r"C:\hadoop", r"C:\hadoop3", r"C:\tools\hadoop",
        ]:
            winutils = os.path.join(caminho, "bin", "winutils.exe")
            if os.path.isfile(winutils):
                os.environ["HADOOP_HOME"] = caminho
                os.environ["PATH"] = os.path.join(caminho, "bin") + ";" + os.environ.get("PATH", "")
                winutils_ok = True
                break

        if not winutils_ok:
            # Cria diretório mínimo para o Spark não crashar
            hadoop_tmp = os.path.join(tempfile.gettempdir(), "hadoop_spark")
            bin_dir = os.path.join(hadoop_tmp, "bin")
            os.makedirs(bin_dir, exist_ok=True)
            winutils_path = os.path.join(bin_dir, "winutils.exe")
            if not os.path.isfile(winutils_path):
                open(winutils_path, "wb").close()  # arquivo vazio

            os.environ["HADOOP_HOME"] = hadoop_tmp
            os.environ["hadoop.home.dir"] = hadoop_tmp
            os.environ["PATH"] = bin_dir + ";" + os.environ.get("PATH", "")

            # Suprime warning do NativeCodeLoader
            os.environ.setdefault(
                "HADOOP_OPTS", "-Djava.library.path=" + bin_dir
            )

            # Diretório hive para warehouse
            os.makedirs(os.path.join(tempfile.gettempdir(), "hive"), exist_ok=True)

    elif not hadoop_home:
        # Linux sem HADOOP_HOME — cria mínimo para não dar warning
        hadoop_tmp = os.path.join(tempfile.gettempdir(), "hadoop_spark")
        os.makedirs(os.path.join(hadoop_tmp, "bin"), exist_ok=True)
        os.environ["HADOOP_HOME"] = hadoop_tmp
        os.environ["hadoop.home.dir"] = hadoop_tmp


# Executa ANTES de importar pyspark
_configurar_ambiente()

import nbformat
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import IntegerType, StringType, DoubleType, BooleanType


# ═══════════════════════════════════════════════════════════
#  2. SPARK
# ═══════════════════════════════════════════════════════════

def iniciar_spark() -> SparkSession:
    """Cria SparkSession local, otimizada para testes."""
    spark = (
        SparkSession.builder
        .appName("ValidadorCredito_v2")
        .master("local[*]")
        .config("spark.ui.showConsoleProgress", "false")
        .config("spark.sql.warehouse.dir",
                os.path.join(tempfile.gettempdir(), "spark-warehouse"))
        .config("spark.driver.extraJavaOptions",
                "-Dderby.system.home=" + os.path.join(tempfile.gettempdir(), "derby"))
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark


# ═══════════════════════════════════════════════════════════
#  3. LEITOR DE NOTEBOOK
# ═══════════════════════════════════════════════════════════

def resolver_caminho_notebook(entrada: Optional[str] = None) -> str:
    """
    Resolve o caminho do notebook a partir da entrada do usuário.
    Aceita:
      - Caminho absoluto ou relativo
      - Só o nome do arquivo (busca na pasta notebooks/)
      - None → pega o primeiro .ipynb em notebooks/
    """
    pasta_base = os.path.dirname(os.path.abspath(__file__))
    pasta_notebooks = os.path.join(pasta_base, "notebooks")

    if entrada is None:
        # Sem argumento: pega o primeiro .ipynb na pasta notebooks/
        nbs = glob.glob(os.path.join(pasta_notebooks, "*.ipynb"))
        if not nbs:
            print("[ERRO] Nenhum notebook encontrado em notebooks/")
            sys.exit(1)
        return nbs[0]

    # Caminho direto existe?
    if os.path.isfile(entrada):
        return os.path.abspath(entrada)

    # Tenta como nome dentro de notebooks/
    tentativa = os.path.join(pasta_notebooks, entrada)
    if os.path.isfile(tentativa):
        return os.path.abspath(tentativa)

    # Tenta adicionando .ipynb
    if not entrada.endswith(".ipynb"):
        tentativa2 = tentativa + ".ipynb"
        if os.path.isfile(tentativa2):
            return os.path.abspath(tentativa2)

    print(f"[ERRO] Notebook não encontrado: {entrada}")
    print(f"       Tentei: {entrada}")
    print(f"       Tentei: {tentativa}")
    sys.exit(1)


def ler_regras(caminho_nb: str) -> list[dict]:
    """Lê o notebook e extrai regras (.withColumn)."""
    with open(caminho_nb, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    regras = []
    regex = r"\.withColumn\s*\(\s*[\"'](.*?)[\"']"

    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code" or not cell.source.strip():
            continue

        for match in re.finditer(regex, cell.source):
            # Ignora linhas comentadas
            antes = cell.source[: match.start()]
            ultima_linha = antes.split("\n")[-1]
            if "#" in ultima_linha:
                continue

            regras.append({
                "id": len(regras) + 1,
                "nome": match.group(1),
                "codigo": cell.source,
                "celula": i + 1,
            })

    return regras


# ═══════════════════════════════════════════════════════════
#  4. VALIDAÇÃO
# ═══════════════════════════════════════════════════════════

PREFIXO_RMA = "rma_"
CHAVE_PRIMARIA = "id_cliente"


def validar_regra(spark, regra: dict, df_input, df_rma) -> dict:
    """
    Executa uma regra do notebook e compara com o gabarito.
    Retorna dict com resultado.
    """
    resultado = {
        "id": regra["id"],
        "nome": regra["nome"],
        "celula": regra["celula"],
        "status": "?",
        "erros": 0,
        "mensagem": "",
    }

    ctx = {
        "spark": spark,
        "F": F,
        "df": df_input.alias("df_input"),
        "IntegerType": IntegerType,
        "StringType": StringType,
        "DoubleType": DoubleType,
        "BooleanType": BooleanType,
    }

    try:
        exec(regra["codigo"], {**globals()}, ctx)
        df_resultado = ctx.get("df")

        # Coluna foi criada?
        if regra["nome"] not in df_resultado.columns:
            resultado["status"] = "ERRO"
            resultado["mensagem"] = "Coluna não foi criada após execução."
            return resultado

        # Tem gabarito?
        col_rma = f"{PREFIXO_RMA}{regra['nome']}"
        if col_rma not in df_rma.columns:
            resultado["status"] = "SKIP"
            resultado["mensagem"] = "Sem gabarito no RMA."
            return resultado

        # Compara
        df_cmp = (
            df_resultado
            .select(CHAVE_PRIMARIA, F.col(regra["nome"]).alias("calc"))
            .join(
                df_rma.select(CHAVE_PRIMARIA, F.col(col_rma).alias("rma")),
                on=CHAVE_PRIMARIA,
            )
        )

        divergentes = df_cmp.filter(
            (F.col("calc") != F.col("rma"))
            | (F.col("calc").isNull() & F.col("rma").isNotNull())
            | (F.col("calc").isNotNull() & F.col("rma").isNull())
        )

        total = divergentes.count()
        resultado["erros"] = total

        if total == 0:
            resultado["status"] = "OK"
            resultado["mensagem"] = "Regra correta."
        else:
            resultado["status"] = "FALHA"
            resultado["mensagem"] = f"{total} divergência(s) encontrada(s)."
            resultado["amostra"] = divergentes

    except Exception as e:
        resultado["status"] = "ERRO"
        resultado["mensagem"] = str(e)

    return resultado


# ═══════════════════════════════════════════════════════════
#  5. RELATÓRIO
# ═══════════════════════════════════════════════════════════

def imprimir_relatorio(resultados: list[dict], caminho_nb: str, tempo: float):
    """Imprime relatório final formatado."""
    ok = sum(1 for r in resultados if r["status"] == "OK")
    falha = sum(1 for r in resultados if r["status"] == "FALHA")
    erro = sum(1 for r in resultados if r["status"] == "ERRO")
    skip = sum(1 for r in resultados if r["status"] == "SKIP")
    total = len(resultados)

    icone = {"OK": "✅", "FALHA": "❌", "ERRO": "🔥", "SKIP": "⏭️", "?": "❓"}

    print()
    print("\n     VALIDADOR DE POLÍTICAS DE CRÉDITO     \n")
    print(f"  Notebook: {os.path.basename(caminho_nb)}")
    print(f"  Data:     {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"  Tempo:    {tempo:.1f}s")
    print(f"  Sistema:  {platform.system()}")
    print()
    print("\nRESULTADO POR REGRA                             \n")

    for r in resultados:
        ic = icone.get(r["status"], "?")
        nome = r["nome"][:30]
        print(f"│  {ic} [{r['status']:>5}] {nome:<30} cel.{r['celula']:<3} │")
        if r["status"] == "FALHA":
            print(f"│         → {r['mensagem']:<39}│")
        elif r["status"] == "ERRO":
            msg = r["mensagem"][:39]
            print(f"│         → {msg:<39}│")

    print(f"\n TOTAL: {total}  ok {ok}  erro {falha}   {erro}    {skip:<11}\n")

    # Mostra amostras de divergências
    for r in resultados:
        if r["status"] == "FALHA" and "amostra" in r:
            print(f"\n  Divergências em '{r['nome']}':")
            r["amostra"].show(5, truncate=False)

    
# ═══════════════════════════════════════════════════════════
#  6. MAIN
# ═══════════════════════════════════════════════════════════

def main(caminho_notebook: Optional[str] = None):
    """
    Executa a validação.

    Args:
        caminho_notebook: caminho do .ipynb (local ou na pasta notebooks/).
                          Se None, pega da CLI ou o primeiro da pasta.
    """
    import time

    # Resolve notebook
    if caminho_notebook is None and len(sys.argv) > 1:
        caminho_notebook = sys.argv[1]

    caminho_nb = resolver_caminho_notebook(caminho_notebook)
    print(f"\n  📓 Notebook: {caminho_nb}")

    # Lê regras
    regras = ler_regras(caminho_nb)
    if not regras:
        print("[AVISO] Nenhuma regra (.withColumn) encontrada no notebook.")
        return

    print(f"  Regras encontradas: {len(regras)}")

    # Inicia Spark
    print("  Iniciando Spark...")
    inicio = time.time()
    spark = iniciar_spark()

    # Carrega dados
    pasta_base = os.path.dirname(os.path.abspath(__file__))
    path_input = os.path.join(pasta_base, "dados", "mock_input")
    path_rma = os.path.join(pasta_base, "dados", "mock_rma")

    if not os.path.exists(path_input):
        print(f"[ERRO] Dados de input não encontrados em: {path_input}")
        return
    if not os.path.exists(path_rma):
        print(f"[ERRO] Dados RMA não encontrados em: {path_rma}")
        return

    df_input = spark.read.parquet(path_input)
    df_rma = spark.read.parquet(path_rma)

    # Valida cada regra
    resultados = []
    for regra in regras:
        resultado = validar_regra(spark, regra, df_input, df_rma)
        resultados.append(resultado)

    tempo = time.time() - inicio

    # Relatório
    imprimir_relatorio(resultados, caminho_nb, tempo)


if __name__ == "__main__":
    main()