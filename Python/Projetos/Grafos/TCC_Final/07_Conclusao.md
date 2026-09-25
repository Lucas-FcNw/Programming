# 7. CONCLUSÕES E TRABALHOS FUTUROS

O presente Trabalho de Conclusão de Curso executou uma imersão profunda na engenharia de algoritmos visando preencher uma lacuna endêmica na gestão primária da capital. Diferindo-se tangencialmente das rotas concebidas sob a ótica da prancheta orçamentária do governante, "Rede de Acesso SP" empodera o cidadão no epicentro do Sistema Único de Saúde, municiando a tomada de decisão em cenários agudos não agendados através de complexidade matemática pura e escalável.

## 7.1 Síntese do Artefato Metodológico

As abstrações de Grafos Clássicos comprovaram total superioridade analítica ao unificar a topologia do espaço urbano metropolitano sob a ótica mista. A formatação de vértices ($V$) detentores das sobrecargas populacionais da Área de Abrangência — importadas pela malha do CEINFO e microdados Censitários 2022 (IBGE) — revelou disparidades aterrorizantes, onde postos fronteiriços recebem encargos habitacionais até 10 vezes inferiores àqueles dispostos no epicentro. 

O arcabouço computacional demonstrou excelência inconteste: rechaçou-se o peso computacional predatório de Matrizes Densas a favor de Listas de Adjacência para abraçar a densidade pífia do Grafo ($D \approx 0.0865$). Na mesma esteira, o confinamento temporal $\mathcal{O}((|V| + |E|) \log |V|)$ ofertado pelas Estruturas em *Min-Heap* no miolo do algoritmo de Dijkstra esmagou as exigências de processamento. Atingiu-se o nirvana arquitetural de $115$ ms (na cauda percentil de $95\%$) mesmo sob saraivadas destrutivas de 100.000 requisições randômicas. E por fim, o postulado científico que cravava a vitória esmagadora do percurso inteligente foi sacramentado: evidenciou-se a viabilidade suprema de evitar dezenas de milhares de habitantes na disputa local de leitos ao trânsitar poucos quarteirões adicionais nas intersecções poligonais.

## 7.2 Limitações Declaradas da Pesquisa

Nenhum artefato acadêmico subsiste sem a admissão de viés, particularmente aqueles baseados no dinamismo indomável do espaço geográfico intra-urbano:
*   A fonte da verdade repousa sobre a rigidez das estatísticas. Dados extraídos por IBGE representam cortes estáticos. O peso do vértice não absorve a migração pendular diurna para centros trabalhistas. Em essência, a métrica avalia o estrangulamento demográfico passivo, não monitorando as filas dinâmicas de recepção daquele milissegundo de atendimento.
*   Em consonância a esse fenômeno, a invisibilidade demográfica de cidadãos não mapeados em setores fixos (comunidades recentes não legalizadas e extrema marginalização de pessoas em situação de rua) acarreta o subdimensionamento do $w_v$ nos vértices críticos no entorno central de São Paulo.

## 7.3 Perspectivas para Trabalhos Futuros

As bases sólidas deixadas por este *software* instigam futuras linhas de experimentação interdisciplinar, permitindo o escopo das pesquisas nos anos vindouros por meio de:
1.  **Enriquecimento das Arestas em Tempo Real:** Abandonar as medidas geocartográficas unicamente baseadas na quilometragem em linha, substituindo as integrações do vetor $w_e$ por interfaces de Programação API (como Waze SDK), convertendo as arestas do Grafo numa variável flutuante sensível à imprevisibilidade dos alagamentos, greves ou bloqueios viários.
2.  **Machine Learning Estocástico (Previsão Sazonal):** Substituir a carga habitacional estática dos vértices implementando topologias acopladas em *Long Short-Term Memory* (Redes Neurais LSTM). O peso $w_v$ passaria a oscilar de modo cíclico baseado na correlação epidemiológica, prevenindo antecipadamente surtos gripais invernais específicos em determinadas geografias poligonais de postos com carência em pediatria.
3.  **Portabilidade do Motor de Recomendação:** Englobar a integralidade absoluta do estado de São Paulo no Grafo e instanciar aplicações Mobile Nativas acessíveis (Microserviço escalável), transformando a tese monográfica numa política de estado operante nas palmas da população desassistida.

---
`FIM DO DOCUMENTO DO TRABALHO DE CONCLUSÃO DE CURSO`
