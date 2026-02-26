# Validador de Políticas de Crédito — v2

Versão simplificada: a entrada é apenas o **caminho de um notebook Jupyter**.

## Estrutura

```
Validador_v2/
├── validador.py          ← script principal (roda tudo)
├── gerar_dados.py        ← (re)gera dados mock de teste
├── requirements.txt
├── notebooks/
│   └── regras_credito.ipynb   ← coloque seus notebooks aqui
└── dados/
    ├── mock_input/        ← parquet com dados dos clientes
    └── mock_rma/          ← parquet com gabarito (RMA)
```

## Como usar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Rodar o validador

```bash
# Usa o primeiro notebook da pasta notebooks/
python validador.py

# Passa o caminho do notebook
python validador.py notebooks/regras_credito.ipynb

# Passa um caminho absoluto
python validador.py /caminho/para/notebook.ipynb

# Windows — funciona igual
python validador.py C:\Users\user\regras.ipynb
```

### 3. Regenerar dados de teste (opcional)
```bash
python gerar_dados.py
```

## Compatibilidade Windows

O validador configura automaticamente `HADOOP_HOME` e `winutils.exe`
para que o PySpark funcione em Windows corporativo sem instalação do Hadoop.
Nenhuma ação manual é necessária.

## Como funciona

1. Lê o notebook e encontra todas as chamadas `.withColumn("nome_regra", ...)`
2. Executa cada célula com os dados de input
3. Compara a coluna gerada com a coluna `rma_nome_regra` do gabarito
4. Imprime relatório com sucessos, falhas e divergências
