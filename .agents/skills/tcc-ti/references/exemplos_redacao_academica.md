# Exemplos de Redação Acadêmica — Material de Estrutura e Estilo

> **AVISO ESSENCIAL**
>
> Este arquivo contém **exclusivamente modelos de estrutura e estilo acadêmico**.
>
> - Todos os autores, títulos, números, resultados, métricas, datas, nomes de projetos e dados presentes neste arquivo são **placeholders** representados por `[COLCHETES]`.
> - Não há referências reais. Não há dados reais. Não há resultados reais.
> - Nenhum elemento deste arquivo deve ser copiado, adaptado ou utilizado como dado, fonte ou resultado no TCC do Rede de Acesso SP.
> - Use este arquivo apenas para aprender **como construir argumento, estrutura e linguagem acadêmica**.
>
> **Antes de qualquer citação no TCC:** verificar a referência real em base acadêmica (Scopus, IEEE, ACM, etc.).

---

## SUMÁRIO

1. Introdução — como construir o argumento inicial
2. Referencial Teórico — como apresentar conceitos e analisar fontes
3. Trabalhos Relacionados — como construir quadro comparativo e GAP
4. Metodologia — como descrever método e ambiente
5. Código — como contextualizar implementação dentro do artigo
6. Resultados e Discussão — como apresentar e interpretar dados reais
7. Considerações Finais — como articular conclusão com objetivos
8. Transformação: manual de sistema → artigo científico
9. Modelagem Formal — como formalizar matematicamente antes do código
10. ETL — como documentar proveniência de dados
11. GAP — como redigir o parágrafo comparativo
12. Conectivos e expressões variadas
13. Expressões a evitar

---

## 1. COMO CONSTRUIR O ARGUMENTO DE INTRODUÇÃO

### Padrão a evitar

> A tecnologia da informação é muito importante no mundo atual. Nesse contexto, os sistemas computacionais desempenham um papel crucial. É importante ressaltar que o desenvolvimento de software evolui rapidamente. Diante do exposto, este trabalho propõe um sistema.

**Problema:** genérico, sem dados, sem posicionamento, sem problema real.

---

### Padrão recomendado — estrutura com placeholders

> [DADO CONCRETO E VERIFICADO sobre o problema — ex: volume de demanda, déficit de cobertura, lacuna operacional]. Esse cenário contrasta com [SITUAÇÃO EXISTENTE QUE NÃO RESOLVE O PROBLEMA]. Soluções existentes como [CATEGORIA DE SOLUÇÃO CONHECIDA] apresentam [LIMITAÇÃO ESPECÍFICA], o que as torna inadequadas para [CONTEXTO ESPECÍFICO DO PROJETO] (REFERÊNCIA VERIFICADA, ANO).
>
> Diante dessa lacuna, este trabalho propõe [NOME DO SISTEMA/ABORDAGEM], que [DESCRIÇÃO TÉCNICA OBJETIVA DO QUE O SISTEMA FAZ]. O objetivo geral é [OBJETIVO GERAL EM INFINITIVO]. Os objetivos específicos compreendem: (a) [OBJETIVO A]; (b) [OBJETIVO B]; (c) [OBJETIVO C].

**Por que funciona:** dado verificado, problema delimitado, limitação das soluções existentes nomeada, solução proposta descrita objetivamente, objetivos específicos.

---

## 2. COMO APRESENTAR CONCEITOS NO REFERENCIAL TEÓRICO

### Padrão a evitar

> Grafos são estruturas de dados muito utilizadas. Um grafo tem vértices e arestas. O algoritmo de Dijkstra é amplamente utilizado para calcular caminhos mínimos.

**Problema:** descritivo, superficial, sem análise, sem conexão com o projeto.

---

### Padrão recomendado — análise crítica com conexão ao projeto

> O problema de [NOME DO PROBLEMA] pode ser modelado como [CONCEITO FORMAL]. Formalmente, [AUTOR VERIFICADO] ([ANO]) define [CONCEITO] como [DEFINIÇÃO]. Essa formulação é relevante para o presente trabalho porque [RAZÃO ESPECÍFICA LIGADA AO PROJETO].
>
> Contudo, a abordagem de [MÉTODO A] difere de [MÉTODO B] em aspectos relevantes ao contexto deste projeto. Enquanto [MÉTODO A] [CARACTERÍSTICA A], [MÉTODO B] [CARACTERÍSTICA B] — distinção que incide diretamente sobre [ASPECTO DO PROJETO] (REFERÊNCIA VERIFICADA, ANO). A escolha de [MÉTODO ADOTADO] fundamenta-se em [JUSTIFICATIVA TÉCNICA].

**Por que funciona:** apresenta o conceito com definição formal, conecta imediatamente ao problema, compara alternativas com razão técnica e cita fontes verificadas.

---

## 3. COMO CONSTRUIR TRABALHOS RELACIONADOS

### Estrutura do quadro comparativo

```
Quadro [N] — Comparação entre trabalhos relacionados e a proposta

+------------------+----------+----------+----------+----------+
| Critério         | [AUTOR1] | [AUTOR2] | [AUTOR3] | Proposta |
|                  |  ([ANO]) |  ([ANO]) |  ([ANO]) |          |
+------------------+----------+----------+----------+----------+
| [CRITÉRIO 1]     | [VALOR]  | [VALOR]  | [VALOR]  | [VALOR]  |
| [CRITÉRIO 2]     | [VALOR]  | [VALOR]  | [VALOR]  | [VALOR]  |
| [CRITÉRIO 3]     | Sim/Não  | Sim/Não  | Sim/Não  | Sim/Não  |
| [CRITÉRIO 4]     | [VALOR]  | [VALOR]  | [VALOR]  | [VALOR]  |
+------------------+----------+----------+----------+----------+

Fonte: Elaborado pelo autor ([ANO]).
Nota: critérios selecionados conforme relevância ao problema de pesquisa.
```

**AVISO:** `[AUTOR1]`, `[AUTOR2]`, `[AUTOR3]` devem ser autores reais verificados antes de inserir no TCC.

---

### Como redigir a análise após o quadro

> Conforme evidenciado no Quadro [N], [AUTOR1] ([ANO]) e [AUTOR2] ([ANO]) abordam [ASPECTO COMUM], mas divergem em [ASPECTO QUE DIFERE]. O trabalho de [AUTOR3] ([ANO]) é o que mais se aproxima da abordagem proposta, ao [SIMILARIDADE], porém não contempla [LIMITAÇÃO ESPECÍFICA DO TRABALHO RELACIONADO].
>
> O presente estudo diferencia-se ao [DESCRIÇÃO DA CONTRIBUIÇÃO ESPECÍFICA]. Essa combinação, com base na revisão realizada, não foi encontrada nos trabalhos analisados — embora reconheça-se que a revisão não é exaustiva.

**Por que funciona:** cita autores reais verificados, identifica similaridades e diferenças específicas, posiciona a contribuição de forma proporcional e honesta sobre os limites da revisão.

---

## 4. COMO ESCREVER A METODOLOGIA

### Estrutura com placeholders

> ### [N].1 Classificação da pesquisa
>
> Este trabalho caracteriza-se como pesquisa de natureza [NATUREZA: aplicada/básica], com abordagem [ABORDAGEM: quantitativa/qualitativa/mista] e objetivos [TIPO: exploratório/descritivo/explicativo]. Quanto aos procedimentos técnicos, adota-se [METODOLOGIA] ([REFERÊNCIA VERIFICADA, ANO]). Essa escolha justifica-se por [RAZÃO TÉCNICA LIGADA AO PROJETO].
>
> ### [N].2 Método de desenvolvimento
>
> O desenvolvimento do sistema seguiu [MÉTODO ADOTADO: descrever]. [DESCREVER AS ETAPAS E DECISÕES ADOTADAS NO PROJETO REAL].
>
> ### [N].3 Ferramentas e tecnologias
>
> O Quadro [N] apresenta as tecnologias utilizadas no desenvolvimento.
>
> | Componente | Tecnologia | Versão | Justificativa |
> |---|---|---|---|
> | [COMPONENTE] | [TECNOLOGIA VERIFICADA] | [VERSÃO VERIFICADA] | [RAZÃO TÉCNICA] |
>
> Fonte: Elaborado pelo autor ([ANO]).
>
> ### [N].4 Métricas de avaliação
>
> A avaliação do sistema foi conduzida em [DESCREVER EIXOS DE AVALIAÇÃO]. Para [EIXO 1], utilizou-se [MÉTRICA], calculada sobre [DADOS UTILIZADOS]. Para [EIXO 2], adotou-se [MÉTRICA] — escolha justificada por [RAZÃO].

**AVISO:** versões de tecnologias devem ser verificadas no código ou documentação do projeto antes de inserir.

---

## 5. COMO APRESENTAR CÓDIGO NO TCC

### Padrão a evitar

> O Código [N] mostra a implementação da função principal.
>
> ```python
> def calcular():
>     # faz o cálculo
>     return resultado
> ```
>
> O código funciona corretamente.

**Problema:** sem contexto, sem análise, sem relação com a metodologia ou hipótese.

---

### Padrão recomendado — código como elemento do experimento

> O [NOME DO MÓDULO] é responsável por [DESCREVER FUNÇÃO NO SISTEMA]. Sua implementação está diretamente relacionada ao [OBJETIVO/REQUISITO ESPECÍFICO], pois [EXPLICAÇÃO DO PORQUÊ].
>
> O Código [N] apresenta [DESCREVER O QUE O TRECHO FAZ]. Dois aspectos merecem destaque técnico: (a) [DECISÃO DE IMPLEMENTAÇÃO A] — motivada por [RAZÃO]; (b) [DECISÃO DE IMPLEMENTAÇÃO B] — adotada em conformidade com [REFERÊNCIA OU PADRÃO VERIFICADO].
>
> ```python
> # [TRECHO DE CÓDIGO REAL DO PROJETO, COM COMENTÁRIOS]
> ```
> Fonte: Elaborado pelo autor ([ANO]).
>
> A escolha de [ESTRUTURA/ALGORITMO/PADRÃO] em detrimento de [ALTERNATIVA] baseia-se em [JUSTIFICATIVA TÉCNICA]. Essa decisão impacta diretamente [ASPECTO DO SISTEMA] conforme demonstrado em [REFERÊNCIA VERIFICADA, ANO].
>
> [SE MEDIDO: No ambiente de teste [DESCREVER], a execução completou em [TEMPO MEDIDO] para [ENTRADA DESCRITA]. | SE NÃO MEDIDO: [RESULTADO PENDENTE: descrever como o desempenho será avaliado]]

**Por que funciona:** contextualiza o código no problema, explica decisões com razão técnica, cita padrões ou referências verificadas, apresenta dados de desempenho apenas quando medidos.

---

## 6. COMO APRESENTAR RESULTADOS E DISCUSSÃO

### Padrão a evitar

> Os resultados foram muito bons. O sistema funcionou corretamente em todos os testes. O tempo de resposta foi satisfatório. Portanto, o objetivo foi alcançado.

**Problema:** sem dados, sem análise, sem comparação, sem ligação com a hipótese/questão.

---

### Padrão recomendado — resultados reais com interpretação

> ### [N].1 [NOME DO EIXO DE AVALIAÇÃO]
>
> [DESCREVER O EXPERIMENTO REALIZADO: ambiente, dados usados, procedimento]. A Tabela [N] apresenta os resultados obtidos.
>
> | Métrica | [CONDIÇÃO 1] | [CONDIÇÃO 2] | [CONDIÇÃO 3] |
> |---|---|---|---|
> | [MÉTRICA 1] | [VALOR MEDIDO] | [VALOR MEDIDO] | [VALOR MEDIDO] |
> | [MÉTRICA 2] | [VALOR MEDIDO] | [VALOR MEDIDO] | [VALOR MEDIDO] |
>
> Fonte: Dados da pesquisa ([ANO]).
>
> Os resultados revelam [PADRÃO OBSERVADO]. [VALOR/CONDIÇÃO] apresentou [CARACTERÍSTICA], o que [INTERPRETAÇÃO TÉCNICA]. Esse comportamento converge com o que [REFERÊNCIA VERIFICADA, ANO] aponta sobre [CONCEITO RELACIONADO].
>
> Não obstante, [LIMITAÇÃO OBSERVADA] constitui uma restrição a ser considerada. [RAZÃO TÉCNICA DA LIMITAÇÃO]. Em trabalhos futuros, [DIREÇÃO POSSÍVEL].

**AVISO:** `[VALOR MEDIDO]` deve ser preenchido exclusivamente com dados reais obtidos no projeto. Nunca com estimativas ou valores plausíveis.

---

## 7. COMO ESCREVER AS CONSIDERAÇÕES FINAIS

### Estrutura com placeholders

> Este trabalho propôs [DESCRIÇÃO OBJETIVA DO QUE FOI DESENVOLVIDO]. O objetivo geral — [RETOMAR O OBJETIVO GERAL] — foi [alcançado/parcialmente alcançado/não alcançado], com as ressalvas descritas a seguir.
>
> Os objetivos específicos foram [DESCREVER O STATUS DE CADA UM]:
> - [OBJETIVO A]: [COMO FOI ALCANÇADO, COM BASE NOS RESULTADOS REAIS].
> - [OBJETIVO B]: [COMO FOI ALCANÇADO].
> - [OBJETIVO C]: [COMO FOI ALCANÇADO OU JUSTIFICATIVA DE NÃO ALCANCE].
>
> Reconhece-se que [LIMITAÇÃO 1] constitui uma restrição do presente trabalho. Além disso, [LIMITAÇÃO 2]. [LIMITAÇÃO 3]. Essas limitações delimitam o escopo de generalização dos resultados.
>
> Como trabalhos futuros, identificam-se [N] direções: (a) [DIREÇÃO A], que permitiria [BENEFÍCIO TÉCNICO]; (b) [DIREÇÃO B]; (c) [DIREÇÃO C].

**Por que funciona:** retoma objetivos de forma específica, informa o status com base em resultados reais, declara limitações com honestidade, propõe futuros com justificativa.

---

## 8. TRANSFORMAÇÃO: MANUAL DE SISTEMA → ARTIGO CIENTÍFICO

### Escrita de manual (a evitar no TCC)

> ### Funcionalidade de Recomendação
>
> Para obter uma recomendação, o usuário deve ativar a geolocalização no dispositivo. O sistema exibe uma lista de UBSs próximas ordenadas por distância. O usuário pode clicar em qualquer UBS para ver mais detalhes.

**Problema:** descreve como usar, não como o sistema resolve o problema científico.

---

### Escrita de artigo científico (buscar)

> ### [N] Módulo de Recomendação e sua Relação com [OBJETIVO/REQUISITO]
>
> O módulo de recomendação é o elemento central que materializa a resposta à questão de pesquisa proposta. Ele recebe [ENTRADA], aplica [ALGORITMO/MODELO REAL IMPLEMENTADO] e produz [SAÍDA]. A escolha de [DECISÃO TÉCNICA] em detrimento de [ALTERNATIVA] fundamenta-se em [RAZÃO TÉCNICA VERIFICADA].
>
> [DESCREVER O FUNCIONAMENTO COM CONEXÃO AO PROBLEMA]. Essa abordagem é coerente com [REFERÊNCIA VERIFICADA, ANO], que demonstra [ASPECTO RELEVANTE]. A diferença em relação a [TRABALHO RELACIONADO] reside em [DISTINÇÃO ESPECÍFICA].
>
> [SE AVALIADO: Os resultados dessa implementação são apresentados na Seção [N]. | SE PENDENTE: [RESULTADO PENDENTE: descrever como será avaliado]]

**Por que funciona:** o módulo é descrito em função de sua relação com o problema de pesquisa, não como funcionalidade para o usuário.

---

## 9. COMO FORMALIZAR MATEMATICAMENTE ANTES DO CÓDIGO

### Estrutura com placeholders

> ### [N] Formalização do Problema
>
> O problema de [NOME DO PROBLEMA] pode ser modelado como [CLASSE DO PROBLEMA: ex. problema de caminho mínimo, problema de localização, problema multicritério]. Formalmente:
>
> Seja G = ([V], [E], [FUNÇÃO DE PESO]) um grafo [TIPO: direcionado/não-direcionado] onde:
> - [V] = {v₁, v₂, ..., vₙ} é o conjunto de nós representando [O QUE REPRESENTA — confirmar no código];
> - [E] ⊆ [V] × [V] é o conjunto de arestas representando [O QUE REPRESENTA — confirmar no código];
> - w: [E] → ℝ⁺ é a função peso das arestas, onde w(eᵢⱼ) corresponde a [O QUE O PESO REPRESENTA — confirmar].
>
> [SE HOUVER ATRIBUTOS DE VÉRTICE: Adicionalmente, cada vértice vᵢ possui o atributo [ATRIBUTO] = [O QUE REPRESENTA]]
>
> O objetivo é [DESCREVER O OBJETIVO FORMAL DO ALGORITMO].
>
> Esse problema pertence à classe [CLASSE FORMAL], cuja complexidade é [COMPLEXIDADE CONHECIDA] ([REFERÊNCIA VERIFICADA, ANO]). A escolha de [ALGORITMO] fundamenta-se em [PROPRIEDADES DO PROBLEMA QUE JUSTIFICAM A ESCOLHA].

**AVISO:** `|V|`, `|E|`, tipo do grafo, função de peso, atributos de vértice — todos devem ser preenchidos com valores confirmados no código (categoria A), não estimados.

---

## 10. COMO DOCUMENTAR PROVENIÊNCIA DE DADOS (ETL)

### Quadro de fontes de dados

```
Quadro [N] — Fontes de dados utilizadas

+----+------------------------+---------------+------------+--------+--------+
| #  | Fonte                  | Tipo de Acesso| Data de    | Volume | Formato|
|    |                        |               | Extração   | Bruto  |        |
+----+------------------------+---------------+------------+--------+--------+
| 1  | [NOME REAL DA FONTE]   | [TIPO REAL]   | [DATA REAL]| [REAL] | [REAL] |
| 2  | [NOME REAL DA FONTE]   | [TIPO REAL]   | [DATA REAL]| [REAL] | [REAL] |
+----+------------------------+---------------+------------+--------+--------+

Fonte: Elaborado pelo autor ([ANO]).
```

**AVISO:** todos os campos devem ser preenchidos com valores reais do projeto.

---

### Como descrever o tratamento de dados

> A etapa de transformação envolveu os seguintes procedimentos:
>
> 1. **Dados nulos:** identificados [N REAL] registros com [CAMPO] nulo ([PERCENTUAL REAL]%). Esses registros foram [TRATAMENTO ADOTADO], seguindo a abordagem de [REFERÊNCIA VERIFICADA, ANO]. A alternativa de [OUTRA ABORDAGEM] foi descartada porque [RAZÃO].
>
> 2. **Outliers:** identificados [N REAL] registros com [CONDIÇÃO]. Após inspeção, [N REAL] foram mantidos por [RAZÃO] e [N REAL] foram removidos por [RAZÃO].
>
> 3. **Normalização de coordenadas:** [DESCREVER O QUE FOI FEITO, SE FOI FEITO — confirmar no código].
>
> **Limitações conhecidas dos dados:**
> - [LIMITAÇÃO REAL 1]
> - [LIMITAÇÃO REAL 2]
> - [LIMITAÇÃO REAL 3]

**AVISO:** valores entre colchetes devem ser preenchidos com dados reais. Nunca estimar percentuais ou contagens.

---

## 11. COMO REDIGIR O PARÁGRAFO DE GAP

### Padrão a evitar

> Nenhum trabalho na literatura combina algoritmos de grafo com dados populacionais para recomendação de UBSs. Portanto, esta pesquisa é pioneira.

**Problema:** afirmação absoluta sem revisão suficiente.

---

### Padrão recomendado — GAP comparativo

> A análise dos trabalhos relacionados, sintetizada no Quadro [N], evidencia que [ASPECTO COMUM DOS TRABALHOS]. Em particular, [TRABALHO VERIFICADO A] e [TRABALHO VERIFICADO B] abordam [ASPECTO COMPARTILHADO], mas limitam-se a [LIMITAÇÃO ESPECÍFICA] — o que impede [CONSEQUÊNCIA RELEVANTE AO PROBLEMA DESTE PROJETO].
>
> [TRABALHO VERIFICADO C], por sua vez, é o que mais se aproxima da abordagem proposta, ao [SIMILARIDADE]. Contudo, [LIMITAÇÃO DESSE TRABALHO].
>
> O presente estudo propõe [DESCRIÇÃO DA CONTRIBUIÇÃO] como forma de suprir [LACUNA ESPECÍFICA IDENTIFICADA]. Essa combinação não foi encontrada nos trabalhos analisados — com a ressalva de que a revisão, embora sistemática, não é exaustiva.

**Por que funciona:** identifica lacunas específicas com base em trabalhos reais, nomeia os trabalhos, não faz afirmações absolutas, e reconhece os limites da revisão.

---

## 12. CONECTIVOS VARIADOS PARA USO NO TCC

Em vez de repetir os mesmos conectivos, variar conforme o contexto:

**Adição:** além disso, ademais, acresce-se, soma-se a isso, de igual modo

**Contraste:** entretanto, contudo, todavia, no entanto, em contrapartida, ao passo que, por outro lado

**Causa:** porquanto, visto que, uma vez que, em virtude de, dado que, em razão de

**Consequência:** por conseguinte, de modo que, em decorrência, como resultado, dessa forma

**Exemplificação:** a título de exemplo, como ilustração, conforme observado em, tal como demonstrado por

**Conclusão:** em síntese, ante o exposto, em face do argumentado, por todo o demonstrado

**Ênfase:** sobretudo, especialmente, particularmente, notadamente

**Concessão:** ainda que, mesmo que, conquanto, a despeito de, não obstante

**Sequência:** subsequentemente, em um segundo momento, na sequência

---

## 13. EXPRESSÕES A EVITAR E ALTERNATIVAS

| Evitar | Alternativa |
|---|---|
| "É importante ressaltar que" | "Merece atenção o fato de que" / "Cabe observar que" |
| "Nesse contexto" (repetido) | "Nesse cenário" / "Sob essa perspectiva" / "Nessa conjuntura" |
| "Vale destacar" | "Convém salientar" / "Um aspecto relevante é" |
| "Diante do exposto" | "Ante o argumentado" / "Em face do apresentado" |
| "Extremamente importante" | "Central para" / "Determinante em" |
| "É fundamental" | "Constitui requisito" / "Mostra-se essencial" |
| "Desempenha um papel crucial" | "Contribui de forma decisiva para" / "Incide diretamente em" |
| "Ampla gama de" | "Diversas" / "Múltiplas" / "Variadas" |
| "Robusto" (em excesso) | "Consistente" / "Sólido" / "Confiável" |
| "Não se pode negar que" | Reformular com afirmação direta |
| "O sistema garante atendimento mais rápido" | "O sistema apoia a identificação de UBSs mais próximas" |
| "A UBS com maior população é mais sobrecarregada" | "A população da área é utilizada como proxy de demanda potencial" |
| "O método demonstrou superioridade" | "O método foi implementado e avaliado sob [condições descritas]" |

---

## NOTA FINAL SOBRE ESTE ARQUIVO

Este arquivo ensina **como construir argumentos acadêmicos**. Ele não fornece:
- Autores reais para citar.
- Resultados reais para usar.
- Dados do projeto para copiar.
- Referências para a bibliografia.

Qualquer referência bibliográfica usada no TCC deve ser verificada de forma independente nas bases acadêmicas (Scopus, IEEE Xplore, ACM Digital Library, Portal CAPES, SciELO).

Qualquer dado numérico no TCC deve ter origem rastreável ao código, dataset, documentação ou experimento real do projeto Rede de Acesso SP.
