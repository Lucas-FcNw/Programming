# Manual Completo de Análise de Dados com Python, Pandas, Matplotlib e Seaborn

Este manual é prático e direto: cada seção explica o conceito, mostra o padrão de uso e oferece exemplos prontos para copiar e adaptar.

Sumário rápido:
- Instalação e ambiente
- Pandas (importação, limpeza, transformação, agregação, junções, datas)
- Visualização (Matplotlib e Seaborn)
- Receitas “Como fazer…”
- Boas práticas e desempenho
- Dúvidas comuns e erros

---

## 0) Instalação e Ambiente

Escolha uma das opções.

### Opção A: `venv` + `pip`
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r "Python/Data Analysis/requirements.txt"
```

### Opção B: Conda (opcional)
```bash
conda create -n dados python=3.11 -y
conda activate dados
pip install -r "Python/Data Analysis/requirements.txt"
```

### Jupyter (opcional mas recomendado)
```bash
python -m ipykernel install --user --name dados --display-name "Python (dados)"
jupyter lab
```

---

## 1) Conceitos Fundamentais

- DataFrame: tabela com rótulos de linhas (index) e colunas.
- Série: coluna unidimensional com rótulo de índice.
- Operações vetorizadas: operações aplicadas a colunas inteiras, rápidas e idiomáticas.
- Matplotlib: biblioteca base para gráficos.
- Seaborn: camada de alto nível com gráficos estatísticos prontos.

---

## 2) Pandas Essencial

### 2.1 Criar e inspecionar
```python
import pandas as pd

# DataFrame a partir de dict
df = pd.DataFrame({
    'nome': ['Ana', 'Bruno', 'Carla', 'Daniel'],
    'idade': [23, 31, 29, 40],
    'cidade': ['SP', 'RJ', 'SP', 'BH'],
    'salario': [5000, 7200, 6100, 9800],
})

print(df.head())       # primeiras linhas
print(df.info())       # tipos, nulos
print(df.describe())   # estatísticas numéricas
print(df.dtypes)       # tipos por coluna
```

### 2.2 Importar e exportar dados
```python
# CSV
df = pd.read_csv('dados.csv', sep=',', decimal='.', encoding='utf-8')
df.to_csv('saida.csv', index=False)

# Excel
df_x = pd.read_excel('planilha.xlsx', sheet_name='Aba1')
df_x.to_excel('saida.xlsx', index=False)

# JSON
df_j = pd.read_json('dados.json', lines=False)
df_j.to_json('saida.json', orient='records', force_ascii=False)
```

### 2.3 Seleção, filtro e ordenação
```python
# Seleção de colunas
idade = df['idade']
subset = df[['nome', 'salario']]

# Filtro (linhas)
sp = df[df['cidade'] == 'SP']
ricos = df[df['salario'] > 7000]

# loc (por rótulo) / iloc (por posição)
linha_rotulo = df.loc[0]
linha_posicao = df.iloc[0]

# Ordenar
por_salario = df.sort_values('salario', ascending=False)
por_cidade_idade = df.sort_values(['cidade', 'idade'])
```

### 2.4 Criar/transformar colunas
```python
# Colunas derivadas
df['salario_k'] = df['salario'] / 1000
df['faixa'] = pd.cut(df['salario'], bins=[0,6000,9000, float('inf')], labels=['baixa','media','alta'])

# Operações com string
df['nome_maiusculo'] = df['nome'].str.upper()
df['iniciais'] = df['nome'].str[0]

# map/apply
mapa = {'SP':'Sao Paulo','RJ':'Rio','BH':'Belo Horizonte'}
df['cidade_nome'] = df['cidade'].map(mapa)
df['bonus'] = df['salario'].apply(lambda s: s*0.10 if s>7000 else s*0.05)
```

### 2.5 Missing values
```python
# Detectar e tratar nulos
df.isna().sum()
df['idade'] = df['idade'].fillna(df['idade'].median())
df = df.dropna(subset=['salario'])  # remove linhas sem salário
```

### 2.6 Agregações e groupby
```python
# Estatística por grupo
por_cidade = df.groupby('cidade').agg(
    qtd=('nome','count'),
    media_sal=('salario','mean'),
    mediana_idade=('idade','median'),
)

# Agregações múltiplas na mesma coluna
agg_multi = df.groupby('cidade')['salario'].agg(['mean','median','min','max'])
```

### 2.7 Tabelas dinâmicas (pivot)
```python
pivot = pd.pivot_table(
    df,
    values='salario',
    index='cidade',
    columns='faixa',
    aggfunc='mean',
    fill_value=0,
)
```

### 2.8 Junções (merge)
```python
clientes = pd.DataFrame({'id':[1,2,3], 'nome':['Ana','Bruno','Carla']})
compras  = pd.DataFrame({'id_cliente':[1,2,2,4], 'valor':[100, 200, 50, 80]})

# left join: mantém todos os clientes
joined = clientes.merge(compras, left_on='id', right_on='id_cliente', how='left')
```

### 2.9 Datas e séries temporais
```python
# Converter para datetime
df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')

# Extrações comuns
df['ano'] = df['data'].dt.year
df['mes'] = df['data'].dt.month
df['dia_sem'] = df['data'].dt.day_name(locale='pt_BR')

# Reamostragem (resample) após definir índice temporal
ts = df.set_index('data').sort_index()
mensal = ts['salario'].resample('M').sum()
movel = ts['salario'].rolling(window=3, min_periods=1).mean()
```

---

## 3) Visualização com Matplotlib

### 3.1 Primeiros passos
```python
import matplotlib.pyplot as plt

x = [1,2,3,4]
y = [10,20,15,30]

plt.figure(figsize=(6,4))
plt.plot(x, y, marker='o', linewidth=2, color='tab:blue')
plt.title('Exemplo de Linha')
plt.xlabel('Eixo X')
plt.ylabel('Eixo Y')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### 3.2 Tipos comuns
```python
# Barras
plt.bar(['A','B','C'], [3,7,5], color='tab:green')

# Histograma
plt.hist(df['salario'], bins=20, color='tab:purple', alpha=0.7)

# Dispersão
plt.scatter(df['idade'], df['salario'], alpha=0.6)

# Boxplot
plt.boxplot([df['salario']], labels=['salario'])
```

### 3.3 Subplots e personalização
```python
fig, ax = plt.subplots(1,2, figsize=(10,4))
ax[0].plot(x,y, marker='o')
ax[0].set_title('Linha')
ax[1].hist(y, bins=4)
ax[1].set_title('Histograma')
fig.suptitle('Dois Gráficos')
fig.tight_layout()
plt.show()
```

---

## 4) Visualização com Seaborn

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')

tips = sns.load_dataset('tips')  # dataset exemplo
```

### 4.1 Gráficos relacionais e categóricos
```python
# Relacionais
sns.relplot(data=tips, x='total_bill', y='tip', hue='time', kind='scatter')

# Categóricos
sns.catplot(data=tips, x='day', y='total_bill', kind='box')
sns.catplot(data=tips, x='day', y='total_bill', kind='violin', hue='sex', split=True)
sns.catplot(data=tips, x='day', y='total_bill', kind='bar', ci='sd')
```

### 4.2 Distribuições e regressão
```python
sns.displot(data=tips, x='total_bill', kde=True)
sns.jointplot(data=tips, x='total_bill', y='tip', kind='hex')
sns.lmplot(data=tips, x='total_bill', y='tip', hue='sex', height=4)
```

### 4.3 Matriz, correlação e mapas de calor
```python
corr = tips.corr(numeric_only=True)
plt.figure(figsize=(6,4))
sns.heatmap(corr, annot=True, cmap='vlag', center=0)
plt.show()
```

### 4.4 Facetas (pequenos múltiplos)
```python
g = sns.FacetGrid(tips, col='time', row='sex', margin_titles=True)
g.map_dataframe(sns.scatterplot, x='total_bill', y='tip', hue='smoker')
g.add_legend()
plt.show()
```

---

## 5) Receitas “Como Fazer…”

### 5.1 Importar CSV grande com tipos corretos e datas
```python
import pandas as pd

dtypes = {
  'id': 'int64',
  'cidade': 'category',
  'produto': 'category',
  'preco': 'float64',
}
parse_dates = ['data_venda']

df = pd.read_csv('vendas.csv', dtype=dtypes, parse_dates=parse_dates)
```

### 5.2 Remover outliers simples (IQR)
```python
q1 = df['preco'].quantile(0.25)
q3 = df['preco'].quantile(0.75)
iqr = q3 - q1
mask = (df['preco'] >= q1 - 1.5*iqr) & (df['preco'] <= q3 + 1.5*iqr)
df_sem_outlier = df[mask]
```

### 5.3 Top N por grupo
```python
top2 = (df
  .sort_values(['cidade','preco'], ascending=[True, False])
  .groupby('cidade')
  .head(2)
)
```

### 5.4 Percentual por categoria
```python
cont = df['cidade'].value_counts()
perc = (cont / cont.sum() * 100).round(2)
resultado = pd.DataFrame({'qtd': cont, 'perc_%': perc})
```

### 5.5 Unir DataFrames com chaves diferentes
```python
# df1: chave A, df2: chave B
res = df1.merge(df2, left_on='A', right_on='B', how='inner')
```

### 5.6 Converter, ordenar e plotar série temporal mensal
```python
df['data'] = pd.to_datetime(df['data'], dayfirst=True)
ts = df.set_index('data').sort_index()
mensal = ts['valor'].resample('M').sum()
mensal.plot(title='Soma Mensal')
plt.show()
```

### 5.7 Heatmap de tabela dinâmica
```python
pv = pd.pivot_table(df, index='categoria', columns='mes', values='valor', aggfunc='sum', fill_value=0)
plt.figure(figsize=(8,4))
sns.heatmap(pv, cmap='YlGnBu')
plt.show()
```

### 5.8 Pairplot para explorar relações
```python
num_cols = ['idade','salario','gastos']
sns.pairplot(df[num_cols], corner=True, diag_kind='kde')
plt.show()
```

### 5.9 Adicionar linhas de referência (targets)
```python
ax = sns.boxplot(data=df, x='cidade', y='salario')
ax.axhline(7000, color='red', linestyle='--', label='Meta')
ax.legend()
plt.show()
```

### 5.10 Salvar figuras com alta resolução
```python
fig, ax = plt.subplots(figsize=(6,4))
sns.scatterplot(data=df, x='idade', y='salario', ax=ax)
fig.tight_layout()
fig.savefig('figuras/dispersao.png', dpi=300)
```

---

## 6) Boas Práticas e Desempenho

- Tipos eficientes: use `category` para colunas com poucos valores distintos.
- Evite `apply` linha a linha; prefira operações vetorizadas.
- Use filtragem e atribuição com `.loc[mask, 'col'] = ...`.
- Para CSVs grandes, especifique `dtype`, `usecols`, `chunksize`.
- Limpeza incremental: primeiro padronize colunas, depois trate nulos, depois derive colunas.
- Documente decisões (por que removeu outliers, definiu regras de negócio, etc.).

Exemplo `chunksize`:
```python
reader = pd.read_csv('grande.csv', chunksize=100_000)
acum = []
for chunk in reader:
    chunk['total'] = chunk['qtd'] * chunk['preco']
    acum.append(chunk.groupby('categoria')['total'].sum())

res = pd.concat(acum).groupby(level=0).sum().sort_values(ascending=False)
```

---

## 7) Dúvidas Comuns e Erros

- UnicodeDecodeError ao ler CSV: tente `encoding='latin1'` ou `errors='replace'`.
- Separador errado: ajuste `sep` (ponto e vírgula é comum: `sep=';'`).
- Decimal com vírgula: use `decimal=','`.
- Datas inválidas: `errors='coerce'` em `to_datetime` e depois trate `NaT`.
- Gráficos “vazios”: confirme filtros/joins; verifique `df.shape` após operações.

---

## 8) Próximos Passos

- Rode o script de exemplo: `Python/Data Analysis/exemplos/eda_basico.py`.
- Crie um notebook e replique as receitas com seus dados.
- Salve suas funções utilitárias em um módulo (ex.: `utils.py`).
 

Bom trabalho e boas análises!