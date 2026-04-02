from __future__ import annotations

from pathlib import Path
import shlex

BASE = Path(__file__).resolve().parent
ARQ_GRAFO = BASE / "grafo.txt"
ARQ_MERMAID_FULL = BASE / "modelagem_mermaid.md"
ARQ_MERMAID_RESUMO = BASE / "modelagem_mermaid_resumo.md"


def parse_grafo_txt(path: Path):
    linhas = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    i = 0
    tipo = int(linhas[i]); i += 1
    n = int(linhas[i]); i += 1

    vertices: list[tuple[int, str]] = []
    for _ in range(n):
        tok = shlex.split(linhas[i]); i += 1
        vid = int(tok[0])
        rotulo = tok[1] if len(tok) > 1 else f"V{vid}"
        vertices.append((vid, rotulo))

    m = int(linhas[i]); i += 1
    arestas: list[tuple[int, int, float | None]] = []
    tem_peso_aresta = tipo in {2, 3, 6, 7}
    for _ in range(m):
        tok = shlex.split(linhas[i]); i += 1
        u = int(tok[0])
        v = int(tok[1])
        w = float(tok[2]) if tem_peso_aresta and len(tok) >= 3 else None
        arestas.append((u, v, w))

    return tipo, vertices, arestas


def escape_label(texto: str) -> str:
    return texto.replace('"', "'")


def gerar_mermaid(tipo: int, vertices: list[tuple[int, str]], arestas: list[tuple[int, int, float | None]], limite_arestas: int | None = None) -> str:
    orientado = tipo in {4, 5, 6, 7}
    operador = "-->" if orientado else "---"

    linhas: list[str] = []
    linhas.append("```mermaid")
    linhas.append("graph LR")

    for vid, rotulo in vertices:
        linhas.append(f'  N{vid}["{vid} - {escape_label(rotulo)}"]')

    arestas_finais = arestas if limite_arestas is None else arestas[:limite_arestas]
    for u, v, w in arestas_finais:
        if w is None:
            linhas.append(f"  N{u} {operador} N{v}")
        else:
            linhas.append(f"  N{u} {operador}|{w:.2f}| N{v}")

    linhas.append("```")
    return "\n".join(linhas)


def main() -> None:
    tipo, vertices, arestas = parse_grafo_txt(ARQ_GRAFO)

    cabecalho = [
        "# Modelagem do Grafo em Mermaid",
        "",
        f"Tipo do grafo: {tipo}",
        f"Vértices: {len(vertices)}",
        f"Arestas: {len(arestas)}",
        "",
        "## Grafo completo",
        "",
    ]
    full = "\n".join(cabecalho) + gerar_mermaid(tipo, vertices, arestas) + "\n"
    ARQ_MERMAID_FULL.write_text(full, encoding="utf-8")

    cabecalho_resumo = [
        "# Modelagem do Grafo em Mermaid (Resumo)",
        "",
        f"Tipo do grafo: {tipo}",
        f"Vértices: {len(vertices)}",
        f"Arestas exibidas no resumo: {min(60, len(arestas))}",
        "",
        "## Subgrafo para visualização rápida",
        "",
    ]
    resumo = "\n".join(cabecalho_resumo) + gerar_mermaid(tipo, vertices, arestas, limite_arestas=60) + "\n"
    ARQ_MERMAID_RESUMO.write_text(resumo, encoding="utf-8")

    print(f"Gerado: {ARQ_MERMAID_FULL}")
    print(f"Gerado: {ARQ_MERMAID_RESUMO}")


if __name__ == "__main__":
    main()
