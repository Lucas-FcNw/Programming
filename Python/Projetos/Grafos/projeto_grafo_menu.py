"""
Projeto de Grafos - Parte 2 (Menu obrigatório)
================================================
Aplicação textual com menu de opções para leitura, gravação e manipulação
no formato grafo.txt solicitado na disciplina.

Integrantes:
- Lucas Fernandes de Camargo — RA 10419400
- Lendy Naiara Carpio Pacheco — RA 10428525
- Anna Luiza Stella Santos — RA 10417401

"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from collections import deque
import shlex


ARQUIVO_PADRAO = Path("grafo.txt")


@dataclass
class Vertice:
    id: int
    rotulo: str
    peso: float | None = None


class GrafoListaAdj:
    """Grafo em lista de adjacência compatível com o arquivo grafo.txt."""

    def __init__(self) -> None:
        self.tipo: int = 2
        self.vertices: dict[int, Vertice] = {}
        self.adj: dict[int, dict[int, float | None]] = {}

    # -----------------------------------------------------------------
    # Regras derivadas do tipo
    # -----------------------------------------------------------------
    @property
    def orientado(self) -> bool:
        return self.tipo in {4, 5, 6, 7}

    @property
    def peso_vertice(self) -> bool:
        return self.tipo in {1, 3, 5, 7}

    @property
    def peso_aresta(self) -> bool:
        return self.tipo in {2, 3, 6, 7}

    # -----------------------------------------------------------------
    # Operações básicas
    # -----------------------------------------------------------------
    def limpar(self) -> None:
        self.vertices.clear()
        self.adj.clear()

    def inserir_vertice(self, vid: int, rotulo: str, peso: float | None = None) -> bool:
        if vid in self.vertices:
            return False
        if self.peso_vertice and peso is None:
            peso = 0.0
        self.vertices[vid] = Vertice(id=vid, rotulo=rotulo, peso=peso)
        self.adj[vid] = {}
        return True

    def inserir_aresta(self, u: int, v: int, peso: float | None = None) -> bool:
        if u not in self.vertices or v not in self.vertices:
            return False
        if self.peso_aresta and peso is None:
            peso = 1.0
        if not self.peso_aresta:
            peso = None

        self.adj[u][v] = peso
        if not self.orientado:
            self.adj[v][u] = peso
        return True

    def remover_aresta(self, u: int, v: int) -> bool:
        if u not in self.adj or v not in self.adj:
            return False

        removeu = False
        if v in self.adj[u]:
            del self.adj[u][v]
            removeu = True
        if not self.orientado and u in self.adj[v]:
            del self.adj[v][u]
            removeu = True or removeu
        return removeu

    def remover_vertice(self, vid: int) -> bool:
        if vid not in self.vertices:
            return False

        del self.vertices[vid]
        if vid in self.adj:
            del self.adj[vid]

        for u in list(self.adj.keys()):
            if vid in self.adj[u]:
                del self.adj[u][vid]
        return True

    def numero_arestas(self) -> int:
        if self.orientado:
            return sum(len(vs) for vs in self.adj.values())
        total = sum(len(vs) for vs in self.adj.values())
        return total // 2

    # -----------------------------------------------------------------
    # Entrada/Saída (grafo.txt)
    # -----------------------------------------------------------------
    def carregar_arquivo(self, caminho: Path) -> None:
        linhas = [ln.strip() for ln in caminho.read_text(encoding="utf-8").splitlines() if ln.strip()]
        if len(linhas) < 3:
            raise ValueError("Arquivo inválido: conteúdo insuficiente.")

        p = 0
        tipo = int(linhas[p]); p += 1
        n = int(linhas[p]); p += 1

        novo = GrafoListaAdj()
        novo.tipo = tipo

        for _ in range(n):
            tokens = shlex.split(linhas[p])
            p += 1
            if len(tokens) < 2:
                raise ValueError("Linha de vértice inválida.")
            vid = int(tokens[0])
            rotulo = tokens[1]
            peso_v = float(tokens[2]) if novo.peso_vertice and len(tokens) >= 3 else None
            novo.inserir_vertice(vid, rotulo, peso_v)

        m = int(linhas[p]); p += 1
        for _ in range(m):
            tokens = shlex.split(linhas[p])
            p += 1
            if len(tokens) < 2:
                raise ValueError("Linha de aresta inválida.")
            u = int(tokens[0])
            v = int(tokens[1])
            peso_a = float(tokens[2]) if novo.peso_aresta and len(tokens) >= 3 else None
            novo.inserir_aresta(u, v, peso_a)

        self.tipo = novo.tipo
        self.vertices = novo.vertices
        self.adj = novo.adj

    def salvar_arquivo(self, caminho: Path) -> None:
        linhas: list[str] = []
        linhas.append(str(self.tipo))
        linhas.append(str(len(self.vertices)))

        for vid in sorted(self.vertices):
            v = self.vertices[vid]
            if self.peso_vertice:
                linhas.append(f'{v.id} "{v.rotulo}" {float(v.peso if v.peso is not None else 0.0):.2f}')
            else:
                linhas.append(f'{v.id} "{v.rotulo}"')

        arestas = self._listar_arestas_salvamento()
        linhas.append(str(len(arestas)))
        for u, v, peso in arestas:
            if self.peso_aresta:
                linhas.append(f"{u} {v} {float(peso if peso is not None else 1.0):.2f}")
            else:
                linhas.append(f"{u} {v}")

        caminho.write_text("\n".join(linhas) + "\n", encoding="utf-8")

    def _listar_arestas_salvamento(self) -> list[tuple[int, int, float | None]]:
        arestas: list[tuple[int, int, float | None]] = []
        if self.orientado:
            for u in sorted(self.adj):
                for v in sorted(self.adj[u]):
                    arestas.append((u, v, self.adj[u][v]))
            return arestas

        vistos: set[tuple[int, int]] = set()
        for u in sorted(self.adj):
            for v in sorted(self.adj[u]):
                a, b = (u, v) if u <= v else (v, u)
                if (a, b) not in vistos:
                    vistos.add((a, b))
                    arestas.append((a, b, self.adj[u][v]))
        return arestas

    # -----------------------------------------------------------------
    # Visualização
    # -----------------------------------------------------------------
    def mostrar_lista_adjacencia(self) -> str:
        linhas = []
        linhas.append(f"Tipo: {self.tipo} ({'orientado' if self.orientado else 'não orientado'})")
        linhas.append(f"Vértices: {len(self.vertices)} | Arestas: {self.numero_arestas()}")
        linhas.append("-")
        for vid in sorted(self.vertices):
            v = self.vertices[vid]
            if self.peso_vertice:
                cab = f"[{vid}] {v.rotulo} (peso={v.peso})"
            else:
                cab = f"[{vid}] {v.rotulo}"

            vizinhos = []
            for nb in sorted(self.adj.get(vid, {})):
                if self.peso_aresta:
                    vizinhos.append(f"{nb}(w={self.adj[vid][nb]})")
                else:
                    vizinhos.append(str(nb))
            linhas.append(cab + " -> " + (", ".join(vizinhos) if vizinhos else "∅"))
        return "\n".join(linhas)

    # -----------------------------------------------------------------
    # Conexidade e reduzido
    # -----------------------------------------------------------------
    def analisar_conexidade(self) -> str:
        if not self.vertices:
            return "Grafo vazio."
        if not self.orientado:
            eh_conexo = self._eh_conexo_nao_orientado()
            return "Grafo não orientado: CONEXO." if eh_conexo else "Grafo não orientado: DESCONEXO."

        cat = self._categoria_direcionado()
        partes = [f"Grafo orientado: categoria {cat}."]

        comps = self._componentes_fortemente_conexas()
        partes.append(f"Componentes fortemente conexas (FCONEX): {len(comps)}")

        reduzido = self._grafo_reduzido(comps)
        partes.append("Grafo reduzido (componentes como nós):")
        for c in sorted(reduzido):
            alvos = sorted(reduzido[c])
            partes.append(f"  C{c} -> {alvos if alvos else []}")

        return "\n".join(partes)

    def _eh_conexo_nao_orientado(self) -> bool:
        inicio = next(iter(self.vertices))
        visitados = set([inicio])
        fila = deque([inicio])
        while fila:
            u = fila.popleft()
            for v in self.adj.get(u, {}):
                if v not in visitados:
                    visitados.add(v)
                    fila.append(v)
        return len(visitados) == len(self.vertices)

    def _alcanca(self, origem: int, alvo: int) -> bool:
        if origem == alvo:
            return True
        pilha = [origem]
        vis = {origem}
        while pilha:
            u = pilha.pop()
            for v in self.adj.get(u, {}):
                if v == alvo:
                    return True
                if v not in vis:
                    vis.add(v)
                    pilha.append(v)
        return False

    def _categoria_direcionado(self) -> str:
        ids = sorted(self.vertices.keys())

        # C3: fortemente conexo
        if all(self._alcanca(u, v) and self._alcanca(v, u) for i, u in enumerate(ids) for v in ids[i + 1:]):
            return "C3 (fortemente conexo)"

        # C2: unilateralmente conexo
        if all(self._alcanca(u, v) or self._alcanca(v, u) for i, u in enumerate(ids) for v in ids[i + 1:]):
            return "C2 (unilateralmente conexo)"

        # C1: fracamente conexo
        if self._eh_fracamente_conexo():
            return "C1 (fracamente conexo)"

        # C0: desconexo
        return "C0 (desconexo)"

    def _eh_fracamente_conexo(self) -> bool:
        # Converte implicitamente para não orientado
        und: dict[int, set[int]] = {v: set() for v in self.vertices}
        for u in self.adj:
            for v in self.adj[u]:
                und[u].add(v)
                und[v].add(u)

        inicio = next(iter(self.vertices))
        vis = {inicio}
        fila = deque([inicio])
        while fila:
            u = fila.popleft()
            for v in und[u]:
                if v not in vis:
                    vis.add(v)
                    fila.append(v)
        return len(vis) == len(self.vertices)

    def _componentes_fortemente_conexas(self) -> list[list[int]]:
        # Kosaraju
        vis: set[int] = set()
        ordem: list[int] = []

        def dfs1(u: int) -> None:
            vis.add(u)
            for v in self.adj.get(u, {}):
                if v not in vis:
                    dfs1(v)
            ordem.append(u)

        for u in self.vertices:
            if u not in vis:
                dfs1(u)

        rev: dict[int, list[int]] = {u: [] for u in self.vertices}
        for u in self.adj:
            for v in self.adj[u]:
                rev[v].append(u)

        vis.clear()
        comps: list[list[int]] = []

        def dfs2(u: int, comp: list[int]) -> None:
            vis.add(u)
            comp.append(u)
            for v in rev.get(u, []):
                if v not in vis:
                    dfs2(v, comp)

        for u in reversed(ordem):
            if u not in vis:
                comp: list[int] = []
                dfs2(u, comp)
                comps.append(sorted(comp))

        return comps

    def _grafo_reduzido(self, comps: list[list[int]]) -> dict[int, set[int]]:
        comp_id: dict[int, int] = {}
        for i, comp in enumerate(comps, start=1):
            for v in comp:
                comp_id[v] = i

        reduzido: dict[int, set[int]] = {i: set() for i in range(1, len(comps) + 1)}
        for u in self.adj:
            for v in self.adj[u]:
                cu, cv = comp_id[u], comp_id[v]
                if cu != cv:
                    reduzido[cu].add(cv)
        return reduzido


def mostrar_titulo() -> None:
    print("\n" + "=" * 70)
    print("SPGraph - Projeto de Teoria dos Grafos (Parte 2)")
    print("Menu de Operações no arquivo grafo.txt")
    print("=" * 70)


def mostrar_menu() -> None:
    print("\nEscolha uma opção:")
    print("a) Ler dados do arquivo grafo.txt")
    print("b) Gravar dados no arquivo grafo.txt")
    print("c) Inserir vértice")
    print("d) Inserir aresta")
    print("e) Remover vértice")
    print("f) Remover aresta")
    print("g) Mostrar conteúdo do arquivo")
    print("h) Mostrar grafo (lista de adjacência)")
    print("i) Apresentar conexidade e reduzido")
    print("j) Encerrar aplicação")


def ler_float(msg: str) -> float:
    while True:
        try:
            return float(input(msg).strip().replace(",", "."))
        except ValueError:
            print("Valor inválido. Tente novamente.")


def ler_int(msg: str) -> int:
    while True:
        try:
            return int(input(msg).strip())
        except ValueError:
            print("Valor inválido. Tente novamente.")


def main() -> None:
    grafo = GrafoListaAdj()

    mostrar_titulo()

    while True:
        mostrar_menu()
        op = input("Opção: ").strip().lower()

        if op == "a":
            caminho = Path(input(f"Arquivo [{ARQUIVO_PADRAO}]: ").strip() or str(ARQUIVO_PADRAO))
            try:
                grafo.carregar_arquivo(caminho)
                print("Leitura concluída com sucesso.")
            except Exception as e:
                print(f"Erro na leitura: {e}")

        elif op == "b":
            caminho = Path(input(f"Arquivo [{ARQUIVO_PADRAO}]: ").strip() or str(ARQUIVO_PADRAO))
            try:
                grafo.salvar_arquivo(caminho)
                print("Gravação concluída com sucesso.")
            except Exception as e:
                print(f"Erro na gravação: {e}")

        elif op == "c":
            vid = ler_int("ID do vértice: ")
            rotulo = input("Rótulo/apelido do vértice: ").strip() or f"V{vid}"
            peso = ler_float("Peso do vértice: ") if grafo.peso_vertice else None
            ok = grafo.inserir_vertice(vid, rotulo, peso)
            print("Vértice inserido." if ok else "ID já existente.")

        elif op == "d":
            u = ler_int("Vértice origem: ")
            v = ler_int("Vértice destino: ")
            peso = ler_float("Peso da aresta: ") if grafo.peso_aresta else None
            ok = grafo.inserir_aresta(u, v, peso)
            print("Aresta inserida." if ok else "Falha: vértices inexistentes.")

        elif op == "e":
            vid = ler_int("ID do vértice a remover: ")
            ok = grafo.remover_vertice(vid)
            print("Vértice removido." if ok else "Vértice não encontrado.")

        elif op == "f":
            u = ler_int("Vértice origem da aresta: ")
            v = ler_int("Vértice destino da aresta: ")
            ok = grafo.remover_aresta(u, v)
            print("Aresta removida." if ok else "Aresta não encontrada.")

        elif op == "g":
            caminho = Path(input(f"Arquivo [{ARQUIVO_PADRAO}]: ").strip() or str(ARQUIVO_PADRAO))
            if not caminho.exists():
                print("Arquivo não encontrado.")
            else:
                print("\n--- Conteúdo do arquivo ---")
                print(caminho.read_text(encoding="utf-8"))
                print("--- fim ---")

        elif op == "h":
            print("\n" + grafo.mostrar_lista_adjacencia())

        elif op == "i":
            print("\n" + grafo.analisar_conexidade())

        elif op == "j":
            print("Aplicação encerrada.")
            break

        else:
            print("Opção inválida. Escolha entre a e j.")


if __name__ == "__main__":
    main()
