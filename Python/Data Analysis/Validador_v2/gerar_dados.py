"""
Gerador de dados mock para testes do validador.
Cria os parquets de input e RMA na pasta dados/.

Uso:
  python gerar_dados.py
"""

import os
import sys
import platform
import tempfile
import glob


def _configurar_ambiente():
    """Mesma lógica do validador — garante Windows funcionar."""
    sistema = platform.system().lower()

    if not os.environ.get("JAVA_HOME"):
        if sistema == "windows":
            candidatos = [
                r"C:\Program Files\Java\jdk-17*",
                r"C:\Program Files\Eclipse Adoptium\jdk-17*",
                r"C:\Program Files\Microsoft\jdk-17*",
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

    hadoop_home = os.environ.get("HADOOP_HOME", "")
    if sistema == "windows" and not hadoop_home:
        hadoop_tmp = os.path.join(tempfile.gettempdir(), "hadoop_spark")
        bin_dir = os.path.join(hadoop_tmp, "bin")
        os.makedirs(bin_dir, exist_ok=True)
        winutils_path = os.path.join(bin_dir, "winutils.exe")
        if not os.path.isfile(winutils_path):
            open(winutils_path, "wb").close()
        os.environ["HADOOP_HOME"] = hadoop_tmp
        os.environ["hadoop.home.dir"] = hadoop_tmp
        os.environ["PATH"] = bin_dir + ";" + os.environ.get("PATH", "")
    elif not hadoop_home:
        hadoop_tmp = os.path.join(tempfile.gettempdir(), "hadoop_spark")
        os.makedirs(os.path.join(hadoop_tmp, "bin"), exist_ok=True)
        os.environ["HADOOP_HOME"] = hadoop_tmp
        os.environ["hadoop.home.dir"] = hadoop_tmp


_configurar_ambiente()

from pyspark.sql import SparkSession


def main():
    pasta_base = os.path.dirname(os.path.abspath(__file__))
    pasta_dados = os.path.join(pasta_base, "dados")

    spark = (
        SparkSession.builder
        .appName("GeradorMocks")
        .master("local[*]")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    # ── Input: dados dos clientes ──
    dados_clientes = [
        (1, 1500.0,  600, "SP", 25),
        (2, 5000.0,  850, "RJ", 30),
        (3, 800.0,   350, "MG", 40),
        (4, 16000.0, 900, "BA", 50),
        (5, 3500.0,  750, "SP", 17),
    ]

    df_input = spark.createDataFrame(
        dados_clientes,
        ["id_cliente", "renda", "score", "uf", "idade"],
    )

    path_input = os.path.join(pasta_dados, "mock_input")
    df_input.write.mode("overwrite").parquet(path_input)
    print(f"✅ mock_input criado: {path_input}")

    # ── RMA: gabarito oficial ──
    dados_gabarito = [
        (1, False, False, False, False, False),
        (2, True,  True,  True,  False, False),
        (3, False, False, False, True,  False),
        (4, True,  True,  True,  False, True),
        (5, True,  False, True,  True,  False),
    ]

    colunas_rma = [
        "id_cliente",
        "rma_regra_renda_alta",
        "rma_regra_score_bom",
        "rma_regra_elegivel_premium",
        "rma_regra_bloqueio_risco",
        "rma_regra_aprovacao_auto",
    ]

    df_rma = spark.createDataFrame(dados_gabarito, colunas_rma)

    path_rma = os.path.join(pasta_dados, "mock_rma")
    df_rma.write.mode("overwrite").parquet(path_rma)
    print(f"✅ mock_rma criado: {path_rma}")

    print("\nDados gerados com sucesso!")
    spark.stop()


if __name__ == "__main__":
    main()
