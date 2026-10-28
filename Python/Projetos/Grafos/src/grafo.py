"""
SPGraph - Módulo de Grafo da Rede de UBSs de São Paulo
=======================================================
Classe principal para construção e manipulação do grafo das 454 Unidades
Básicas de Saúde (UBSs) de São Paulo.

Implementa nativamente (e mantém compatibilidade com NetworkX quando presente):
- Representação por Lista de Adjacência Ponderada G = (V, E, W_V, W_E)
- Vértices (UBSs) com Capacidade (C_v), Demanda Base (D_v^0) e Regra 70/30 do SUS
- Arestas com Distância Haversine (km) e Impedância Topográfica de Tobler (km)
- Algoritmo de Dijkstra com Fila de Prioridade Mínima (Min-Heap / heapq)
- Busca em Largura (BFS) em camadas com deque
- Centralidade de Grau, Proximidade (Closeness) e Intermediação (Brandes)
"""

from __future__ import annotations

import heapq
import json
from collections import deque
from pathlib import Path

try:
    import networkx as nx
except ImportError:
    nx = None


class GrafoNativo:
    """
    Estrutura de Grafo Não-Orientado Ponderado em Lista de Adjacência,
    com interface 100% compatível com networkx.Graph para independência de ambiente.
    """

    def __init__(self) -> None:
        self._nodes: dict[int, dict] = {}
        self._adj: dict[int, dict[int, dict]] = {}

    def add_node(self, node_id: int, **attrs) -> None:
        if node_id not in self._nodes:
            self._nodes[node_id] = {}
            self._adj[node_id] = {}
        self._nodes[node_id].update(attrs)

    def add_edge(self, u: int, v: int, **attrs) -> None:
        if u not in self._nodes:
            self.add_node(u)
        if v not in self._nodes:
            self.add_node(v)
        edge_dict = dict(attrs)
        self._adj[u][v] = edge_dict
        self._adj[v][u] = edge_dict

    def remove_node(self, node_id: int) -> None:
        if node_id in self._adj:
            for viz in list(self._adj[node_id].keys()):
                self._adj[viz].pop(node_id, None)
            del self._adj[node_id]
        self._nodes.pop(node_id, None)

    def remove_nodes_from(self, nodes) -> None:
        for n in list(nodes):
            self.remove_node(n)

    def remove_edge(self, u: int, v: int) -> None:
        if u in self._adj:
            self._adj[u].pop(v, None)
        if v in self._adj:
            self._adj[v].pop(u, None)

    def nodes(self) -> list[int]:
        return list(self._nodes.keys())

    def edges(self) -> list[tuple[int, int]]:
        vistos: set[tuple[int, int]] = set()
        res: list[tuple[int, int]] = []
        for u in self._adj:
            for v in self._adj[u]:
                par = (u, v) if u <= v else (v, u)
                if par not in vistos:
                    vistos.add(par)
                    res.append(par)
        return res

    def neighbors(self, u: int):
        return iter(self._adj.get(u, {}).keys())

    def degree(self, u: int | None = None):
        if u is not None:
            return len(self._adj.get(u, {}))
        return [(n, len(self._adj[n])) for n in self._nodes]

    def number_of_nodes(self) -> int:
        return len(self._nodes)

    def number_of_edges(self) -> int:
        return sum(len(viz) for viz in self._adj.values()) // 2

    def copy(self) -> "GrafoNativo":
        novo = GrafoNativo()
        for n, attrs in self._nodes.items():
            novo._nodes[n] = dict(attrs)
            novo._adj[n] = {}
        for u, viz_dict in self._adj.items():
            for v, e_attrs in viz_dict.items():
                if u <= v:
                    copia_e = dict(e_attrs)
                    novo._adj[u][v] = copia_e
                    novo._adj[v][u] = copia_e
        return novo

    def __contains__(self, node_id: int) -> bool:
        return node_id in self._nodes

    def __getitem__(self, u: int) -> dict[int, dict]:
        return self._adj[u]


class GrafoSP:
    """
    Grafo da Malha Conectada de UBSs de São Paulo.

    Modela cada UBS como um vértice v ∈ V dotado de Capacidade (C_v),
    Demanda Territorial Base (D_v^0) e Folga Operacional (Regra 70/30 do SUS),
    e conecta UBSs vizinhas por arestas ponderadas pela distância geodésica
    e pela impedância topográfica de Tobler.
    """

    def __init__(self, data_dir: str | Path = "data"):
        caminho = Path(data_dir)
        if not caminho.exists():
            caminho_alt = Path(__file__).resolve().parent.parent / data_dir
            if caminho_alt.exists():
                caminho = caminho_alt
        self.data_dir = caminho
        self.G = nx.Graph() if nx is not None else GrafoNativo()
        self.distritos: dict[int, dict] = {}
        self.mapa_distritos_kml: dict[int, dict] = {}
        self.servicos: list[dict] = []
        self.servicos_por_distrito: dict[int, list[dict]] = {}
        self.servicos_por_tipo: dict[str, list[dict]] = {}

        self._carregar_dados()
        self._construir_grafo()

    # ================================================================
    # Carregamento e Construção
    # ================================================================

    def _carregar_dados(self) -> None:
        """Carrega os vértices das UBSs, adjacências topográficas e metadados."""
        vertices_path = self.data_dir / "ubs_vertices.json"
        if not vertices_path.exists():
            vertices_path = self.data_dir / "distritos.json"

        with open(vertices_path, "r", encoding="utf-8") as f:
            lista_vertices = json.load(f)
        self.distritos = {d["id"]: d for d in lista_vertices}

        dist_kml_path = self.data_dir / "distritos.json"
        if dist_kml_path.exists():
            with open(dist_kml_path, "r", encoding="utf-8") as f:
                self.mapa_distritos_kml = {d["id"]: d for d in json.load(f)}

        with open(self.data_dir / "adjacencias.json", "r", encoding="utf-8") as f:
            self.adjacencias = json.load(f)

        servicos_path = self.data_dir / "servicos.json"
        if servicos_path.exists():
            with open(servicos_path, "r", encoding="utf-8") as f:
                servicos_brutos = json.load(f)
        else:
            servicos_brutos = []

        tipos_permitidos = {"ubs", "upa", "hospital_sus"}
        self.servicos = []
        for s in servicos_brutos:
            tipo = str(s.get("tipo", "")).strip().lower()
            if tipo == "hospital":
                tipo = "hospital_sus"
            if tipo not in tipos_permitidos:
                continue
            s_norm = dict(s)
            s_norm["tipo"] = tipo
            self.servicos.append(s_norm)

        self.servicos_por_distrito = {}
        self.servicos_por_tipo = {}
        for s in self.servicos:
            did = s["distrito_id"]
            self.servicos_por_distrito.setdefault(did, []).append(s)
            self.servicos_por_tipo.setdefault(s["tipo"], []).append(s)

    def _construir_grafo(self) -> None:
        """Constrói o grafo em lista de adjacência com atributos de capacidade e topografia."""
        for uid, u in self.distritos.items():
            demanda = int(u.get("demanda_base", u.get("populacao", 0)))
            capacidade = int(u.get("capacidade", max(10000, int(round(demanda / 0.70)))))
            cota_prog = int(u.get("cota_programada_70", int(round(capacidade * 0.70))))
            cota_esp = int(u.get("cota_espontanea_30", capacidade - cota_prog))
            folga = int(u.get("folga_operacional", min(cota_esp, max(0, capacidade - demanda))))

            u["demanda_base"] = demanda
            u["populacao"] = demanda
            u["capacidade"] = capacidade
            u["cota_programada_70"] = cota_prog
            u["cota_espontanea_30"] = cota_esp
            u["folga_operacional"] = folga
            u.setdefault("taxa_ocupacao", round(demanda / capacidade, 4) if capacidade else 1.0)
            u.setdefault("folga_percentual", round((folga / capacidade) * 100.0, 2) if capacidade else 0.0)

            self.G.add_node(
                uid,
                nome=u["nome"],
                zona=u["zona"],
                distrito=u.get("distrito", u["nome"]),
                lat=u["lat"],
                lon=u["lon"],
                altitude_m=u.get("altitude_m", 760.0),
                populacao=demanda,
                demanda_base=demanda,
                capacidade=capacidade,
                cota_programada_70=cota_prog,
                cota_espontanea_30=cota_esp,
                folga_operacional=folga,
            )

        for adj in self.adjacencias:
            u = adj["distrito1_id"]
            v = adj["distrito2_id"]
            w_km = float(adj["distancia_km"])
            w_topo = float(adj.get("impedancia_topografica_km", w_km))
            decliv = float(adj.get("declividade_pct", 0.0))
            self.G.add_edge(
                u,
                v,
                weight=w_km,
                impedancia_topografica_km=w_topo,
                declividade_pct=decliv,
            )

    # ================================================================
    # Algoritmos Clássicos de Grafos (Implementação Direta Verificável)
    # ================================================================

    def dijkstra_todos(
        self, origem_id: int, attr_peso: str = "weight"
    ) -> dict[int, float]:
        """
        Calcula a distância mínima de uma UBS de origem para todas as demais
        usando o Algoritmo de Dijkstra com Min-Heap (heapq).
        Complexidade: O((|V| + |E|) log |V|).
        """
        if origem_id not in self.G:
            return {}
        dist: dict[int, float] = {origem_id: 0.0}
        heap: list[tuple[float, int]] = [(0.0, origem_id)]

        while heap:
            d_u, u = heapq.heappop(heap)
            if d_u > dist.get(u, float("inf")):
                continue
            for v in self.G.neighbors(u):
                peso = float(self.G[u][v].get(attr_peso, self.G[u][v].get("weight", 1.0)))
                nova_dist = d_u + peso
                if nova_dist < dist.get(v, float("inf")):
                    dist[v] = nova_dist
                    heapq.heappush(heap, (nova_dist, v))
        return dist

    def dijkstra(
        self, origem_id: int, destino_id: int, attr_peso: str = "weight"
    ) -> tuple[float, list[int]]:
        """
        Calcula o menor caminho entre duas UBSs usando Dijkstra com Min-Heap.
        Complexidade: O((|V| + |E|) log |V|).
        """
        if origem_id not in self.G or destino_id not in self.G:
            return float("inf"), []
        dist: dict[int, float] = {origem_id: 0.0}
        prev: dict[int, int] = {}
        heap: list[tuple[float, int]] = [(0.0, origem_id)]

        while heap:
            d_u, u = heapq.heappop(heap)
            if u == destino_id:
                break
            if d_u > dist.get(u, float("inf")):
                continue
            for v in self.G.neighbors(u):
                peso = float(self.G[u][v].get(attr_peso, self.G[u][v].get("weight", 1.0)))
                nova_dist = d_u + peso
                if nova_dist < dist.get(v, float("inf")):
                    dist[v] = nova_dist
                    prev[v] = u
                    heapq.heappush(heap, (nova_dist, v))

        if destino_id not in dist:
            return float("inf"), []

        caminho: list[int] = []
        atual: int | None = destino_id
        while atual is not None:
            caminho.append(atual)
            atual = prev.get(atual)
        caminho.reverse()
        return round(dist[destino_id], 2), caminho

    def bfs(self, origem_id: int, max_profundidade: int | None = None) -> dict[int, int]:
        """
        Executa Busca em Largura (BFS) em camadas a partir de uma UBS.
        Complexidade: O(|V| + |E|).
        """
        if origem_id not in self.G:
            return {}
        visitados = {origem_id: 0}
        fila = deque([origem_id])

        while fila:
            atual = fila.popleft()
            profundidade_atual = visitados[atual]

            if max_profundidade is not None and profundidade_atual >= max_profundidade:
                continue

            for vizinho in self.G.neighbors(atual):
                if vizinho not in visitados:
                    visitados[vizinho] = profundidade_atual + 1
                    fila.append(vizinho)

        return visitados

    def servico_mais_proximo(
        self, distrito_id: int, tipo_servico: str = "ubs"
    ) -> tuple[dict | None, float, list[int]]:
        """
        Encontra a unidade ativa mais próxima com vagas disponíveis ou do tipo solicitado.
        """
        servicos_locais = [
            s for s in self.servicos_por_distrito.get(distrito_id, [])
            if s["tipo"] == tipo_servico
        ]
        if servicos_locais:
            return servicos_locais[0], 0.0, [distrito_id]

        distritos_com_servico = {
            s["distrito_id"]
            for s in self.servicos_por_tipo.get(tipo_servico, [])
        }
        if not distritos_com_servico:
            return None, float("inf"), []

        distancias = self.dijkstra_todos(distrito_id)
        menor_dist = float("inf")
        melhor_id = None
        for did in distritos_com_servico:
            if did in distancias and distancias[did] < menor_dist:
                menor_dist = distancias[did]
                melhor_id = did

        if melhor_id is None:
            return None, float("inf"), []

        _, caminho = self.dijkstra(distrito_id, melhor_id)
        servico = next(
            s for s in self.servicos_por_tipo[tipo_servico]
            if s["distrito_id"] == melhor_id
        )
        return servico, round(menor_dist, 2), caminho

    # ================================================================
    # Métricas de Centralidade e Topologia
    # ================================================================

    def grau_vertices(self) -> dict[int, int]:
        return dict(self.G.degree())

    def centralidade_grau(self) -> dict[int, float]:
        n = self.G.number_of_nodes()
        if n <= 1:
            return {v: 0.0 for v in self.G.nodes()}
        return {v: deg / (n - 1) for v, deg in self.G.degree()}

    def centralidade_proximidade(self) -> dict[int, float]:
        n = self.G.number_of_nodes()
        res: dict[int, float] = {}
        for u in self.G.nodes():
            dists = self.dijkstra_todos(u)
            soma = sum(d for v, d in dists.items() if v != u and d < float("inf"))
            alcancados = len(dists) - 1
            if soma > 0 and alcancados > 0 and n > 1:
                res[u] = (alcancados / soma) * (alcancados / (n - 1))
            else:
                res[u] = 0.0
        return res

    def centralidade_intermediacao(self) -> dict[int, float]:
        """
        Calcula a Centralidade de Intermediação (Betweenness Centrality) ponderada
        pelo algoritmo de Brandes (2001).
        """
        if nx is not None and hasattr(nx, "betweenness_centrality"):
            return nx.betweenness_centrality(self.G, weight="weight")

        nodes = self.G.nodes()
        cb: dict[int, float] = {v: 0.0 for v in nodes}
        n = len(nodes)
        if n <= 2:
            return cb

        for s in nodes:
            pilha: list[int] = []
            pred: dict[int, list[int]] = {w: [] for w in nodes}
            sigma: dict[int, float] = {w: 0.0 for w in nodes}
            sigma[s] = 1.0
            dist: dict[int, float] = {s: 0.0}
            heap: list[tuple[float, int]] = [(0.0, s)]

            while heap:
                d_v, v = heapq.heappop(heap)
                if d_v > dist.get(v, float("inf")):
                    continue
                pilha.append(v)
                for w in self.G.neighbors(v):
                    peso = float(self.G[v][w].get("weight", 1.0))
                    vw_dist = d_v + peso
                    w_dist = dist.get(w, float("inf"))
                    if vw_dist < w_dist - 1e-9:
                        dist[w] = vw_dist
                        heapq.heappush(heap, (vw_dist, w))
                        sigma[w] = sigma[v]
                        pred[w] = [v]
                    elif abs(vw_dist - w_dist) <= 1e-9:
                        sigma[w] += sigma[v]
                        pred[w].append(v)

            delta: dict[int, float] = {w: 0.0 for w in nodes}
            while pilha:
                w = pilha.pop()
                for v in pred[w]:
                    if sigma[w] > 0:
                        delta[v] += (sigma[v] / sigma[w]) * (1.0 + delta[w])
                if w != s:
                    cb[w] += delta[w]

        fator = 2.0 / ((n - 1) * (n - 2))
        for v in cb:
            cb[v] *= fator
        return cb

    # ================================================================
    # Estatísticas do Grafo
    # ================================================================

    def estatisticas(self) -> dict:
        graus = [d for _, d in self.G.degree()]
        n = self.G.number_of_nodes()
        m = self.G.number_of_edges()
        comps = self.componentes_conexas()
        densidade = (2.0 * m) / (n * (n - 1)) if n > 1 else 0.0
        cap_total = sum(d.get("capacidade", 0) for d in self.distritos.values())
        dem_total = sum(d.get("demanda_base", 0) for d in self.distritos.values())
        folga_total = sum(d.get("folga_operacional", 0) for d in self.distritos.values())
        return {
            "num_vertices": n,
            "num_arestas": m,
            "grau_medio": round(sum(graus) / len(graus), 2) if graus else 0,
            "grau_maximo": max(graus) if graus else 0,
            "grau_minimo": min(graus) if graus else 0,
            "eh_conexo": len(comps) == 1 if n > 0 else False,
            "num_componentes": len(comps),
            "densidade": round(densidade, 4),
            "capacidade_total": cap_total,
            "demanda_total": dem_total,
            "folga_total": folga_total,
        }

    # ================================================================
    # Utilidades e Operações Estruturais
    # ================================================================

    def get_posicoes(self) -> dict[int, tuple[float, float]]:
        return {did: (d["lon"], d["lat"]) for did, d in self.distritos.items()}

    def get_nome(self, distrito_id: int) -> str:
        return self.distritos.get(distrito_id, {}).get("nome", "Desconhecido")

    def get_nomes_ordenados(self) -> list[tuple[int, str]]:
        return sorted(
            [(did, d["nome"]) for did, d in self.distritos.items()],
            key=lambda x: x[1],
        )

    def get_tipos_servico(self) -> list[str]:
        return sorted(self.servicos_por_tipo.keys())

    def contar_servicos_distrito(self, distrito_id: int) -> dict[str, int]:
        contagem: dict[str, int] = {}
        for s in self.servicos_por_distrito.get(distrito_id, []):
            contagem[s["tipo"]] = contagem.get(s["tipo"], 0) + 1
        return contagem

    def copiar_sem_nos(self, ids_remover: set[int]) -> "GrafoSP":
        copia = GrafoSP.__new__(GrafoSP)
        copia.data_dir = self.data_dir
        copia.G = self.G.copy()
        copia.mapa_distritos_kml = self.mapa_distritos_kml
        copia.distritos = {
            did: dict(d) for did, d in self.distritos.items()
            if did not in ids_remover
        }
        copia.servicos = [
            s for s in self.servicos
            if s["distrito_id"] not in ids_remover
        ]

        for nid in ids_remover:
            if nid in copia.G:
                copia.G.remove_node(nid)

        copia.servicos_por_distrito = {}
        copia.servicos_por_tipo = {}
        for s in copia.servicos:
            did = s["distrito_id"]
            copia.servicos_por_distrito.setdefault(did, []).append(s)
            copia.servicos_por_tipo.setdefault(s["tipo"], []).append(s)

        copia.adjacencias = [
            a for a in self.adjacencias
            if a["distrito1_id"] not in ids_remover
            and a["distrito2_id"] not in ids_remover
        ]
        return copia

    def componentes_conexas(self) -> list[set[int]]:
        """
        Encontra todas as componentes conexas do grafo via BFS em tempo O(|V| + |E|).
        """
        visitados: set[int] = set()
        componentes: list[set[int]] = []
        for no in self.G.nodes():
            if no not in visitados:
                comp: set[int] = set()
                fila = deque([no])
                visitados.add(no)
                while fila:
                    atual = fila.popleft()
                    comp.add(atual)
                    for viz in self.G.neighbors(atual):
                        if viz not in visitados:
                            visitados.add(viz)
                            fila.append(viz)
                componentes.append(comp)
        return componentes

    def distritos_com_servico(self, tipo_servico: str = "ubs") -> set[int]:
        return {
            s["distrito_id"]
            for s in self.servicos_por_tipo.get(tipo_servico, [])
        }
