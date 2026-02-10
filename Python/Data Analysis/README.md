# Manual Completo de Análise de Dados com Python, Pandas, Matplotlib e Seaborn

Este manual é pensado como **guia de bolso**: se você precisar fazer algo em análise de dados ("quero filtrar linhas", "quero ver correlação", "quero um gráfico de distribuição"), deve conseguir achar **um exemplo pronto** aqui.

- Cada seção diz **quando usar**, **para que serve** e **mostra o padrão de código**.
- Os exemplos são curtos, copiáveis e fáceis de adaptar.

---

## Mapa Rápido: "Quero Fazer X"

### PARTE I - Fundamentos
- **Instalar ambiente**: veja **0) Instalação e Ambiente**
- **Entender conceitos básicos** (DataFrame, Series, operações vetorizadas): veja **1) Conceitos Fundamentais**

### PARTE II - Manipulação de Dados (Pandas)
- **Carregar dados** (CSV, Excel, JSON): veja **2.1 Importar e exportar dados**
- **Inspecionar estrutura** (tipos, nulos, estatísticas): veja **2.2 Criar e inspecionar**
- **Filtrar linhas e colunas**: veja **2.3 Seleção, filtro e ordenação**
- **Criar colunas novas, tratar texto, categorias**: veja **2.4 Criar/transformar colunas**
- **Tratar valores faltantes (NaN)**: veja **2.5 Missing values**
- **Agrupar, somar, tirar média por grupo**: veja **2.6 Agregações e groupby**
- **Fazer tabela dinâmica (tipo Excel)**: veja **2.7 Tabelas dinâmicas (pivot)**
- **Juntar tabelas (joins)**: veja **2.8 Junções (merge)**
- **Trabalhar com datas e séries temporais**: veja **2.9 Datas e séries temporais**

### PARTE III - Análise e Visualização
- **Fazer análise exploratória (EDA)**: veja **3) Análise Exploratória de Dados (EDA)**
- **Calcular métricas de negócio** (taxas, percentis, comparação de cenários): veja **4) Métricas e Decisões de Negócio**
- **Gráficos básicos e customizados**: veja **5) Matplotlib**
- **Gráficos estatísticos rápidos**: veja **6) Seaborn**
- **Decidir qual gráfico usar**: veja **6.10 Galeria: Qual Gráfico Usar Quando?**
- **Receitas práticas de análise**: veja **7) Receitas "Como fazer…"**

### PARTE IV - Escalabilidade e Big Data
- **Pensar em SQL mas escrever em Python**: veja **8) Pensamento Tabular (SQL-like)**
- **Entender quando Pandas não é suficiente**: veja **9) Limitações do Pandas**
- **Migrar de Pandas para PySpark**: veja **10) Transição para Big Data**
- **Processar grandes volumes (> 10GB)**: veja **11) PySpark para Big Data**
- **Joins, nulos, cache e I/O em produção**: veja **11.22) PySpark Prático Corporativo**
- **Análise de impacto antes/depois, A/B test e rollout**: veja **11.23) Análise de Impacto em Produção**
- **Ler e entender código Spark legado**: veja **11.24) Como Ler Código Spark Legado**

---

# PARTE I - FUNDAMENTOS

## 0) Instalação e Ambiente

Escolha uma das opções.

### Opção A: `venv` + `pip` (recomendada se você não usa Conda)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r "Python/Data Analysis/requirements.txt"
```

### Opção B: Conda (opcional)

Use se você já trabalha com Anaconda/Miniconda.

```bash
conda create -n dados python=3.11 -y
conda activate dados
pip install -r "Python/Data Analysis/requirements.txt"
```

### Jupyter (opcional mas recomendado)

Para trabalhar em notebooks (análises iterativas, gráficos inline):

```bash
python -m ipykernel install --user --name dados --display-name "Python (dados)"
jupyter lab
```

Abra o notebook `Python/Data Analysis/Receitas_Analise_Dados.ipynb` ou crie um novo e copie os exemplos deste manual.

---

## 1) Conceitos Fundamentais

- **DataFrame (pandas.DataFrame)**: tabela com colunas nomeadas e linhas indexadas.
  - Use para representar **dados tabulares** (planilhas, tabelas SQL, CSV etc.).
- **Série (pandas.Series)**: coluna única com índice.
  - Use para trabalhar com **uma coluna isolada** (ex.: `df['salario']`).
- **Operações vetorizadas**: operações aplicadas a colunas inteiras de uma vez.
  - Muito mais **rápidas e legíveis** que loops `for` linha a linha.
- **Matplotlib**: biblioteca base de gráficos em Python.
  - Use quando você quer **controle fino** do gráfico (eixos, anotações, layout).
- **Seaborn**: camada de alto nível sobre Matplotlib, focada em gráficos estatísticos.
  - Use quando quer **EDA rápida** (exploração), gráficos bonitos em poucas linhas.
- **Pipeline típico de EDA (Análise Exploratória de Dados)**:
  1. Carregar dados (2.2)
  2. Inspecionar estrutura e qualidade (2.1, 2.5)
  3. Limpar e transformar (2.4, 2.5)
  4. Agregar e resumir (2.6, 2.7, 2.8)
  5. Visualizar padrões (3, 4, 5.7, 5.8)

---

## 2) Pandas Essencial

### 2.1 Importar e exportar dados

**Quando usar:**
- Ler arquivos de **CSV, Excel, JSON** para DataFrame e salvar resultados.

```python
import pandas as pd

# CSV (mais comum)
df = pd.read_csv(
  'dados.csv',
  sep=',',
  decimal='.',
  encoding='utf-8', # tente 'latin1' se der UnicodeDecodeError
)

# Salvar limpando o índice
df.to_csv('saida.csv', index=False)

# Excel
df_x = pd.read_excel('planilha.xlsx', sheet_name='Aba1')
df_x.to_excel('saida.xlsx', index=False)

# JSON
df_j = pd.read_json('dados.json', lines=False)
df_j.to_json('saida.json', orient='records', force_ascii=False, indent=2)
```

### 2.2 Criar e inspecionar

**Quando usar:**
- Primeiro contato com os dados: entender **colunas, tipos, nulos, ordem de grandeza**.

```python
import pandas as pd

# DataFrame a partir de dict
df = pd.DataFrame({
  'nome': ['Ana', 'Bruno', 'Carla', 'Daniel'],
  'idade': [23, 31, 29, 40],
  'cidade': ['SP', 'RJ', 'SP', 'BH'],
  'salario': [5000, 7200, 6100, 9800],
})

df.head()        # 5 primeiras linhas (padrão)
df.tail(3)       # 3 últimas linhas
df.sample(5)     # 5 linhas aleatórias (bom para checar qualidade)
df.info()        # tipos, contagem de nulos, memória
df.describe()    # estatísticas numéricas básicas
df.dtypes        # tipos por coluna
```

### 2.2 Importar e exportar dados

**Quando usar:**
- Ler arquivos de **CSV, Excel, JSON** para DataFrame e salvar resultados.

```python
import pandas as pd

# CSV (mais comum)
df = pd.read_csv(
  'dados.csv',
  sep=',',          # separador: use ';' se for CSV brasileiro
  decimal='.',      # use ',' se decimal for vírgula
  encoding='utf-8', # tente 'latin1' se der UnicodeDecodeError
)

# Salvar limpando o índice
df.to_csv('saida.csv', index=False)

# Excel
df_x = pd.read_excel('planilha.xlsx', sheet_name='Aba1')
df_x.to_excel('saida.xlsx', index=False)

# JSON
df_j = pd.read_json('dados.json', lines=False)
df_j.to_json('saida.json', orient='records', force_ascii=False, indent=2)
```

### 2.3 Seleção, filtro e ordenação

**Quando usar:**
- Precisa **isolar colunas**, **filtrar linhas** por condição ou **ordenar** os dados.

```python
# Seleção de colunas
idade = df['idade']                 # Series
subset = df[['nome', 'salario']]    # DataFrame com 2 colunas

# Filtro (linhas)
sp = df[df['cidade'] == 'SP']
ricos = df[df['salario'] > 7000]

# Combinação de condições (use parênteses)
ricos_sp = df[(df['cidade'] == 'SP') & (df['salario'] > 7000)]

# loc (por rótulo) / iloc (por posição)
linha_rotulo = df.loc[0]            # linha com índice 0
linha_posicao = df.iloc[0]          # primeira linha, independente do índice

# Selecionar linhas e colunas ao mesmo tempo
subset2 = df.loc[df['cidade'] == 'SP', ['nome', 'salario']]

# Ordenar
por_salario = df.sort_values('salario', ascending=False)
por_cidade_idade = df.sort_values(['cidade', 'idade'])
```

### 2.4 Criar/transformar colunas

**Quando usar:**
- Criar **colunas derivadas** (faixas, indicadores, flags), tratar **string** e **categorias**.

```python
# Colunas derivadas numéricas
df['salario_k'] = df['salario'] / 1000
df['dobro_idade'] = df['idade'] * 2

# Criar faixas salariais
df['faixa_sal'] = pd.cut(
  df['salario'],
  bins=[0, 6000, 9000, float('inf')],
  labels=['baixa', 'media', 'alta']
)

# Operações com string
df['nome_maiusculo'] = df['nome'].str.upper()
df['iniciais'] = df['nome'].str[0]
df['tem_a_no_nome'] = df['nome'].str.contains('a', case=False)

# map: substituição de valores
mapa = {'SP': 'Sao Paulo', 'RJ': 'Rio de Janeiro', 'BH': 'Belo Horizonte'}
df['cidade_nome'] = df['cidade'].map(mapa)

# apply linha a linha (use com parcimônia, pode ser lento)
def calcula_bonus(salario):
  if salario > 8000:
    return salario * 0.15
  elif salario > 6000:
    return salario * 0.10
  else:
    return salario * 0.05

df['bonus'] = df['salario'].apply(calcula_bonus)
```

### 2.5 Missing values (valores ausentes)

**Quando usar:**
- Sempre que houver valores **NaN/None**. Você precisa decidir se vai **remover** ou **preencher**.

```python
# Ver quantidade de nulos por coluna
df.isna().sum()

# Substituir nulos em uma coluna numérica pela mediana
df['idade'] = df['idade'].fillna(df['idade'].median())

# Substituir nulos com valor fixo
df['cidade'] = df['cidade'].fillna('Desconhecida')

# Remover linhas que não têm salário
df = df.dropna(subset=['salario'])

# Remover qualquer linha que tenha pelo menos 1 nulo
df_sem_nulos = df.dropna()
```

### 2.6 Agregações e groupby

**Quando usar:**
- Quer **resumir dados por grupo** (por cidade, produto, cliente, mês etc.).

```python
# Estatística por grupo
por_cidade = df.groupby('cidade').agg(
  qtd=('nome', 'count'),
  media_sal=('salario', 'mean'),
  mediana_idade=('idade', 'median'),
)

# Agregações múltiplas na mesma coluna
agg_multi = df.groupby('cidade')['salario'].agg(['mean', 'median', 'min', 'max'])

# Filtrar grupos depois de agregar (ex.: cidades com média salarial > 7000)
altas_medias = agg_multi[agg_multi['mean'] > 7000]
```

### 2.7 Tabelas dinâmicas (pivot)

**Quando usar:**
- Quer tabelas no estilo **tabela dinâmica do Excel**, cruzando linhas x colunas.

```python
pivot = pd.pivot_table(
  df,
  values='salario',
  index='cidade',      # vira linha
  columns='faixa_sal', # vira coluna
  aggfunc='mean',
  fill_value=0,
)

print(pivot)
```

### 2.8 Junções (merge)

**Quando usar:**
- Precisa juntar informações que estão em **tabelas diferentes** (como joins em SQL).

```python
import pandas as pd

clientes = pd.DataFrame({'id': [1, 2, 3], 'nome': ['Ana', 'Bruno', 'Carla']})
compras  = pd.DataFrame({'id_cliente': [1, 2, 2, 4], 'valor': [100, 200, 50, 80]})

# left join: mantém todos os clientes, mesmo sem compra
joined = clientes.merge(compras, left_on='id', right_on='id_cliente', how='left')

# inner join: só quem tem correspondência nos dois lados
inner = clientes.merge(compras, left_on='id', right_on='id_cliente', how='inner')

# right, outer também existem
```

### 2.9 Datas e séries temporais

**Quando usar:**
- Dados com **datas** (vendas diárias, acessos por dia, logs, séries financeiras etc.).

```python
# Converter para datetime
df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')

# Extrações comuns
df['ano'] = df['data'].dt.year
df['mes'] = df['data'].dt.month
df['dia_sem'] = df['data'].dt.day_name(locale='pt_BR')

# Reamostragem (resample) após definir índice temporal
ts = df.set_index('data').sort_index()

# Soma mensal
mensal = ts['salario'].resample('M').sum()

# Média móvel de 3 períodos
movel = ts['salario'].rolling(window=3, min_periods=1).mean()
```

---


# PARTE III - ANÁLISE E VISUALIZAÇÃO

## 3) Análise Exploratória de Dados (EDA)

**O que é EDA?**

EDA não é "fazer gráficos". É **pensar análise antes de modelar ou decidir**.

EDA é o processo de **entender o dataset** através de 4 pilares:

### 1. Distribuição: Como os dados se comportam?

**Por que importa:**
- Identifica se a variável é **simétrica, assimétrica, bimodal**.
- Mostra se há **concentração** em valores específicos.
- Revela se **transformações** (log, raiz quadrada) são necessárias.

**Quando usar:**
- Sempre que pegar uma **nova variável numérica**.
- Antes de calcular médias (se a distribuição for muito assimétrica, mediana é melhor).

**Gráficos principais:**
- `histplot`: frequência por intervalos (bins)
- `kdeplot`: curva suave de densidade
- `boxplot`: quartis e outliers

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Ver distribuição de salários
sns.histplot(df['salario'], bins=30, kde=True)
plt.title('Distribuição de Salários')

# Comparar com normal
from scipy import stats
stats.probplot(df['salario'], dist="norm", plot=plt)
plt.title('Q-Q Plot (Salário vs Normal)')
```

### 2. Outliers: Tem valores extremos?

**Por que importa:**
- Outliers podem ser **erros de digitação** ou **casos raros legítimos**.
- Afetam drasticamente **média, regressões e modelos**.
- Podem indicar **fraudes, anomalias ou oportunidades**.

**Quando usar:**
- Sempre antes de agregar (média, soma).
- Em análises de crédito, detecção de fraude, controle de qualidade.

**Técnicas:**
- **IQR (Interquartile Range)**: valores fora de Q1 - 1.5×IQR ou Q3 + 1.5×IQR
- **Z-score**: valores com |z| > 3
- **Visualização**: boxplot, scatter plot

```python
# Identificar outliers com IQR
Q1 = df['salario'].quantile(0.25)
Q3 = df['salario'].quantile(0.75)
IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

outliers = df[(df['salario'] < limite_inferior) | (df['salario'] > limite_superior)]
print(f"Outliers encontrados: {len(outliers)}")

# Visualizar
sns.boxplot(x=df['salario'])
```

### 3. Correlação: Variáveis se relacionam?

**Por que importa:**
- Identifica **variáveis redundantes** (multicolinearidade).
- Mostra quais variáveis têm **relação forte** com o alvo.
- Ajuda a **escolher features** para modelagem.

**Quando usar:**
- Antes de construir modelos preditivos.
- Para entender **drivers de negócio** (o que afeta vendas, churn, etc.).

**Importante:**
- Correlação ≠ causalidade.
- Correlação mede **relação linear** (pode existir relação não-linear).

```python
# Matriz de correlação
corr = df.corr(numeric_only=True)

# Visualizar
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Matriz de Correlação')

# Focar no alvo
corr_alvo = corr['target'].sort_values(ascending=False)
print(corr_alvo)

# Scatter plot das mais correlacionadas
sns.pairplot(df[['salario', 'idade', 'score', 'target']], hue='target')
```

### 4. Comparação entre grupos: Há diferenças significativas?

**Por que importa:**
- Identifica **segmentos** com comportamentos distintos.
- Valida **hipóteses de negócio** (homens ganham mais? SP tem mais inadimplência?).
- Guia **estratégias diferenciadas** por grupo.

**Quando usar:**
- Comparar cidades, produtos, períodos, segmentos de clientes.
- Testar se **políticas diferentes** tiveram impacto diferente.

```python
# Comparar salário médio por cidade
sns.barplot(data=df, x='cidade', y='salario', ci=95)
plt.title('Salário Médio por Cidade (com IC 95%)')

# Ver distribuição completa
sns.violinplot(data=df, x='cidade', y='salario')

# Teste estatístico (ANOVA ou Kruskal-Wallis)
from scipy.stats import kruskal
grupos = [df[df['cidade'] == c]['salario'].dropna() for c in df['cidade'].unique()]
statistic, pvalue = kruskal(*grupos)
print(f"Kruskal-Wallis: p-value = {pvalue:.4f}")
if pvalue < 0.05:
    print("Há diferença significativa entre os grupos")
```

### Checklist de EDA

Use isso **antes de qualquer análise**:

- [ ] Carreguei os dados e entendi as dimensões?
- [ ] Verifiquei tipos de dados e valores nulos?
- [ ] Vi a distribuição das variáveis numéricas principais?
- [ ] Identifiquei outliers?
- [ ] Calculei correlação entre variáveis?
- [ ] Comparei grupos relevantes (cidade, produto, período)?
- [ ] Documentei insights e decisões de limpeza?

---




## 4) Métricas e Decisões de Negócio

**Por que importa:**

Código técnico (`.mean()`, `.groupby()`) resolve o "como".
Métricas de negócio respondem o "por quê" e o "o que fazer".

### 1. Média vs Mediana: Qual usar?

**Média (mean):**
- Sensível a **outliers**.
- Use quando a distribuição é **simétrica** ou você quer o **valor total dividido**.

**Mediana (median):**
- **Robusta** a outliers.
- Use quando há **assimetria** ou **valores extremos**.

```python
# Exemplo: salários com outliers
salarios = [3000, 3500, 4000, 4200, 50000]  # CEO ganha muito mais

media = np.mean(salarios)      # 12.940 (distorcido)
mediana = np.median(salarios)  # 4.000 (representativo)

# Regra prática
if df['salario'].skew() > 1:  # assimetria alta
    print("Use mediana")
else:
    print("Média é ok")
```

### 2. Taxas e Proporções

**Quando usar:**
- Comparar **incidências** entre grupos de tamanhos diferentes.
- Medir **conversão, inadimplência, churn, aprovação**.

```python
# Taxa de inadimplência por cidade
taxa = df.groupby('cidade').agg(
    total=('cpf', 'count'),
    inadimplentes=('inadimplente', 'sum')
)
taxa['taxa_inadimplencia'] = (taxa['inadimplentes'] / taxa['total'] * 100).round(2)

# Taxa de conversão (funil)
total_leads = 10000
convertidos = 1200
taxa_conversao = (convertidos / total_leads) * 100  # 12%
```

### 3. Percentis: Entendendo a Distribuição

**Quando usar:**
- Definir **políticas de aprovação** (aprovar top 30%).
- Identificar **faixas de risco** (bottom 10% = alto risco).
- Criar **segmentações**.

```python
# Percentis de score de crédito
p25 = df['score'].quantile(0.25)  # 25% têm score abaixo disso
p50 = df['score'].quantile(0.50)  # mediana
p75 = df['score'].quantile(0.75)
p90 = df['score'].quantile(0.90)

# Criar faixas de risco
df['faixa_risco'] = pd.cut(
    df['score'],
    bins=[0, p25, p75, 1000],
    labels=['Alto Risco', 'Médio Risco', 'Baixo Risco']
)

# Ver inadimplência por faixa
df.groupby('faixa_risco')['inadimplente'].mean() * 100
```

### 4. Comparação de Cenários

**Quando usar:**
- Avaliar **impacto de políticas** (antes vs depois).
- Testar **A/B tests**.
- Simular **mudanças de regras**.

```python
# Cenário atual vs proposto
# Política atual: aprovar score > 600
atual = df[df['score'] > 600]
taxa_inad_atual = atual['inadimplente'].mean() * 100
volume_atual = len(atual)

# Política proposta: aprovar score > 650
proposta = df[df['score'] > 650]
taxa_inad_proposta = proposta['inadimplente'].mean() * 100
volume_proposta = len(proposta)

print(f"Atual: {volume_atual} aprovações, {taxa_inad_atual:.2f}% inadimplência")
print(f"Proposta: {volume_proposta} aprovações, {taxa_inad_proposta:.2f}% inadimplência")

# Trade-off
perda_volume = ((volume_atual - volume_proposta) / volume_atual * 100)
ganho_qualidade = taxa_inad_atual - taxa_inad_proposta
print(f"Perdemos {perda_volume:.1f}% de volume, mas reduzimos {ganho_qualidade:.2f}pp de inadimplência")
```

### Métricas Comuns por Área

**Crédito:**
- Taxa de inadimplência
- Taxa de aprovação
- Ticket médio
- Perda esperada (Exposure × PD × LGD)

**Marketing:**
- Taxa de conversão
- CAC (Custo de Aquisição de Cliente)
- LTV (Lifetime Value)
- ROI de campanha

**Produto:**
- Taxa de churn
- Retenção (cohort analysis)
- NPS (Net Promoter Score)
- DAU/MAU (Daily/Monthly Active Users)

---



# PARTE III - ANÁLISE E VISUALIZAÇÃO

## 3) Análise Exploratória de Dados (EDA)

**Quando usar Matplotlib:**

- Você quer **controle detalhado** de cada elemento do gráfico (eixos, legendas, anotações).
- Vai montar **figuras mais customizadas ou relatórios estáticos**.
- Seaborn usa Matplotlib por baixo; muitas vezes você combina ambos.

### 7.1 Primeiros passos

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [10, 20, 15, 30]

plt.figure(figsize=(6, 4))
plt.plot(x, y, marker='o', linewidth=2, color='tab:blue')
plt.title('Exemplo de Linha')
plt.xlabel('Eixo X')
plt.ylabel('Eixo Y')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### 7.2 Tipos comuns

```python
# Barras
plt.bar(['A', 'B', 'C'], [3, 7, 5], color='tab:green')

# Histograma (distribuição de salário)
plt.figure(figsize=(6, 4))
plt.hist(df['salario'], bins=20, color='tab:purple', alpha=0.7)
plt.xlabel('Salário')
plt.ylabel('Frequência')

# Dispersão (idade x salário)
plt.figure(figsize=(6, 4))
plt.scatter(df['idade'], df['salario'], alpha=0.6)
plt.xlabel('Idade')
plt.ylabel('Salário')

# Boxplot
plt.figure(figsize=(4, 4))
plt.boxplot([df['salario']], labels=['salario'])
```

### 7.3 Subplots e personalização

```python
fig, ax = plt.subplots(1, 2, figsize=(10, 4))

ax[0].plot(x, y, marker='o')
ax[0].set_title('Linha')

ax[1].hist(y, bins=4)
ax[1].set_title('Histograma')

fig.suptitle('Dois Gráficos')
fig.tight_layout()
plt.show()
```

### 7.4 Galeria Matplotlib: Gráficos Essenciais

```python
import matplotlib.pyplot as plt
import numpy as np

# Dados de exemplo
x = np.linspace(0, 10, 100)
y = np.sin(x)
categorias = ['A', 'B', 'C', 'D']
valores = [23, 45, 12, 67]

# 1. Gráfico de linha com marcadores
plt.figure(figsize=(8, 4))
plt.plot(x, y, '-o', label='Seno', linewidth=2, markersize=3)
plt.plot(x, np.cos(x), '--s', label='Cosseno', markersize=3)
plt.legend()
plt.grid(alpha=0.3)
plt.title('Linhas com marcadores')

# 2. Barras verticais e horizontais
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].bar(categorias, valores, color='steelblue', edgecolor='black')
axes[0].set_title('Barras Verticais')
axes[1].barh(categorias, valores, color='coral')
axes[1].set_title('Barras Horizontais')

# 3. Histograma com customização
dados = np.random.randn(1000)
plt.figure(figsize=(8, 4))
plt.hist(dados, bins=30, color='purple', alpha=0.7, edgecolor='black')
plt.axvline(dados.mean(), color='red', linestyle='--', label=f'Média: {dados.mean():.2f}')
plt.legend()
plt.title('Histograma com linha de referência')

# 4. Scatter plot com cores e tamanhos
x_scatter = np.random.rand(100)
y_scatter = np.random.rand(100)
cores = np.random.rand(100)
tamanhos = np.random.rand(100) * 1000

plt.figure(figsize=(8, 6))
scatter = plt.scatter(x_scatter, y_scatter, c=cores, s=tamanhos, 
                     alpha=0.6, cmap='viridis', edgecolors='black')
plt.colorbar(scatter, label='Valor da cor')
plt.title('Dispersão com cores e tamanhos variáveis')

# 5. Boxplot
dados_grupos = [np.random.normal(0, std, 100) for std in range(1, 5)]
plt.figure(figsize=(8, 4))
bp = plt.boxplot(dados_grupos, labels=['Grupo A', 'Grupo B', 'Grupo C', 'Grupo D'],
                 patch_artist=True, notch=True)
for patch in bp['boxes']:
    patch.set_facecolor('lightblue')
plt.title('Boxplot com customização')

# 6. Área preenchida (fill_between)
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.sin(x) + 0.5

plt.figure(figsize=(10, 4))
plt.plot(x, y1, 'b-', label='Inferior')
plt.plot(x, y2, 'r-', label='Superior')
plt.fill_between(x, y1, y2, alpha=0.3, color='gray', label='Área')
plt.legend()
plt.title('Área entre curvas')

# 7. Gráfico de pizza
plt.figure(figsize=(7, 7))
explode = (0.1, 0, 0, 0)  # "explodir" a primeira fatia
plt.pie(valores, labels=categorias, autopct='%1.1f%%', 
        explode=explode, shadow=True, startangle=90)
plt.title('Gráfico de Pizza')

# 8. Heatmap (com Matplotlib puro)
data = np.random.rand(10, 10)
plt.figure(figsize=(8, 6))
im = plt.imshow(data, cmap='YlOrRd', aspect='auto')
plt.colorbar(im, label='Intensidade')
plt.title('Heatmap com Matplotlib')
plt.xlabel('Colunas')
plt.ylabel('Linhas')

# 9. Stem plot (hastes)
x = np.linspace(0, 2*np.pi, 20)
y = np.sin(x)
plt.figure(figsize=(10, 4))
plt.stem(x, y, linefmt='b-', markerfmt='ro', basefmt='k-')
plt.title('Stem Plot')

# 10. Múltiplos subplots com layout complexo
fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
ax1 = fig.add_subplot(gs[0, :])  # primeira linha inteira
ax2 = fig.add_subplot(gs[1, :-1]) # segunda linha, 2 primeiras colunas
ax3 = fig.add_subplot(gs[1:, -1]) # últimas 2 linhas, última coluna
ax4 = fig.add_subplot(gs[-1, 0])  # canto inferior esquerdo
ax5 = fig.add_subplot(gs[-1, 1])  # canto inferior centro

ax1.plot(x, y)
ax1.set_title('Subplot 1')
ax2.scatter(x_scatter, y_scatter)
ax2.set_title('Subplot 2')
ax3.hist(dados, bins=20, orientation='horizontal')
ax3.set_title('Subplot 3')
ax4.bar(['A', 'B'], [1, 2])
ax5.pie([30, 70], labels=['X', 'Y'])
```

---

## 6) Visualização com Seaborn (Guia Completo)

**Quando usar Seaborn:**

- Quer **gráficos estatísticos prontos** em poucas linhas.
- Está fazendo **análise exploratória** e quer ver rapidamente **relações, distribuições e comparações**.
- Quer gráficos com **estilo consistente e bonito** por padrão.

Configuração básica:

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')  # tema global dos gráficos
# Outros estilos: 'darkgrid', 'white', 'dark', 'ticks'

tips = sns.load_dataset('tips')   # dataset de exemplo do Seaborn
```

### 11.1 Gráficos relacionais (relplot, scatterplot, lineplot)

**Para que serve:**

- Ver **relação entre duas variáveis numéricas** (ex.: conta x gorjeta, idade x salário).
- Analisar **tendências ao longo do tempo** (séries temporais).

```python
# Dispersão simples
sns.scatterplot(data=tips, x='total_bill', y='tip')

# Adicionando cor por categoria (hue) e tamanho (size)
sns.scatterplot(
    data=tips, 
    x='total_bill', y='tip', 
    hue='time', size='size',
    sizes=(20, 200), alpha=0.6
)

# relplot: figura mais flexível, com facetas
sns.relplot(
    data=tips,
    x='total_bill', y='tip',
    hue='time', style='sex',
    kind='scatter', height=4, aspect=1.4
)

# Linha para séries temporais
# Exemplo com dataset de voos
flights = sns.load_dataset('flights')
sns.lineplot(
    data=flights,
    x='year', y='passengers',
    hue='month', style='month',
    markers=True, dashes=False
)
```

### 11.2 Gráficos categóricos (catplot, barplot, boxplot, violinplot)

**Para que serve:**

- Comparar **distribuições ou médias** entre **categorias** (dia da semana, cidade, produto etc.).

#### 4.2.1 Barras (barplot, countplot)

**Quando usar:**
- Comparar **médias ou totais** entre categorias.
- Mostrar **contagem** de observações.

```python
# Barra com intervalo de confiança (média por dia)
sns.barplot(data=tips, x='day', y='total_bill', ci='sd')

# Contagem de observações por categoria
sns.countplot(data=tips, x='day', hue='sex')

# Barras horizontais
sns.barplot(data=tips, y='day', x='total_bill', orient='h')

# catplot permite facetas
sns.catplot(
    data=tips,
    x='day', y='total_bill',
    kind='bar', col='time', ci=95
)
```

#### 4.2.2 Boxplot e Violinplot

**Quando usar:**
- Ver **distribuição completa** (quartis, outliers, formato).
- Comparar **dispersão** entre grupos.

```python
# Boxplot por dia da semana
sns.boxplot(data=tips, x='day', y='total_bill')

# Violino (mostra densidade + quartis)
sns.violinplot(data=tips, x='day', y='total_bill')

# Violino com divisão por sexo
sns.violinplot(
    data=tips,
    x='day', y='total_bill',
    hue='sex', split=True, inner='quartile'
)

# Boxen plot (mais detalhes que boxplot)
sns.boxenplot(data=tips, x='day', y='total_bill')
```

#### 4.2.3 Swarmplot e Stripplot

**Quando usar:**
- Mostrar **cada ponto individual** mantendo a categoria.
- Datasets **pequenos/médios** (até ~1000 pontos por grupo).

```python
# Swarmplot: pontos sem sobreposição
sns.swarmplot(data=tips, x='day', y='total_bill', hue='sex')

# Stripplot: pontos com jitter
sns.stripplot(data=tips, x='day', y='total_bill', alpha=0.5)

# Combinando boxplot + swarmplot
fig, ax = plt.subplots(figsize=(8, 4))
sns.boxplot(data=tips, x='day', y='total_bill', ax=ax, color='lightgray')
sns.swarmplot(data=tips, x='day', y='total_bill', ax=ax, color='black', alpha=0.4)
```

#### 4.2.4 Pointplot

**Quando usar:**
- Mostrar **média com intervalo de confiança** como pontos + linhas.
- Comparar **mudanças entre categorias ordenadas** (ex.: antes/depois, níveis crescentes).

```python
sns.pointplot(data=tips, x='day', y='total_bill', hue='sex')
```

### 11.3 Distribuições (displot, histplot, kdeplot, ecdfplot)

**Para que serve:**

- Entender **forma da distribuição** (assimetria, caudas, multimodal etc.).
- Identificar **valores típicos e extremos**.

#### 4.3.1 Histograma (histplot)

**Quando usar:**
- Ver **frequência de intervalos** (bins).
- Comparar distribuições entre grupos.

```python
# Histograma básico
sns.histplot(data=tips, x='total_bill', bins=20)

# Com densidade (KDE) sobreposta
sns.histplot(data=tips, x='total_bill', kde=True, bins=30)

# Múltiplas categorias empilhadas
sns.histplot(data=tips, x='total_bill', hue='sex', multiple='stack')

# Lado a lado (dodge)
sns.histplot(data=tips, x='total_bill', hue='sex', multiple='dodge', shrink=0.8)

# displot: interface de alto nível
sns.displot(data=tips, x='total_bill', kde=True, bins=20, height=4, aspect=1.5)
```

#### 4.3.2 Densidade (kdeplot)

**Quando usar:**
- Ver **curva suave** da distribuição.
- Comparar **formas de distribuição** sem depender de bins.

```python
# KDE simples
sns.kdeplot(data=tips, x='total_bill', fill=True)

# KDE 2D (bivariada)
sns.kdeplot(data=tips, x='total_bill', y='tip', fill=True, cmap='Blues')

# Múltiplas categorias
sns.kdeplot(data=tips, x='total_bill', hue='time', fill=True, alpha=0.5)
```
w
#### 4.3.3 ECDF (ecdfplot)

**Quando usar:**
- Ver **proporção acumulada** de valores.
- Comparar distribuições de forma **robusta** (não depende de bins).

```python
sns.ecdfplot(data=tips, x='total_bill', hue='sex')
```

#### 4.3.4 Rug plot

**Quando usar:**
- Adicionar **marcas de cada observação** na margem do gráfico.

```python
fig, ax = plt.subplots()
sns.histplot(data=tips, x='total_bill', kde=True, ax=ax)
sns.rugplot(data=tips, x='total_bill', ax=ax, height=0.05, alpha=0.5)
```

### 11.4 Regressão (lmplot, regplot, residplot)

**Para que serve:**

- Ver **tendência linear** entre duas variáveis e **intervalo de confiança**.
- Avaliar qualidade do ajuste linear.

```python
# Regressão linear simples
sns.regplot(data=tips, x='total_bill', y='tip')

# Com ordem polinomial
sns.regplot(data=tips, x='total_bill', y='tip', order=2)

# lmplot: permite facetas e mais opções
sns.lmplot(
    data=tips,
    x='total_bill', y='tip',
    hue='sex', col='time', height=4
)

# Gráfico de resíduos (avaliar qualidade do ajuste)
sns.residplot(data=tips, x='total_bill', y='tip', lowess=True)
```

### 11.5 Matriz de correlação e heatmap

**Para que serve:**

- Ver **força da relação linear** entre variáveis numéricas.
- Visualizar **tabelas de valores** com cores.

```python
# Heatmap de correlação
corr = tips.corr(numeric_only=True)

plt.figure(figsize=(6, 4))
sns.heatmap(
    corr, 
    annot=True,      # mostrar valores
    cmap='vlag',     # paleta divergente
    center=0,        # centro da paleta em zero
    square=True,     # células quadradas
    linewidths=0.5,  # linhas entre células
    cbar_kws={'label': 'Correlação'}
)
plt.show()

# Clustermap: agrupa linhas/colunas similares
sns.clustermap(
    corr,
    annot=True,
    cmap='coolwarm',
    center=0,
    figsize=(8, 8)
)
```

### 11.6 Jointplot (bivariada com marginais)

**Para que serve:**

- Ver **relação entre duas variáveis** + **distribuições marginais** de cada uma.

```python
# Dispersão + histogramas nas margens
sns.jointplot(data=tips, x='total_bill', y='tip', kind='scatter')

# Com KDE
sns.jointplot(data=tips, x='total_bill', y='tip', kind='kde', fill=True)

# Hexbin (para muitos pontos)
sns.jointplot(data=tips, x='total_bill', y='tip', kind='hex', gridsize=20)

# Regressão
sns.jointplot(data=tips, x='total_bill', y='tip', kind='reg')
```

### 11.7 Pairplot (matriz de dispersão)

**Para que serve:**

- Ver **todas as relações bivariadas** entre variáveis numéricas de uma vez.
- Identificar **correlações e padrões** rapidamente.

```python
# Pairplot completo
sns.pairplot(tips, hue='time', corner=False)

# Apenas triângulo inferior (mais limpo)
sns.pairplot(
    tips[['total_bill', 'tip', 'size']], 
    corner=True, 
    diag_kind='kde',
    plot_kws={'alpha': 0.6}
)
```

### 11.8 Facetas (FacetGrid - pequenos múltiplos)

**Para que serve:**

- Comparar o **mesmo gráfico** em **subconjuntos diferentes** (por tempo, sexo, cidade, etc.).
- Criar **painéis de visualização** customizados.

```python
# Facetas básicas
g = sns.FacetGrid(tips, col='time', row='sex', margin_titles=True, height=3)
g.map_dataframe(sns.scatterplot, x='total_bill', y='tip')
g.add_legend()

# Com histogramas
g = sns.FacetGrid(tips, col='day', col_wrap=2, height=3)
g.map(sns.histplot, 'total_bill', bins=15, kde=True)

# Customização avançada
g = sns.FacetGrid(
    tips, 
    col='time', 
    hue='sex',
    palette='Set2',
    height=4, aspect=1.2
)
g.map(sns.scatterplot, 'total_bill', 'tip', alpha=0.6)
g.add_legend()
g.set_axis_labels('Conta Total', 'Gorjeta')
g.fig.suptitle('Gorjetas por Período e Sexo', y=1.02)
```

### 11.9 Paletas de cores e estilos

**Para que serve:**

- Deixar gráficos **consistentes e profissionais**.
- Adaptar para **apresentações, relatórios, publicações**.

```python
# Definir paleta global
sns.set_palette('deep')  # 'deep', 'muted', 'pastel', 'bright', 'dark', 'colorblind'

# Paletas específicas
sns.color_palette('viridis', as_cmap=True)      # contínua
sns.color_palette('Set2')                        # categórica
sns.diverging_palette(250, 10, as_cmap=True)    # divergente

# Estilos de tema
sns.set_style('whitegrid')  # 'darkgrid', 'white', 'dark', 'ticks'

# Contexto (tamanho de fontes)
sns.set_context('notebook')  # 'paper', 'notebook', 'talk', 'poster'

# Exemplo de uso
with sns.axes_style('darkgrid'):
    sns.scatterplot(data=tips, x='total_bill', y='tip')
```

---

## 4.10 Galeria Completa: Qual Gráfico Usar Quando?

### Guia de Decisão por Objetivo

#### 📊 Quero comparar VALORES entre CATEGORIAS

| Situação | Gráfico | Código |
|----------|---------|--------|
| Média/total por categoria | `barplot` | `sns.barplot(x='categoria', y='valor')` |
| Contagem de observações | `countplot` | `sns.countplot(x='categoria')` |
| Comparar médias ao longo do tempo/ordem | `pointplot` | `sns.pointplot(x='tempo', y='valor')` |

#### 📈 Quero ver DISTRIBUIÇÃO de uma variável

| Situação | Gráfico | Código |
|----------|---------|--------|
| Frequência em intervalos | `histplot` | `sns.histplot(x='valor', bins=20)` |
| Curva suave de densidade | `kdeplot` | `sns.kdeplot(x='valor', fill=True)` |
| Distribuição acumulada | `ecdfplot` | `sns.ecdfplot(x='valor')` |
| Comparar quartis entre grupos | `boxplot` | `sns.boxplot(x='grupo', y='valor')` |
| Ver forma da distribuição + outliers | `violinplot` | `sns.violinplot(x='grupo', y='valor')` |

#### 🔗 Quero ver RELAÇÃO entre DUAS variáveis numéricas

| Situação | Gráfico | Código |
|----------|---------|--------|
| Relação geral | `scatterplot` | `sns.scatterplot(x='var1', y='var2')` |
| Com tendência linear | `regplot` | `sns.regplot(x='var1', y='var2')` |
| Relação + distribuições marginais | `jointplot` | `sns.jointplot(x='var1', y='var2', kind='scatter')` |
| Muitos pontos (densidade) | `jointplot(kind='hex')` | `sns.jointplot(x='var1', y='var2', kind='hex')` |

#### 🌐 Quero ver MÚLTIPLAS relações de uma vez

| Situação | Gráfico | Código |
|----------|---------|--------|
| Todas as relações bivariadas | `pairplot` | `sns.pairplot(df)` |
| Matriz de correlação | `heatmap(corr)` | `sns.heatmap(df.corr(), annot=True)` |

#### 📅 Quero ver EVOLUÇÃO ao longo do TEMPO

| Situação | Gráfico | Código |
|----------|---------|--------|
| Série temporal única | `lineplot` | `sns.lineplot(x='data', y='valor')` |
| Múltiplas séries | `lineplot(hue=...)` | `sns.lineplot(x='data', y='valor', hue='grupo')` |
| Área acumulada | `plt.fill_between` | `plt.fill_between(x, y)` |

#### 👥 Quero ver cada PONTO individual mantendo a categoria

| Situação | Gráfico | Código |
|----------|---------|--------|
| Poucos pontos, sem sobreposição | `swarmplot` | `sns.swarmplot(x='grupo', y='valor')` |
| Muitos pontos | `stripplot` | `sns.stripplot(x='grupo', y='valor', alpha=0.4)` |

#### 🎯 Quero COMPARAR grupos em SUBPLOTS

| Situação | Gráfico | Código |
|----------|---------|--------|
| Mesmo gráfico para cada subgrupo | `FacetGrid` | `g = sns.FacetGrid(col='grupo'); g.map(...)` |
| Usar funções prontas com facetas | `catplot`, `relplot`, `displot` | `sns.catplot(x=..., col='grupo')` |

### Exemplos Práticos Completos

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Dataset de exemplo
tips = sns.load_dataset('tips')
iris = sns.load_dataset('iris')
flights = sns.load_dataset('flights')

# 1. Comparar médias entre categorias
sns.barplot(data=tips, x='day', y='total_bill', ci=95)
plt.title('Conta média por dia da semana')

# 2. Ver distribuição completa
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
sns.histplot(data=tips, x='total_bill', bins=20, ax=axes[0])
sns.kdeplot(data=tips, x='total_bill', fill=True, ax=axes[1])
sns.violinplot(data=tips, y='total_bill', ax=axes[2])

# 3. Relação bivariada
sns.jointplot(data=tips, x='total_bill', y='tip', kind='reg', height=5)

# 4. Matriz de correlação
corr = tips.corr(numeric_only=True)
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)

# 5. Todas as relações de uma vez
sns.pairplot(iris, hue='species', corner=True)

# 6. Série temporal
pivot = flights.pivot(index='month', columns='year', values='passengers')
sns.lineplot(data=flights, x='year', y='passengers', hue='month', legend=False)

# 7. Comparar distribuições entre grupos
sns.violinplot(data=tips, x='day', y='total_bill', hue='sex', split=True)

# 8. Facetas (pequenos múltiplos)
g = sns.FacetGrid(tips, col='time', row='sex', height=3)
g.map_dataframe(sns.scatterplot, x='total_bill', y='tip')
g.add_legend()
```

---

## 7) Receitas "Como Fazer…" (Guia por Exemplo)

### 7.1 Importar CSV grande com tipos corretos e datas

**Uso típico:** arquivos grandes de vendas/logs com colunas categóricas.

```python
import pandas as pd

dtypes = {
    'id': 'int64',
    'cidade': 'category',, bbox_inches='tight')

# Salvar em múltiplos formatos
for fmt in ['png', 'pdf', 'svg']:
    fig.savefig(f'figuras/grafico.{fmt}', dpi=300, bbox_inches='tight')
```

### 7.11 Gráfico de barras empilhadas

**Para que serve:** mostrar composição de categorias ao longo de grupos.

```python
# Dados de exemplo: vendas por produto e região
vendas = pd.DataFrame({
    'regiao': ['Norte', 'Sul', 'Leste', 'Oeste'],
    'produto_A': [20, 35, 30, 25],
    'produto_B': [25, 30, 25, 30],
    'produto_C': [30, 20, 25, 20],
})

vendas.set_index('regiao').plot(kind='bar', stacked=True, figsize=(8, 5))
plt.title('Vendas por Região e Produto')
plt.ylabel('Vendas')
plt.legend(title='Produto')
```

### 7.12 Gráfico de linha com área sombreada (intervalo de confiança)

```python
x = np.linspace(0, 10, 50)
y = np.sin(x)
erro = 0.3

plt.figure(figsize=(10, 4))
plt.plot(x, y, 'b-', label='Valor médio')
plt.fill_between(x, y - erro, y + erro, alpha=0.3, label='Intervalo de confiança')
plt.legend()
plt.title('Linha com intervalo de confiança')
```

### 7.13 Criar DataFrame de resumo estatístico customizado

```python
resumo = df.groupby('categoria').agg(
    contagem=('valor', 'count'),
    soma=('valor', 'sum'),
    media=('valor', 'mean'),
    mediana=('valor', 'median'),
    desvio=('valor', 'std'),
    minimo=('valor', 'min'),
    q25=('valor', lambda x: x.quantile(0.25)),
    q75=('valor', lambda x: x.quantile(0.75)),
    maximo=('valor', 'max'),
).round(2)

print(resumo)
```

### 7.14 Detectar e remover duplicatas

```python
# Ver duplicatas
duplicadas = df.duplicated(subset=['nome', 'cpf'], keep='first')
print(f"Encontradas {duplicadas.sum()} linhas duplicadas")

# Remover duplicatas
df_limpo = df.drop_duplicates(subset=['nome', 'cpf'], keep='first')

# Ver duplicatas completas (todas as colunas)
df_duplicatas_completas = df[df.duplicated(keep=False)]
```

### 7.15 Renomear colunas em lote

```python
# Renomear específicas
df = df.rename(columns={'nome_antigo': 'nome_novo', 'outro': 'novo_nome'})

# Padronizar: minúsculas, sem espaços
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Remover acentos
import unicodedata
def remove_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

df.columns = [remove_acentos(col) for col in df.columns]
```

### 7.16 Filtrar por múltiplas condições com query

```python
# Sintaxe SQL-like (mais legível em filtros complexos)
filtrado = df.query('idade > 25 and salario >= 5000 and cidade in ["SP", "RJ"]')

# Equivalente com operadores
filtrado = df[(df['idade'] > 25) & (df['salario'] >= 5000) & (df['cidade'].isin(['SP', 'RJ']))]
```

### 7.17 Criar bins customizados e contar frequência

```python
# Faixas de idade
bins = [0, 18, 30, 50, 100]
labels = ['Jovem', 'Adulto', 'Meia-idade', 'Idoso']

df['faixa_idade'] = pd.cut(df['idade'], bins=bins, labels=labels)

# Tabela de frequência
freq = df['faixa_idade'].value_counts().sort_index()
print(freq)

# Percentual
perc = (freq / freq.sum() * 100).round(1)
tabela = pd.DataFrame({'frequencia': freq, 'percentual': perc})
```

### 7.18 Transpor DataFrame (linhas ↔ colunas)

```python
df_transposto = df.T

# Pivot manual
pivot = df.pivot(index='data', columns='produto', values='quantidade')
```

### 7.19 Concatenar múltiplos DataFrames

```python
# Empilhar verticalmente (append)
df_total = pd.concat([df1, df2, df3], ignore_index=True)

# Lado a lado (horizontalmente)
df_junto = pd.concat([df1, df2], axis=1)

# Com chave de identificação
df_marcado = pd.concat([df1, df2], keys=['fonte_1', 'fonte_2'])
```

### 7.20 Gráfico de barras horizontais ordenado

```python
# Top 10 cidades por valor
top10 = df.groupby('cidade')['valor'].sum().sort_values(ascending=True).tail(10)

plt.figure(figsize=(8, 6))
plt.barh(top10.index, top10.values, color='teal')
plt.xlabel('Valor Total')
plt.title('Top 10 Cidades por Valor')
plt.tight_layout()
plt.show(
  'produto': 'category',
  'preco': 'float64',
}
parse_dates = ['data_venda']

df = pd.read_csv(
  'vendas.csv',
  dtype=dtypes,
  parse_dates=parse_dates,
  sep=';',          # comum em CSV brasileiro
  decimal=',',      # se decimal vier com vírgula
)
```

### 7.2 Remover outliers simples (IQR)

**Para que serve:** excluir valores muito extremos antes de calcular médias/modelos.

```python
q1 = df['preco'].quantile(0.25)
q3 = df['preco'].quantile(0.75)
iqr = q3 - q1

mask = (df['preco'] >= q1 - 1.5 * iqr) & (df['preco'] <= q3 + 1.5 * iqr)
df_sem_outlier = df[mask]
```

### 7.3 Top N por grupo

**Exemplo:** top 2 produtos mais caros por cidade.

```python
top2 = (
  df
  .sort_values(['cidade', 'preco'], ascending=[True, False])
  .groupby('cidade')
  .head(2)
)
```

### 7.4 Percentual por categoria

**Exemplo:** participação (%) de cada cidade no total de registros.

```python
cont = df['cidade'].value_counts()
perc = (cont / cont.sum() * 100).round(2)

resultado = pd.DataFrame({'qtd': cont, 'perc_%': perc})
```

### 7.5 Unir DataFrames com chaves diferentes

```python
# df1: chave A, df2: chave B
res = df1.merge(df2, left_on='A', right_on='B', how='inner')
```

### 7.6 Converter, ordenar e plotar série temporal mensal

```python
df['data'] = pd.to_datetime(df['data'], dayfirst=True)
ts = df.set_index('data').sort_index()

mensal = ts['valor'].resample('M').sum()
mensal.plot(title='Soma Mensal')
plt.show()
```

### 7.7 Heatmap de tabela dinâmica

```python
pv = pd.pivot_table(
  df,
  index='categoria',
  columns='mes',
  values='valor',
  aggfunc='sum',
  fill_value=0,
)

plt.figure(figsize=(8, 4))
sns.heatmap(pv, cmap='YlGnBu')
plt.show()
```

### 7.8 Pairplot para explorar relações

```python
num_cols = ['idade', 'salario', 'gastos']
sns.pairplot(df[num_cols], corner=True, diag_kind='kde')
plt.show()
```

### 7.9 Adicionar linhas de referência (targets)

```python
ax = sns.boxplot(data=df, x='cidade', y='salario')
ax.axhline(7000, color='red', linestyle='--', label='Meta')
ax.legend()
plt.show()
```

### 7.10 Salvar figuras com alta resolução

```python
fig, ax = plt.subplots(figsize=(6, 4))
sns.scatterplot(data=df, x='idade', y='salario', ax=ax)
fig.tight_layout()
fig.savefig('figuras/dispersao.png', dpi=300)
```

---

## 7) Boas Práticas e Desempenho

### Pandas

- Use tipos eficientes (`category` para colunas com poucos valores distintos).
- Evite `apply` linha a linha; prefira operações vetorizadas quando possível.
- Use filtragem e atribuição com `.loc[mask, 'col'] = ...`.
- Para CSVs grandes, especifique `dtype`, `usecols`, `chunksize`.
- Faça limpeza incremental: padronize colunas → trate nulos → derive colunas.
- Documente decisões (por que removeu outliers, regras de negócio etc.).

Exemplo `chunksize` (processamento em partes):

```python
reader = pd.read_csv('grande.csv', chunksize=100_000)
acum = []

for chunk in reader:
    chunk['total'] = chunk['qtd'] * chunk['preco']
    acum.append(chunk.groupby('categoria')['total'].sum())

res = (
    pd.concat(acum)
    .groupby(level=0)
    .sum()
    .sort_values(ascending=False)
)
```

### PySpark

- **Cache DataFrames** que serão reutilizados: `.cache()` ou `.persist()`
- **Evite collect()** em datasets grandes (traz tudo para memória do driver)
- **Use broadcast** para joins com tabelas pequenas (< 100 MB)
- **Particione adequadamente**: nem muito poucas (não paraleliza), nem muitas (overhead)
- **Prefira SQL nativo** ou funções do PySpark a UDFs Python (mais lentas)
- **Use Parquet**: formato colunar, comprimido, muito mais rápido que CSV
- **Monitore o Spark UI** (porta 4040) para identificar gargalos

---

## 8) Dúvidas Comuns e Erros
- **Separador errado**: ajuste `sep` (ponto e vírgula é comum: `sep=';'`).
- **Decimal com vírgula**: use `decimal=','`.
- **Datas inválidas**: use `errors='coerce'` em `to_datetime` e depois trate `NaT`.
- **Gráficos “vazios”**: confira filtros/joins; verifique `df.shape` após operações.

---10

## 8) Próximos Passos

- Rode o script de exemplo: `Python/Data Analysis/exemplos/eda_basico.py`.
- Crie um notebook e replique as receitas com **seus dados reais**.
- Crie um módulo com suas funções utilitárias (ex.: `utils.py`) para **reaproveitar código**.

---

## 9) Recursos Adicionais e Referências

### Documentação Oficial

- **Pandas**: https://pandas.pydata.org/docs/
- **Matplotlib**: https://matplotlib.org/stable/contents.html
- **Seaborn**: https://seaborn.pydata.org/
- **NumPy**: https://numpy.org/doc/

### Cheat Sheets (Folhas de Cola)

- [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
- [Matplotlib Cheat Sheets](https://matplotlib.org/cheatsheets/)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)

### Datasets de Exemplo para Praticar

```python
import seaborn as sns

# Datasets embutidos no Seaborn
tips = sns.load_dataset('tips')          # Gorjetas em restaurante
iris = sns.load_dataset('iris')          # Flores Iris
flights = sns.load_dataset('flights')    # Passageiros de voos
titanic = sns.load_dataset('titanic')    # Sobreviventes do Titanic
planets = sns.load_dataset('planets')    # Exoplanetas
penguins = sns.load_dataset('penguins')  # Pinguins

# Listar todos disponíveis
print(sns.get_dataset_names())
```

### Galeria de Inspiração

- **Seaborn Gallery**: https://seaborn.pydata.org/examples/index.html
- **Matplotlib Gallery**: https://matplotlib.org/stable/gallery/index.html
- **Python Graph Gallery**: https://python-graph-gallery.com/

### Dicas Finais

1. **Sempre explore os dados primeiro** com `.info()`, `.describe()`, `.head()`.
2. **Visualize antes de modelar**: gráficos revelam padrões e problemas nos dados.
3. **Documente seu código**: use comentários e markdown cells em notebooks.
4. **Salve versões intermediárias**: facilita debug e permite voltar atrás.
5. **Aprenda com exemplos**: copie código que funciona e adapte aos poucos.

---



---

# PARTE IV - ESCALABILIDADE E BIG DATA

## 8) Pensamento Tabular (SQL-like)

**Por que importa:**

Pandas e PySpark usam a **mesma lógica** de manipulação de tabelas que SQL.

Entender essa ponte é essencial para:
- Migrar de SQL para Python.
- Escalar de Pandas para PySpark.
- Pensar em **operações declarativas** (o que você quer) em vez de loops (como fazer).

### Equivalência: SQL ↔ Pandas ↔ PySpark

| Operação | SQL | Pandas | PySpark (conceito) |
|----------|-----|--------|-------------------|
| Selecionar colunas | `SELECT nome, idade` | `df[['nome', 'idade']]` | `df.select('nome', 'idade')` |
| Filtrar linhas | `WHERE idade > 25` | `df[df['idade'] > 25]` | `df.filter(col('idade') > 25)` |
| Ordenar | `ORDER BY salario DESC` | `df.sort_values('salario', ascending=False)` | `df.orderBy(col('salario').desc())` |
| Agrupar | `GROUP BY cidade` | `df.groupby('cidade')` | `df.groupBy('cidade')` |
| Agregação | `COUNT(*), AVG(salario)` | `.agg({'salario': 'mean'})` | `.agg(avg('salario'))` |
| Join | `INNER JOIN ON ...` | `df1.merge(df2, on='id')` | `df1.join(df2, on='id')` |
| Criar coluna | `salario * 0.3 AS bonus` | `df['bonus'] = df['salario'] * 0.3` | `.withColumn('bonus', col('salario') * 0.3)` |
| Limitar | `LIMIT 10` | `df.head(10)` | `df.limit(10)` |
| Distinct | `SELECT DISTINCT cidade` | `df['cidade'].unique()` | `df.select('cidade').distinct()` |

### 1. SELECT → Selecionar Colunas

```python
# SQL: SELECT nome, salario FROM df WHERE cidade = 'SP'

# Pandas
df_sp = df[df['cidade'] == 'SP'][['nome', 'salario']]

# Mais idiomático
df_sp = df.loc[df['cidade'] == 'SP', ['nome', 'salario']]
```

### 2. WHERE → Filtrar Linhas

```python
# SQL: WHERE idade > 25 AND cidade IN ('SP', 'RJ')

# Pandas
filtrado = df[(df['idade'] > 25) & (df['cidade'].isin(['SP', 'RJ']))]

# Ou com query (mais legível)
filtrado = df.query("idade > 25 and cidade in ['SP', 'RJ']")
```

### 3. GROUP BY → Agrupar e Agregar

```python
# SQL:
# SELECT cidade, COUNT(*) as qtd, AVG(salario) as media
# FROM df
# GROUP BY cidade

# Pandas
resumo = df.groupby('cidade').agg(
    qtd=('nome', 'count'),
    media=('salario', 'mean')
).round(2)
```

### 4. ORDER BY → Ordenar

```python
# SQL: ORDER BY salario DESC, idade ASC

# Pandas
ordenado = df.sort_values(['salario', 'idade'], ascending=[False, True])
```

### 5. JOIN → Juntar Tabelas

```python
# SQL:
# SELECT c.nome, p.produto, p.valor
# FROM clientes c
# INNER JOIN pedidos p ON c.id = p.id_cliente

# Pandas
resultado = clientes.merge(
    pedidos,
    left_on='id',
    right_on='id_cliente',
    how='inner'
)
```

### 6. Subqueries → Filtros com Agregação

```python
# SQL: SELECT * FROM df WHERE salario > (SELECT AVG(salario) FROM df)

# Pandas
media_sal = df['salario'].mean()
acima_media = df[df['salario'] > media_sal]

# Ou em uma linha
acima_media = df[df['salario'] > df['salario'].mean()]
```

### 7. CASE WHEN → Criar Colunas Condicionais

```python
# SQL:
# CASE WHEN salario > 8000 THEN 'Alto'
#      WHEN salario > 5000 THEN 'Médio'
#      ELSE 'Baixo' END AS faixa

# Pandas
import numpy as np
df['faixa'] = np.select(
    [df['salario'] > 8000, df['salario'] > 5000],
    ['Alto', 'Médio'],
    default='Baixo'
)
```

### Por que isso importa para PySpark?

PySpark usa **exatamente o mesmo raciocínio**, mas com sintaxe ligeiramente diferente:

```python
# Pandas
df[df['idade'] > 25][['nome', 'salario']]

# PySpark
df.filter(col('idade') > 25).select('nome', 'salario')
```

**A lógica é idêntica:**
1. Filtrar linhas (`filter` = `WHERE`)
2. Selecionar colunas (`select` = `SELECT`)
3. Agrupar e agregar (`groupBy` = `GROUP BY`)

---




## 9) Limitações do Pandas

**Quando Pandas deixa de ser suficiente?**

Pandas é excelente para datasets que **cabem na memória RAM**.
Mas há limites:

### 1. Memória (RAM)

**Problema:**
- Pandas carrega **todo o dataset na RAM**.
- Se o arquivo é maior que a RAM disponível, **não funciona**.

**Regra prática:**
- Arquivo CSV de 1GB → precisa de ~5-8GB de RAM para processar.
- Se seu dataset > 50% da RAM, prepare-se para lentidão.

**Sintomas:**
```python
df = pd.read_csv('dados_gigantes.csv')
# MemoryError: Unable to allocate array
```

**Soluções:**
- **Chunking**: processar em pedaços
  ```python
  for chunk in pd.read_csv('grande.csv', chunksize=100000):
      processar(chunk)
  ```
- **Otimizar tipos**: usar `category` para strings repetidas
  ```python
  df['cidade'] = df['cidade'].astype('category')  # economiza 80%+
  ```
- **PySpark**: processamento distribuído

### 2. Performance (Velocidade)

**Problema:**
- Pandas é **single-threaded** (usa 1 núcleo de CPU).
- Operações complexas ficam lentas em datasets médios/grandes.

**Exemplo lento:**
```python
# Evite apply com funções Python (lento)
df['bonus'] = df['salario'].apply(lambda x: x * 0.3 if x > 8000 else 0)

# Prefira operações vetorizadas (100x mais rápido)
df['bonus'] = np.where(df['salario'] > 8000, df['salario'] * 0.3, 0)
```

**Quando vira problema:**
- Datasets > 10GB
- Agregações em > 100 milhões de linhas
- Joins complexos entre tabelas grandes

### 3. Escala (Crescimento)

**Problema:**
- Pandas não é feito para **crescer horizontalmente** (adicionar mais máquinas).
- Se o dado não cabe em 1 máquina, Pandas não resolve.

**Quando usar PySpark:**
- Datasets > 20GB
- Dados distribuídos em clusters (HDFS, S3)
- Necessidade de processar terabytes
- Pipelines de produção com alto volume

### 4. Lazy Evaluation (Pandas é Eager)

**Pandas executa imediatamente:**
```python
df_filtrado = df[df['idade'] > 25]  # executa agora
df_selecionado = df_filtrado[['nome', 'salario']]  # executa agora
```

**Problema:**
- Processa dados intermediários desnecessariamente.
- Não otimiza a sequência de operações.

**PySpark é lazy:**
```python
df_spark = df.filter(col('idade') > 25).select('nome', 'salario')
# Nada executou ainda! Apenas criou um "plano"

df_spark.show()  # Só aqui executa, de forma otimizada
```

**Benefício do lazy:**
- Spark analisa **todas as operações** antes de executar.
- Elimina passos redundantes.
- Paraleliza automaticamente.

### Comparação Resumida

| Aspecto | Pandas | PySpark |
|---------|--------|---------|
| Tamanho ideal | < 10GB | > 20GB, até petabytes |
| Memória | Tudo na RAM | Distribuído em cluster |
| Processamento | 1 núcleo (single-thread) | Centenas de núcleos paralelos |
| Execução | Eager (imediata) | Lazy (otimizada) |
| Facilidade | Muito fácil | Curva de aprendizado |
| Onde roda | Notebook local | Cluster (Databricks, EMR, GCP) |

### Quando migrar?

**Continue com Pandas se:**
- Dataset < 5GB
- Análise exploratória rápida
- Ambiente local
- Prototipagem

**Migre para PySpark se:**
- Dataset > 20GB ou crescendo rápido
- Produção com alto volume
- Infraestrutura de cluster disponível
- Performance crítica

---




## 10) Transição para Big Data (Pandas → PySpark)

**Por que Spark existe?**

Spark foi criado para resolver o problema que Pandas não resolve:
**Processar dados maiores que a memória de uma máquina.**

### O que muda?

| Aspecto | Pandas | PySpark |
|---------|--------|---------|
| **Estrutura de dados** | `pandas.DataFrame` | `pyspark.sql.DataFrame` |
| **Execução** | Imediata (eager) | Preguiçosa (lazy) |
| **API** | Métodos em DataFrame | SQL ou métodos em DataFrame |
| **Modificação** | Mutable (altera no local) | Immutable (cria novo DF) |
| **Índice** | Tem índice explícito | Sem índice (ordem não garantida) |

### O que NÃO muda?

**A lógica de pensamento é idêntica:**

1. **Selecionar** colunas
2. **Filtrar** linhas
3. **Agrupar** e agregar
4. **Juntar** tabelas
5. **Criar** colunas derivadas

**Apenas a sintaxe é ligeiramente diferente.**

### Exemplos Lado a Lado

#### 1. Carregar dados

```python
# Pandas
import pandas as pd
df = pd.read_csv('dados.csv')

# PySpark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('app').getOrCreate()
df = spark.read.csv('dados.csv', header=True, inferSchema=True)
```

#### 2. Ver primeiras linhas

```python
# Pandas
df.head()

# PySpark
df.show(5)
df.limit(5).toPandas()  # converte para Pandas se quiser
```

#### 3. Filtrar e selecionar

```python
# Pandas
df_sp = df[df['cidade'] == 'SP'][['nome', 'salario']]

# PySpark
from pyspark.sql.functions import col
df_sp = df.filter(col('cidade') == 'SP').select('nome', 'salario')
```

#### 4. Agrupar e agregar

```python
# Pandas
resumo = df.groupby('cidade')['salario'].mean()

# PySpark
from pyspark.sql.functions import avg
resumo = df.groupBy('cidade').agg(avg('salario').alias('media_salario'))
```

#### 5. Criar coluna derivada

```python
# Pandas
df['salario_k'] = df['salario'] / 1000

# PySpark
df = df.withColumn('salario_k', col('salario') / 1000)
```

#### 6. Juntar tabelas

```python
# Pandas
resultado = clientes.merge(pedidos, on='id', how='inner')

# PySpark
resultado = clientes.join(pedidos, on='id', how='inner')
```

### Conceitos Novos em PySpark

#### 1. Lazy Evaluation

**Spark não executa até você pedir explicitamente:**

```python
df_filtrado = df.filter(col('idade') > 25)  # Não executou!
df_resultado = df_filtrado.select('nome')    # Ainda não executou!

# Só aqui executa:
df_resultado.show()
df_resultado.collect()
df_resultado.write.csv('saida.csv')
```

**Por quê?**
- Spark cria um **plano de execução otimizado**.
- Elimina etapas redundantes.
- Paraleliza automaticamente.

#### 2. Transformações vs Ações

**Transformações (lazy):**
- Criam novo DataFrame, não executam.
- Exemplos: `select`, `filter`, `groupBy`, `withColumn`, `join`

**Ações (executam tudo):**
- Disparam a execução do plano.
- Exemplos: `show`, `collect`, `count`, `write`, `take`

#### 3. Imutabilidade

```python
# Pandas (muta o DataFrame original)
df['nova_col'] = df['col1'] * 2

# PySpark (cria novo DataFrame)
df_novo = df.withColumn('nova_col', col('col1') * 2)
# df original não mudou!
```

#### 4. Sem índice

```python
# Pandas
df.loc[0]  # linha com índice 0
df.iloc[0]  # primeira linha

# PySpark
# Não tem loc/iloc!
# Use filter ou limit
df.limit(1).show()
```

### Como começar com PySpark?

**1. Instalar:**
```bash
pip install pyspark
```

**2. Setup básico:**
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName('MinhaAnalise') \
    .config('spark.driver.memory', '4g') \
    .getOrCreate()

# Carregar
df = spark.read.csv('dados.csv', header=True, inferSchema=True)

# Ver estrutura
df.printSchema()
df.show(5)

# Trabalhar
resultado = df.filter(col('idade') > 25) \
              .groupBy('cidade') \
              .agg(avg('salario').alias('media')) \
              .orderBy(col('media').desc())

resultado.show()

# Salvar
resultado.write.csv('resultado.csv', header=True, mode='overwrite')
```

### Quando estudar Spark?

**Depois de dominar:**
- Pandas (filtros, groupby, joins)
- SQL (lógica tabular)
- Conceito de distribuição

**Você está pronto quando:**
- Consegue resolver problemas em Pandas fluentemente.
- Entende por que Pandas não escala.
- Tem acesso a cluster (Databricks, AWS EMR, etc.) ou quer simular localmente.

---

# PARTE II - MANIPULAÇÃO DE DADOS



## 11) PySpark para Big Data para Big Data

### 11.1 Quando usar PySpark?

**Use PySpark quando:**
- Seus dados **não cabem na memória** (> 10-20 GB).
- Precisa **processar grandes volumes** de dados (centenas de GB, TB, PB).
- Quer **processamento distribuído** em cluster (múltiplas máquinas).
- Trabalha com **dados em formato parquet, delta, ou data lakes**.
- Tem acesso a **cluster Spark** (Databricks, AWS EMR, Azure HDInsight).

**NÃO use PySpark quando:**
- Dados cabem confortavelmente em memória (< 5 GB) → use Pandas.
- Processamento é simples e rápido → Pandas é mais simples e direto.
- Não tem cluster disponível e dados são pequenos → overhead não compensa.
- Precisa de análises exploratórias rápidas → Pandas + Jupyter é mais ágil.

**Comparação rápida:**

| Critério | Pandas | PySpark |
|----------|--------|---------|
| Tamanho ideal | < 5-10 GB | > 10 GB até PB |
| Execução | Single machine | Distribuída (cluster) |
| Velocidade (dados pequenos) | Muito rápida | Overhead de distribuição |
| Velocidade (dados grandes) | Lenta/impossível | Muito rápida |
| Curva de aprendizado | Fácil | Moderada |
| Integração com visualização | Direta | Via conversão para Pandas |

### 11.2 Instalação e Configuração

```bash
# Instalação básica
pip install pyspark

# Com suporte a Delta Lake (recomendado)
pip install pyspark delta-spark

# Opcional: instalar Java (Spark precisa de JVM)
# Ubuntu/Debian: sudo apt install default-jdk
# Mac: brew install openjdk@11
```

**Configuração básica em Python:**

```python
from pyspark.sql import SparkSession

# Criar sessão Spark (ponto de entrada)
spark = SparkSession.builder \
    .appName("Analise de Dados") \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "4g") \
    .getOrCreate()

# Ver configuração
print(spark.sparkContext.getConf().getAll())

# Parar sessão quando terminar
# spark.stop()
```

### 11.3 Conceitos Fundamentais

- **SparkSession**: ponto de entrada para todas as funcionalidades do Spark.
- **DataFrame (Spark)**: tabela distribuída, similar ao Pandas mas processada em paralelo.
- **RDD (Resilient Distributed Dataset)**: estrutura de dados de baixo nível (raramente usada diretamente).
- **Transformações**: operações lazy (não executam imediatamente): `select`, `filter`, `groupBy`.
- **Ações**: operações que disparam execução: `show()`, `count()`, `collect()`.
- **Partições**: divisões dos dados para processamento paralelo.

### 11.4 Criar e Inspecionar DataFrames

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("exemplo").getOrCreate()

# 1. Criar DataFrame a partir de lista
data = [
    ("Ana", 23, "SP", 5000),
    ("Bruno", 31, "RJ", 7200),
    ("Carla", 29, "SP", 6100),
    ("Daniel", 40, "BH", 9800),
]
colunas = ["nome", "idade", "cidade", "salario"]

df = spark.createDataFrame(data, colunas)

# 2. Ver estrutura
df.printSchema()  # tipos de dados
df.show()         # primeiras 20 linhas
df.show(5)        # 5 linhas
df.show(5, truncate=False)  # sem truncar strings

# 3. Estatísticas básicas
df.describe().show()
df.count()        # número de linhas
df.columns        # lista de colunas

# 4. Primeiras linhas como lista de Row
df.head(3)
df.take(5)        # similar ao head

# 5. Ver amostra
df.sample(fraction=0.1).show()  # 10% dos dados
```

### 11.5 Ler e Escrever Dados

```python
# CSV
df_csv = spark.read.csv(
    'dados.csv',
    header=True,           # primeira linha é cabeçalho
    inferSchema=True,      # inferir tipos automaticamente
    sep=',',
    encoding='UTF-8'
)

# Salvar CSV
df.write.csv('saida_csv', mode='overwrite', header=True)

# Parquet (formato colunar, muito eficiente)
df_parquet = spark.read.parquet('dados.parquet')
df.write.parquet('saida.parquet', mode='overwrite')

# JSON
df_json = spark.read.json('dados.json')
df.write.json('saida.json', mode='overwrite')

# Modos de escrita: 'overwrite', 'append', 'ignore', 'error'

# Delta Lake (versionamento, ACID, upserts)
df.write.format("delta").mode("overwrite").save("delta_table")
df_delta = spark.read.format("delta").load("delta_table")
```

### 11.6 Seleção, Filtro e Ordenação

```python
from pyspark.sql.functions import col

# Selecionar colunas
df.select("nome", "salario").show()
df.select(col("nome"), col("salario")).show()

# Filtrar linhas
df.filter(col("cidade") == "SP").show()
df.filter(df["salario"] > 7000).show()

# Múltiplas condições
df.filter((col("cidade") == "SP") & (col("salario") > 6000)).show()
df.filter((col("idade") > 25) | (col("cidade") == "RJ")).show()

# WHERE (equivalente a filter)
df.where(col("salario") > 7000).show()

# Ordenar
df.orderBy("salario", ascending=False).show()
df.orderBy(col("salario").desc()).show()
df.orderBy(["cidade", "salario"], ascending=[True, False]).show()

# Distinct
df.select("cidade").distinct().show()

# Limitar linhas
df.limit(10).show()
```

### 11.7 Criar e Transformar Colunas

```python
from pyspark.sql.functions import col, lit, when, concat, upper, lower, length

# Adicionar coluna nova
df_novo = df.withColumn("salario_k", col("salario") / 1000)
df_novo = df.withColumn("bonus", col("salario") * 0.1)

# Condicional (if-then-else)
df_faixa = df.withColumn(
    "faixa_salarial",
    when(col("salario") > 8000, "alta")
    .when(col("salario") > 6000, "media")
    .otherwise("baixa")
)

# Operações com strings
df_str = df.withColumn("nome_upper", upper(col("nome")))
df_str = df.withColumn("nome_lower", lower(col("nome")))
df_str = df.withColumn("tam_nome", length(col("nome")))
df_str = df.withColumn("nome_cidade", concat(col("nome"), lit(" - "), col("cidade")))

# Renomear coluna
df_renomeado = df.withColumnRenamed("nome", "nome_completo")

# Remover coluna
df_sem_col = df.drop("salario")

# Cast (conversão de tipo)
df_cast = df.withColumn("idade_str", col("idade").cast("string"))
```

### 11.8 Agregações e GroupBy

```python
from pyspark.sql.functions import count, sum, avg, max, min, stddev, mean

# Agregação simples
df.agg({"salario": "mean"}).show()
df.agg(avg("salario")).show()

# GroupBy
por_cidade = df.groupBy("cidade").agg(
    count("nome").alias("qtd_pessoas"),
    avg("salario").alias("media_salarial"),
    max("salario").alias("salario_max"),
    min("salario").alias("salario_min"),
    stddev("salario").alias("desvio_padrao")
)
por_cidade.show()

# Múltiplas agregações
df.groupBy("cidade").agg(
    count("*").alias("total"),
    sum("salario").alias("soma_salarios")
).show()

# Filtrar após agregação (HAVING)
por_cidade.filter(col("media_salarial") > 6000).show()
```

### 11.9 Joins (Junções)

```python
# Criar segundo DataFrame
clientes = spark.createDataFrame([
    (1, "Ana", "ana@email.com"),
    (2, "Bruno", "bruno@email.com"),
    (3, "Carla", "carla@email.com")
], ["id", "nome", "email"])

compras = spark.createDataFrame([
    (1, 100, "2024-01-15"),
    (1, 200, "2024-02-20"),
    (2, 150, "2024-01-18"),
    (4, 80, "2024-03-10")
], ["id_cliente", "valor", "data"])

# Inner join
inner = clientes.join(compras, clientes.id == compras.id_cliente, "inner")
inner.show()

# Left join (mantém todos os clientes)
left = clientes.join(compras, clientes.id == compras.id_cliente, "left")
left.show()

# Right join
right = clientes.join(compras, clientes.id == compras.id_cliente, "right")

# Full outer join
full = clientes.join(compras, clientes.id == compras.id_cliente, "outer")

# Left anti join (clientes sem compras)
sem_compras = clientes.join(compras, clientes.id == compras.id_cliente, "left_anti")
```

### 11.10 Datas e Séries Temporais

```python
from pyspark.sql.functions import (
    to_date, to_timestamp, year, month, dayofmonth, 
    dayofweek, hour, minute, current_date, date_add, datediff
)

# Converter string para data
df_datas = df.withColumn("data", to_date(col("data_str"), "yyyy-MM-dd"))

# Extrair componentes
df_datas = df_datas.withColumn("ano", year(col("data")))
df_datas = df_datas.withColumn("mes", month(col("data")))
df_datas = df_datas.withColumn("dia", dayofmonth(col("data")))
df_datas = df_datas.withColumn("dia_semana", dayofweek(col("data")))

# Data atual
df_hoje = df.withColumn("hoje", current_date())

# Diferença entre datas (em dias)
df_diff = df.withColumn("dias_diff", datediff(col("data_fim"), col("data_inicio")))

# Adicionar dias
df_futuro = df.withColumn("data_futura", date_add(col("data"), 30))

# Window functions para séries temporais
from pyspark.sql.window import Window
from pyspark.sql.functions import lag, lead, row_number

windowSpec = Window.orderBy("data")
df_window = df.withColumn("valor_anterior", lag("valor", 1).over(windowSpec))
df_window = df.withColumn("valor_proximo", lead("valor", 1).over(windowSpec))
```

### 11.11 Window Functions (Funções de Janela)

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, dense_rank, lag, lead, sum as spark_sum

# Ranking por grupo
windowSpec = Window.partitionBy("cidade").orderBy(col("salario").desc())

df_rank = df.withColumn("ranking", rank().over(windowSpec))
df_rank = df_rank.withColumn("row_num", row_number().over(windowSpec))
df_rank.show()

# Top 2 por cidade
top2 = df_rank.filter(col("row_num") <= 2)

# Soma acumulada
windowSpec_acum = Window.orderBy("data").rowsBetween(Window.unboundedPreceding, 0)
df_acum = df.withColumn("soma_acumulada", spark_sum("valor").over(windowSpec_acum))

# Média móvel (últimas 3 linhas)
windowSpec_movel = Window.orderBy("data").rowsBetween(-2, 0)
from pyspark.sql.functions import avg as spark_avg
df_movel = df.withColumn("media_movel_3", spark_avg("valor").over(windowSpec_movel))
```

### 11.12 SQL Queries (Consultas SQL)

```python
# Registrar DataFrame como tabela temporária
df.createOrReplaceTempView("pessoas")

# Executar SQL
resultado = spark.sql("""
    SELECT 
        cidade,
        COUNT(*) as qtd,
        AVG(salario) as media_sal,
        MAX(salario) as max_sal
    FROM pessoas
    WHERE idade > 25
    GROUP BY cidade
    HAVING AVG(salario) > 6000
    ORDER BY media_sal DESC
""")

resultado.show()

# SQL complexo com joins
clientes.createOrReplaceTempView("clientes")
compras.createOrReplaceTempView("compras")

spark.sql("""
    SELECT 
        c.nome,
        COUNT(cp.id_cliente) as total_compras,
        SUM(cp.valor) as total_gasto
    FROM clientes c
    LEFT JOIN compras cp ON c.id = cp.id_cliente
    GROUP BY c.nome
    ORDER BY total_gasto DESC
""").show()
```

### 11.13 Integração com Pandas

```python
# Converter Spark DataFrame para Pandas
pandas_df = df.toPandas()

# Converter Pandas para Spark
spark_df = spark.createDataFrame(pandas_df)

# Usar Pandas UDF (User Defined Function) para processamento vetorizado
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf("double")
def calcular_bonus(salario: pd.Series) -> pd.Series:
    return salario * 0.15

df_bonus = df.withColumn("bonus", calcular_bonus(col("salario")))
df_bonus.show()
```

### 11.14 Performance e Otimização

```python
# 1. Cache (manter na memória para reutilizar)
df_cache = df.cache()
df_cache.count()  # primeira execução: carrega cache
df_cache.count()  # segunda execução: usa cache (rápido)

# Remover cache quando não precisar mais
df_cache.unpersist()

# 2. Persist (mais controle que cache)
from pyspark import StorageLevel
df.persist(StorageLevel.MEMORY_AND_DISK)

# 3. Repartição (redistribuir dados entre partições)
df_repartitioned = df.repartition(10)  # 10 partições
df_repartitioned = df.repartition("cidade")  # particionar por coluna

# 4. Coalesce (reduzir partições sem shuffle completo)
df_coalesced = df.coalesce(5)

# 5. Ver plano de execução
df.explain()           # plano físico
df.explain(True)       # plano completo (lógico + físico)

# 6. Broadcast join (para tabelas pequenas)
from pyspark.sql.functions import broadcast
df_joined = df_grande.join(broadcast(df_pequeno), "chave")

# 7. Ver número de partições
df.rdd.getNumPartitions()
```

### 11.15 Tratamento de Valores Nulos

```python
from pyspark.sql.functions import isnan, isnull, when, coalesce

# Detectar nulos
df.filter(col("salario").isNull()).show()
df.filter(col("salario").isNotNull()).show()

# Preencher nulos
df_filled = df.fillna({"salario": 0, "cidade": "Desconhecida"})
df_filled = df.fillna(0)  # preencher todas colunas numéricas

# Remover linhas com nulos
df_sem_nulos = df.dropna()              # remove se qualquer coluna tiver null
df_sem_nulos = df.dropna(subset=["salario"])  # apenas se salário for null
df_sem_nulos = df.dropna(how='all')     # remove se TODAS colunas forem null

# Substituir usando coalesce (primeira não-nula)
df_coalesced = df.withColumn(
    "salario_final",
    coalesce(col("salario"), col("salario_estimado"), lit(0))
)
```

### 11.16 UDFs (User Defined Functions)

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, IntegerType

# Definir função Python
def categorizar_idade(idade):
    if idade < 25:
        return "Jovem"
    elif idade < 40:
        return "Adulto"
    else:
        return "Senior"

# Registrar como UDF
categorizar_udf = udf(categorizar_idade, StringType())

# Usar UDF
df_categorizado = df.withColumn("categoria_idade", categorizar_udf(col("idade")))
df_categorizado.show()

# UDF com múltiplos parâmetros
def calcular_bonus(salario, anos_empresa):
    return salario * (0.05 + anos_empresa * 0.01)

calcular_bonus_udf = udf(calcular_bonus, IntegerType())
df_bonus = df.withColumn("bonus", calcular_bonus_udf(col("salario"), col("anos")))
```

### 11.17 Exemplo Completo: Pipeline de ETL

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, avg, count, to_date, year

# 1. Inicializar Spark
spark = SparkSession.builder \
    .appName("ETL_Vendas") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

# 2. Ler dados brutos
vendas = spark.read.csv("vendas_2024.csv", header=True, inferSchema=True)

# 3. Limpeza: remover nulos críticos
vendas_limpo = vendas.dropna(subset=["id_venda", "valor", "data"])

# 4. Transformação: adicionar colunas derivadas
vendas_prep = vendas_limpo \
    .withColumn("data", to_date(col("data"), "yyyy-MM-dd")) \
    .withColumn("ano", year(col("data"))) \
    .withColumn(
        "faixa_valor",
        when(col("valor") > 1000, "alta")
        .when(col("valor") > 500, "media")
        .otherwise("baixa")
    )

# 5. Agregação: estatísticas por produto e ano
relatorio = vendas_prep.groupBy("produto", "ano").agg(
    count("id_venda").alias("qtd_vendas"),
    avg("valor").alias("ticket_medio"),
    sum("valor").alias("receita_total")
).orderBy(["ano", "receita_total"], ascending=[True, False])

# 6. Filtrar: apenas produtos com mais de 100 vendas
relatorio_filtrado = relatorio.filter(col("qtd_vendas") > 100)

# 7. Salvar resultado
relatorio_filtrado.write.parquet(
    "saida/relatorio_vendas_2024.parquet",
    mode="overwrite"
)

# 8. Mostrar amostra
relatorio_filtrado.show(20, truncate=False)

# 9. Estatísticas
print(f"Total de linhas processadas: {vendas_prep.count()}")
print(f"Total de linhas no relatório: {relatorio_filtrado.count()}")

# 10. Parar Spark
spark.stop()
```

### 11.18 Diferenças Principais: Pandas vs PySpark

| Aspecto | Pandas | PySpark |
|---------|--------|---------|
| **Execução** | Em memória, single-thread | Distribuído, paralelo |
| **Tamanho de dados** | < 10 GB | GB, TB, PB |
| **Lazy evaluation** | Não (executa imediatamente) | Sim (monta plano, executa no final) |
| **Sintaxe** | `df['coluna']` | `col('coluna')` ou `df.coluna` |
| **Mutabilidade** | Mutável (altera in-place) | Imutável (retorna novo DF) |
| **Indexação** | `.loc`, `.iloc` | `filter`, `select` |
| **Conversão** | `spark_df.toPandas()` | `spark.createDataFrame(pandas_df)` |

### 11.19 Quando Migrar de Pandas para PySpark?

**Sinais de que você precisa de PySpark:**

1. **Tempo de processamento > 10 minutos** com Pandas.
2. **MemoryError**: dados não cabem na RAM.
3. **Processamento em cluster** disponível (AWS EMR, Databricks, on-premise).
4. **Dados crescem rapidamente** e Pandas não escala.
5. **Integração com data lakes** (S3, HDFS, Delta Lake).

**Estratégia de migração:**

```python
# 1. Prototipe com Pandas em amostra pequena
import pandas as pd
amostra = pd.read_csv("vendas.csv", nrows=10000)
# ... desenvolve lógica ...

# 2. Converta para PySpark quando validado
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("producao").getOrCreate()
df_completo = spark.read.csv("vendas.csv", header=True, inferSchema=True)
# ... adapta lógica para PySpark ...

# 3. Teste com dados completos
# 4. Otimize (cache, partições, broadcast)
```

### 11.20 Recursos PySpark

**Documentação:**
- Documentação oficial: https://spark.apache.org/docs/latest/api/python/
- Guia de SQL: https://spark.apache.org/docs/latest/sql-programming-guide.html

**Tutoriais:**
- Databricks Academy (gratuito): https://www.databricks.com/learn
- Apache Spark Examples: https://github.com/apache/spark/tree/master/examples

**Ferramentas:**
- Databricks Community Edition (gratuito)
- AWS EMR, Google Dataproc, Azure HDInsight
- Jupyter com PySpark kernel

---

### 11.21 Exemplo Completo: Análise de E-commerce com PySpark

Este exemplo mostra um **pipeline completo de análise** de dados de um e-commerce, desde a leitura até insights finais.

**Contexto:**
- Empresa tem 50 milhões de transações (15 GB de dados)
- 3 tabelas: clientes, produtos, transações
- Objetivo: análise de vendas, comportamento de cliente, produtos top

#### 6.21.1 Setup e Criação de Dados de Exemplo

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
from pyspark.sql.types import *
import random
from datetime import datetime, timedelta

# Configurar Spark com mais memória
spark = SparkSession.builder \
    .appName("Analise_Ecommerce") \
    .config("spark.driver.memory", "8g") \
    .config("spark.executor.memory", "8g") \
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()

print(f"Spark versão: {spark.version}")
print(f"Configurações ativas:")

# Criar dados de exemplo (simulando big data)
# Em produção, você leria de S3, HDFS, ou Delta Lake

# 1. TABELA DE CLIENTES (500 mil clientes)
print("\n=== Gerando dados de clientes ===")

clientes_data = []
estados = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'PE', 'CE', 'DF']
categorias = ['Bronze', 'Prata', 'Ouro', 'Platina']

for i in range(1, 500001):
    clientes_data.append((
        i,
        f"Cliente_{i}",
        random.choice(estados),
        random.choice(categorias),
        datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1460))
    ))

clientes = spark.createDataFrame(
    clientes_data,
    ["id_cliente", "nome", "estado", "categoria", "data_cadastro"]
)

# 2. TABELA DE PRODUTOS (10 mil produtos)
print("=== Gerando dados de produtos ===")

produtos_data = []
categorias_prod = ['Eletrônicos', 'Roupas', 'Casa', 'Esportes', 'Livros', 'Beleza', 'Alimentos']
marcas = ['Marca_A', 'Marca_B', 'Marca_C', 'Marca_D', 'Marca_E']

for i in range(1, 10001):
    produtos_data.append((
        i,
        f"Produto_{i}",
        random.choice(categorias_prod),
        random.choice(marcas),
        round(random.uniform(10, 5000), 2)
    ))

produtos = spark.createDataFrame(
    produtos_data,
    ["id_produto", "nome_produto", "categoria_produto", "marca", "preco"]
)

# 3. TABELA DE TRANSAÇÕES (5 milhões de transações)
print("=== Gerando dados de transações (pode demorar um pouco) ===")

# Gerar em lotes para não travar a memória
num_transacoes = 5000000
batch_size = 100000
transacoes_list = []

for batch in range(0, num_transacoes, batch_size):
    batch_data = []
    for i in range(batch, min(batch + batch_size, num_transacoes)):
        batch_data.append((
            i + 1,
            random.randint(1, 500000),  # id_cliente
            random.randint(1, 10000),   # id_produto
            random.randint(1, 5),       # quantidade
            datetime(2023, 1, 1) + timedelta(days=random.randint(0, 364)),
            random.choice(['Aprovada', 'Aprovada', 'Aprovada', 'Aprovada', 'Cancelada'])
        ))
    
    transacoes_batch = spark.createDataFrame(
        batch_data,
        ["id_transacao", "id_cliente", "id_produto", "quantidade", "data_transacao", "status"]
    )
    transacoes_list.append(transacoes_batch)

# Unir todos os batches
transacoes = transacoes_list[0]
for batch in transacoes_list[1:]:
    transacoes = transacoes.union(batch)

print(f"\n=== Dados gerados com sucesso ===")
print(f"Clientes: {clientes.count():,}")
print(f"Produtos: {produtos.count():,}")
print(f"Transações: {transacoes.count():,}")
```

#### 6.21.2 Análise Exploratória

```python
print("\n" + "="*80)
print("ANÁLISE EXPLORATÓRIA DE DADOS")
print("="*80)

# 1. VERIFICAR ESTRUTURA DOS DADOS
print("\n--- Estrutura: Clientes ---")
clientes.printSchema()
clientes.show(5, truncate=False)

print("\n--- Estrutura: Produtos ---")
produtos.printSchema()
produtos.show(5, truncate=False)

print("\n--- Estrutura: Transações ---")
transacoes.printSchema()
transacoes.show(5, truncate=False)

# 2. ESTATÍSTICAS BÁSICAS
print("\n--- Estatísticas de Produtos ---")
produtos.select("preco").summary().show()

print("\n--- Distribuição de Status ---")
transacoes.groupBy("status").count().orderBy(desc("count")).show()

print("\n--- Distribuição por Estado ---")
clientes.groupBy("estado").count().orderBy(desc("count")).show()
```

#### 6.21.3 Preparação e Limpeza

```python
print("\n" + "="*80)
print("LIMPEZA E PREPARAÇÃO DE DADOS")
print("="*80)

# 1. Filtrar apenas transações aprovadas
transacoes_aprovadas = transacoes.filter(col("status") == "Aprovada")

print(f"Transações aprovadas: {transacoes_aprovadas.count():,}")
print(f"Taxa de aprovação: {transacoes_aprovadas.count() / transacoes.count() * 100:.2f}%")

# 2. JOIN: Enriquecer transações com dados de produtos e clientes
vendas = transacoes_aprovadas \
    .join(produtos, "id_produto") \
    .join(clientes, "id_cliente") \
    .select(
        "id_transacao",
        "id_cliente",
        "nome",
        "estado",
        "categoria",
        "id_produto",
        "nome_produto",
        "categoria_produto",
        "marca",
        "preco",
        "quantidade",
        "data_transacao"
    )

# Cache porque vamos reutilizar muito
vendas.cache()

print(f"\nDataFrame vendas criado: {vendas.count():,} registros")
vendas.show(5, truncate=False)

# 3. Adicionar colunas derivadas
vendas_enriquecidas = vendas \
    .withColumn("valor_total", col("preco") * col("quantidade")) \
    .withColumn("ano", year("data_transacao")) \
    .withColumn("mes", month("data_transacao")) \
    .withColumn("trimestre", quarter("data_transacao")) \
    .withColumn("dia_semana", dayofweek("data_transacao")) \
    .withColumn(
        "faixa_valor",
        when(col("valor_total") > 1000, "Alto")
        .when(col("valor_total") > 500, "Médio")
        .otherwise("Baixo")
    )

vendas_enriquecidas.cache()
print("\nColunas derivadas adicionadas")
vendas_enriquecidas.select("id_transacao", "valor_total", "ano", "mes", "faixa_valor").show(10)
```

#### 6.21.4 Análises de Negócio

```python
print("\n" + "="*80)
print("ANÁLISES DE NEGÓCIO")
print("="*80)

# ANÁLISE 1: Receita total por mês
print("\n--- 1. RECEITA POR MÊS (2023) ---")
receita_mensal = vendas_enriquecidas \
    .groupBy("ano", "mes") \
    .agg(
        sum("valor_total").alias("receita_total"),
        count("id_transacao").alias("num_vendas"),
        avg("valor_total").alias("ticket_medio")
    ) \
    .orderBy("ano", "mes")

receita_mensal.show(12)

# ANÁLISE 2: Top 20 produtos mais vendidos
print("\n--- 2. TOP 20 PRODUTOS MAIS VENDIDOS ---")
top_produtos = vendas_enriquecidas \
    .groupBy("id_produto", "nome_produto", "categoria_produto", "marca") \
    .agg(
        sum("quantidade").alias("qtd_vendida"),
        sum("valor_total").alias("receita"),
        count("id_transacao").alias("num_transacoes")
    ) \
    .orderBy(desc("receita"))

top_produtos.show(20, truncate=False)

# ANÁLISE 3: Receita por categoria de produto
print("\n--- 3. RECEITA POR CATEGORIA DE PRODUTO ---")
receita_categoria = vendas_enriquecidas \
    .groupBy("categoria_produto") \
    .agg(
        sum("valor_total").alias("receita_total"),
        count("id_transacao").alias("num_vendas"),
        avg("valor_total").alias("ticket_medio")
    ) \
    .withColumn("percentual", 
                round(col("receita_total") / sum("receita_total").over(Window.partitionBy()) * 100, 2)
    ) \
    .orderBy(desc("receita_total"))

receita_categoria.show()

# ANÁLISE 4: Receita por estado
print("\n--- 4. RECEITA POR ESTADO ---")
receita_estado = vendas_enriquecidas \
    .groupBy("estado") \
    .agg(
        sum("valor_total").alias("receita_total"),
        count("id_transacao").alias("num_vendas"),
        countDistinct("id_cliente").alias("clientes_unicos")
    ) \
    .orderBy(desc("receita_total"))

receita_estado.show()

# ANÁLISE 5: Segmentação de clientes (RFM simplificado)
print("\n--- 5. SEGMENTAÇÃO DE CLIENTES (TOP 20) ---")

# Data de referência (última compra do dataset)
data_ref = vendas_enriquecidas.agg(max("data_transacao")).collect()[0][0]

segmentacao_clientes = vendas_enriquecidas \
    .groupBy("id_cliente", "nome", "estado", "categoria") \
    .agg(
        count("id_transacao").alias("frequencia"),
        sum("valor_total").alias("valor_total_gasto"),
        avg("valor_total").alias("ticket_medio"),
        max("data_transacao").alias("ultima_compra")
    ) \
    .withColumn("dias_desde_ultima", datediff(lit(data_ref), col("ultima_compra"))) \
    .orderBy(desc("valor_total_gasto"))

segmentacao_clientes.show(20, truncate=False)

# ANÁLISE 6: Produtos mais vendidos por estado
print("\n--- 6. PRODUTO MAIS VENDIDO POR ESTADO ---")

windowSpec = Window.partitionBy("estado").orderBy(desc("receita_estado_produto"))

produto_por_estado = vendas_enriquecidas \
    .groupBy("estado", "nome_produto", "categoria_produto") \
    .agg(sum("valor_total").alias("receita_estado_produto")) \
    .withColumn("rank", row_number().over(windowSpec)) \
    .filter(col("rank") == 1) \
    .select("estado", "nome_produto", "categoria_produto", "receita_estado_produto") \
    .orderBy("estado")

produto_por_estado.show(10, truncate=False)

# ANÁLISE 7: Tendência de vendas (dia da semana)
print("\n--- 7. VENDAS POR DIA DA SEMANA ---")
vendas_dia_semana = vendas_enriquecidas \
    .groupBy("dia_semana") \
    .agg(
        sum("valor_total").alias("receita"),
        count("id_transacao").alias("num_vendas")
    ) \
    .withColumn("dia_nome",
        when(col("dia_semana") == 1, "Domingo")
        .when(col("dia_semana") == 2, "Segunda")
        .when(col("dia_semana") == 3, "Terça")
        .when(col("dia_semana") == 4, "Quarta")
        .when(col("dia_semana") == 5, "Quinta")
        .when(col("dia_semana") == 6, "Sexta")
        .otherwise("Sábado")
    ) \
    .orderBy("dia_semana")

vendas_dia_semana.show()
```

#### 6.21.5 KPIs e Métricas Consolidadas

```python
print("\n" + "="*80)
print("KPIs CONSOLIDADOS")
print("="*80)

# Calcular todos os KPIs
kpis = vendas_enriquecidas.agg(
    sum("valor_total").alias("receita_total"),
    count("id_transacao").alias("total_vendas"),
    countDistinct("id_cliente").alias("clientes_ativos"),
    countDistinct("id_produto").alias("produtos_vendidos"),
    avg("valor_total").alias("ticket_medio"),
    min("data_transacao").alias("primeira_venda"),
    max("data_transacao").alias("ultima_venda")
).collect()[0]

print(f"\n{'='*60}")
print(f"RESUMO EXECUTIVO - E-COMMERCE 2023")
print(f"{'='*60}")
print(f"Receita Total:        R$ {kpis['receita_total']:,.2f}")
print(f"Total de Vendas:      {kpis['total_vendas']:,}")
print(f"Clientes Ativos:      {kpis['clientes_ativos']:,}")
print(f"Produtos Vendidos:    {kpis['produtos_vendidos']:,}")
print(f"Ticket Médio:         R$ {kpis['ticket_medio']:,.2f}")
print(f"Período:              {kpis['primeira_venda']} a {kpis['ultima_venda']}")
print(f"{'='*60}\n")
```

#### 6.21.6 Salvar Resultados

```python
print("\n" + "="*80)
print("SALVANDO RESULTADOS")
print("="*80)

# Criar diretório de saída
output_dir = "analise_ecommerce_output"

# Salvar datasets principais em Parquet (formato eficiente)
print(f"\nSalvando em: {output_dir}/")

vendas_enriquecidas.write.mode("overwrite").parquet(f"{output_dir}/vendas_completas.parquet")
print("✓ Vendas completas salvas")

receita_mensal.write.mode("overwrite").parquet(f"{output_dir}/receita_mensal.parquet")
print("✓ Receita mensal salva")

top_produtos.write.mode("overwrite").parquet(f"{output_dir}/top_produtos.parquet")
print("✓ Top produtos salvos")

receita_categoria.write.mode("overwrite").parquet(f"{output_dir}/receita_por_categoria.parquet")
print("✓ Receita por categoria salva")

segmentacao_clientes.write.mode("overwrite").parquet(f"{output_dir}/segmentacao_clientes.parquet")
print("✓ Segmentação de clientes salva")

# Salvar um resumo em CSV (para abrir no Excel)
top_produtos.limit(100).toPandas().to_csv(f"{output_dir}/top_100_produtos.csv", index=False)
print("✓ Top 100 produtos salvos em CSV")

print("\n✅ Análise completa! Todos os resultados foram salvos.")
```

#### 6.21.7 Visualização com Pandas (conversão)

```python
print("\n" + "="*80)
print("VISUALIZAÇÃO (convertendo para Pandas)")
print("="*80)

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid')

# Converter datasets pequenos para Pandas para visualizar
receita_mensal_pd = receita_mensal.toPandas()
receita_categoria_pd = receita_categoria.toPandas()
receita_estado_pd = receita_estado.toPandas()

# Gráfico 1: Receita mensal
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

axes[0, 0].plot(receita_mensal_pd['mes'], receita_mensal_pd['receita_total'], 
                marker='o', linewidth=2, markersize=8)
axes[0, 0].set_title('Receita por Mês - 2023', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Mês')
axes[0, 0].set_ylabel('Receita (R$)')
axes[0, 0].grid(alpha=0.3)

# Gráfico 2: Receita por categoria
axes[0, 1].barh(receita_categoria_pd['categoria_produto'], 
                receita_categoria_pd['receita_total'])
axes[0, 1].set_title('Receita por Categoria de Produto', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Receita (R$)')

# Gráfico 3: Top 10 estados
top_estados = receita_estado_pd.head(10)
axes[1, 0].bar(top_estados['estado'], top_estados['receita_total'], color='teal')
axes[1, 0].set_title('Top 10 Estados por Receita', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Estado')
axes[1, 0].set_ylabel('Receita (R$)')
axes[1, 0].tick_params(axis='x', rotation=45)

# Gráfico 4: Distribuição de categorias (pizza)
axes[1, 1].pie(receita_categoria_pd['receita_total'], 
               labels=receita_categoria_pd['categoria_produto'],
               autopct='%1.1f%%', startangle=90)
axes[1, 1].set_title('Participação por Categoria', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/dashboard_vendas.png', dpi=300, bbox_inches='tight')
print(f"\n✅ Dashboard salvo em: {output_dir}/dashboard_vendas.png")
plt.show()

print("\n" + "="*80)
print("ANÁLISE CONCLUÍDA COM SUCESSO!")
print("="*80)
```

#### 6.21.8 Limpeza

```python
# Liberar memória
vendas.unpersist()
vendas_enriquecidas.unpersist()

# Parar Spark
# spark.stop()
print("\n✅ Pipeline completo executado com sucesso!")
```

### Principais Aprendizados deste Exemplo:

1. **Geração de dados em lote** para não travar memória
2. **Cache estratégico** de DataFrames reutilizados
3. **Joins** para enriquecer dados
4. **Window functions** para rankings e análises por grupo
5. **Agregações complexas** com múltiplas métricas
6. **Salvamento eficiente** em Parquet
7. **Conversão para Pandas** apenas para visualização (dados pequenos)
8. **KPIs consolidados** para relatórios executivos

---

### 11.22 PySpark Prático Corporativo

Esta seção cobre os **padrões mais comuns** que você vai encontrar (e escrever) em ambientes corporativos com PySpark.

#### 11.22.1 Joins: Padrões e Armadilhas

**Por que importa:**
- Joins mal feitos são a **maior causa de lentidão** em pipelines Spark.
- Dados duplicados ou perdidos geralmente vêm de joins incorretos.

##### Tipos de Join e Quando Usar

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, broadcast

spark = SparkSession.builder.appName("joins").getOrCreate()

# Dados de exemplo
clientes = spark.createDataFrame([
    (1, "Ana", "SP"),
    (2, "Bruno", "RJ"),
    (3, "Carla", "MG"),
    (4, "Daniel", "SP")
], ["id_cliente", "nome", "estado"])

pedidos = spark.createDataFrame([
    (101, 1, 500.0),
    (102, 1, 300.0),
    (103, 2, 700.0),
    (104, 5, 200.0)  # cliente 5 não existe!
], ["id_pedido", "id_cliente", "valor"])

# 1. INNER JOIN (padrão): apenas registros que existem nos dois lados
inner_join = clientes.join(pedidos, "id_cliente", "inner")
print("=== INNER JOIN ===")
inner_join.show()
# Resultado: 3 pedidos (pedido 104 foi descartado, cliente 3 e 4 não aparecem)

# 2. LEFT JOIN: mantém TODOS os clientes, mesmo sem pedidos
left_join = clientes.join(pedidos, "id_cliente", "left")
print("\n=== LEFT JOIN ===")
left_join.show()
# Resultado: 4 clientes (Carla e Daniel aparecem com id_pedido=null)

# 3. RIGHT JOIN: mantém TODOS os pedidos, mesmo sem cliente
right_join = clientes.join(pedidos, "id_cliente", "right")
print("\n=== RIGHT JOIN ===")
right_join.show()
# Resultado: 4 pedidos (pedido 104 aparece com nome=null)

# 4. OUTER JOIN: mantém TUDO (clientes sem pedido + pedidos sem cliente)
outer_join = clientes.join(pedidos, "id_cliente", "outer")
print("\n=== OUTER JOIN ===")
outer_join.show()

# 5. LEFT ANTI JOIN: clientes SEM pedidos
sem_pedidos = clientes.join(pedidos, "id_cliente", "left_anti")
print("\n=== LEFT ANTI (clientes sem pedidos) ===")
sem_pedidos.show()

# 6. LEFT SEMI JOIN: clientes COM pedidos (mas não traz colunas de pedidos)
com_pedidos = clientes.join(pedidos, "id_cliente", "left_semi")
print("\n=== LEFT SEMI (clientes com pedidos) ===")
com_pedidos.show()
```

##### Broadcast Join: Otimização para Tabelas Pequenas

**Quando usar:**
- Uma tabela é **pequena** (< 10 MB, até ~100 MB dependendo da memória).
- Quer evitar **shuffle** (redistribuição de dados entre nós).

```python
from pyspark.sql.functions import broadcast

# Tabela de referência (pequena)
categorias = spark.createDataFrame([
    (1, "Eletrônicos"),
    (2, "Roupas"),
    (3, "Livros")
], ["id_categoria", "nome_categoria"])

# Tabela grande
produtos = spark.createDataFrame([
    (101, "Notebook", 1),
    (102, "Camiseta", 2),
    (103, "Romance", 3)
], ["id_produto", "nome_produto", "id_categoria"])

# SEM broadcast: Spark faz shuffle dos dois lados (lento)
join_normal = produtos.join(categorias, "id_categoria")

# COM broadcast: categoria é enviada para todos os nós (rápido)
join_broadcast = produtos.join(broadcast(categorias), "id_categoria")

join_broadcast.explain()  # veja "BroadcastHashJoin" no plano
join_broadcast.show()
```

**Regra prática:**
- Tabela < 10 MB: sempre use `broadcast()`
- Tabela 10-100 MB: teste e veja se acelera
- Tabela > 100 MB: não use broadcast

##### Joins com Múltiplas Colunas

```python
# Quando a chave é composta por várias colunas
vendas = spark.createDataFrame([
    ("SP", 2024, 1000),
    ("RJ", 2024, 1500),
    ("SP", 2023, 900)
], ["estado", "ano", "receita"])

metas = spark.createDataFrame([
    ("SP", 2024, 1200),
    ("RJ", 2024, 1400),
    ("MG", 2024, 800)
], ["estado", "ano", "meta"])

# Join com múltiplas colunas
resultado = vendas.join(
    metas,
    (vendas.estado == metas.estado) & (vendas.ano == metas.ano),
    "left"
).select(
    vendas.estado,
    vendas.ano,
    col("receita"),
    col("meta")
)

resultado.show()
```

##### Armadilha: Duplicação por Joins 1:N

```python
# PROBLEMA: cliente com múltiplos pedidos duplica dados do cliente
clientes_dup = spark.createDataFrame([
    (1, "Ana", 25),
    (2, "Bruno", 30)
], ["id", "nome", "idade"])

pedidos_dup = spark.createDataFrame([
    (1, 100),
    (1, 200),  # Ana tem 2 pedidos
    (1, 150),  # 3 pedidos!
    (2, 300)
], ["id_cliente", "valor"])

# Join ingênuo
resultado_dup = clientes_dup.join(pedidos_dup, clientes_dup.id == pedidos_dup.id_cliente)

print("Contagem de linhas:")
print(f"Clientes: {clientes_dup.count()}")  # 2
print(f"Pedidos: {pedidos_dup.count()}")    # 4
print(f"Join: {resultado_dup.count()}")     # 4 (Ana aparece 3x!)

# SOLUÇÃO: agregar antes de jointar
pedidos_agg = pedidos_dup.groupBy("id_cliente").agg(
    sum("valor").alias("total_gasto"),
    count("*").alias("num_pedidos")
)

resultado_correto = clientes_dup.join(pedidos_agg, clientes_dup.id == pedidos_agg.id_cliente)
print(f"Join agregado: {resultado_correto.count()}")  # 2 (correto!)
resultado_correto.show()
```

#### 11.22.2 Tratamento de Nulos: Padrões Profissionais

**Por que importa:**
- Nulos causam **joins que não batem**, **agregações erradas** e **filtros inesperados**.
- Spark trata `null` diferente de Pandas em algumas operações.

##### Detecção de Nulos

```python
from pyspark.sql.functions import col, isnan, isnull, when, count

df = spark.createDataFrame([
    (1, "Ana", 5000, "SP"),
    (2, "Bruno", None, "RJ"),
    (3, None, 7000, "MG"),
    (4, "Carla", 6000, None)
], ["id", "nome", "salario", "cidade"])

# 1. Ver quantidade de nulos por coluna
df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in df.columns
]).show()

# 2. Filtrar linhas com nulos em coluna específica
df.filter(col("salario").isNull()).show()

# 3. Filtrar linhas SEM nulos
df.filter(col("salario").isNotNull()).show()

# 4. Filtrar linhas com qualquer nulo
from functools import reduce
df.filter(
    reduce(lambda a, b: a | b, [col(c).isNull() for c in df.columns])
).show()
```

##### Substituição de Nulos

```python
# 1. fillna: preencher nulos
df_filled = df.fillna({
    "salario": 0,
    "cidade": "Desconhecida",
    "nome": "Sem Nome"
})
df_filled.show()

# 2. Preencher todos os numéricos com 0
df.fillna(0).show()

# 3. Substituir usando coalesce (primeira não-nula)
from pyspark.sql.functions import coalesce, lit

df_backup = df.withColumn(
    "cidade_final",
    coalesce(col("cidade"), lit("Não Informada"))
)
df_backup.show()

# 4. Substituir com valor calculado (média, mediana)
media_salario = df.agg({"salario": "avg"}).collect()[0][0]
df_media = df.withColumn(
    "salario",
    coalesce(col("salario"), lit(media_salario))
)
df_media.show()
```

##### Remoção de Nulos

```python
# 1. Remover linhas com qualquer nulo
df.dropna().show()

# 2. Remover apenas se salário for nulo
df.dropna(subset=["salario"]).show()

# 3. Remover apenas se TODAS as colunas forem nulas
df.dropna(how="all").show()

# 4. Remover se tiver nulos em múltiplas colunas específicas
df.dropna(subset=["nome", "salario"], how="any").show()
```

##### Nulos em Joins: Comportamento Crítico

```python
# IMPORTANTE: Nulos nunca fazem match em joins!
tabela_a = spark.createDataFrame([
    (1, "Ana"),
    (None, "Bruno"),  # null na chave
    (3, "Carla")
], ["id", "nome"])

tabela_b = spark.createDataFrame([
    (1, "SP"),
    (None, "RJ"),  # null na chave
    (2, "MG")
], ["id", "cidade"])

# Join: null não casa com null!
resultado = tabela_a.join(tabela_b, "id", "inner")
print(f"Linhas resultado: {resultado.count()}")  # 1 (só id=1)
resultado.show()

# SOLUÇÃO: tratar nulos antes do join
tabela_a_limpa = tabela_a.fillna({"id": -1})
tabela_b_limpa = tabela_b.fillna({"id": -1})
resultado_limpo = tabela_a_limpa.join(tabela_b_limpa, "id", "inner")
print(f"Linhas resultado limpo: {resultado_limpo.count()}")  # 2
resultado_limpo.show()
```

#### 11.22.3 Cache e Persist: Quando e Como

**Por que importa:**
- Cache salva **horas** de reprocessamento em pipelines complexos.
- Usado errado, **quebra a memória** do cluster.

##### Quando Usar Cache

```python
# USE cache quando:
# 1. Vai reutilizar o mesmo DataFrame várias vezes
# 2. Processamento até aquele ponto é custoso
# 3. Dataset cabe na memória disponível

# Exemplo SEM cache (lento)
df_base = spark.read.parquet("dados_grandes.parquet")  # 50 GB

# Cada operação relê do disco!
df_base.filter(col("ano") == 2024).count()  # Lê 50 GB
df_base.filter(col("ano") == 2024).agg(sum("valor")).show()  # Lê 50 GB de novo!
df_base.filter(col("ano") == 2024).groupBy("categoria").count().show()  # Mais 50 GB!

# Exemplo COM cache (rápido)
df_2024 = df_base.filter(col("ano") == 2024).cache()
df_2024.count()  # Primeira execução: processa e guarda na memória

# Agora é instantâneo:
df_2024.count()
df_2024.agg(sum("valor")).show()
df_2024.groupBy("categoria").count().show()

# SEMPRE libere quando terminar
df_2024.unpersist()
```

##### Persist: Níveis de Armazenamento

```python
from pyspark import StorageLevel

# cache() é atalho para persist(MEMORY_AND_DISK)
df.cache()  # = df.persist(StorageLevel.MEMORY_AND_DISK)

# Opções de persist:
df.persist(StorageLevel.MEMORY_ONLY)       # Só memória (rápido, mas arriscado)
df.persist(StorageLevel.MEMORY_AND_DISK)   # Memória + disco se não couber
df.persist(StorageLevel.DISK_ONLY)         # Só disco (lento, mas seguro)
df.persist(StorageLevel.MEMORY_ONLY_2)     # Replica em 2 nós (tolerância a falhas)

# Quando usar cada um:
# MEMORY_ONLY: dataset pequeno, muita RAM disponível
# MEMORY_AND_DISK: caso geral (recomendado)
# DISK_ONLY: dataset gigante, pouca RAM
```

##### Padrão Profissional: Cache Estratégico

```python
# Pipeline típico
df_raw = spark.read.parquet("raw_data.parquet")

# Limpeza pesada
df_limpo = df_raw \
    .filter(col("data").isNotNull()) \
    .filter(col("valor") > 0) \
    .withColumn("ano", year("data")) \
    .withColumn("mes", month("data")) \
    .dropDuplicates(["id_transacao"])

# CACHE aqui: processamento pesado feito, vamos reutilizar
df_limpo.cache()
df_limpo.count()  # força cache

# Agora podemos criar múltiplas análises sem reprocessar:
analise_mensal = df_limpo.groupBy("ano", "mes").agg(sum("valor"))
analise_produto = df_limpo.groupBy("produto").agg(count("*"))
analise_cliente = df_limpo.groupBy("id_cliente").agg(avg("valor"))

# Salvar todas
analise_mensal.write.parquet("output/mensal")
analise_produto.write.parquet("output/produto")
analise_cliente.write.parquet("output/cliente")

# Liberar cache
df_limpo.unpersist()
```

##### Monitorar Cache: Spark UI

```python
# Acessar Spark UI (enquanto aplicação está rodando):
# http://localhost:4040

# Ver:
# - Storage tab: quanto de memória está em cache
# - Executors tab: uso de memória por executor

# Código para debug:
print(f"Está em cache? {df_limpo.is_cached}")
print(f"Nível de armazenamento: {df_limpo.storageLevel}")
```

#### 11.22.4 Leitura e Gravação: Padrões Corporativos

##### Leitura Eficiente

```python
# 1. Parquet: formato padrão corporativo
df = spark.read.parquet("s3://bucket/data/*.parquet")

# 2. Leitura com esquema explícito (mais rápido que inferSchema)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

schema = StructType([
    StructField("id", IntegerType(), False),
    StructField("nome", StringType(), True),
    StructField("salario", DoubleType(), True),
    StructField("data", StringType(), True)
])

df = spark.read.csv(
    "dados.csv",
    header=True,
    schema=schema  # Não precisa inferir, é mais rápido
)

# 3. Leitura particionada (por data, região, etc.)
# Estrutura: /data/ano=2024/mes=01/*.parquet
df = spark.read.parquet("s3://bucket/data/")  # Lê todas partições

# Filtrar só 2024 (Spark lê apenas essa partição!)
df_2024 = spark.read.parquet("s3://bucket/data/").filter(col("ano") == 2024)

# 4. Leitura incremental (apenas arquivos novos)
df = spark.read.parquet("s3://bucket/data/").filter(col("data") >= "2024-01-01")
```

##### Gravação Otimizada

```python
# 1. Parquet com particionamento
df.write \
    .mode("overwrite") \
    .partitionBy("ano", "mes") \
    .parquet("output/vendas")

# Estrutura resultante:
# output/vendas/ano=2024/mes=01/*.parquet
# output/vendas/ano=2024/mes=02/*.parquet

# 2. Controlar número de arquivos (coalesce)
df.coalesce(10).write.parquet("output/data")  # 10 arquivos

# 3. Repartição antes de gravar (melhor distribuição)
df.repartition(50, "estado").write \
    .partitionBy("estado") \
    .parquet("output/por_estado")

# 4. Append (adicionar dados sem sobrescrever)
df_novos.write.mode("append").parquet("output/vendas")

# 5. Delta Lake: controle de versão e ACID
df.write.format("delta").mode("overwrite").save("delta/vendas")

# Ler Delta
df_delta = spark.read.format("delta").load("delta/vendas")

# Time travel (ler versão antiga)
df_ontem = spark.read.format("delta") \
    .option("versionAsOf", 1) \
    .load("delta/vendas")
```

##### Padrão: Checkpoint Intermediário

```python
# Em pipelines longos, salve resultados intermediários

# Etapa 1: limpeza
df_limpo = df_raw.filter(...).dropDuplicates(...)
df_limpo.write.mode("overwrite").parquet("checkpoint/limpo")

# Etapa 2: enriquecimento
df_limpo = spark.read.parquet("checkpoint/limpo")  # Relê se falhar
df_enriquecido = df_limpo.join(...)
df_enriquecido.write.mode("overwrite").parquet("checkpoint/enriquecido")

# Etapa 3: agregação final
df_enriquecido = spark.read.parquet("checkpoint/enriquecido")
df_final = df_enriquecido.groupBy(...)
df_final.write.mode("overwrite").parquet("output/final")
```

##### Padrão: Configuração de Compressão

```python
# Parquet com compressão (economiza 70-90% de espaço)
df.write \
    .option("compression", "snappy") \  # Padrão, boa relação velocidade/compressão
    .parquet("output/data")

# Outras opções:
# - "gzip": máxima compressão, mais lento
# - "snappy": rápido, boa compressão (recomendado)
# - "lzo": rápido, menos compressão
# - "uncompressed": sem compressão (raramente usado)

# CSV com compressão
df.write.option("compression", "gzip").csv("output/data.csv.gz")
```

---

### 11.23 Análise de Impacto em Produção

**Por que importa:**

Mudanças em produção (nova regra de crédito, campanha, precificação) afetam **pessoas reais** e **receita**.
Você precisa **quantificar o impacto** antes e depois, identificar **quem foi afetado** e fazer **rollout seguro**.

#### 11.23.1 Análise Antes/Depois

**Cenário:**
Você quer mudar a regra de aprovação de crédito de `score > 600` para `score > 650`.

##### Simulação: Impacto Esperado

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count, sum as spark_sum, avg, round as spark_round

spark = SparkSession.builder.appName("impacto").getOrCreate()

# Dados históricos (últimos 6 meses)
df_historico = spark.read.parquet("dados/propostas_6m.parquet")

# Regra ATUAL
df_atual = df_historico.withColumn(
    "aprovado_atual",
    when(col("score") > 600, 1).otherwise(0)
)

# Regra PROPOSTA
df_proposta = df_atual.withColumn(
    "aprovado_proposta",
    when(col("score") > 650, 1).otherwise(0)
)

# Comparação
comparacao = df_proposta.agg(
    count("*").alias("total_propostas"),
    spark_sum("aprovado_atual").alias("aprovados_atual"),
    spark_sum("aprovado_proposta").alias("aprovados_proposta"),
    avg(when(col("aprovado_atual") == 1, col("inadimplente"))).alias("inad_atual"),
    avg(when(col("aprovado_proposta") == 1, col("inadimplente"))).alias("inad_proposta")
).collect()[0]

print("="*70)
print("ANÁLISE DE IMPACTO: Mudança de Score 600 → 650")
print("="*70)
print(f"Total de propostas (6m): {comparacao['total_propostas']:,}")
print(f"\nREGRA ATUAL (score > 600):")
print(f"  Aprovações: {comparacao['aprovados_atual']:,}")
print(f"  Taxa de aprovação: {comparacao['aprovados_atual']/comparacao['total_propostas']*100:.1f}%")
print(f"  Taxa de inadimplência: {comparacao['inad_atual']*100:.2f}%")
print(f"\nREGRA PROPOSTA (score > 650):")
print(f"  Aprovações: {comparacao['aprovados_proposta']:,}")
print(f"  Taxa de aprovação: {comparacao['aprovados_proposta']/comparacao['total_propostas']*100:.1f}%")
print(f"  Taxa de inadimplência: {comparacao['inad_proposta']*100:.2f}%")
print(f"\nIMPACTO:")
perda_volume = comparacao['aprovados_atual'] - comparacao['aprovados_proposta']
ganho_qualidade = (comparacao['inad_atual'] - comparacao['inad_proposta']) * 100
print(f"  Perda de volume: {perda_volume:,} aprovações ({perda_volume/comparacao['aprovados_atual']*100:.1f}%)")
print(f"  Ganho de qualidade: {ganho_qualidade:.2f} pp de inadimplência")
print("="*70)
```

##### Análise Antes/Depois Real (Pós-Deploy)

```python
# Dados: 30 dias antes da mudança vs 30 dias depois
df_antes = spark.read.parquet("dados/propostas/data>=2024-11-01/data<=2024-11-30")
df_depois = spark.read.parquet("dados/propostas/data>=2024-12-01/data<=2024-12-31")

# Métricas antes
metricas_antes = df_antes.agg(
    count("*").alias("propostas"),
    spark_sum("aprovado").alias("aprovacoes"),
    avg("valor_aprovado").alias("ticket_medio"),
    spark_sum("valor_aprovado").alias("volume_total")
).withColumn("periodo", lit("Antes")).collect()[0]

# Métricas depois
metricas_depois = df_depois.agg(
    count("*").alias("propostas"),
    spark_sum("aprovado").alias("aprovacoes"),
    avg("valor_aprovado").alias("ticket_medio"),
    spark_sum("valor_aprovado").alias("volume_total")
).withColumn("periodo", lit("Depois")).collect()[0]

# Comparação
print("\n" + "="*70)
print("RESULTADOS REAIS: ANTES vs DEPOIS")
print("="*70)
print(f"\nANTES (Nov 2024):")
print(f"  Propostas: {metricas_antes['propostas']:,}")
print(f"  Aprovações: {metricas_antes['aprovacoes']:,}")
print(f"  Taxa: {metricas_antes['aprovacoes']/metricas_antes['propostas']*100:.1f}%")
print(f"  Ticket médio: R$ {metricas_antes['ticket_medio']:,.2f}")
print(f"  Volume: R$ {metricas_antes['volume_total']:,.2f}")

print(f"\nDEPOIS (Dez 2024):")
print(f"  Propostas: {metricas_depois['propostas']:,}")
print(f"  Aprovações: {metricas_depois['aprovacoes']:,}")
print(f"  Taxa: {metricas_depois['aprovacoes']/metricas_depois['propostas']*100:.1f}%")
print(f"  Ticket médio: R$ {metricas_depois['ticket_medio']:,.2f}")
print(f"  Volume: R$ {metricas_depois['volume_total']:,.2f}")

print(f"\nVARIAÇÃO:")
var_taxa = (metricas_depois['aprovacoes']/metricas_depois['propostas'] - 
            metricas_antes['aprovacoes']/metricas_antes['propostas']) * 100
var_volume = ((metricas_depois['volume_total'] - metricas_antes['volume_total']) / 
              metricas_antes['volume_total']) * 100
print(f"  Taxa de aprovação: {var_taxa:+.2f} pp")
print(f"  Volume financeiro: {var_volume:+.1f}%")
print("="*70)
```

#### 11.23.2 População Afetada

**Quem ganhou e quem perdeu com a mudança?**

```python
# Criar flag de mudança de decisão
df_impacto = df_proposta.withColumn(
    "tipo_impacto",
    when((col("aprovado_atual") == 1) & (col("aprovado_proposta") == 0), "PERDEU")
    .when((col("aprovado_atual") == 0) & (col("aprovado_proposta") == 1), "GANHOU")
    .when((col("aprovado_atual") == 1) & (col("aprovado_proposta") == 1), "MANTEVE (aprovado)")
    .otherwise("MANTEVE (negado)")
)

# Análise por grupo
resumo_impacto = df_impacto.groupBy("tipo_impacto").agg(
    count("*").alias("quantidade"),
    avg("score").alias("score_medio"),
    avg("renda").alias("renda_media"),
    avg("inadimplente").alias("taxa_inad")
).orderBy(col("quantidade").desc())

print("\n=== POPULAÇÃO AFETADA ===")
resumo_impacto.show(truncate=False)

# Perfil de quem PERDEU aprovação
print("\n=== PERFIL: Quem PERDEU com a mudança ===")
perdedores = df_impacto.filter(col("tipo_impacto") == "PERDEU")

perdedores.groupBy("faixa_renda").agg(
    count("*").alias("qtd"),
    avg("score").alias("score_medio")
).orderBy(col("qtd").desc()).show()

# Segmentar por geografia
perdedores.groupBy("estado").agg(
    count("*").alias("afetados")
).orderBy(col("afetados").desc()).show()
```

#### 11.23.3 Rollout Seguro (Teste A/B)

**Não mude tudo de uma vez. Teste em pequena escala primeiro.**

##### Padrão: Rollout Gradual

```python
from pyspark.sql.functions import rand

# 1. FASE 1: 5% da população (teste)
df_producao = spark.read.parquet("dados/propostas_hoje.parquet")

df_teste = df_producao.withColumn("grupo", 
    when(rand() < 0.05, "TESTE")  # 5% grupo teste
    .otherwise("CONTROLE")         # 95% controle
)

# Aplicar regra nova apenas no grupo TESTE
df_decisao = df_teste.withColumn(
    "aprovado",
    when(
        col("grupo") == "TESTE",
        when(col("score") > 650, 1).otherwise(0)  # Regra nova
    ).otherwise(
        when(col("score") > 600, 1).otherwise(0)  # Regra antiga
    )
)

# Salvar com flag de grupo
df_decisao.write.mode("append").partitionBy("data", "grupo").parquet("output/decisoes")

# 2. MONITORAR (após 7 dias)
df_teste_resultado = spark.read.parquet("output/decisoes") \
    .filter(col("data").between("2024-12-01", "2024-12-07"))

comparacao_grupos = df_teste_resultado.groupBy("grupo").agg(
    count("*").alias("propostas"),
    spark_sum("aprovado").alias("aprovacoes"),
    avg(when(col("aprovado") == 1, col("inadimplente"))).alias("taxa_inad")
)

comparacao_grupos.show()

# 3. DECISÃO: Se teste foi bom, aumentar para 20% → 50% → 100%
```

##### Padrão: Rollout por Segmento

```python
# Testar primeiro em estados menos críticos
df_rollout = df_producao.withColumn(
    "regra",
    when(col("estado").isin("AC", "RO", "AP"), "NOVA")  # Estados pequenos
    .otherwise("ANTIGA")
)

# Ou por faixa de risco
df_rollout = df_producao.withColumn(
    "regra",
    when(col("score") > 700, "NOVA")  # Testar em baixo risco primeiro
    .otherwise("ANTIGA")
)

# Aplicar regra
df_decisao = df_rollout.withColumn(
    "aprovado",
    when(
        col("regra") == "NOVA",
        # Lógica nova
        (col("score") > 650) & (col("renda") > 2000)
    ).otherwise(
        # Lógica antiga
        col("score") > 600
    )
)
```

##### Padrão: Kill Switch (Reverter Rápido)

```python
# Usar parâmetro de configuração externo
config_regra = spark.read.json("s3://config/regra_aprovacao.json").collect()[0]

# Se config_regra['ativa'] == False, voltar para regra antiga
df_decisao = df_producao.withColumn(
    "aprovado",
    when(
        lit(config_regra['ativa']),
        # Regra nova
        when(col("score") > lit(config_regra['score_minimo']), 1).otherwise(0)
    ).otherwise(
        # Regra antiga (fallback)
        when(col("score") > 600, 1).otherwise(0)
    )
)

# Para reverter em emergência: altere o JSON e republique
# {"ativa": false}  ← desliga regra nova instantaneamente
```

#### 11.23.4 Checklist: Análise de Impacto Profissional

Antes de fazer mudança em produção:

- [ ] **Simulei** o impacto com dados históricos?
- [ ] **Quantifiquei** ganhos e perdas (volume, receita, qualidade)?
- [ ] **Identifiquei** população afetada (quem ganha, quem perde)?
- [ ] **Validei** com stakeholders (produto, negócio, compliance)?
- [ ] **Planejei** rollout gradual (5% → 20% → 50% → 100%)?
- [ ] **Defini** métricas de sucesso (o que monitorar)?
- [ ] **Implementei** kill switch (como reverter rápido)?
- [ ] **Agendei** reunião de revisão (7 dias pós-deploy)?

---

### 11.24 Como Ler Código Spark Legado

**Por que importa:**

Você vai herdar código Spark escrito por outros. Código legado geralmente:
- Não tem comentários
- Mistura lógicas diferentes
- Tem nomes ruins de variáveis
- Acumula transformações complexas

Aprender a **decodificar** esse código é essencial para manutenção e debugging.

#### 11.24.1 Estratégia: Identificar 4 Blocos

Todo código Spark segue o mesmo padrão:

1. **ENTRADA**: De onde vêm os dados?
2. **TRANSFORMAÇÕES**: O que fazemos com os dados?
3. **SAÍDA**: Para onde vão os dados?
4. **VALIDAÇÕES**: Há checks de qualidade?

##### Exemplo de Código Legado

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, sum, count, avg, year, month, datediff, lit, broadcast

spark = SparkSession.builder.appName("job_misterioso").getOrCreate()

# Bloco 1
df1 = spark.read.parquet("s3://data-lake/raw/transactions/")
df2 = spark.read.parquet("s3://data-lake/raw/customers/")
df3 = spark.read.json("s3://config/lookup_table.json")

# Bloco 2
df_filtered = df1.filter(col("status") == "approved").filter(col("amount") > 100)
df_joined = df_filtered.join(broadcast(df2), df_filtered.customer_id == df2.id, "left")
df_enriched = df_joined.join(broadcast(df3), df_joined.category == df3.cat_code, "left")

# Bloco 3
df_final = df_enriched.withColumn("year", year("transaction_date")) \
    .withColumn("month", month("transaction_date")) \
    .withColumn("high_value", when(col("amount") > 1000, 1).otherwise(0)) \
    .withColumn("days_since_signup", datediff(col("transaction_date"), col("signup_date")))

# Bloco 4
agg = df_final.groupBy("year", "month", "category_name").agg(
    count("*").alias("num_transactions"),
    sum("amount").alias("total_amount"),
    avg("amount").alias("avg_amount"),
    sum("high_value").alias("high_value_count")
).orderBy("year", "month", "total_amount")

# Bloco 5
agg.write.mode("overwrite").partitionBy("year", "month").parquet("s3://data-lake/processed/monthly_summary/")
```

#### 11.24.2 Decodificar: Entrada

**Perguntas:**
- Quantas fontes de dados?
- Qual formato (parquet, CSV, JSON)?
- Onde estão (S3, HDFS, local)?
- Há esquema explícito ou inferido?

**Análise do exemplo:**

```python
# ENTRADA 1: Transações (parquet, S3)
df1 = spark.read.parquet("s3://data-lake/raw/transactions/")

# ENTRADA 2: Clientes (parquet, S3)
df2 = spark.read.parquet("s3://data-lake/raw/customers/")

# ENTRADA 3: Tabela de lookup/referência (JSON, S3)
df3 = spark.read.json("s3://config/lookup_table.json")
```

**Interpretação:**
- **3 fontes diferentes**: transações, clientes, categorias
- Todas em S3 (ambiente cloud)
- df1 e df2 são grandes (parquet), df3 é pequena (JSON de config)

**Próximo passo:** Inspecionar estrutura

```python
df1.printSchema()  # Ver colunas de transações
df2.printSchema()  # Ver colunas de clientes
df3.printSchema()  # Ver lookup table
```

#### 11.24.3 Decodificar: Transformações

**Perguntas:**
- Quais filtros estão sendo aplicados?
- Quais joins acontecem?
- Quais colunas são criadas?
- Há lógica de negócio escondida?

**Análise do exemplo:**

```python
# FILTRO 1: Só transações aprovadas e > R$ 100
df_filtered = df1.filter(col("status") == "approved").filter(col("amount") > 100)

# JOIN 1: Adicionar dados de clientes (left join)
df_joined = df_filtered.join(broadcast(df2), df_filtered.customer_id == df2.id, "left")
# → Traz nome, data de signup, etc. do cliente

# JOIN 2: Adicionar nome da categoria (lookup table)
df_enriched = df_joined.join(broadcast(df3), df_joined.category == df3.cat_code, "left")
# → Traduz código de categoria para nome legível

# CRIAÇÃO DE COLUNAS:
df_final = df_enriched \
    .withColumn("year", year("transaction_date"))      # Ano da transação
    .withColumn("month", month("transaction_date"))    # Mês da transação
    .withColumn("high_value", when(col("amount") > 1000, 1).otherwise(0))  # Flag alto valor
    .withColumn("days_since_signup",  # Dias desde cadastro
                datediff(col("transaction_date"), col("signup_date")))
```

**Interpretação:**
1. **Filtra** transações válidas (aprovadas, valor mínimo)
2. **Enriquece** com dados de cliente (join com df2)
3. **Traduz** categorias (join com df3)
4. **Adiciona** colunas derivadas (ano, mês, flags, métricas)

**Padrão comum:**
```
Dados brutos → Filtro → Enriquecimento (joins) → Colunas derivadas
```

#### 11.24.4 Decodificar: Saída

**Perguntas:**
- Onde os dados são salvos?
- Qual formato?
- Há particionamento?
- Modo de escrita (overwrite, append)?

**Análise do exemplo:**

```python
agg.write \
    .mode("overwrite") \           # Sobrescreve dados antigos
    .partitionBy("year", "month") \ # Particiona por ano e mês
    .parquet("s3://data-lake/processed/monthly_summary/")
```

**Interpretação:**
- Salva em **S3** (data lake)
- Formato **parquet** (eficiente)
- **Particionado** por ano/mês (facilita queries filtradas por período)
- **Overwrite**: toda execução substitui dados antigos

**Estrutura resultante:**
```
s3://data-lake/processed/monthly_summary/
  year=2024/
    month=01/
      part-00000.parquet
      part-00001.parquet
    month=02/
      ...
```

#### 11.24.5 Decodificar: Validações

**Perguntas:**
- Há contagens de linhas?
- Há checks de nulos?
- Há asserts ou logs de qualidade?

**No exemplo:** NENHUMA validação! (código legado típico)

**O que DEVERIA ter:**

```python
# Validação 1: Contagem de linhas
print(f"Transações lidas: {df1.count():,}")
print(f"Após filtros: {df_filtered.count():,}")
print(f"Após joins: {df_enriched.count():,}")

# Validação 2: Nulos críticos
nulos = df_final.select([
    count(when(col(c).isNull(), c)).alias(c) 
    for c in ["customer_id", "amount", "transaction_date"]
])
nulos.show()

# Validação 3: Valores inesperados
assert df_final.filter(col("amount") < 0).count() == 0, "Valores negativos encontrados!"

# Validação 4: Duplicatas
duplicatas = df_final.groupBy("transaction_id").count().filter(col("count") > 1)
if duplicatas.count() > 0:
    print("ALERTA: Transações duplicadas!")
    duplicatas.show()

# Validação 5: Cobertura de join
sem_cliente = df_final.filter(col("customer_id").isNull()).count()
print(f"Transações sem cliente: {sem_cliente}")
```

#### 11.24.6 Ferramenta: Explain Plan

**Use `.explain()` para ver o que Spark realmente vai fazer:**

```python
# Ver plano de execução
df_final.explain()

# Plano completo (lógico + físico)
df_final.explain(True)

# Procurar por:
# - BroadcastHashJoin: join otimizado (bom)
# - SortMergeJoin: join pesado (pode ser lento)
# - Filter: filtros aplicados cedo (bom) ou tarde (ruim)
# - Project: seleção de colunas
```

#### 11.24.7 Padrão: Refatorar Código Legado

**Transforme código legado em código limpo:**

**ANTES (legado):**
```python
df = spark.read.parquet("data.parquet")
df2 = df.filter(col("status") == "A").filter(col("value") > 100).join(...)
df3 = df2.withColumn("x", ...).withColumn("y", ...).groupBy(...).agg(...)
df3.write.parquet("output")
```

**DEPOIS (limpo):**
```python
from pyspark.sql import DataFrame

def ler_transacoes() -> DataFrame:
    """Lê transações do data lake."""
    return spark.read.parquet("s3://data-lake/raw/transactions/")

def filtrar_validas(df: DataFrame) -> DataFrame:
    """Filtra apenas transações aprovadas e com valor mínimo."""
    return df.filter(
        (col("status") == "approved") & 
        (col("amount") > 100)
    )

def enriquecer_clientes(df_trans: DataFrame, df_cli: DataFrame) -> DataFrame:
    """Adiciona dados de cliente via join."""
    return df_trans.join(
        broadcast(df_cli),
        df_trans.customer_id == df_cli.id,
        "left"
    )

def criar_metricas(df: DataFrame) -> DataFrame:
    """Adiciona colunas derivadas."""
    return df \
        .withColumn("year", year("transaction_date")) \
        .withColumn("month", month("transaction_date")) \
        .withColumn("high_value", when(col("amount") > 1000, 1).otherwise(0))

def salvar_resultado(df: DataFrame, caminho: str):
    """Salva resultado particionado."""
    df.write \
        .mode("overwrite") \
        .partitionBy("year", "month") \
        .parquet(caminho)

# Pipeline principal
df_trans = ler_transacoes()
df_validas = filtrar_validas(df_trans)
df_clientes = spark.read.parquet("s3://data-lake/raw/customers/")
df_enriquecido = enriquecer_clientes(df_validas, df_clientes)
df_metricas = criar_metricas(df_enriquecido)
salvar_resultado(df_metricas, "s3://data-lake/processed/monthly/")
```

#### 11.24.8 Checklist: Ler Código Legado

Ao pegar código Spark de outro dev:

- [ ] **Identifiquei** todas as entradas (fontes de dados)?
- [ ] **Entendi** cada transformação (filtros, joins, colunas)?
- [ ] **Verifiquei** se há lógica de negócio escondida?
- [ ] **Localizei** onde os dados são salvos?
- [ ] **Procurei** validações (ou adicionei se não houver)?
- [ ] **Executei** `.explain()` para ver plano de execução?
- [ ] **Testei** com amostra pequena antes de rodar completo?
- [ ] **Documentei** o que o código faz (comentários/docstrings)?

**Dica profissional:**

Sempre que pegar código legado, adicione isso no topo do arquivo:

```python
"""
JOB: Resumo Mensal de Transações

ENTRADAS:
- s3://data-lake/raw/transactions/ (transações, parquet)
- s3://data-lake/raw/customers/ (clientes, parquet)  
- s3://config/lookup_table.json (categorias, JSON)

TRANSFORMAÇÕES:
1. Filtrar transações aprovadas e amount > 100
2. Join com clientes (left) para enriquecer
3. Join com lookup para traduzir categorias
4. Adicionar colunas: year, month, high_value, days_since_signup
5. Agregar por year/month/category

SAÍDAS:
- s3://data-lake/processed/monthly_summary/ (parquet, particionado por year/month)

VALIDAÇÕES:
- TODO: adicionar checks de nulos
- TODO: verificar duplicatas
- TODO: validar cobertura de joins

FREQUÊNCIA: Diário (roda todo dia às 3h)
DONO: time-analytics@empresa.com
ÚLTIMA MODIFICAÇÃO: 2024-01-15
"""
```

---

### 11.25 PySpark no Databricks (Ambiente Corporativo)

**Por que Databricks?**

Databricks é a **plataforma corporativa mais comum** para PySpark. Combina:
- Cluster gerenciado (você não precisa instalar Spark)
- Notebooks colaborativos
- Delta Lake nativo
- Integração com Azure/AWS/GCP
- Orquestração de jobs

Esta seção cobre os **padrões específicos** do Databricks que diferem de PySpark local.

#### 11.25.1 Como Pensar Notebooks no Databricks

**Diferença fundamental:**

| Aspecto | Script Python (.py) | Notebook Databricks |
|---------|---------------------|---------------------|
| **Execução** | Top-down, uma vez | Células independentes, iterativa |
| **Estado** | Recriado a cada run | Persiste entre execuções |
| **Debugging** | Print + logs | Visualização inline |
| **Colaboração** | Git only | Inline comments + Git |
| **Outputs** | Logs e arquivos | Tabelas, gráficos inline |

##### Padrão: Estruturar Notebook de Análise

```python
# ============================================================
# CÉLULA 1: Setup e Configuração
# ============================================================

# Título e metadados
"""
# Análise de Vendas - Q1 2024

**Objetivo:** Calcular métricas de vendas por região e produto

**Dados:**
- Input: s3://data/vendas/2024-Q1/
- Output: /dbfs/mnt/analytics/relatorios/vendas_Q1_2024/

**Autor:** analytics-team@empresa.com
**Última atualização:** 2024-01-20
"""

# Imports
from pyspark.sql.functions import col, sum, avg, count, when, lit, current_date
from pyspark.sql.window import Window
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações
sns.set_theme(style='whitegrid')
pd.options.display.max_columns = None

# ============================================================
# CÉLULA 2: Parâmetros (Widgets)
# ============================================================

# Widgets para parametrização (podem ser alterados sem mexer no código)
dbutils.widgets.text("data_inicio", "2024-01-01", "Data Início")
dbutils.widgets.text("data_fim", "2024-03-31", "Data Fim")
dbutils.widgets.dropdown("estado", "SP", ["SP", "RJ", "MG", "ALL"], "Estado")

# Recuperar valores
data_inicio = dbutils.widgets.get("data_inicio")
data_fim = dbutils.widgets.get("data_fim")
estado = dbutils.widgets.get("estado")

print(f"Parâmetros:")
print(f"  Período: {data_inicio} a {data_fim}")
print(f"  Estado: {estado}")

# ============================================================
# CÉLULA 3: Leitura de Dados
# ============================================================

# Delta Table (padrão no Databricks)
vendas = spark.table("bronze.vendas")

# Ou de arquivo
# vendas = spark.read.format("delta").load("/mnt/data/vendas")

print(f"Linhas totais: {vendas.count():,}")
vendas.printSchema()

# ============================================================
# CÉLULA 4: Exploração Rápida
# ============================================================

# Display é MUITO melhor que show() no Databricks
display(vendas.limit(10))

# Ver estatísticas
display(vendas.select("valor", "quantidade").summary())

# ============================================================
# CÉLULA 5: Limpeza e Filtros
# ============================================================

vendas_filtrado = vendas.filter(
    (col("data_venda").between(data_inicio, data_fim)) &
    (col("status") == "aprovada") &
    (col("valor") > 0)
)

# Aplicar filtro de estado se não for "ALL"
if estado != "ALL":
    vendas_filtrado = vendas_filtrado.filter(col("estado") == estado)

print(f"Após filtros: {vendas_filtrado.count():,} linhas")

# Cache aqui - vamos reutilizar
vendas_filtrado.cache()
vendas_filtrado.count()  # Materializa cache

# ============================================================
# CÉLULA 6: Análises
# ============================================================

# Vendas por estado
por_estado = vendas_filtrado.groupBy("estado").agg(
    count("*").alias("num_vendas"),
    sum("valor").alias("receita_total"),
    avg("valor").alias("ticket_medio")
).orderBy(col("receita_total").desc())

display(por_estado)

# ============================================================
# CÉLULA 7: Visualização
# ============================================================

# Converter para Pandas para plotar
por_estado_pd = por_estado.toPandas()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gráfico 1: Receita por estado
axes[0].barh(por_estado_pd['estado'], por_estado_pd['receita_total'])
axes[0].set_xlabel('Receita Total (R$)')
axes[0].set_title('Receita por Estado')

# Gráfico 2: Ticket médio
axes[1].bar(por_estado_pd['estado'], por_estado_pd['ticket_medio'])
axes[1].set_ylabel('Ticket Médio (R$)')
axes[1].set_title('Ticket Médio por Estado')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# ============================================================
# CÉLULA 8: Salvar Resultados
# ============================================================

# Salvar como Delta Table
por_estado.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("silver.analise_vendas_estado")

print("✅ Tabela salva: silver.analise_vendas_estado")

# Também salvar em CSV para compartilhar
por_estado.toPandas().to_csv(
    "/dbfs/FileStore/reports/vendas_estado_Q1_2024.csv",
    index=False
)

print("✅ CSV salvo: /dbfs/FileStore/reports/vendas_estado_Q1_2024.csv")

# ============================================================
# CÉLULA 9: Limpeza
# ============================================================

# Liberar cache
vendas_filtrado.unpersist()

print("✅ Análise concluída!")
```

##### Princípios para Notebooks

1. **Uma célula = uma responsabilidade**
   - Setup, leitura, filtro, análise, visualização, saída
   - Não misture tudo em uma célula gigante

2. **Use `display()` em vez de `show()`**
   - Tabelas interativas, ordenáveis
   - Gráficos automáticos
   - Exportação fácil

3. **Cache estratégico**
   - Depois de filtros pesados
   - Antes de múltiplas análises
   - SEMPRE libere no final

4. **Documentação inline**
   - Markdown nas primeiras células
   - Comentários em blocos claros
   - Prints informativos

5. **Widgets para parâmetros**
   - Datas, regiões, thresholds
   - Facilita reuso sem mexer no código

#### 11.25.2 Leitura/Escrita Padrão no Databricks

##### Leitura de Delta Tables

```python
# PADRÃO 1: Ler tabela do catálogo (recomendado)
df = spark.table("catalog.schema.tabela")

# Exemplos:
clientes = spark.table("bronze.clientes")
vendas = spark.table("silver.vendas_processadas")

# PADRÃO 2: Ler de path
df = spark.read.format("delta").load("/mnt/data/vendas")

# PADRÃO 3: SQL
df = spark.sql("SELECT * FROM silver.vendas WHERE ano = 2024")

# PADRÃO 4: Time Travel (versões antigas)
df_ontem = spark.read.format("delta") \
    .option("versionAsOf", 1) \
    .load("/mnt/data/vendas")

df_semana_passada = spark.read.format("delta") \
    .option("timestampAsOf", "2024-01-13") \
    .load("/mnt/data/vendas")
```

##### Escrita de Delta Tables

```python
# PADRÃO 1: Criar/sobrescrever tabela managed
df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("silver.vendas_agregadas")

# PADRÃO 2: Append (adicionar dados)
df_novos.write \
    .format("delta") \
    .mode("append") \
    .saveAsTable("bronze.vendas_raw")

# PADRÃO 3: Merge (upsert) - MUITO COMUM
from delta.tables import DeltaTable

# Tabela destino
vendas_delta = DeltaTable.forName(spark, "silver.vendas")

# Merge (atualiza se existe, insere se não)
vendas_delta.alias("destino").merge(
    df_novos.alias("origem"),
    "destino.id_venda = origem.id_venda"  # Condição de match
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()

print("✅ Merge concluído")

# PADRÃO 4: Particionamento
df.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy("ano", "mes") \
    .saveAsTable("silver.vendas_particionadas")
```

##### Leitura de Arquivos (CSV, Parquet, JSON)

```python
# CSV
df_csv = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("/mnt/uploads/vendas.csv")

# Parquet
df_parquet = spark.read.parquet("/mnt/data/*.parquet")

# JSON
df_json = spark.read.json("/mnt/raw/logs/*.json")

# Múltiplos arquivos
df = spark.read.parquet(
    "/mnt/data/2024-01-01/*.parquet",
    "/mnt/data/2024-01-02/*.parquet"
)
```

##### Escrita para Compartilhamento

```python
# CSV para analistas (Excel, Power BI)
df.toPandas().to_csv("/dbfs/FileStore/reports/relatorio.csv", index=False)

# Link para download:
# https://<seu-workspace>.cloud.databricks.com/files/reports/relatorio.csv

# Excel (precisa instalar openpyxl)
df.toPandas().to_excel("/dbfs/FileStore/reports/relatorio.xlsx", index=False)

# Delta para outros notebooks
df.write.format("delta").mode("overwrite").save("/mnt/shared/analise_resultado")
```

#### 11.25.3 Cache e Performance no Databricks

##### Quando Usar Cache

```python
# USE cache quando vai reutilizar o DataFrame MÚLTIPLAS VEZES no mesmo notebook

# Exemplo SEM cache (ruim - relê 3x)
df_filtrado = vendas.filter(col("ano") == 2024)

analise1 = df_filtrado.groupBy("estado").count()  # Lê tudo
analise2 = df_filtrado.groupBy("produto").count()  # Lê tudo de novo
analise3 = df_filtrado.filter(col("valor") > 1000).count()  # Lê de novo

# Exemplo COM cache (bom)
df_filtrado = vendas.filter(col("ano") == 2024).cache()
df_filtrado.count()  # Materializa o cache

analise1 = df_filtrado.groupBy("estado").count()  # Rápido (memória)
analise2 = df_filtrado.groupBy("produto").count()  # Rápido
analise3 = df_filtrado.filter(col("valor") > 1000).count()  # Rápido

# SEMPRE limpe no final
df_filtrado.unpersist()
```

##### Display como Cache Implícito

```python
# DICA: display() NÃO mantém cache entre células
# Cada célula que usa o DataFrame vai reprocessar

# CÉLULA 1
df = vendas.filter(col("ano") == 2024)
display(df.limit(10))  # Processa uma vez

# CÉLULA 2
df.count()  # Processa TUDO de novo!

# SOLUÇÃO: Cache explícito
df = vendas.filter(col("ano") == 2024).cache()
df.count()  # Materializa

# CÉLULA 1
display(df.limit(10))  # Rápido

# CÉLULA 2
df.count()  # Rápido
```

##### Otimizações Databricks-Específicas

```python
# 1. Adaptive Query Execution (ativado por padrão)
# Spark otimiza automaticamente joins e agregações

# 2. Delta Cache (diferente de .cache())
# Databricks cacheia Delta Tables automaticamente em SSD local
# Você não precisa fazer nada, é automático

# 3. Z-Ordering (otimiza leitura de colunas frequentemente filtradas)
from delta.tables import DeltaTable

DeltaTable.forName(spark, "silver.vendas").optimize().executeZOrderBy("estado", "data_venda")

# Agora filtros por estado/data são MUITO mais rápidos
df = spark.table("silver.vendas").filter(col("estado") == "SP")  # ⚡ rápido

# 4. Autoloader (leitura incremental)
df = spark.readStream \
    .format("cloudFiles") \
    .option("cloudFiles.format", "json") \
    .schema(schema) \
    .load("/mnt/raw/vendas/")

df.writeStream \
    .format("delta") \
    .option("checkpointLocation", "/mnt/checkpoints/vendas") \
    .start("/mnt/bronze/vendas")
```

#### 11.25.4 Cuidados Comuns no Databricks

##### 1. Não Misturar Pandas e Spark Indiscriminadamente

```python
# ❌ RUIM: Converte tudo para Pandas (quebra memória)
df_spark = spark.table("vendas")  # 10 milhões de linhas
df_pandas = df_spark.toPandas()  # BOOM! Memória estoura
df_pandas.groupby("estado")["valor"].sum()

# ✅ BOM: Faz agregação no Spark, converte resultado pequeno
df_spark = spark.table("vendas")
agregado = df_spark.groupBy("estado").agg(sum("valor"))  # Resultado pequeno
agregado_pd = agregado.toPandas()  # OK, poucas linhas
```

##### 2. Cuidado com Collect()

```python
# ❌ RUIM: Traz tudo para o driver (quebra memória)
df = spark.table("vendas")  # 50 GB
linhas = df.collect()  # BOOM!

# ✅ BOM: Use limit ou sample
amostra = df.limit(1000).collect()  # OK
amostra_aleatoria = df.sample(0.01).collect()  # OK (1%)

# ✅ MELHOR: Use display()
display(df)  # Mostra amostra, DataFrame fica distribuído
```

##### 3. Sempre Libere Cache

```python
# ❌ RUIM: Cache "vaza" entre execuções
df.cache()
# ... faz análises ...
# esquece de unpersist()

# Próxima execução: memória do cluster vai encher!

# ✅ BOM: Sempre limpe
df.cache()
df.count()
# ... análises ...
df.unpersist()  # Libera memória

# ✅ MELHOR: Use try/finally
df = vendas.filter(...).cache()
df.count()

try:
    # Análises
    display(df.groupBy("estado").count())
finally:
    df.unpersist()  # Garante limpeza
```

##### 4. Não Sobrescreva Tabelas de Produção Sem Querer

```python
# ❌ PERIGO: Sobrescreve tabela de produção
df_teste.write \
    .mode("overwrite") \  # 💀 Apaga dados de produção!
    .saveAsTable("production.vendas")

# ✅ SEGURO: Use ambiente de DEV
df_teste.write \
    .mode("overwrite") \
    .saveAsTable("dev.vendas_teste")

# ✅ OU: Valide antes
if ambiente == "producao":
    raise ValueError("Não rode em produção sem aprovação!")
```

##### 5. Widgets com Validação

```python
# ❌ RUIM: Aceita qualquer valor
dbutils.widgets.text("data", "2024-01-01")
data = dbutils.widgets.get("data")
# E se alguém colocar "abc"? Quebra depois

# ✅ BOM: Valide
from datetime import datetime

data_str = dbutils.widgets.get("data")
try:
    data = datetime.strptime(data_str, "%Y-%m-%d")
    print(f"✅ Data válida: {data}")
except ValueError:
    raise ValueError(f"Data inválida: {data_str}. Use formato YYYY-MM-DD")
```

#### 11.25.5 Como Entregar Saída Analítica

##### 1. Para Analistas de Negócio (Excel/BI)

```python
# Opção A: CSV simples
resultado = vendas.groupBy("estado", "produto").agg(
    sum("valor").alias("receita"),
    count("*").alias("vendas")
).orderBy("receita", ascending=False)

# Salvar
resultado.toPandas().to_csv(
    "/dbfs/FileStore/reports/vendas_estado_produto.csv",
    index=False
)

# Compartilhar link:
print("📊 Relatório disponível em:")
print("https://<workspace>.cloud.databricks.com/files/reports/vendas_estado_produto.csv")

# Opção B: Excel com formatação
resultado_pd = resultado.toPandas()

with pd.ExcelWriter("/dbfs/FileStore/reports/vendas.xlsx", engine='openpyxl') as writer:
    resultado_pd.to_excel(writer, sheet_name="Vendas", index=False)
    
    # Formatar (opcional)
    worksheet = writer.sheets["Vendas"]
    worksheet.column_dimensions['A'].width = 15
    worksheet.column_dimensions['B'].width = 20

print("📊 Excel disponível em: /dbfs/FileStore/reports/vendas.xlsx")
```

##### 2. Para Cientistas de Dados (Delta Table)

```python
# Salvar como Delta para reutilização em modelos
resultado.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("gold.vendas_agregadas")

# Documentar
spark.sql("""
    COMMENT ON TABLE gold.vendas_agregadas IS 
    'Vendas agregadas por estado e produto. Atualizado diariamente às 3h.'
""")

print("✅ Tabela disponível: gold.vendas_agregadas")
print("📖 Use: spark.table('gold.vendas_agregadas')")
```

##### 3. Para Dashboards (BI Integration)

```python
# Power BI, Tableau etc conectam direto em Delta Tables

# Criar tabela otimizada para BI
resultado.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy("ano", "mes") \  # Facilita filtros de data
    .saveAsTable("bi.dashboard_vendas")

# Otimizar leitura
from delta.tables import DeltaTable
DeltaTable.forName(spark, "bi.dashboard_vendas") \
    .optimize() \
    .executeZOrderBy("estado", "produto")

print("✅ Tabela BI disponível: bi.dashboard_vendas")
print("📊 Configure conexão no Power BI:")
print("   Server: <workspace-url>")
print("   Database: bi")
print("   Table: dashboard_vendas")
```

##### 4. Para Executivos (Email Automatizado)

```python
# Enviar email com resumo (via SendGrid, SMTP, etc)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Calcular KPIs
kpis = vendas.agg(
    sum("valor").alias("receita_total"),
    count("*").alias("num_vendas"),
    avg("valor").alias("ticket_medio")
).collect()[0]

# Criar HTML
html = f"""
<html>
<body>
    <h2>Relatório de Vendas - {data_inicio} a {data_fim}</h2>
    <table border="1">
        <tr><th>Métrica</th><th>Valor</th></tr>
        <tr><td>Receita Total</td><td>R$ {kpis['receita_total']:,.2f}</td></tr>
        <tr><td>Número de Vendas</td><td>{kpis['num_vendas']:,}</td></tr>
        <tr><td>Ticket Médio</td><td>R$ {kpis['ticket_medio']:,.2f}</td></tr>
    </table>
    <p>Relatório completo: <a href="https://...">Link</a></p>
</body>
</html>
"""

# Enviar email (pseudocódigo)
# enviar_email(
#     to="executivos@empresa.com",
#     subject=f"Vendas {data_inicio} - {data_fim}",
#     html=html
# )

print("✅ Email enviado para executivos")
```

##### 5. Para Jobs Downstream (Parquet/Delta)

```python
# Salvar em formato consumível por outros jobs/pipelines

# Local centralizado
output_path = f"/mnt/analytics/vendas/processado/ano={ano}/mes={mes}/"

resultado.write \
    .format("delta") \
    .mode("overwrite") \
    .save(output_path)

# Registrar metadados
metadata = {
    "job": "analise_vendas",
    "data_processamento": current_date(),
    "linhas": resultado.count(),
    "path": output_path
}

print(f"✅ Dados salvos em: {output_path}")
print(f"📊 Metadados: {metadata}")

# Próximo job pode ler:
# df = spark.read.format("delta").load(output_path)
```

#### 11.25.6 Checklist Final: Notebook Databricks Profissional

Antes de compartilhar ou agendar seu notebook:

- [ ] **Documentação** clara no topo (objetivo, autor, inputs/outputs)?
- [ ] **Widgets** para parâmetros (datas, filtros)?
- [ ] **Células organizadas** (setup → leitura → análise → saída)?
- [ ] **Cache usado** estrategicamente e **liberado** no final?
- [ ] **Validações** de parâmetros e dados?
- [ ] **Saída clara** (CSV, Delta Table, email, dashboard)?
- [ ] **Erro handling** (try/except em operações críticas)?
- [ ] **Testado** com dados reais e edge cases?
- [ ] **Cleanup** de tabelas temporárias?
- [ ] **Comentários** em lógicas não-óbvias?

#### 11.25.7 Template Completo: Notebook Pronto para Produção

```python
# ============================================================
# CONFIGURAÇÃO INICIAL
# ============================================================

"""
# [TÍTULO DO PROJETO]

## Objetivo
[Descreva o que este notebook faz]

## Inputs
- Tabelas: bronze.vendas, silver.clientes
- Período: Parametrizável via widget

## Outputs
- Delta Table: gold.relatorio_vendas
- CSV: /dbfs/FileStore/reports/vendas_YYYY-MM-DD.csv

## Frequência
- Diário (executado via Job às 3h)

## Autor
- analytics@empresa.com
"""

from pyspark.sql.functions import *
from delta.tables import DeltaTable
import pandas as pd

# ============================================================
# WIDGETS (PARÂMETROS)
# ============================================================

dbutils.widgets.text("data_inicio", "2024-01-01")
dbutils.widgets.text("data_fim", "2024-01-31")

data_inicio = dbutils.widgets.get("data_inicio")
data_fim = dbutils.widgets.get("data_fim")

print(f"▶️  Executando análise para {data_inicio} até {data_fim}")

# ============================================================
# VALIDAÇÃO
# ============================================================

from datetime import datetime

try:
    dt_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
    dt_fim = datetime.strptime(data_fim, "%Y-%m-%d")
    assert dt_inicio <= dt_fim, "Data início deve ser <= data fim"
    print("✅ Parâmetros válidos")
except Exception as e:
    raise ValueError(f"Erro nos parâmetros: {e}")

# ============================================================
# LEITURA
# ============================================================

vendas = spark.table("bronze.vendas")
clientes = spark.table("silver.clientes")

print(f"📊 Vendas: {vendas.count():,} linhas")
print(f"👥 Clientes: {clientes.count():,} linhas")

# ============================================================
# PROCESSAMENTO
# ============================================================

vendas_periodo = vendas.filter(
    col("data_venda").between(data_inicio, data_fim)
).cache()

vendas_periodo.count()  # Materializa cache

vendas_enriquecidas = vendas_periodo.join(
    broadcast(clientes),
    "id_cliente",
    "left"
)

resultado = vendas_enriquecidas.groupBy("estado", "categoria_produto").agg(
    sum("valor").alias("receita"),
    count("*").alias("vendas"),
    avg("valor").alias("ticket_medio")
).orderBy("receita", ascending=False)

display(resultado)

# ============================================================
# SALVAMENTO
# ============================================================

# Delta Table
resultado.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold.relatorio_vendas")

# CSV para compartilhamento
resultado.toPandas().to_csv(
    f"/dbfs/FileStore/reports/vendas_{data_inicio}_{data_fim}.csv",
    index=False
)

# ============================================================
# LIMPEZA
# ============================================================

vendas_periodo.unpersist()

print("✅ Análise concluída com sucesso!")
```

---

**🎯 Você agora tem um guia completo:**

- ✅ Pandas para dados em memória
- ✅ SQL para pensamento tabular
- ✅ PySpark para big data
- ✅ Databricks para ambiente corporativo real

**Com isso, você cobre 95% dos cenários de análise de dados em empresas.**

---
