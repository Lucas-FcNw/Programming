"""
CONFIGURAÇÃO CENTRAL — Validador de Políticas de Crédito
=========================================================
Detecta plataforma (Windows/Linux/Databricks), configura Spark
corretamente e define fontes de dados (Notebook, FICO, BD, Databricks).

Uso:
  from config import Config
  cfg = Config()
  spark = cfg.iniciar_spark()
  df = cfg.carregar_dados("input")
"""

from __future__ import annotations

import os
import sys
import platform
import tempfile
import shutil
from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════════
#  Detecção de Ambiente
# ═══════════════════════════════════════════════════════════════

class Ambiente(Enum):
    LINUX_LOCAL = "linux_local"
    WINDOWS_LOCAL = "windows_local"
    DATABRICKS = "databricks"


def detectar_ambiente() -> Ambiente:
    """Detecta o ambiente de execução automaticamente."""
    # Databricks: variável de ambiente ou contexto spark nativo
    if os.environ.get("DATABRICKS_RUNTIME_VERSION") or \
       os.path.exists("/databricks"):
        return Ambiente.DATABRICKS

    sistema = platform.system().lower()
    if sistema == "windows":
        return Ambiente.WINDOWS_LOCAL
    return Ambiente.LINUX_LOCAL


# ═══════════════════════════════════════════════════════════════
#  Fontes de Dados
# ═══════════════════════════════════════════════════════════════

class TipoFonte(Enum):
    PARQUET_LOCAL = "parquet_local"        # Arquivo parquet local
    TABELA_BD = "tabela_bd"                # Tabela via JDBC (Oracle, SQL Server, etc.)
    TABELA_DATABRICKS = "tabela_databricks"  # Tabela Delta no Databricks
    LINK_FICO = "link_fico"                # API/tabela FICO


@dataclass
class FonteDados:
    """Configuração de uma fonte de dados."""
    tipo: TipoFonte
    nome: str                     # Nome descritivo
    # Parquet local
    caminho: str = ""
    # JDBC (BD externo)
    jdbc_url: str = ""
    jdbc_tabela: str = ""
    jdbc_usuario: str = ""
    jdbc_senha: str = ""
    jdbc_driver: str = ""
    # Databricks
    databricks_catalog: str = ""
    databricks_schema: str = ""
    databricks_tabela: str = ""
    # FICO
    fico_endpoint: str = ""
    fico_tabela: str = ""
    fico_token: str = ""
    # Opções extras
    opcoes: Dict[str, str] = field(default_factory=dict)

    def resumo(self) -> str:
        if self.tipo == TipoFonte.PARQUET_LOCAL:
            return f"[{self.nome}] Parquet: {self.caminho}"
        elif self.tipo == TipoFonte.TABELA_BD:
            return f"[{self.nome}] JDBC: {self.jdbc_url} → {self.jdbc_tabela}"
        elif self.tipo == TipoFonte.TABELA_DATABRICKS:
            ref = f"{self.databricks_catalog}.{self.databricks_schema}.{self.databricks_tabela}"
            return f"[{self.nome}] Databricks: {ref}"
        elif self.tipo == TipoFonte.LINK_FICO:
            return f"[{self.nome}] FICO: {self.fico_endpoint} → {self.fico_tabela}"
        return f"[{self.nome}] {self.tipo.value}"


# ═══════════════════════════════════════════════════════════════
#  Configuração Principal
# ═══════════════════════════════════════════════════════════════

class Config:
    """
    Configuração central do validador.
    Detecta ambiente, configura Hadoop/Spark e gerencia fontes de dados.
    """

    def __init__(
        self,
        # ─── Caminhos do Notebook ───
        caminho_notebook: str = "",
        # ─── Fontes de dados ───
        fonte_input: Optional[FonteDados] = None,
        fonte_rma: Optional[FonteDados] = None,
        # ─── Negócio ───
        prefixo_rma: str = "rma_",
        chave_primaria: str = "id_cliente",
        # ─── Spark ───
        app_name: str = "ValidadorCredito",
        spark_config_extra: Optional[Dict[str, str]] = None,
        # ─── Java (para ambientes locais) ───
        java_home: str = "",
    ):
        self.ambiente = detectar_ambiente()
        self.caminho_notebook = caminho_notebook
        self.fonte_input = fonte_input
        self.fonte_rma = fonte_rma
        self.prefixo_rma = prefixo_rma
        self.chave_primaria = chave_primaria
        self.app_name = app_name
        self.spark_config_extra = spark_config_extra or {}
        self.java_home = java_home

        # Configura ambiente antes de qualquer coisa
        self._configurar_ambiente()

    # ─────────────────────────────────────────────────────
    #  Configuração de Ambiente (Hadoop/Java/Windows)
    # ─────────────────────────────────────────────────────

    def _configurar_ambiente(self):
        """Configura variáveis de ambiente conforme plataforma."""
        if self.ambiente == Ambiente.DATABRICKS:
            # No Databricks, Spark já está configurado
            print("[CONFIG] Ambiente Databricks detectado — Spark nativo disponível.")
            return

        # Java
        self._configurar_java()

        # Hadoop (crítico para Windows)
        if self.ambiente == Ambiente.WINDOWS_LOCAL:
            self._configurar_hadoop_windows()
        else:
            self._configurar_hadoop_linux()

    def _configurar_java(self):
        """Configura JAVA_HOME se necessário."""
        if self.java_home:
            os.environ["JAVA_HOME"] = self.java_home
            return

        # Tenta detectar automaticamente
        java_home_env = os.environ.get("JAVA_HOME", "")
        if java_home_env and os.path.isdir(java_home_env):
            return  # Já configurado

        # Caminhos comuns por plataforma
        candidatos = []
        if self.ambiente == Ambiente.WINDOWS_LOCAL:
            candidatos = [
                r"C:\Program Files\Java\jdk-17",
                r"C:\Program Files\Eclipse Adoptium\jdk-17*",
                r"C:\Program Files\Java\jdk-11*",
                r"C:\Program Files\Microsoft\jdk-17*",
            ]
        else:
            candidatos = [
                "/usr/lib/jvm/java-17-temurin-jdk",
                "/usr/lib/jvm/java-17-openjdk-amd64",
                "/usr/lib/jvm/java-11-openjdk-amd64",
            ]

        import glob
        for padrao in candidatos:
            matches = glob.glob(padrao)
            if matches:
                os.environ["JAVA_HOME"] = matches[0]
                print(f"[CONFIG] JAVA_HOME detectado: {matches[0]}")
                return

        print("[AVISO] JAVA_HOME não encontrado. Defina manualmente se houver erro.")

    def _configurar_hadoop_windows(self):
        """
        Configura Hadoop para Windows.
        Resolve: 'Did not find winutils.exe' e 'HADOOP_HOME is unset'.
        """
        hadoop_home = os.environ.get("HADOOP_HOME", "")

        if hadoop_home and os.path.isfile(os.path.join(hadoop_home, "bin", "winutils.exe")):
            print(f"[CONFIG] HADOOP_HOME já configurado: {hadoop_home}")
            return

        # Tenta localizar winutils em caminhos conhecidos
        candidatos_hadoop = [
            os.path.join(os.path.expanduser("~"), "hadoop"),
            os.path.join(os.path.expanduser("~"), "hadoop3"),
            r"C:\hadoop",
            r"C:\hadoop3",
            r"C:\tools\hadoop",
        ]

        for caminho in candidatos_hadoop:
            winutils = os.path.join(caminho, "bin", "winutils.exe")
            if os.path.isfile(winutils):
                os.environ["HADOOP_HOME"] = caminho
                os.environ["PATH"] = os.path.join(caminho, "bin") + ";" + os.environ.get("PATH", "")
                print(f"[CONFIG] HADOOP_HOME encontrado: {caminho}")
                return

        # Se não encontrou, cria um diretório mínimo com winutils dummy
        # Isso permite o Spark rodar sem funcionalidades HDFS
        hadoop_tmp = os.path.join(tempfile.gettempdir(), "hadoop_spark_tmp")
        bin_dir = os.path.join(hadoop_tmp, "bin")
        os.makedirs(bin_dir, exist_ok=True)

        winutils_path = os.path.join(bin_dir, "winutils.exe")
        if not os.path.isfile(winutils_path):
            print("[CONFIG] winutils.exe não encontrado. Criando configuração mínima...")
            print(f"[CONFIG] Diretório temporário: {hadoop_tmp}")
            print("[CONFIG] Para funcionalidade completa, baixe winutils.exe de:")
            print("         https://github.com/cdarlint/winutils")
            print(f"         e coloque em: {bin_dir}")
            # Cria arquivo vazio para evitar FileNotFoundException
            try:
                with open(winutils_path, "wb") as f:
                    f.write(b"")
            except OSError:
                pass

        os.environ["HADOOP_HOME"] = hadoop_tmp
        os.environ["hadoop.home.dir"] = hadoop_tmp
        os.environ["PATH"] = bin_dir + ";" + os.environ.get("PATH", "")

        # Configuração extra para suprimir avisos do NativeCodeLoader
        os.environ["HADOOP_OPTS"] = "-Djava.library.path=" + bin_dir

        # Cria diretório /tmp/hive para warehouse do Spark no Windows
        hive_tmp = os.path.join(tempfile.gettempdir(), "hive")
        os.makedirs(hive_tmp, exist_ok=True)

        print(f"[CONFIG] HADOOP_HOME configurado (mínimo): {hadoop_tmp}")

    def _configurar_hadoop_linux(self):
        """Configuração leve de Hadoop para Linux."""
        hadoop_home = os.environ.get("HADOOP_HOME", "")
        if not hadoop_home:
            # No Linux local, Spark funciona sem Hadoop para uso básico
            # Mas definimos para evitar warnings
            hadoop_tmp = os.path.join(tempfile.gettempdir(), "hadoop_spark_tmp")
            os.makedirs(os.path.join(hadoop_tmp, "bin"), exist_ok=True)
            os.environ["HADOOP_HOME"] = hadoop_tmp
            os.environ["hadoop.home.dir"] = hadoop_tmp

    # ─────────────────────────────────────────────────────
    #  Inicialização do Spark
    # ─────────────────────────────────────────────────────

    def iniciar_spark(self):
        """
        Inicializa SparkSession conforme o ambiente.
        - Databricks: usa spark existente
        - Local (Win/Linux): cria sessão local
        """
        if self.ambiente == Ambiente.DATABRICKS:
            return self._spark_databricks()
        return self._spark_local()

    def _spark_databricks(self):
        """Obtém SparkSession existente no Databricks."""
        try:
            # No Databricks, 'spark' já existe no escopo global
            from pyspark.sql import SparkSession
            spark = SparkSession.builder.getOrCreate()
            print("[SPARK] Sessão Databricks obtida.")
            return spark
        except Exception as e:
            print(f"[ERRO] Falha ao obter Spark no Databricks: {e}")
            raise

    def _spark_local(self):
        """Cria SparkSession local com configurações otimizadas."""
        from pyspark.sql import SparkSession

        builder = SparkSession.builder \
            .appName(self.app_name) \
            .master("local[*]")

        # Configurações para suprimir warnings e melhorar compatibilidade
        configs_padrao = {
            "spark.sql.warehouse.dir": os.path.join(tempfile.gettempdir(), "spark-warehouse"),
            "spark.driver.extraJavaOptions": "-Dderby.system.home=" + os.path.join(tempfile.gettempdir(), "derby"),
            "spark.ui.showConsoleProgress": "false",
        }

        # No Windows, configurações adicionais
        if self.ambiente == Ambiente.WINDOWS_LOCAL:
            configs_padrao.update({
                "spark.sql.shuffle.partitions": "2",
                "spark.default.parallelism": "2",
                "spark.driver.memory": "1g",
            })

        # Aplica configs padrão + extras do usuário
        configs_padrao.update(self.spark_config_extra)
        for chave, valor in configs_padrao.items():
            builder = builder.config(chave, valor)

        spark = builder.getOrCreate()
        spark.sparkContext.setLogLevel("ERROR")
        print(f"[SPARK] Sessão local criada ({self.ambiente.value}).")
        return spark

    # ─────────────────────────────────────────────────────
    #  Carregamento de Dados
    # ─────────────────────────────────────────────────────

    def carregar_dados(self, spark, fonte: FonteDados):
        """
        Carrega DataFrame de qualquer fonte configurada.

        Args:
            spark: SparkSession ativa
            fonte: Configuração da fonte de dados

        Returns:
            DataFrame do Spark
        """
        if fonte.tipo == TipoFonte.PARQUET_LOCAL:
            return self._carregar_parquet(spark, fonte)
        elif fonte.tipo == TipoFonte.TABELA_BD:
            return self._carregar_jdbc(spark, fonte)
        elif fonte.tipo == TipoFonte.TABELA_DATABRICKS:
            return self._carregar_databricks(spark, fonte)
        elif fonte.tipo == TipoFonte.LINK_FICO:
            return self._carregar_fico(spark, fonte)
        else:
            raise ValueError(f"Tipo de fonte desconhecido: {fonte.tipo}")

    def _carregar_parquet(self, spark, fonte: FonteDados):
        """Carrega dados de arquivo Parquet local."""
        caminho = fonte.caminho
        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Parquet não encontrado: {caminho}")
        print(f"[DADOS] Carregando Parquet: {caminho}")
        return spark.read.parquet(caminho)

    def _carregar_jdbc(self, spark, fonte: FonteDados):
        """
        Carrega dados via JDBC (Oracle, SQL Server, PostgreSQL, etc.).
        Exemplo de uso:
            fonte = FonteDados(
                tipo=TipoFonte.TABELA_BD,
                nome="Base Produção",
                jdbc_url="jdbc:oracle:thin:@host:1521:ORCL",
                jdbc_tabela="SCHEMA.TABELA_CLIENTES",
                jdbc_usuario="user",
                jdbc_senha="pass",
                jdbc_driver="oracle.jdbc.driver.OracleDriver"
            )
        """
        print(f"[DADOS] Conectando via JDBC: {fonte.jdbc_url} → {fonte.jdbc_tabela}")

        reader = spark.read.format("jdbc") \
            .option("url", fonte.jdbc_url) \
            .option("dbtable", fonte.jdbc_tabela) \
            .option("user", fonte.jdbc_usuario) \
            .option("password", fonte.jdbc_senha)

        if fonte.jdbc_driver:
            reader = reader.option("driver", fonte.jdbc_driver)

        # Opções extras (fetchsize, partitionColumn, etc.)
        for chave, valor in fonte.opcoes.items():
            reader = reader.option(chave, valor)

        return reader.load()

    def _carregar_databricks(self, spark, fonte: FonteDados):
        """
        Carrega tabela do Databricks (Unity Catalog ou Hive).
        Exemplo de uso:
            fonte = FonteDados(
                tipo=TipoFonte.TABELA_DATABRICKS,
                nome="Tabela Clientes",
                databricks_catalog="catalogo_prod",
                databricks_schema="credito",
                databricks_tabela="clientes_score"
            )
        """
        if fonte.databricks_catalog:
            ref = f"{fonte.databricks_catalog}.{fonte.databricks_schema}.{fonte.databricks_tabela}"
        elif fonte.databricks_schema:
            ref = f"{fonte.databricks_schema}.{fonte.databricks_tabela}"
        else:
            ref = fonte.databricks_tabela

        print(f"[DADOS] Carregando tabela Databricks: {ref}")
        return spark.table(ref)

    def _carregar_fico(self, spark, fonte: FonteDados):
        """
        Carrega dados do FICO (Decision Management / Blaze Advisor).
        O FICO pode expor dados via:
          1. Tabela JDBC (usa mesma lógica de BD)
          2. API REST (baixa JSON e converte para DataFrame)
          3. Arquivo exportado (CSV/Parquet)

        Exemplo de uso:
            fonte = FonteDados(
                tipo=TipoFonte.LINK_FICO,
                nome="FICO Scores",
                fico_endpoint="https://fico-server.empresa.com/api/v1",
                fico_tabela="decision_scores",
                fico_token="Bearer xxx..."
            )
        """
        print(f"[DADOS] Conectando ao FICO: {fonte.fico_endpoint} → {fonte.fico_tabela}")

        # Estratégia 1: FICO expõe via JDBC
        if fonte.jdbc_url:
            print("[DADOS] FICO via JDBC...")
            return self._carregar_jdbc(spark, fonte)

        # Estratégia 2: FICO expõe via API REST
        if fonte.fico_endpoint:
            import requests
            url = f"{fonte.fico_endpoint}/{fonte.fico_tabela}"
            headers = {}
            if fonte.fico_token:
                headers["Authorization"] = fonte.fico_token

            print(f"[DADOS] Requisitando FICO REST: {url}")

            try:
                resp = requests.get(url, headers=headers, timeout=60)
                resp.raise_for_status()
                dados = resp.json()

                # Converte JSON para DataFrame
                if isinstance(dados, list):
                    return spark.createDataFrame(dados)
                elif isinstance(dados, dict) and "data" in dados:
                    return spark.createDataFrame(dados["data"])
                else:
                    raise ValueError("Formato de resposta FICO não reconhecido. "
                                     "Esperado: lista de objetos ou {data: [...]}.")
            except requests.RequestException as e:
                raise ConnectionError(f"Falha ao conectar ao FICO: {e}")

        raise ValueError("FonteDados FICO requer fico_endpoint ou jdbc_url configurado.")

    # ─────────────────────────────────────────────────────
    #  Resumo
    # ─────────────────────────────────────────────────────

    def resumo(self) -> str:
        """Exibe resumo da configuração atual."""
        linhas = [
            "┌─────────────────────────────────────────────┐",
            "│         CONFIGURAÇÃO DO VALIDADOR            │",
            "├─────────────────────────────────────────────┤",
            f"│  Ambiente:       {self.ambiente.value:<27}│",
            f"│  Plataforma:     {platform.system():<27}│",
            f"│  JAVA_HOME:      {os.environ.get('JAVA_HOME', 'N/A')[:27]:<27}│",
            f"│  HADOOP_HOME:    {os.environ.get('HADOOP_HOME', 'N/A')[:27]:<27}│",
            f"│  Notebook:       {os.path.basename(self.caminho_notebook) if self.caminho_notebook else 'N/A':<27}│",
        ]

        if self.fonte_input:
            linhas.append(f"│  Fonte Input:    {self.fonte_input.tipo.value[:27]:<27}│")
        if self.fonte_rma:
            linhas.append(f"│  Fonte RMA:      {self.fonte_rma.tipo.value[:27]:<27}│")

        linhas.append("└─────────────────────────────────────────────┘")
        return "\n".join(linhas)


# ═══════════════════════════════════════════════════════════════
#  Fábricas de configuração pré-definidas (atalhos)
# ═══════════════════════════════════════════════════════════════

def config_local_parquet(
    caminho_notebook: str,
    caminho_input: str,
    caminho_rma: str,
    **kwargs,
) -> Config:
    """Configuração rápida para execução local com Parquet."""
    return Config(
        caminho_notebook=caminho_notebook,
        fonte_input=FonteDados(
            tipo=TipoFonte.PARQUET_LOCAL,
            nome="Input Local",
            caminho=caminho_input,
        ),
        fonte_rma=FonteDados(
            tipo=TipoFonte.PARQUET_LOCAL,
            nome="RMA Local",
            caminho=caminho_rma,
        ),
        **kwargs,
    )


def config_databricks(
    caminho_notebook: str,
    catalog: str,
    schema: str,
    tabela_input: str,
    tabela_rma: str,
    **kwargs,
) -> Config:
    """Configuração rápida para Databricks."""
    return Config(
        caminho_notebook=caminho_notebook,
        fonte_input=FonteDados(
            tipo=TipoFonte.TABELA_DATABRICKS,
            nome="Input Databricks",
            databricks_catalog=catalog,
            databricks_schema=schema,
            databricks_tabela=tabela_input,
        ),
        fonte_rma=FonteDados(
            tipo=TipoFonte.TABELA_DATABRICKS,
            nome="RMA Databricks",
            databricks_catalog=catalog,
            databricks_schema=schema,
            databricks_tabela=tabela_rma,
        ),
        **kwargs,
    )


def config_jdbc(
    caminho_notebook: str,
    jdbc_url: str,
    tabela_input: str,
    tabela_rma: str,
    usuario: str,
    senha: str,
    driver: str = "",
    **kwargs,
) -> Config:
    """Configuração rápida para BD via JDBC."""
    return Config(
        caminho_notebook=caminho_notebook,
        fonte_input=FonteDados(
            tipo=TipoFonte.TABELA_BD,
            nome="Input BD",
            jdbc_url=jdbc_url,
            jdbc_tabela=tabela_input,
            jdbc_usuario=usuario,
            jdbc_senha=senha,
            jdbc_driver=driver,
        ),
        fonte_rma=FonteDados(
            tipo=TipoFonte.TABELA_BD,
            nome="RMA BD",
            jdbc_url=jdbc_url,
            jdbc_tabela=tabela_rma,
            jdbc_usuario=usuario,
            jdbc_senha=senha,
            jdbc_driver=driver,
        ),
        **kwargs,
    )


def config_fico(
    caminho_notebook: str,
    fico_endpoint: str,
    tabela_input: str,
    tabela_rma: str,
    fico_token: str = "",
    **kwargs,
) -> Config:
    """Configuração rápida para FICO."""
    return Config(
        caminho_notebook=caminho_notebook,
        fonte_input=FonteDados(
            tipo=TipoFonte.LINK_FICO,
            nome="Input FICO",
            fico_endpoint=fico_endpoint,
            fico_tabela=tabela_input,
            fico_token=fico_token,
        ),
        fonte_rma=FonteDados(
            tipo=TipoFonte.LINK_FICO,
            nome="RMA FICO",
            fico_endpoint=fico_endpoint,
            fico_tabela=tabela_rma,
            fico_token=fico_token,
        ),
        **kwargs,
    )
