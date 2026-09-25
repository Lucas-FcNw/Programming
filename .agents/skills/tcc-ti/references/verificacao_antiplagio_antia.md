# Guia de Verificação Antiplágio e Anti-IA para TCC de T.I.

Este documento detalha as estratégias e técnicas para garantir que o TCC passe em verificações de plágio e detecção de IA.

---

## 1. VERIFICAÇÃO ANTIPLÁGIO

### 1.1 Ferramentas de Verificação

| Ferramenta | Tipo | Acesso | Observações |
|------------|------|--------|-------------|
| CopySpider | Gratuita | copyspider.com.br | Popular no Brasil, compara com web |
| Plagius | Paga (teste grátis) | plagius.com | Boa para português |
| Turnitin | Institucional | turnitin.com | Padrão internacional |
| Scribbr | Paga | scribbr.com | Baseada no Turnitin |
| iThenticate | Institucional | ithenticate.com | Usado por periódicos |
| MOSS (Stanford) | Gratuita | theory.stanford.edu/~aiken/moss/ | Específica para **código-fonte** |

### 1.2 Índices Aceitáveis de Similaridade
- **Até 15%**: Aceitável na maioria das instituições.
- **15-25%**: Zona de alerta — revisar trechos sinalizados.
- **Acima de 25%**: Inaceitável — necessita reescrita significativa.
- **Para código**: MOSS analisa similaridade estrutural, não textual. Percentuais variam conforme a linguagem.
- **Observação**: Citações diretas corretamente formatadas e referências bibliográficas frequentemente são contabilizadas. Algumas ferramentas permitem excluí-las.

### 1.3 Técnicas de Escrita Antiplágio

#### Paráfrase em 5 Passos:
1. **Ler** a fonte original completa (não apenas o trecho).
2. **Fechar** a fonte e esperar alguns minutos.
3. **Escrever** a ideia com suas próprias palavras, sem consultar a fonte.
4. **Comparar** com o original e ajustar se a estrutura ficou parecida.
5. **Citar** a fonte adequadamente.

#### Regras de Ouro:
- Nunca copiar mais de 3 palavras consecutivas da fonte sem aspas.
- Mudar a ordem das ideias na paráfrase.
- Usar sinônimos adequados (atenção: termos técnicos de T.I. NÃO devem ser trocados por sinônimos — "API RESTful" é "API RESTful", não "interface de programação com transferência de estado representacional").
- Combinar informações de múltiplas fontes em um mesmo parágrafo.
- Após parafrasear, fazer o "teste de leitura em voz alta".

#### Exemplo Prático:

**Fonte original (fictícia):**
> "Microsserviços são um estilo arquitetural que estrutura uma aplicação como uma coleção de serviços pequenos e autônomos, cada um executando em seu próprio processo e comunicando-se por mecanismos leves, geralmente APIs HTTP."

**❌ Paráfrase superficial (plágio disfarçado):**
> Microsserviços consistem em um estilo de arquitetura que organiza um aplicativo como um conjunto de serviços pequenos e independentes, cada um rodando em seu processo e se comunicando por meios leves, normalmente APIs HTTP (AUTOR, 2023).

**✅ Paráfrase genuína:**
> A arquitetura de microsserviços rompe com o modelo monolítico ao decompor o sistema em unidades de deploy independentes, cada qual responsável por uma capacidade de negócio específica. A comunicação entre essas unidades opera tipicamente sobre protocolos HTTP, embora alternativas como mensageria assíncrona (RabbitMQ, Apache Kafka) sejam adotadas quando a resiliência ao acoplamento temporal é prioritária (AUTOR, 2023; NEWMAN, 2021).

### 1.4 Antiplágio de Código-Fonte

O código apresentado no TCC deve ser **autoral**. Estratégias:

- **Não copiar código de tutoriais, Stack Overflow ou repositórios sem creditação.**
- Se inspirar-se em código de terceiros, **reescrever com lógica própria** e citar a inspiração.
- **Bibliotecas e frameworks não são plágio** — usar React, FastAPI, etc. é esperado. Plágio é copiar a lógica de negócio de outro projeto.
- **Boilerplates** gerados por ferramentas (create-react-app, cookiecutter) devem ser mencionados: "A estrutura inicial do projeto foi gerada com create-react-app v5.0".
- **Código gerado por IA**: Se a instituição permitir uso de IA como ferramenta auxiliar, declarar explicitamente. Se não permitir, todo código deve ser escrito manualmente.
- Usar **MOSS (Stanford)** para verificar similaridade de código com projetos anteriores de alunos.

---

## 2. VERIFICAÇÃO ANTI-IA

### 2.1 Ferramentas de Detecção de IA

| Ferramenta | Acesso | Eficácia em PT-BR | Observações |
|------------|--------|-------------------|-------------|
| GPTZero | gptzero.me | Moderada | Mais eficaz em inglês |
| Originality.ai | originality.ai | Boa | Detecta GPT, Claude, Gemini, etc. |
| ZeroGPT | zerogpt.com | Moderada | Gratuita |
| Copyleaks | copyleaks.com | Boa | Detecção + plágio |
| Sapling AI | sapling.ai/ai-content-detector | Limitada em PT-BR | Gratuita |
| Writer.com | writer.com/ai-content-detector | Limitada em PT-BR | Gratuita |

### 2.2 O Que as Ferramentas de Detecção Medem

1. **Perplexidade (Perplexity)**: O quanto o texto é "previsível". IA gera texto com perplexidade uniformemente baixa. Humanos variam mais.

2. **Burstiness**: Variação no comprimento e complexidade das frases. IA produz frases de comprimento uniforme. Humanos alternam entre curtas e longas.

3. **Entropia**: A distribuição de probabilidade das palavras. IA tende a escolher palavras de alta probabilidade consistentemente.

### 2.3 Estratégias para Garantir que o Texto Soe Humano

#### A. Variação Estrutural
```
PADRÃO DE IA (evitar):
- Parágrafo 1: [Tópico frasal] + [Desenvolvimento] + [Conclusão parcial]
- Parágrafo 2: [Tópico frasal] + [Desenvolvimento] + [Conclusão parcial]
- Parágrafo 3: [Tópico frasal] + [Desenvolvimento] + [Conclusão parcial]
(Todos com mesma extensão, mesma estrutura)

PADRÃO HUMANO (buscar):
- Parágrafo 1: Começa com dado estatístico, desenvolve com análise longa
- Parágrafo 2: Uma reflexão curta, três frases apenas
- Parágrafo 3: Citação direta seguida de análise extensa
- Parágrafo 4: Pergunta retórica + argumentação técnica
```

#### B. Variação de Início de Parágrafos
Nunca iniciar mais de 2 parágrafos consecutivos com a mesma estrutura gramatical.

**❌ Padrão de IA:**
> "A arquitetura de microsserviços permite..."
> "A utilização de containers Docker possibilita..."
> "A implementação de pipelines CI/CD garante..."
> "A adoção de bancos NoSQL oferece..."

**✅ Padrão humano:**
> "Quando o sistema atingiu 10.000 requisições simultâneas no teste de carga..."
> "Sob a perspectiva de Richardson (2018), esse nível de acoplamento..."
> "Houve, contudo, um obstáculo não previsto na fase de design..."
> "Na prática, a migração para microsserviços revelou-se mais complexa do que a literatura sugere."

#### C. Inserção de Elementos Humanos
- **Dados concretos e específicos**: "No benchmark executado em uma instância EC2 t3.medium, o tempo médio de resposta foi de 142ms..."
- **Problemas encontrados**: "Durante a implementação, a biblioteca X apresentou um bug conhecido (#4521) que exigiu contorno via..."
- **Referências ao contexto brasileiro**: Mercado de T.I., LGPD, e-Gov, startups nacionais, dados do IBGE sobre acesso à internet.
- **Decisões com trade-offs**: "Optou-se por PostgreSQL em vez de MongoDB porque, apesar do menor throughput em operações de escrita..."
- **Limitações admitidas**: "Reconhece-se que a amostra de 12 participantes limita a generalização..."
- **Perguntas reflexivas** (na discussão): "Seria viável escalar esta abordagem para redes com mais de 500 endpoints?"

#### D. Complexidade Sintática Variada
Misturar:
- Frases simples (sujeito + verbo + complemento)
- Frases compostas coordenadas
- Frases compostas subordinadas
- Frases intercaladas com apostos e orações parentéticas
- Períodos longos com múltiplas orações

#### E. Vocabulário
- Usar palavras menos comuns quando adequado, sem forçar erudição.
- Termos técnicos em inglês são NORMAIS em T.I. — usá-los com naturalidade (em itálico na primeira ocorrência).
- Manter consistência de registro: não alternar entre ultra-formal e casual.
- Nível esperado: estudante de graduação com bom domínio técnico, não um professor titular com 30 anos de carreira.

### 2.4 Checklist Anti-IA (Verificação Manual)

Antes de finalizar cada seção, perguntar-se:

- [ ] As frases deste parágrafo variam entre 8 e 35 palavras?
- [ ] Os parágrafos variam entre 3 e 15 linhas?
- [ ] Os inícios de parágrafo são todos diferentes?
- [ ] Há pelo menos uma frase "inesperada" por página (problema real, dado de benchmark, opinião, pergunta)?
- [ ] O texto contém referências geográficas ou contextuais específicas?
- [ ] Há posicionamento crítico do autor (não apenas compilação)?
- [ ] O nível de linguagem é consistente com um estudante de graduação?
- [ ] As transições entre parágrafos são naturais (não mecânicas)?
- [ ] O texto foi lido em voz alta sem soar "robótico"?
- [ ] Termos técnicos de T.I. estão em itálico na primeira ocorrência?

---

## 3. PROTOCOLO DE REVISÃO FINAL

### Passo 1: Revisão de Conteúdo
- O texto responde ao problema de pesquisa?
- Os objetivos foram alcançados?
- As conclusões são sustentadas pelos resultados?
- O código funciona e está testado?

### Passo 2: Revisão Antiplágio
- Submeter texto a pelo menos UMA ferramenta de detecção de plágio.
- Submeter código a MOSS (se a instituição fornecer acesso).
- Revisar e reescrever trechos com similaridade > 15%.
- Confirmar que todas as citações estão corretamente formatadas.
- Verificar que código de terceiros está creditado.

### Passo 3: Revisão Anti-IA
- Submeter a pelo menos DUAS ferramentas de detecção de IA.
- Se algum trecho for sinalizado, reescrever aplicando as estratégias da seção 2.3.
- Pedir para uma pessoa (colega, orientador) ler trechos específicos.

### Passo 4: Revisão Linguística
- Ortografia e gramática (usar corretor + revisão manual).
- Coesão (conectivos, referenciação, progressão temática).
- Coerência (lógica argumentativa, ausência de contradições).
- Adequação ao registro acadêmico.
- Termos em inglês em itálico.
- Siglas definidas na primeira ocorrência.

### Passo 5: Revisão Técnica
- Todo código no TCC compila/executa.
- Diagramas estão consistentes com o código.
- Referências a versões de software estão atualizadas.
- Screenshots correspondem à versão final do sistema.
- Testes passam e cobertura atende ao mínimo definido.

### Passo 6: Revisão de Formatação
- Conferir TODAS as normas ABNT (ver references/templates_abnt.md).
- Numeração de páginas, figuras, tabelas, códigos.
- Lista de referências vs. citações no texto (bidirecional).
- Código formatado com fonte monoespaçada, tamanho 10.

### Passo 7: Revisão com o Orientador
- Submeter ao orientador para feedback.
- Incorporar sugestões.
- Não alterar decisões já aprovadas sem consulta.
