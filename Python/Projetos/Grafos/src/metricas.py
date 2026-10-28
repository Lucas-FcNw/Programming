"""
SPGraph - Módulo de Métricas de Cobertura, Capacidade e Pressão Operacional
===========================================================================
Calcula métricas de cobertura territorial, pressão de demanda sobre a regra
70% Demanda Programada / 30% Demanda Espontânea (SUS) e comparativo entre
a visão de Tabela Estática Isolada e a Topologia em Grafo.
"""

from __future__ import annotations

try:
    import pandas as pd
except ImportError:
    pd = None

from src.grafo import GrafoSP


class MetricasAcessibilidade:
    """
    Calcula métricas operacionais e territoriais para as 454 UBSs de São Paulo.
    """

    def __init__(self, grafo: GrafoSP):
        self.grafo = grafo

    def distancia_servico_mais_proximo(self, tipo_servico: str = "ubs") -> dict[int, float]:
        """
        Para cada UBS u, retorna a menor distância (km) até a UBS vizinha ativa
        mais próxima (distância de socorro / 1º salto de transbordo).
        """
        distancias: dict[int, float] = {}
        for uid in self.grafo.distritos:
            vizinhos = list(self.grafo.G.neighbors(uid))
            if vizinhos:
                menor = min(float(self.grafo.G[uid][v].get("weight", 0.0)) for v in vizinhos)
                distancias[uid] = round(menor, 2)
            else:
                distancias[uid] = float("inf")
        return distancias

    def score_acessibilidade(self, distrito_id: int, tipo_servico: str = "ubs") -> float:
        """
        Calcula o Índice de Saúde Operacional e Proximidade de Socorro (0 a 100),
        combinando a folga operacional da regra 30% com a proximidade da UBS vizinha.
        """
        u = self.grafo.distritos.get(distrito_id, {})
        cap = float(u.get("capacidade", 1))
        folga = float(u.get("folga_operacional", 0))
        folga_norm = min(1.0, (folga / (0.30 * cap))) if cap > 0 else 0.0

        vizinhos = list(self.grafo.G.neighbors(distrito_id))
        if not vizinhos:
            return 0.0
        dist_viz = min(float(self.grafo.G[distrito_id][v].get("weight", 20.0)) for v in vizinhos)
        prox_norm = max(0.0, 1.0 - (dist_viz / 10.0))

        score = (0.60 * folga_norm + 0.40 * prox_norm) * 100.0
        return round(score, 1)

    def ranking(self, tipo_servico: str = "ubs"):
        """
        Gera o ranking das UBSs contendo Capacidade, Demanda Base, Folga (<=30%),
        Distância ao vizinho mais próximo e Score.
        """
        dists_viz = self.distancia_servico_mais_proximo(tipo_servico)
        dados: list[dict] = []
        for uid, u in self.grafo.distritos.items():
            dist = dists_viz.get(uid, float("inf"))
            score = self.score_acessibilidade(uid, tipo_servico)
            dados.append({
                "distrito_id": uid,
                "distrito": u["nome"],
                "distrito_adm": u.get("distrito", ""),
                "zona": u["zona"],
                "populacao": u.get("demanda_base", u.get("populacao", 0)),
                "capacidade": u.get("capacidade", 0),
                "folga_operacional": u.get("folga_operacional", 0),
                "folga_percentual": u.get("folga_percentual", 0.0),
                "status_tabela_isolada": u.get("status_tabela_isolada", ""),
                "distancia_km": dist,
                "score": score,
            })

        dados.sort(key=lambda x: (-x["score"], x["distancia_km"]))
        for i, row in enumerate(dados, start=1):
            row["posicao"] = i

        if pd is not None:
            colunas = [
                "posicao", "distrito_id", "distrito", "zona",
                "populacao", "distancia_km", "score",
                "capacidade", "folga_operacional", "folga_percentual",
                "status_tabela_isolada", "distrito_adm",
            ]
            return pd.DataFrame(dados)[colunas]
        return dados

    def media_cidade(self, tipo_servico: str = "ubs") -> dict:
        dists = self.distancia_servico_mais_proximo(tipo_servico)
        dists_finitas = sorted(d for d in dists.values() if d < float("inf"))
        if not dists_finitas:
            return {
                "media_distancia": 0.0,
                "score_medio": 0.0,
                "mediana_distancia": 0.0,
                "melhor_distancia": 0.0,
                "pior_distancia": 0.0,
            }

        n = len(dists_finitas)
        mediana = (
            dists_finitas[n // 2]
            if n % 2 == 1
            else (dists_finitas[n // 2 - 1] + dists_finitas[n // 2]) / 2.0
        )
        scores = [self.score_acessibilidade(uid, tipo_servico) for uid in dists]
        return {
            "media_distancia": round(sum(dists_finitas) / n, 2),
            "score_medio": round(sum(scores) / len(scores), 1),
            "mediana_distancia": round(mediana, 2),
            "melhor_distancia": round(min(dists_finitas), 2),
            "pior_distancia": round(max(dists_finitas), 2),
        }

    def distritos_isolados(
        self, tipo_servico: str = "ubs", percentil: float = 0.8
    ) -> list[dict]:
        dists = self.distancia_servico_mais_proximo(tipo_servico)
        dists_finitas = sorted(
            [(uid, d) for uid, d in dists.items() if d < float("inf")],
            key=lambda x: x[1],
            reverse=True,
        )
        if not dists_finitas:
            return []

        n_isolados = max(1, int(len(dists_finitas) * (1.0 - percentil)))
        resultado: list[dict] = []
        for uid, dist in dists_finitas[:n_isolados]:
            u = self.grafo.distritos[uid]
            resultado.append({
                "distrito_id": uid,
                "distrito": u["nome"],
                "zona": u["zona"],
                "populacao": u.get("demanda_base", 0),
                "distancia_km": round(dist, 2),
                "score": self.score_acessibilidade(uid, tipo_servico),
            })
        return resultado
