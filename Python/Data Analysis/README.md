# Manual Completo de Análise de Dados com Python, Pandas, Matplotlib e Seaborn

Este manual é pensado como **guia de bolso**: se você precisar fazer algo em análise de dados ("quero filtrar linhas", "quero ver correlação", "quero um gráfico de distribuição"), deve conseguir achar **um exemplo pronto** aqui.

- Cada seção diz **quando usar**, **para que serve** e **mostra o padrão de código**.
- Os exemplos são curtos, copiáveis e fáceis de adaptar.

---

## Mapa Rápido: "Quero Fazer X"

### Pandas (Dados em Memória)
- **Carregar dados** (CSV, Excel, JSON): veja **2.2 Importar e exportar dados**
- **Entender estrutura dos dados** (tipos, nulos, estatísticas): veja **2.1 Criar e inspecionar**
- **Filtrar linhas e colunas**: veja **2.3 Seleção, filtro e ordenação**
- **Criar colunas novas, tratar texto, categorias**: veja **2.4 Criar/transformar colunas**
- **Tratar valores faltantes (NaN)**: veja **2.5 Missing values**
- **Agrupar, somar, tirar média por grupo**: veja **2.6 Agregações e groupby**
- **Fazer tabela dinâmica (tipo Excel)**: veja **2.7 Tabelas dinâmicas (pivot)**
- **Juntar tabelas (joins)**: veja **2.8 Junções (merge)**
- **Trabalhar com datas e séries temporais**: veja **2.9 Datas e séries temporais**

### Visualização
- **Gráficos básicos, totalmente personalizados**: veja **3) Matplotlib**
- **Gráficos rápidos e bonitos para exploração**: veja **4) Seaborn**
- **Decidir qual gráfico usar**: veja **4.10 Galeria Completa: Qual Gráfico Usar Quando?**

### Receitas Práticas
- **Exemplos prontos de tarefas comuns**: veja **5) Receitas "Como fazer…"**

### Big Data
- **Processar grandes volumes (> 10GB)**: veja **6) PySpark para Big Data**
- **Exemplo completo de pipeline**: veja **6.21 Exemplo Completo: Análise de E-commerce**

---

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

### 2.1 Criar e inspecionar

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

## 3) Visualização com Matplotlib

**Quando usar Matplotlib:**

- Você quer **controle detalhado** de cada elemento do gráfico (eixos, legendas, anotações).
- Vai montar **figuras mais customizadas ou relatórios estáticos**.
- Seaborn usa Matplotlib por baixo; muitas vezes você combina ambos.

### 3.1 Primeiros passos

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

### 3.2 Tipos comuns

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

### 3.3 Subplots e personalização

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

### 3.4 Galeria Matplotlib: Gráficos Essenciais

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

## 4) Visualização com Seaborn (Guia Completo)

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

### 4.1 Gráficos relacionais (relplot, scatterplot, lineplot)

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

### 4.2 Gráficos categóricos (catplot, barplot, boxplot, violinplot)

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

### 4.3 Distribuições (displot, histplot, kdeplot, ecdfplot)

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

### 4.4 Regressão (lmplot, regplot, residplot)

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

### 4.5 Matriz de correlação e heatmap

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

### 4.6 Jointplot (bivariada com marginais)

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

### 4.7 Pairplot (matriz de dispersão)

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

### 4.8 Facetas (FacetGrid - pequenos múltiplos)

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

### 4.9 Paletas de cores e estilos

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

## 5) Receitas "Como Fazer…" (Guia por Exemplo)

### 5.1 Importar CSV grande com tipos corretos e datas

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

### 5.11 Gráfico de barras empilhadas

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

### 5.12 Gráfico de linha com área sombreada (intervalo de confiança)

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

### 5.13 Criar DataFrame de resumo estatístico customizado

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

### 5.14 Detectar e remover duplicatas

```python
# Ver duplicatas
duplicadas = df.duplicated(subset=['nome', 'cpf'], keep='first')
print(f"Encontradas {duplicadas.sum()} linhas duplicadas")

# Remover duplicatas
df_limpo = df.drop_duplicates(subset=['nome', 'cpf'], keep='first')

# Ver duplicatas completas (todas as colunas)
df_duplicatas_completas = df[df.duplicated(keep=False)]
```

### 5.15 Renomear colunas em lote

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

### 5.16 Filtrar por múltiplas condições com query

```python
# Sintaxe SQL-like (mais legível em filtros complexos)
filtrado = df.query('idade > 25 and salario >= 5000 and cidade in ["SP", "RJ"]')

# Equivalente com operadores
filtrado = df[(df['idade'] > 25) & (df['salario'] >= 5000) & (df['cidade'].isin(['SP', 'RJ']))]
```

### 5.17 Criar bins customizados e contar frequência

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

### 5.18 Transpor DataFrame (linhas ↔ colunas)

```python
df_transposto = df.T

# Pivot manual
pivot = df.pivot(index='data', columns='produto', values='quantidade')
```

### 5.19 Concatenar múltiplos DataFrames

```python
# Empilhar verticalmente (append)
df_total = pd.concat([df1, df2, df3], ignore_index=True)

# Lado a lado (horizontalmente)
df_junto = pd.concat([df1, df2], axis=1)

# Com chave de identificação
df_marcado = pd.concat([df1, df2], keys=['fonte_1', 'fonte_2'])
```

### 5.20 Gráfico de barras horizontais ordenado

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

### 5.2 Remover outliers simples (IQR)

**Para que serve:** excluir valores muito extremos antes de calcular médias/modelos.

```python
q1 = df['preco'].quantile(0.25)
q3 = df['preco'].quantile(0.75)
iqr = q3 - q1

mask = (df['preco'] >= q1 - 1.5 * iqr) & (df['preco'] <= q3 + 1.5 * iqr)
df_sem_outlier = df[mask]
```

### 5.3 Top N por grupo

**Exemplo:** top 2 produtos mais caros por cidade.

```python
top2 = (
  df
  .sort_values(['cidade', 'preco'], ascending=[True, False])
  .groupby('cidade')
  .head(2)
)
```

### 5.4 Percentual por categoria

**Exemplo:** participação (%) de cada cidade no total de registros.

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

### 5.8 Pairplot para explorar relações

```python
num_cols = ['idade', 'salario', 'gastos']
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

## 6) PySpark para Big Data

### 6.1 Quando usar PySpark?

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

### 6.2 Instalação e Configuração

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

### 6.3 Conceitos Fundamentais

- **SparkSession**: ponto de entrada para todas as funcionalidades do Spark.
- **DataFrame (Spark)**: tabela distribuída, similar ao Pandas mas processada em paralelo.
- **RDD (Resilient Distributed Dataset)**: estrutura de dados de baixo nível (raramente usada diretamente).
- **Transformações**: operações lazy (não executam imediatamente): `select`, `filter`, `groupBy`.
- **Ações**: operações que disparam execução: `show()`, `count()`, `collect()`.
- **Partições**: divisões dos dados para processamento paralelo.

### 6.4 Criar e Inspecionar DataFrames

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

### 6.5 Ler e Escrever Dados

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

### 6.6 Seleção, Filtro e Ordenação

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

### 6.7 Criar e Transformar Colunas

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

### 6.8 Agregações e GroupBy

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

### 6.9 Joins (Junções)

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

### 6.10 Datas e Séries Temporais

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

### 6.11 Window Functions (Funções de Janela)

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

### 6.12 SQL Queries (Consultas SQL)

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

### 6.13 Integração com Pandas

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

### 6.14 Performance e Otimização

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

### 6.15 Tratamento de Valores Nulos

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

### 6.16 UDFs (User Defined Functions)

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

### 6.17 Exemplo Completo: Pipeline de ETL

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

### 6.18 Diferenças Principais: Pandas vs PySpark

| Aspecto | Pandas | PySpark |
|---------|--------|---------|
| **Execução** | Em memória, single-thread | Distribuído, paralelo |
| **Tamanho de dados** | < 10 GB | GB, TB, PB |
| **Lazy evaluation** | Não (executa imediatamente) | Sim (monta plano, executa no final) |
| **Sintaxe** | `df['coluna']` | `col('coluna')` ou `df.coluna` |
| **Mutabilidade** | Mutável (altera in-place) | Imutável (retorna novo DF) |
| **Indexação** | `.loc`, `.iloc` | `filter`, `select` |
| **Conversão** | `spark_df.toPandas()` | `spark.createDataFrame(pandas_df)` |

### 6.19 Quando Migrar de Pandas para PySpark?

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

### 6.20 Recursos PySpark

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

### 6.21 Exemplo Completo: Análise de E-commerce com PySpark

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

## 7) Boas Práticas e Desempenho
