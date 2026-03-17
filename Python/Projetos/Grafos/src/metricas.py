"""
SPGraph - Módulo de Métricas de Cobertura Territorial
======================================================
Calcula métricas de cobertura territorial em saúde baseadas
na estrutura de grafos dos distritos de São Paulo.

Métricas disponíveis:
- Score de cobertura por distrito
- Ranking de cobertura
- Média da cidade
- Identificação de distritos com menor cobertura
"""

from __future__ import annotations

import pandas as pd
from src.grafo import GrafoSP


class MetricasAcessibilidade:
    """
    Calcula métricas de cobertura territorial para os distritos de São Paulo.

    As métricas consideram a distância mínima de cada distrito até
    o serviço de saúde mais próximo do tipo selecionado.
    """

    def __init__(self, grafo: GrafoSP):
        """
        Inicializa com uma instância do grafo.

        Args:
            grafo: Instância de GrafoSP já construída.
        """
        self.grafo = grafo

    def distancia_servico_mais_proximo(self, tipo_servico: str) -> dict[int, float]:
        """
        Calcula a distância de cada distrito ao serviço mais próximo.

        Args:
            tipo_servico: Tipo de serviço ('hospital' ou 'ubs').

        Returns:
            Dicionário {distrito_id: distância_km}.
        """
        distancias = {}
        for did in self.grafo.distritos:
            _, dist, _ = self.grafo.servico_mais_proximo(did, tipo_servico)
            distancias[did] = dist
        return distancias

    def score_acessibilidade(self, distrito_id: int, tipo_servico: str) -> float:
        """
        Calcula o score de acessibilidade de um distrito (0 a 100).

        Score 100 = serviço no próprio distrito.
        Score diminui proporcionalmente com a distância.

        Args:
            distrito_id: ID do distrito.
            tipo_servico: Tipo de serviço.

        Returns:
            Score de 0 a 100.
        """
        _, distancia, _ = self.grafo.servico_mais_proximo(distrito_id, tipo_servico)

        if distancia == 0:
            return 100.0
        if distancia == float("inf"):
            return 0.0

        # Score inversamente proporcional à distância
        # Referência: 20 km = score 0
        max_dist = 20.0
        score = max(0, (1 - distancia / max_dist)) * 100
        return round(score, 1)

    def ranking(self, tipo_servico: str) -> pd.DataFrame:
        """
        Gera ranking de distritos por cobertura territorial para um tipo de serviço.

        Args:
            tipo_servico: Tipo de serviço.

        Returns:
            DataFrame com colunas: posição, distrito, zona, distância, score.
        """
        dados = []
        for did, d in self.grafo.distritos.items():
            _, dist, _ = self.grafo.servico_mais_proximo(did, tipo_servico)
            score = self.score_acessibilidade(did, tipo_servico)
            dados.append({
                "distrito_id": did,
                "distrito": d["nome"],
                "zona": d["zona"],
                "populacao": d["populacao"],
                "distancia_km": dist,
                "score": score,
            })

        df = pd.DataFrame(dados)
        df = df.sort_values("distancia_km", ascending=True)
        df["posicao"] = range(1, len(df) + 1)
        df = df[["posicao", "distrito_id", "distrito", "zona",
                  "populacao", "distancia_km", "score"]]
        return df.reset_index(drop=True)

    def media_cidade(self, tipo_servico: str) -> dict:
        """
        Calcula a média de acessibilidade da cidade.

        Args:
            tipo_servico: Tipo de serviço.

        Returns:
            Dicionário com média de distância, score médio, mediana.
        """
        distancias = self.distancia_servico_mais_proximo(tipo_servico)

        # Filtrar infinitos
        dists_finitas = [d for d in distancias.values() if d < float("inf")]

        if not dists_finitas:
            return {"media_distancia": 0, "score_medio": 0, "mediana_distancia": 0}

        dists_finitas.sort()
        n = len(dists_finitas)
        mediana = dists_finitas[n // 2] if n % 2 == 1 else (
            dists_finitas[n // 2 - 1] + dists_finitas[n // 2]) / 2

        scores = [self.score_acessibilidade(did, tipo_servico)
                  for did in distancias]

        return {
            "media_distancia": round(sum(dists_finitas) / n, 2),
            "score_medio": round(sum(scores) / len(scores), 1),
            "mediana_distancia": round(mediana, 2),
            "melhor_distancia": round(min(dists_finitas), 2),
            "pior_distancia": round(max(dists_finitas), 2),
        }

    def distritos_isolados(
        self, tipo_servico: str, percentil: float = 0.8
    ) -> list[dict]:
        """
        Identifica distritos relativamente isolados (distância acima do percentil).

        Args:
            tipo_servico: Tipo de serviço.
            percentil: Percentil de corte (0.8 = top 20% mais distantes).

        Returns:
            Lista de dicionários com informações dos distritos isolados.
        """
        distancias = self.distancia_servico_mais_proximo(tipo_servico)

        # Filtrar infinitos
        dists_finitas = sorted(
            [(did, d) for did, d in distancias.items() if d < float("inf")],
            key=lambda x: x[1],
            reverse=True
        )

        if not dists_finitas:
            return []

        # Corte pelo percentil
        n_isolados = max(1, int(len(dists_finitas) * (1 - percentil)))
        isolados = dists_finitas[:n_isolados]

        resultado = []
        for did, dist in isolados:
            d = self.grafo.distritos[did]
            score = self.score_acessibilidade(did, tipo_servico)
            resultado.append({
                "distrito_id": did,
                "distrito": d["nome"],
                "zona": d["zona"],
                "populacao": d["populacao"],
                "distancia_km": round(dist, 2),
                "score": score,
            })

        return resultado

    def comparar_com_media(self, distrito_id: int, tipo_servico: str) -> dict:
        """
        Compara a acessibilidade de um distrito com a média da cidade.

        Args:
            distrito_id: ID do distrito.
            tipo_servico: Tipo de serviço.

        Returns:
            Dicionário com comparação detalhada.
        """
        _, dist_distrito, _ = self.grafo.servico_mais_proximo(
            distrito_id, tipo_servico
        )
        score_distrito = self.score_acessibilidade(distrito_id, tipo_servico)
        media = self.media_cidade(tipo_servico)

        ranking_df = self.ranking(tipo_servico)
        posicao = ranking_df[
            ranking_df["distrito_id"] == distrito_id
        ]["posicao"].values[0]

        diff_dist = round(dist_distrito - media["media_distancia"], 2)
        diff_score = round(score_distrito - media["score_medio"], 1)

        if diff_dist < -0.5:
            classificacao = "Acima da média"
        elif diff_dist > 0.5:
            classificacao = "Abaixo da média"
        else:
            classificacao = "Na média"

        return {
            "distrito": self.grafo.get_nome(distrito_id),
            "distancia_km": round(dist_distrito, 2),
            "score": score_distrito,
            "posicao_ranking": posicao,
            "total_distritos": len(self.grafo.distritos),
            "media_distancia_cidade": media["media_distancia"],
            "score_medio_cidade": media["score_medio"],
            "diferenca_distancia": diff_dist,
            "diferenca_score": diff_score,
            "classificacao": classificacao,
        }
