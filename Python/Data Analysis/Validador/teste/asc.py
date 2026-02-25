import os
import json
import re
import nbformat
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *

# --- 1. GERADOR DE MOCKS (Cria dados e notebook falsos) ---

def criar_dados_mock(spark):
    print("🛠️  Criando Dados Mock (Simulando o FinalRMA)...")
    # Simula uma tabela que já tem o Input (Renda) e o Gabarito (RMA_...)
    dados = [
        # id, renda, idade,  RMA_regra_1 (Correta), RMA_regra_2 (Para falhar)
        (1,   5000,  30,     1500.0,                "Aprovado"),
        (2,   10000, 40,     3000.0,                "Reprovado"), # Erro proposital no gabarito p/ testar
        (3,   2000,  20,     600.0,                 "Aprovado")
    ]
    schema = ["id_contrato", "renda", "idade", "RMA_calculo_30_porcento", "RMA_status_aprovacao"]
    
    df = spark.createDataFrame(dados, schema)
    return df

def criar_notebook_temporario():
    print("📝 Criando Notebook Temporário com Regras...")
    
    # Conteúdo do notebook (Mantive igual)
    notebook_content = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Regra 1: Capacidade de Pagamento\n",
                    "df = df.withColumn('calculo_30_porcento', F.col('renda') * 0.30)"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 2,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Regra 2: Status Aprovação (Erro proposital no dado 2)\n",
                    "df = df.withColumn('status_aprovacao', F.when(F.col('renda') > 3000, 'Aprovado').otherwise('Reprovado'))"
                ]
            }
        ],
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    # --- CORREÇÃO AQUI ---
    # Antes estava: path = "/dbfs/tmp/teste_regras.ipynb"
    # Agora salva na pasta atual do seu Linux:
    path = "./teste_regras_temporario.ipynb"
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(notebook_content, f)
    
    return path

# --- 2. O MOTOR DO VALIDADOR (Sua Lógica Real) ---

def varrer_notebook(caminho_nb):
    with open(caminho_nb, 'r') as f:
        nb = nbformat.read(f, as_version=4)
    
    politicas = []
    regex_regra = r'\.withColumn\s*\(\s*["\'](.*?)["\']'
    
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            codigo = "".join(cell.source)
            matches = re.finditer(regex_regra, codigo)
            for match in matches:
                politicas.append({
                    "id": len(politicas) + 1,
                    "nome_spark": match.group(1),
                    "codigo": codigo
                })
    return politicas

def validar(spark, politica, df_mock):
    print(f"\n🔍 Testando Regra: {politica['nome_spark']}")
    
    # Contexto isolado
    ctx = {"spark": spark, "F": F, "df": df_mock}
    
    try:
        # 1. Executa a regra (Cria a coluna nova)
        exec(politica['codigo'], globals(), ctx)
        df_resultado = ctx['df']
        
        # 2. Procura coluna correspondente no Mock (Gabarito)
        # Lógica: Procura coluna que termine com o nome da regra
        col_gabarito = None
        for col in df_mock.columns:
            if col.endswith(politica['nome_spark']) and col != politica['nome_spark']:
                col_gabarito = col
                break
        
        if not col_gabarito:
            print("⚠️  SKIP: Gabarito não encontrado.")
            return

        # 3. Compara
        print(f"   Comparando: Calculado['{politica['nome_spark']}'] vs Gabarito['{col_gabarito}']")
        
        divergencias = df_resultado.filter(
            F.col(politica['nome_spark']) != F.col(col_gabarito)
        )
        total_erros = divergencias.count()
        
        if total_erros == 0:
            print("   ✅ SUCESSO! A lógica bateu 100%.")
        else:
            print(f"   ❌ FALHA! Encontradas {total_erros} diferenças.")
            divergencias.select("id_contrato", politica['nome_spark'], col_gabarito).show()
            
    except Exception as e:
        print(f"   🔥 Erro de execução: {e}")

# --- 3. EXECUÇÃO PRINCIPAL ---

def main():
    spark = SparkSession.builder.getOrCreate()
    
    # 1. Cria o ambiente de teste
    df_mock = criar_dados_mock(spark)
    path_nb = criar_notebook_temporario()
    
    try:
        # 2. Roda o Validador
        regras = varrer_notebook(path_nb)
        print(f"📋 Regras encontradas no notebook falso: {len(regras)}")
        
        for p in regras:
            validar(spark, p, df_mock)
            
    finally:
        # 3. Limpeza (Apaga o notebook temporário)
        if os.path.exists(path_nb):
            os.remove(path_nb)
            print("\n🧹 Limpeza: Notebook temporário removido.")

if __name__ == "__main__":
    main()