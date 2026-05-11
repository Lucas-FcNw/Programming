# Checklist de Entrega — Projeto Parte 2 (Teoria dos Grafos)

## Arquivos essenciais

- [x] Aplicação com menu textual: [projeto_grafo_menu.py](projeto_grafo_menu.py)
- [x] Arquivo no formato exigido: [grafo.txt](grafo.txt)
- [x] Gerador de `grafo.txt` a partir dos dados reais: [gerar_grafo_txt.py](gerar_grafo_txt.py)
- [ ] Relatório completo no template da disciplina (adicionar)

## Requisitos mínimos do grafo

- Vértices (UBSs): **71** (mínimo exigido: 70)
- Arestas: **215** (mínimo exigido: 180)
- Tipo atual no arquivo: **3** (não orientado com peso em vértice e aresta)

## Dados reais usados no estudo de caso

- [data/deinfosacadsau2014.csv](data/deinfosacadsau2014.csv)
- [data/evolucao_msp_pop_sexo_idade.csv](data/evolucao_msp_pop_sexo_idade.csv)

## Opções do menu (a-j)

A aplicação implementa exatamente:

- a) Ler `grafo.txt`
- b) Gravar `grafo.txt`
- c) Inserir vértice
- d) Inserir aresta
- e) Remover vértice
- f) Remover aresta
- g) Mostrar conteúdo do arquivo
- h) Mostrar grafo (lista de adjacência)
- i) Apresentar conexidade e reduzido
- j) Encerrar

## Como executar

1. Gerar/atualizar `grafo.txt`:
   - `/bin/python gerar_grafo_txt.py`
2. Rodar menu da aplicação:
   - `/bin/python projeto_grafo_menu.py`

## Observação de escopo

Esta entrega está focada somente no que a Parte 2 pede.
Elementos avançados do projeto (dashboard web, análises extras, etc.) não são necessários para a avaliação desta etapa.
