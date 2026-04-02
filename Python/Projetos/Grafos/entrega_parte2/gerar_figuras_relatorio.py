from __future__ import annotations

from pathlib import Path
import json
import shlex

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

BASE = Path(__file__).resolve().parent
ARQ_GRAFO = BASE / "grafo.txt"
DIR_FIG = BASE / "figuras"
ARQ_METRICAS = DIR_FIG / "metricas.json"


def parse_grafo_txt(path: Path):
    linhas = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    i = 0
    tipo = int(linhas[i]); i += 1
    n = int(linhas[i]); i += 1

    vertices: list[tuple[int, str, float | None]] = []
    peso_vertice = tipo in {1, 3, 5, 7}
    for _ in range(n):
        tok = shlex.split(linhas[i]); i += 1
        vid = int(tok[0])
        rotulo = tok[1] if len(tok) > 1 else f"V{vid}"
        pv = float(tok[2]) if peso_vertice and len(tok) >= 3 else None
        vertices.append((vid, rotulo, pv))

    m = int(linhas[i]); i += 1
    arestas: list[tuple[int, int, float | None]] = []
    peso_aresta = tipo in {2, 3, 6, 7}
    for _ in range(m):
        tok = shlex.split(linhas[i]); i += 1
        u = int(tok[0])
        v = int(tok[1])
        pe = float(tok[2]) if peso_aresta and len(tok) >= 3 else None
        arestas.append((u, v, pe))

    return tipo, vertices, arestas


def construir_grafo(tipo: int, vertices, arestas):
    orientado = tipo in {4, 5, 6, 7}
    G = nx.DiGraph() if orientado else nx.Graph()

    for vid, rotulo, pv in vertices:
        G.add_node(vid, rotulo=rotulo, peso=pv)

    for u, v, pe in arestas:
        if pe is None:
            G.add_edge(u, v)
        else:
            G.add_edge(u, v, weight=pe)

    return G


def figura_visao_geral(G: nx.Graph, out: Path):
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, seed=42, k=0.28, iterations=200, weight="weight")

    pesos_pop = np.array([
        G.nodes[n].get("peso", 1.0) if G.nodes[n].get("peso") is not None else 1.0
        for n in G.nodes
    ], dtype=float)
    if pesos_pop.max() > pesos_pop.min():
        tamanhos = 120 + (pesos_pop - pesos_pop.min()) / (pesos_pop.max() - pesos_pop.min()) * 900
    else:
        tamanhos = np.full(len(G.nodes), 180.0)

    nx.draw_networkx_edges(G, pos, alpha=0.35, width=0.8, edge_color="#64748b")
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=tamanhos,
        node_color="#2563eb",
        alpha=0.85,
        linewidths=0.5,
        edgecolors="#0f172a",
    )

    top = sorted(G.degree, key=lambda x: x[1], reverse=True)[:8]
    labels = {n: G.nodes[n].get("rotulo", str(n)) for n, _ in top}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)

    plt.title("Visão Geral do Grafo de Distritos (n=71, m=215)")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out, dpi=220)
    plt.close()


def figura_histograma_graus(G: nx.Graph, out: Path):
    graus = [d for _, d in G.degree()]
    plt.figure(figsize=(10, 6))
    plt.hist(graus, bins=range(min(graus), max(graus) + 2), color="#0ea5e9", edgecolor="#0f172a")
    plt.title("Distribuição de Grau dos Vértices")
    plt.xlabel("Grau")
    plt.ylabel("Frequência")
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(out, dpi=220)
    plt.close()


def figura_matriz_adjacencia(G: nx.Graph, out: Path):
    ordem = sorted(G.nodes)
    A = nx.to_numpy_array(G, nodelist=ordem, weight="weight")

    plt.figure(figsize=(8, 8))
    plt.imshow(A, cmap="Blues", interpolation="nearest")
    plt.title("Matriz de Adjacência (ordem por ID de vértice)")
    plt.xlabel("Vértices")
    plt.ylabel("Vértices")
    plt.colorbar(label="Conexão")
    plt.tight_layout()
    plt.savefig(out, dpi=220)
    plt.close()


def salvar_metricas(G: nx.Graph, tipo: int, out: Path):
    graus = [d for _, d in G.degree()]
    orientado = tipo in {4, 5, 6, 7}

    metricas = {
        "tipo": tipo,
        "orientado": orientado,
        "num_vertices": G.number_of_nodes(),
        "num_arestas": G.number_of_edges(),
        "grau_medio": round(float(np.mean(graus)), 2) if graus else 0.0,
        "grau_maximo": int(np.max(graus)) if graus else 0,
        "grau_minimo": int(np.min(graus)) if graus else 0,
        "densidade": round(nx.density(G), 4),
    }

    if orientado and isinstance(G, nx.DiGraph):
        metricas["categoria_conexidade"] = "C3" if nx.is_strongly_connected(G) else (
            "C2" if nx.is_weakly_connected(G) else "C0/C1"
        )
    else:
        metricas["conexo"] = bool(nx.is_connected(G))
        metricas["num_componentes"] = int(nx.number_connected_components(G))

    top = sorted(G.degree, key=lambda x: x[1], reverse=True)[:10]
    metricas["top_10_graus"] = [
        {"id": int(n), "rotulo": G.nodes[n].get("rotulo", str(n)), "grau": int(g)}
        for n, g in top
    ]

    out.write_text(json.dumps(metricas, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    DIR_FIG.mkdir(parents=True, exist_ok=True)
    tipo, vertices, arestas = parse_grafo_txt(ARQ_GRAFO)
    G = construir_grafo(tipo, vertices, arestas)

    figura_visao_geral(G, DIR_FIG / "01_visao_geral_grafo.png")
    figura_histograma_graus(G, DIR_FIG / "02_histograma_graus.png")
    figura_matriz_adjacencia(G, DIR_FIG / "03_matriz_adjacencia.png")
    salvar_metricas(G, tipo, ARQ_METRICAS)

    print("Figuras e métricas geradas em:", DIR_FIG)


if __name__ == "__main__":
    main()
