"""
SPGraph - Módulo de Análise de Vulnerabilidade
================================================
Analisa a resiliência da rede de saúde pública de São Paulo
usando algoritmos de teoria dos grafos.

Algoritmos implementados:
- Vértices de articulação (Tarjan) — nós cuja remoção desconecta a rede
- Pontes críticas (Tarjan) — arestas cuja remoção desconecta a rede
- Simulação de falha — impacto do fechamento de UBSs/distritos
- Componentes conexas pós-falha — fragmentação da rede
- Ranking de criticidade — classificação por impacto de remoção
"""

from __future__ import annotations

from collections import deque

import networkx as nx
import pandas as pd

from src.grafo import GrafoSP


class AnaliseVulnerabilidade:
    """
    Analisa a vulnerabilidade estrutural da rede de saúde.

    Utiliza o grafo de distritos para identificar pontos críticos,
    simular cenários de falha e medir o impacto na cobertura.
    """

    def __init__(self, grafo: GrafoSP):
        """
        Inicializa com uma instância do grafo.

        Args:
            grafo: Instância de GrafoSP já construída.
        """
        self.grafo = grafo

    # ================================================================
    # Algoritmo 1: Vértices de Articulação (Tarjan)
    # ================================================================

    def vertices_articulacao(self, tipo_servico: str | None = None) -> list[dict]:
        """
        Encontra vértices de articulação no grafo (ou no subgrafo de cobertura).

        Um vértice de articulação é um nó cuja remoção aumenta o número de
        componentes conexas do grafo — indica um ponto estruturalmente crítico.

        Usa o algoritmo de Tarjan (DFS com tracking de low-link values).

        Args:
            tipo_servico: Se fornecido, analisa apenas o subgrafo relevante
                          (distritos com conexão ao serviço). Se None, analisa
                          o grafo completo.

        Returns:
            Lista de dicionários com info de cada vértice de articulação:
            {distrito_id, distrito, zona, populacao, grau, tem_servico}.
        """
        if tipo_servico:
            distritos_servico = self.grafo.distritos_com_servico(tipo_servico)
        else:
            distritos_servico = set()

        # Usar implementação do NetworkX (baseada em Tarjan)
        articulacoes = set(nx.articulation_points(self.grafo.G))

        resultado = []
        for did in sorted(articulacoes):
            d = self.grafo.distritos.get(did, {})
            resultado.append({
                "distrito_id": did,
                "distrito": d.get("nome", "?"),
                "zona": d.get("zona", "?"),
                "populacao": d.get("populacao", 0),
                "grau": self.grafo.G.degree(did),
                "tem_servico": did in distritos_servico if tipo_servico else None,
            })

        return resultado

    # ================================================================
    # Algoritmo 2: Pontes Críticas (Tarjan)
    # ================================================================

    def pontes_criticas(self) -> list[dict]:
        """
        Encontra pontes (bridges) no grafo — arestas cuja remoção desconecta
        componentes do grafo.

        Usa variante do algoritmo de Tarjan para detecção de pontes.

        Returns:
            Lista de dicionários com info de cada ponte:
            {distrito1_id, distrito1, distrito2_id, distrito2, distancia_km,
             pop_lado1, pop_lado2}.
        """
        pontes = list(nx.bridges(self.grafo.G))

        resultado = []
        for u, v in pontes:
            # Calcular população em cada lado se a ponte for removida
            G_temp = self.grafo.G.copy()
            G_temp.remove_edge(u, v)
            componentes = list(nx.connected_components(G_temp))

            pop_lados = []
            for comp in componentes:
                pop = sum(
                    self.grafo.distritos.get(nid, {}).get("populacao", 0)
                    for nid in comp
                )
                pop_lados.append(pop)

            # Ordenar para que o menor lado fique como "lado vulnerável"
            pop_lados.sort()

            peso = self.grafo.G[u][v].get("weight", 0)
            resultado.append({
                "distrito1_id": u,
                "distrito1": self.grafo.get_nome(u),
                "distrito2_id": v,
                "distrito2": self.grafo.get_nome(v),
                "distancia_km": round(peso, 2),
                "pop_lado_menor": pop_lados[0] if len(pop_lados) > 1 else 0,
                "pop_lado_maior": pop_lados[-1] if pop_lados else 0,
            })

        return resultado

    # ================================================================
    # Algoritmo 3: Simulação de Fechamento
    # ================================================================

    def simular_fechamento(
        self,
        ids_remover: list[int],
        tipo_servico: str,
    ) -> dict:
        """
        Simula o fechamento de distritos/UBSs e mede o impacto na rede.

        Remove os nós especificados do grafo e recalcula:
        - Número de componentes conexas resultantes
        - Distritos que perderam acesso ao serviço
        - População total afetada
        - Variação na distância média ao serviço

        Este método percorre o grafo INTEIRO para cada cenário.

        Args:
            ids_remover: Lista de IDs de distritos a remover.
            tipo_servico: Tipo de serviço a analisar.

        Returns:
            Dicionário com métricas de impacto (antes vs depois).
        """
        ids_set = set(ids_remover)

        # === ANTES da remoção ===
        distritos_servico_antes = self.grafo.distritos_com_servico(tipo_servico)
        comp_antes = self.grafo.componentes_conexas()

        # Calcular distância média antes (percorre grafo inteiro)
        dist_antes = {}
        for did in self.grafo.distritos:
            _, dist, _ = self.grafo.servico_mais_proximo(did, tipo_servico)
            dist_antes[did] = dist

        dists_finitas_antes = [d for d in dist_antes.values() if d < float("inf")]
        media_antes = (
            sum(dists_finitas_antes) / len(dists_finitas_antes)
            if dists_finitas_antes else 0
        )

        # Distritos sem acesso antes
        sem_acesso_antes = {
            did for did, d in dist_antes.items() if d == float("inf")
        }

        # === DEPOIS da remoção ===
        grafo_pos = self.grafo.copiar_sem_nos(ids_set)
        comp_depois = grafo_pos.componentes_conexas()

        distritos_servico_depois = grafo_pos.distritos_com_servico(tipo_servico)

        # Calcular distância média depois (percorre grafo modificado inteiro)
        dist_depois = {}
        for did in grafo_pos.distritos:
            _, dist, _ = grafo_pos.servico_mais_proximo(did, tipo_servico)
            dist_depois[did] = dist

        dists_finitas_depois = [d for d in dist_depois.values() if d < float("inf")]
        media_depois = (
            sum(dists_finitas_depois) / len(dists_finitas_depois)
            if dists_finitas_depois else 0
        )

        # Distritos sem acesso depois (excluindo os removidos)
        sem_acesso_depois = {
            did for did, d in dist_depois.items() if d == float("inf")
        }

        # Novos distritos sem acesso (perderam acesso com a remoção)
        novos_sem_acesso = sem_acesso_depois - sem_acesso_antes - ids_set

        # População afetada (distritos que perderam acesso)
        pop_afetada_direta = sum(
            self.grafo.distritos.get(did, {}).get("populacao", 0)
            for did in ids_set
        )
        pop_novos_sem_acesso = sum(
            grafo_pos.distritos.get(did, {}).get("populacao", 0)
            for did in novos_sem_acesso
        )

        # Distritos com aumento significativo de distância
        aumento_distancia = {}
        for did in grafo_pos.distritos:
            d_antes = dist_antes.get(did, float("inf"))
            d_depois = dist_depois.get(did, float("inf"))
            if d_antes < float("inf") and d_depois < float("inf"):
                delta = d_depois - d_antes
                if delta > 0.1:  # Aumento > 100m
                    aumento_distancia[did] = {
                        "distrito": grafo_pos.get_nome(did),
                        "zona": grafo_pos.distritos[did].get("zona", "?"),
                        "populacao": grafo_pos.distritos[did].get("populacao", 0),
                        "distancia_antes": round(d_antes, 2),
                        "distancia_depois": round(d_depois, 2),
                        "aumento_km": round(delta, 2),
                    }

        # Montar componentes pós-falha com detalhes
        componentes_detalhadas = []
        for comp in sorted(comp_depois, key=lambda c: -len(c)):
            pop_comp = sum(
                grafo_pos.distritos.get(nid, {}).get("populacao", 0)
                for nid in comp
            )
            servicos_comp = comp & distritos_servico_depois
            componentes_detalhadas.append({
                "distritos": sorted(comp),
                "nomes": [grafo_pos.get_nome(nid) for nid in sorted(comp)],
                "num_distritos": len(comp),
                "populacao": pop_comp,
                "tem_servico": len(servicos_comp) > 0,
                "num_servicos_tipo": len(servicos_comp),
            })

        return {
            # Resumo
            "distritos_removidos": [
                {"id": did, "nome": self.grafo.get_nome(did)}
                for did in ids_remover
            ],
            "tipo_servico": tipo_servico,

            # Antes
            "componentes_antes": len(comp_antes),
            "media_distancia_antes": round(media_antes, 2),
            "distritos_sem_acesso_antes": len(sem_acesso_antes),

            # Depois
            "componentes_depois": len(comp_depois),
            "media_distancia_depois": round(media_depois, 2),
            "distritos_sem_acesso_depois": len(sem_acesso_depois),

            # Impacto
            "novos_sem_acesso": sorted(novos_sem_acesso),
            "nomes_novos_sem_acesso": [
                grafo_pos.get_nome(did) for did in sorted(novos_sem_acesso)
            ],
            "pop_removida": pop_afetada_direta,
            "pop_novos_sem_acesso": pop_novos_sem_acesso,
            "aumento_medio_distancia": round(media_depois - media_antes, 2),
            "distritos_com_aumento": dict(sorted(
                aumento_distancia.items(),
                key=lambda x: -x[1]["aumento_km"],
            )),

            # Componentes detalhadas
            "componentes": componentes_detalhadas,
        }

    # ================================================================
    # Algoritmo 4: Componentes Conexas Pós-Falha
    # ================================================================

    def componentes_pos_falha(
        self,
        ids_remover: list[int],
        tipo_servico: str,
    ) -> list[dict]:
        """
        Identifica componentes conexas remanescentes após remoção de nós.

        Para cada componente, informa se ela possui serviço do tipo
        especificado. Componentes sem serviço representam populações
        isoladas — o cenário mais crítico.

        Usa BFS para percorrer cada componente.

        Args:
            ids_remover: Lista de IDs de distritos a remover.
            tipo_servico: Tipo de serviço a verificar.

        Returns:
            Lista de dicionários com info de cada componente.
        """
        grafo_pos = self.grafo.copiar_sem_nos(set(ids_remover))
        componentes = grafo_pos.componentes_conexas()
        distritos_servico = grafo_pos.distritos_com_servico(tipo_servico)

        resultado = []
        for i, comp in enumerate(
            sorted(componentes, key=lambda c: -len(c)), start=1
        ):
            pop = sum(
                grafo_pos.distritos.get(nid, {}).get("populacao", 0)
                for nid in comp
            )
            servicos_na_comp = comp & distritos_servico

            resultado.append({
                "componente_id": i,
                "distritos_ids": sorted(comp),
                "nomes": sorted(
                    grafo_pos.get_nome(nid) for nid in comp
                ),
                "num_distritos": len(comp),
                "populacao": pop,
                "tem_servico": len(servicos_na_comp) > 0,
                "num_distritos_com_servico": len(servicos_na_comp),
                "isolada": len(servicos_na_comp) == 0,
            })

        return resultado

    # ================================================================
    # Algoritmo 5: Ranking de Criticidade
    # ================================================================

    def ranking_criticidade(self, tipo_servico: str) -> pd.DataFrame:
        """
        Classifica cada distrito por seu nível de criticidade.

        Para cada distrito, simula sua remoção e mede o impacto:
        - Aumento na distância média ao serviço
        - Número de novos distritos sem acesso
        - População que perde acesso

        Percorre o grafo INTEIRO N vezes (N = número de distritos).

        Args:
            tipo_servico: Tipo de serviço a analisar.

        Returns:
            DataFrame ordenado por criticidade (maior impacto primeiro).
        """
        articulacoes = set(nx.articulation_points(self.grafo.G))

        dados = []
        for did in sorted(self.grafo.distritos.keys()):
            d = self.grafo.distritos[did]

            # Simular remoção deste distrito
            resultado = self.simular_fechamento([did], tipo_servico)

            # Calcular score de criticidade
            # Pondera: componentes geradas, pop afetada, aumento de distância
            score = (
                resultado["componentes_depois"] - resultado["componentes_antes"]
            ) * 10  # +10 por componente nova

            score += len(resultado["novos_sem_acesso"]) * 5  # +5 por distrito isolado
            score += resultado["aumento_medio_distancia"] * 2  # +2 por km de aumento
            score += 15 if did in articulacoes else 0  # +15 se é articulação

            # Bonus por população dos distritos afetados
            score += resultado["pop_novos_sem_acesso"] / 10000  # +1 por 10 mil hab

            tem_servico = did in self.grafo.distritos_com_servico(tipo_servico)

            dados.append({
                "distrito_id": did,
                "distrito": d["nome"],
                "zona": d["zona"],
                "populacao": d["populacao"],
                "grau": self.grafo.G.degree(did),
                "eh_articulacao": did in articulacoes,
                "tem_servico": tem_servico,
                "componentes_apos_remocao": resultado["componentes_depois"],
                "novos_sem_acesso": len(resultado["novos_sem_acesso"]),
                "pop_sem_acesso": resultado["pop_novos_sem_acesso"],
                "aumento_distancia_media": resultado["aumento_medio_distancia"],
                "score_criticidade": round(score, 1),
            })

        df = pd.DataFrame(dados)
        df = df.sort_values("score_criticidade", ascending=False)
        df["posicao"] = range(1, len(df) + 1)
        df = df[["posicao", "distrito_id", "distrito", "zona", "populacao",
                  "grau", "eh_articulacao", "tem_servico",
                  "componentes_apos_remocao", "novos_sem_acesso",
                  "pop_sem_acesso", "aumento_distancia_media",
                  "score_criticidade"]]
        return df.reset_index(drop=True)
