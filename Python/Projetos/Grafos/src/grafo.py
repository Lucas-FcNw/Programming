"""
SPGraph - Módulo de Grafo
==========================
Classe principal para construção e manipulação do grafo
dos distritos de São Paulo usando NetworkX.

Implementa:
- Construção do grafo a partir de dados JSON
- Algoritmo de Dijkstra (menor caminho)
- BFS (busca em largura)
- Cálculo de centralidade
- Busca da referência de serviço de saúde mais próxima
"""

import json
from pathlib import Path
from collections import deque

import networkx as nx


class GrafoSP:
    """
    Grafo dos distritos administrativos de São Paulo.

    Modela os distritos como vértices e suas adjacências geográficas
    como arestas ponderadas pela distância em km.
    """

    def __init__(self, data_dir: str | Path = "data"):
        """
        Inicializa o grafo carregando dados do diretório especificado.

        Args:
            data_dir: Caminho para o diretório com os arquivos JSON.
        """
        self.data_dir = Path(data_dir)
        self.G = nx.Graph()
        self.distritos: dict[int, dict] = {}
        self.servicos: list[dict] = []
        self.servicos_por_distrito: dict[int, list[dict]] = {}
        self.servicos_por_tipo: dict[str, list[dict]] = {}

        self._carregar_dados()
        self._construir_grafo()

    # ================================================================
    # Carregamento e Construção
    # ================================================================

    def _carregar_dados(self):
        """Carrega os dados dos arquivos JSON."""
        # Distritos
        with open(self.data_dir / "distritos.json", "r", encoding="utf-8") as f:
            lista_distritos = json.load(f)
        self.distritos = {d["id"]: d for d in lista_distritos}

        # Adjacências
        with open(self.data_dir / "adjacencias.json", "r", encoding="utf-8") as f:
            self.adjacencias = json.load(f)

        # Serviços
        with open(self.data_dir / "servicos.json", "r", encoding="utf-8") as f:
            self.servicos = json.load(f)

        # Indexar serviços por distrito
        self.servicos_por_distrito = {}
        for s in self.servicos:
            did = s["distrito_id"]
            if did not in self.servicos_por_distrito:
                self.servicos_por_distrito[did] = []
            self.servicos_por_distrito[did].append(s)

        # Indexar serviços por tipo
        self.servicos_por_tipo = {}
        for s in self.servicos:
            tipo = s["tipo"]
            if tipo not in self.servicos_por_tipo:
                self.servicos_por_tipo[tipo] = []
            self.servicos_por_tipo[tipo].append(s)

    def _construir_grafo(self):
        """Constrói o grafo NetworkX a partir dos dados carregados."""
        # Adicionar vértices (distritos)
        for did, d in self.distritos.items():
            self.G.add_node(
                did,
                nome=d["nome"],
                zona=d["zona"],
                lat=d["lat"],
                lon=d["lon"],
                populacao=d["populacao"]
            )

        # Adicionar arestas (adjacências)
        for adj in self.adjacencias:
            self.G.add_edge(
                adj["distrito1_id"],
                adj["distrito2_id"],
                weight=adj["distancia_km"]
            )

    # ================================================================
    # Algoritmos de Grafos
    # ================================================================

    def dijkstra(self, origem_id: int, destino_id: int) -> tuple[float, list[int]]:
        """
        Calcula o menor caminho entre dois distritos usando Dijkstra.

        Args:
            origem_id: ID do distrito de origem.
            destino_id: ID do distrito de destino.

        Returns:
            Tupla (distância_total_km, lista_de_ids_no_caminho).
            Retorna (inf, []) se não houver caminho.
        """
        try:
            distancia = nx.dijkstra_path_length(
                self.G, origem_id, destino_id, weight="weight"
            )
            caminho = nx.dijkstra_path(
                self.G, origem_id, destino_id, weight="weight"
            )
            return round(distancia, 2), caminho
        except nx.NetworkXNoPath:
            return float("inf"), []

    def dijkstra_todos(self, origem_id: int) -> dict[int, float]:
        """
        Calcula a distância mínima de um distrito para todos os outros.

        Args:
            origem_id: ID do distrito de origem.

        Returns:
            Dicionário {distrito_id: distância_km}.
        """
        return dict(nx.single_source_dijkstra_path_length(
            self.G, origem_id, weight="weight"
        ))

    def bfs(self, origem_id: int, max_profundidade: int | None = None) -> dict[int, int]:
        """
        Executa BFS a partir de um distrito, retornando a profundidade de cada nó.

        Args:
            origem_id: ID do distrito de origem.
            max_profundidade: Profundidade máxima (None = sem limite).

        Returns:
            Dicionário {distrito_id: profundidade (nº de saltos)}.
        """
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
        self, distrito_id: int, tipo_servico: str
    ) -> tuple[dict | None, float, list[int]]:
        """
        Encontra a referência de serviço de saúde mais próxima de um distrito.

        Args:
            distrito_id: ID do distrito de origem.
            tipo_servico: Tipo de serviço ('hospital' ou 'ubs').

        Returns:
            Tupla (servico, distância_km, caminho).
            Retorna (None, inf, []) se não houver serviço acessível.
        """
        # Verificar se o próprio distrito tem o serviço
        servicos_locais = [
            s for s in self.servicos_por_distrito.get(distrito_id, [])
            if s["tipo"] == tipo_servico
        ]
        if servicos_locais:
            return servicos_locais[0], 0.0, [distrito_id]

        # Obter todos os distritos que têm esse tipo de serviço
        distritos_com_servico = set()
        for s in self.servicos_por_tipo.get(tipo_servico, []):
            distritos_com_servico.add(s["distrito_id"])

        if not distritos_com_servico:
            return None, float("inf"), []

        # Calcular distâncias mínimas para todos os distritos
        distancias = self.dijkstra_todos(distrito_id)

        # Encontrar o distrito com serviço mais próximo
        menor_dist = float("inf")
        melhor_distrito = None
        for did in distritos_com_servico:
            if did in distancias and distancias[did] < menor_dist:
                menor_dist = distancias[did]
                melhor_distrito = did

        if melhor_distrito is None:
            return None, float("inf"), []

        # Obter o caminho
        _, caminho = self.dijkstra(distrito_id, melhor_distrito)

        # Obter o serviço
        servico = next(
            s for s in self.servicos_por_tipo[tipo_servico]
            if s["distrito_id"] == melhor_distrito
        )

        return servico, round(menor_dist, 2), caminho

    # ================================================================
    # Métricas de Centralidade e Grau
    # ================================================================

    def grau_vertices(self) -> dict[int, int]:
        """Retorna o grau de cada vértice (número de conexões)."""
        return dict(self.G.degree())

    def centralidade_grau(self) -> dict[int, float]:
        """Calcula a centralidade de grau de cada vértice."""
        return nx.degree_centrality(self.G)

    def centralidade_proximidade(self) -> dict[int, float]:
        """Calcula a centralidade de proximidade (closeness) de cada vértice."""
        return nx.closeness_centrality(self.G, distance="weight")

    def centralidade_intermediacao(self) -> dict[int, float]:
        """Calcula a centralidade de intermediação (betweenness) de cada vértice."""
        return nx.betweenness_centrality(self.G, weight="weight")

    # ================================================================
    # Estatísticas do Grafo
    # ================================================================

    def estatisticas(self) -> dict:
        """Retorna estatísticas gerais do grafo."""
        graus = [d for _, d in self.G.degree()]
        return {
            "num_vertices": self.G.number_of_nodes(),
            "num_arestas": self.G.number_of_edges(),
            "grau_medio": round(sum(graus) / len(graus), 2) if graus else 0,
            "grau_maximo": max(graus) if graus else 0,
            "grau_minimo": min(graus) if graus else 0,
            "eh_conexo": nx.is_connected(self.G),
            "num_componentes": nx.number_connected_components(self.G),
            "densidade": round(nx.density(self.G), 4),
        }

    # ================================================================
    # Utilidades
    # ================================================================

    def get_posicoes(self) -> dict[int, tuple[float, float]]:
        """Retorna posições (lon, lat) para visualização do grafo."""
        return {
            did: (d["lon"], d["lat"])
            for did, d in self.distritos.items()
        }

    def get_nome(self, distrito_id: int) -> str:
        """Retorna o nome de um distrito pelo ID."""
        return self.distritos.get(distrito_id, {}).get("nome", "Desconhecido")

    def get_nomes_ordenados(self) -> list[tuple[int, str]]:
        """Retorna lista de (id, nome) ordenada por nome."""
        return sorted(
            [(did, d["nome"]) for did, d in self.distritos.items()],
            key=lambda x: x[1]
        )

    def get_tipos_servico(self) -> list[str]:
        """Retorna os tipos de serviço disponíveis."""
        return sorted(self.servicos_por_tipo.keys())

    def contar_servicos_distrito(self, distrito_id: int) -> dict[str, int]:
        """Conta os serviços por tipo em um distrito."""
        contagem = {}
        for s in self.servicos_por_distrito.get(distrito_id, []):
            contagem[s["tipo"]] = contagem.get(s["tipo"], 0) + 1
        return contagem
