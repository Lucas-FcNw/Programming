import os
from pyspark.sql import SparkSession

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-temurin-jdk"


# Inicia o Spark rapidinho só para salvar os arquivos
spark = SparkSession.builder.master("local[*]").getOrCreate()

# Garante que a pasta dados existe
if not os.path.exists("./dados"):
    os.makedirs("./dados")

# ==============================================================================
# 1. CRIANDO O ARQUIVO MOCK_INPUT (Dados dos Clientes)
# ==============================================================================
# Colunas: ID, Renda, Score, UF, Idade
dados_clientes = [
    (1, 1500.0,  600, "SP", 25), # Caso Básico (Tudo False)
    (2, 5000.0,  850, "RJ", 30), # Caso Premium (Renda>3k e Score>700)
    (3, 800.0,   350, "MG", 40), # Caso Risco Score (<400)
    (4, 16000.0, 900, "BA", 50), # Caso Aprov. Auto (Renda > 15k)
    (5, 3500.0,  750, "SP", 17)  # Caso Risco Idade (<18)
]

df_input = spark.createDataFrame(dados_clientes, ["id_cliente", "renda", "score", "uf", "idade"])
df_input.write.mode("overwrite").parquet("./dados/mock_input")
print("✅ Arquivo 'mock_input' criado com sucesso!")

# ==============================================================================
# 2. CRIANDO O ARQUIVO MOCK_RMA (O Gabarito Oficial)
# ==============================================================================
# Aqui definimos manualmente qual DEVERIA ser a resposta correta para cada cliente
# Baseado nas regras: 
# 1(Renda>2k), 2(Score>800), 3(Renda>3k E Score>700), 4(Idade<18 OU Score<400), 5(Auto)

dados_gabarito = [
    # ID | R1    | R2    | R3 (E)| R4 (OU)| R5 (Mista)
    (1,   False,  False,  False,  False,   False),
    (2,   True,   True,   True,   False,   False),
    (3,   False,  False,  False,  True,    False), # Score baixo ativa R4
    (4,   True,   True,   True,   False,   True),  # Renda alta ativa R5
    (5,   True,   False,  True,   True,    False)  # Idade baixa ativa R4
]

colunas_rma = [
    "id_cliente", 
    "rma_regra_renda_alta", 
    "rma_regra_score_bom", 
    "rma_regra_elegivel_premium", 
    "rma_regra_bloqueio_risco", 
    "rma_regra_aprovacao_auto"
]

df_rma = spark.createDataFrame(dados_gabarito, colunas_rma)
df_rma.write.mode("overwrite").parquet("./dados/mock_rma")
print("✅ Arquivo 'mock_rma' criado com sucesso!")