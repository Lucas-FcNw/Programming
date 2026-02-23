import os
import re
import nbformat
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *

# --- CONFIGURAÇÃO DO JAVA ---
#No bricks tirar a especificação do JAVA_HOME
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-temurin-jdk"

# --- CAMINHOS ---
PATH_NOTEBOOK = "./notebooks/regras_credito.ipynb"
PATH_DADOS_INPUT = "./dados/mock_input"
PATH_DADOS_RMA = "./dados/mock_rma"

# Configurações de Negócio
PREFIXO_RMA = "rma_" 
CHAVE_PRIMARIA = "id_cliente"

#NO BRICKS spark = ... e comenta/tira a linha .master("local[*]") para rodar no cluster

def iniciar_spark():
    spark = SparkSession.builder \
        .appName("ValidadorCredito") \
        .master("local[*]") \
        .getOrCreate()
    # Reduz o ruído do Spark no terminal
    spark.sparkContext.setLogLevel("ERROR")
    return spark

def varrer_notebook(caminho_nb):
    """Lê o notebook e extrai as regras."""
    if not os.path.exists(caminho_nb):
        print(f"[ERRO] Notebook não encontrado em {caminho_nb}")
        return []

    with open(caminho_nb, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    politicas = []
    # Regex flexível para capturar o nome da regra
    regex_regra = r'\.withColumn\s*\(\s*["\'](.*?)["\']'
    
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            codigo = cell.source
            
            # Se a célula estiver vazia, pula
            if not codigo.strip():
                continue

            matches = re.finditer(regex_regra, codigo)
            for match in matches:
                # Verifica se a linha específica do comando está comentada
                texto_antes = codigo[:match.start()]
                linha_atual = texto_antes.split('\n')[-1]
                
                # Se tiver # na linha antes do comando, ignora
                if "#" in linha_atual:
                    continue

                politicas.append({
                    "id": len(politicas) + 1,
                    "nome": match.group(1),
                    "codigo": codigo,
                    "celula": i + 1
                })
    return politicas

def executar_validacao(spark, politica, df_input, df_rma):
    print(f"[TESTE] Validando Regra: {politica['nome']} ... ", end="")
    
    # Prepara contexto
    df_local = df_input.alias("df_input")
    ctx = {
        "spark": spark, "F": F, "df": df_local, 
        "IntegerType": IntegerType, "StringType": StringType, "DoubleType": DoubleType, "BooleanType": BooleanType
    }
    
    try:
        # Executa a lógica do notebook
        exec(politica['codigo'], globals(), ctx)
        df_resultado = ctx.get('df')
        
        # Verifica se a coluna foi criada
        if politica['nome'] not in df_resultado.columns:
            print(f"[ERRO] Coluna não criada após execução.")
            return

        # Monta nomes para comparação
        col_calc = politica['nome']
        col_rma = f"{PREFIXO_RMA}{col_calc}"
        
        if col_rma not in df_rma.columns:
            print(f"[PULAR] Sem gabarito no RMA para esta coluna.")
            return

        # Comparação
        df_compare = df_resultado.select(CHAVE_PRIMARIA, F.col(col_calc).alias("vlr_calc")) \
            .join(df_rma.select(CHAVE_PRIMARIA, F.col(col_rma).alias("vlr_rma")), on=CHAVE_PRIMARIA)
        
        # Lógica de Divergência
        df_divergente = df_compare.filter(
            (F.col("vlr_calc") != F.col("vlr_rma")) |
            (F.col("vlr_calc").isNull() & F.col("vlr_rma").isNotNull()) |
            (F.col("vlr_calc").isNotNull() & F.col("vlr_rma").isNull())
        )
        
        total_erros = df_divergente.count()
        
        if total_erros == 0:
            print(f"[SUCESSO] OK")
        else:
            print(f"[FALHA] DIVERGÊNCIA ENCONTRADA")
            print(f"   -> Encontrados {total_erros} erros. Amostra:")
            df_divergente.show(5)

    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha na execução do código: {e}")

def main():
    print("\n--- VALIDADOR DE POLÍTICAS DE CRÉDITO ---\n")
    spark = iniciar_spark()
    
    # 1. Carregar Dados
    if not os.path.exists(PATH_DADOS_INPUT):
        print("[ERRO] Dados não encontrados.")
        return

#Aqui no caso real após o = viria as tabelas do BD
    try:
        df_input = spark.read.parquet(PATH_DADOS_INPUT)
        df_rma = spark.read.parquet(PATH_DADOS_RMA)
    except Exception as e:
        print(f"[ERRO] Falha ao ler dados: {e}")
        return

    # 2. Ler Regras
    politicas = varrer_notebook(PATH_NOTEBOOK)
    
    if not politicas:
        print("[AVISO] Nenhuma regra encontrada (Verifique se o notebook está salvo).")
        return

    print(f"[INFO] Testando {len(politicas)} políticas...\n")

    # 3. Executar
    for p in politicas:
        executar_validacao(spark, p, df_input, df_rma)
    
    print("\n--- FIM DA VALIDAÇÃO ---")

if __name__ == "__main__":
    main()