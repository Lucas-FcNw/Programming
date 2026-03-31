"""
Geração do arquivo grafo.txt a partir dos JSONs do projeto.

Formato de saída compatível com o enunciado da disciplina.
Tipo escolhido: 3 (não orientado com peso nos vértices e arestas).
- Peso do vértice: população do distrito
- Peso da aresta: distância_km
"""

from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ARQ_DISTRITOS = DATA_DIR / "distritos.json"
ARQ_ARESTAS = DATA_DIR / "adjacencias.json"
ARQ_SAIDA = BASE_DIR / "grafo.txt"

TIPO_GRAFO = 3


def main() -> None:
    with open(ARQ_DISTRITOS, "r", encoding="utf-8") as f:
        distritos = json.load(f)

    with open(ARQ_ARESTAS, "r", encoding="utf-8") as f:
        arestas = json.load(f)

    linhas: list[str] = []
    linhas.append(str(TIPO_GRAFO))

    distritos_ordenados = sorted(distritos, key=lambda d: int(d["id"]))
    linhas.append(str(len(distritos_ordenados)))
    for d in distritos_ordenados:
        linhas.append(f'{int(d["id"])} "{d["nome"]}" {float(d["populacao"]):.2f}')

    arestas_ordenadas = sorted(
        arestas,
        key=lambda a: (int(a["distrito1_id"]), int(a["distrito2_id"]))
    )
    linhas.append(str(len(arestas_ordenadas)))
    for a in arestas_ordenadas:
        u = int(a["distrito1_id"])
        v = int(a["distrito2_id"])
        w = float(a["distancia_km"])
        linhas.append(f"{u} {v} {w:.2f}")

    ARQ_SAIDA.write_text("\n".join(linhas) + "\n", encoding="utf-8")

    print("grafo.txt gerado com sucesso")
    print(f"Tipo: {TIPO_GRAFO}")
    print(f"Vértices: {len(distritos_ordenados)}")
    print(f"Arestas: {len(arestas_ordenadas)}")


if __name__ == "__main__":
    main()
