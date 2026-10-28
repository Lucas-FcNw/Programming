"""
SPGraph - Módulo de Análise de Vulnerabilidade Topológica e Efeito Cascata
===========================================================================
Implementa o motor matemático de diagnóstico de fragilidade topológica e
simulação de colapso em cascata na malha de UBSs de São Paulo:

1. Caça-Gargalos Estruturais (Algoritmo de Tarjan via DFS, O(|V| + |E|)):
   - Detecção de Vértices de Articulação (pontos únicos de falha e "gargalos
     invisíveis" que parecem saudáveis na tabela isolada, mas partem a rede).
   - Detecção de Pontes Críticas (arestas cuja ruptura isola sub-regiões).

2. Simulação de Colapso e Efeito Cascata em Dominó (BFS em Camadas):
   - Redistribuição Local Gravitacional da Demanda (Modelo de Huff, 1963;
     3SFCA de Wan, Zou & Sternberg, 2012; Stacherl & Sauzet, 2023):
         W_uv = (C_v^alpha * d_topo(u,v)^(-beta)) / sum_k (C_k^alpha * d_topo(u,k)^(-beta))
   - Limite Operacional da Atenção Básica no SUS (Regra 70% Demanda Programada
     da região / 30% Demanda Espontânea - Cadernos de Atenção Básica n. 28)
     acoplado ao modelo de sobrecarga em cascata de Motter & Lai (2002),
     Crucitti, Latora & Marchiori (2004) e Wang et al. (2008).
"""

from __future__ import annotations

import sys
from collections import deque

try:
    import pandas as pd
except ImportError:
    pd = None

from src.grafo import GrafoSP


class AnaliseVulnerabilidade:
    """
    Motor de análise de vulnerabilidade topológica e efeito cascata
    da rede de Unidades Básicas de Saúde (UBSs) de São Paulo.
    """

    def __init__(self, grafo: GrafoSP):
        self.grafo = grafo

    # ================================================================
    # Algoritmo 1: Vértices de Articulação (Algoritmo de Tarjan - DFS)
    # ================================================================

    def _executar_tarjan(self, G=None) -> tuple[set[int], list[tuple[int, int]]]:
        """
        Implementação direta do Algoritmo de Tarjan (1972) via Busca em
        Profundidade (DFS) com vetores disc[u] e low[u].
        Complexidade de tempo: O(|V| + |E|).
        Complexidade de espaço: O(|V|).

        Returns:
            Tupla (conjunto_vertices_articulacao, lista_pontes).
        """
        if G is None:
            G = self.grafo.G

        sys.setrecursionlimit(max(2500, G.number_of_nodes() * 4))

        disc: dict[int, int] = {}
        low: dict[int, int] = {}
        parent: dict[int, int | None] = {}
        visitados: set[int] = set()
        articulacoes: set[int] = set()
        pontes: list[tuple[int, int]] = []
        timer = [0]

        def dfs(u: int) -> None:
            visitados.add(u)
            disc[u] = low[u] = timer[0]
            timer[0] += 1
            filhos_dfs = 0

            for v in G.neighbors(u):
                if v not in visitados:
                    filhos_dfs += 1
                    parent[v] = u
                    dfs(v)
                    low[u] = min(low[u], low[v])

                    # Regra 1 de Articulação: raiz da árvore DFS com 2 ou mais filhos
                    if parent.get(u) is None and filhos_dfs > 1:
                        articulacoes.add(u)
                    # Regra 2 de Articulação: u não é raiz e low[v] >= disc[u]
                    if parent.get(u) is not None and low[v] >= disc[u]:
                        articulacoes.add(u)
                    # Regra de Ponte: low[v] > disc[u]
                    if low[v] > disc[u]:
                        pontes.append((min(u, v), max(u, v)))

                elif v != parent.get(u):
                    # Aresta de retorno (back-edge) para ancestral na DFS
                    low[u] = min(low[u], disc[v])

        for no in G.nodes():
            if no not in visitados:
                parent[no] = None
                dfs(no)

        return articulacoes, sorted(pontes)

    def vertices_articulacao(self, tipo_servico: str | None = "ubs") -> list[dict]:
        """
        Identifica todos os vértices de articulação da rede de UBSs via Tarjan
        e destaca os "Gargalos Invisíveis" (unidades que aparentam estar saudáveis
        na tabela isolada, mas são pontos únicos de falha na topologia do grafo).
        """
        distritos_servico = (
            self.grafo.distritos_com_servico(tipo_servico) if tipo_servico else set()
        )
        articulacoes, _ = self._executar_tarjan()

        resultado: list[dict] = []
        for uid in sorted(articulacoes):
            u = self.grafo.distritos.get(uid, {})
            status_tab = u.get("status_tabela_isolada", "Verde (Ótimo)")
            eh_gargalo_invisivel = status_tab.startswith("Verde") or status_tab.startswith("Amarelo")

            # Medir quantas UBSs e moradores ficam desconectados da componente principal se uid cair
            G_sem = self.grafo.copiar_sem_nos({uid})
            comps = sorted(G_sem.componentes_conexas(), key=len, reverse=True)
            ubs_isoladas = sum(len(c) for c in comps[1:]) if len(comps) > 1 else 0
            pop_isolada = (
                sum(
                    self.grafo.distritos.get(nid, {}).get("demanda_base", 0)
                    for c in comps[1:]
                    for nid in c
                )
                if len(comps) > 1
                else 0
            )

            resultado.append({
                "distrito_id": uid,
                "ubs_id": uid,
                "cnes": u.get("cnes", ""),
                "distrito": u.get("nome", "?"),
                "nome_ubs": u.get("nome", "?"),
                "distrito_adm": u.get("distrito", "?"),
                "zona": u.get("zona", "?"),
                "populacao": u.get("demanda_base", u.get("populacao", 0)),
                "demanda_base": u.get("demanda_base", u.get("populacao", 0)),
                "capacidade": u.get("capacidade", 0),
                "folga_operacional": u.get("folga_operacional", 0),
                "folga_percentual": u.get("folga_percentual", 0.0),
                "taxa_ocupacao": u.get("taxa_ocupacao", 0.0),
                "status_tabela_isolada": status_tab,
                "gargalo_invisivel": eh_gargalo_invisivel,
                "ubs_isoladas_se_cair": ubs_isoladas,
                "pop_isolada_se_cair": pop_isolada,
                "grau": self.grafo.G.degree(uid),
                "tem_servico": uid in distritos_servico if tipo_servico else True,
            })

        resultado.sort(key=lambda x: (-x["pop_isolada_se_cair"], -x["grau"]))
        return resultado

    # ================================================================
    # Algoritmo 2: Pontes Críticas (Algoritmo de Tarjan - DFS)
    # ================================================================

    def pontes_criticas(self) -> list[dict]:
        """
        Identifica todas as pontes críticas (arestas de corte) da rede de UBSs
        usando o Algoritmo de Tarjan em O(|V| + |E|).
        """
        _, pontes = self._executar_tarjan()

        resultado: list[dict] = []
        for u, v in pontes:
            G_temp = self.grafo.G.copy()
            G_temp.remove_edge(u, v)

            # Componentes conexas via BFS após remoção da ponte (u, v)
            visitados: set[int] = set()
            pop_lados: list[int] = []
            ubs_lados: list[int] = []
            for no in G_temp.nodes():
                if no not in visitados:
                    comp_pop = 0
                    comp_ubs = 0
                    fila = deque([no])
                    visitados.add(no)
                    while fila:
                        atual = fila.popleft()
                        comp_ubs += 1
                        comp_pop += self.grafo.distritos.get(atual, {}).get("demanda_base", 0)
                        for viz in G_temp.neighbors(atual):
                            if viz not in visitados:
                                visitados.add(viz)
                                fila.append(viz)
                    pop_lados.append(comp_pop)
                    ubs_lados.append(comp_ubs)

            pares = sorted(zip(pop_lados, ubs_lados), key=lambda x: x[0])
            peso_km = float(self.grafo.G[u][v].get("weight", 0.0))
            peso_topo = float(self.grafo.G[u][v].get("impedancia_topografica_km", peso_km))

            resultado.append({
                "distrito1_id": u,
                "distrito1": self.grafo.get_nome(u),
                "distrito2_id": v,
                "distrito2": self.grafo.get_nome(v),
                "distancia_km": round(peso_km, 2),
                "impedancia_topografica_km": round(peso_topo, 2),
                "ubs_lado_menor": pares[0][1] if len(pares) > 1 else 0,
                "pop_lado_menor": pares[0][0] if len(pares) > 1 else 0,
                "pop_lado_maior": pares[-1][0] if pares else 0,
            })

        resultado.sort(key=lambda x: -x["pop_lado_menor"])
        return resultado

    # ================================================================
    # Algoritmo 3: Movimento da População (Huff / 3SFCA) + Cascata BFS
    # ================================================================

    def calcular_pesos_gravitacionais(
        self,
        ubs_origem_id: int,
        vizinhos_ativos: list[int],
        alpha: float = 1.0,
        beta: float = 2.0,
        usar_impedancia_topografica: bool = True,
    ) -> dict[int, dict]:
        """
        Calcula a distribuição probabilística da população que se desloca de
        uma UBS colapsada `u` para suas UBSs vizinhas ativas `v in N_ativas(u)`,
        segundo o Modelo Gravitacional de Huff (1963) e o peso de seleção de
        competição em saúde do método 3SFCA (Wan, Zou & Sternberg, 2012;
        Stacherl & Sauzet, 2023):

            W_uv = (C_v^alpha * d_uv^(-beta)) / sum_{k in N_ativas(u)} (C_k^alpha * d_uk^(-beta))

        Onde:
        - C_v é a capacidade instalada da UBS vizinha v;
        - d_uv é a impedância topográfica (ou distância Haversine) da aresta (u, v);
        - alpha controla a sensibilidade ao porte da unidade (padrão = 1.0);
        - beta é o coeficiente de decaimento por distância (padrão = 2.0).
        """
        if not vizinhos_ativos:
            return {}

        attr_dist = "impedancia_topografica_km" if usar_impedancia_topografica else "weight"
        atracoes: dict[int, float] = {}
        detalhes: dict[int, dict] = {}

        for vid in vizinhos_ativos:
            v_info = self.grafo.distritos[vid]
            cap_v = float(max(1, v_info.get("capacidade", 10000)))
            aresta = self.grafo.G[ubs_origem_id][vid]
            d_uv = max(0.10, float(aresta.get(attr_dist, aresta.get("weight", 1.0))))
            d_km = float(aresta.get("weight", d_uv))
            decliv = float(aresta.get("declividade_pct", 0.0))

            # Utilidade espacial gravitacional: A_uv = C_v^alpha * d_uv^(-beta)
            atracao = (cap_v ** alpha) * (d_uv ** (-beta))
            atracoes[vid] = atracao
            detalhes[vid] = {
                "vizinho_id": vid,
                "vizinho_nome": v_info["nome"],
                "distrito": v_info.get("distrito", ""),
                "zona": v_info.get("zona", ""),
                "capacidade": int(cap_v),
                "folga_operacional": int(v_info.get("folga_operacional", 0)),
                "distancia_km": round(d_km, 2),
                "impedancia_topografica_km": round(d_uv, 2),
                "declividade_pct": round(decliv, 2),
                "atracao_bruta": atracao,
            }

        soma_atracao = sum(atracoes.values())
        k_viz = len(vizinhos_ativos)
        for vid, info in detalhes.items():
            w_grav = (atracoes[vid] / soma_atracao) if soma_atracao > 0 else (1.0 / k_viz)
            info["peso_gravitacional"] = round(w_grav, 4)
            info["percentual_gravitacional"] = round(w_grav * 100.0, 2)
            info["percentual_divisao_igual"] = round((1.0 / k_viz) * 100.0, 2)

        return detalhes

    def comparar_divisao_demanda(
        self,
        ubs_id: int,
        alpha: float = 1.0,
        beta: float = 2.0,
    ) -> dict:
        """
        Compara o deslocamento populacional da UBS `ubs_id` segundo:
        1) A divisão igualitária ingênua (1/k para cada vizinho); vs.
        2) O Modelo Gravitacional Topográfico (Huff, 1963 / 3SFCA de Wan et al., 2012),
        avaliando o impacto sobre o limite de 30% de demanda espontânea (SUS).
        """
        u_info = self.grafo.distritos[ubs_id]
        demanda_u = int(u_info.get("demanda_base", 0))
        vizinhos = sorted(self.grafo.G.neighbors(ubs_id))
        pesos = self.calcular_pesos_gravitacionais(ubs_id, vizinhos, alpha=alpha, beta=beta)

        comparativo: list[dict] = []
        colapsos_igual = 0
        colapsos_grav = 0

        for vid in vizinhos:
            p = pesos[vid]
            folga_v = p["folga_operacional"]
            carga_igual = int(round(demanda_u / len(vizinhos))) if vizinhos else 0
            carga_grav = int(round(demanda_u * p["peso_gravitacional"]))

            estoura_igual = carga_igual > folga_v
            estoura_grav = carga_grav > folga_v
            if estoura_igual:
                colapsos_igual += 1
            if estoura_grav:
                colapsos_grav += 1

            comparativo.append({
                **p,
                "pacientes_divisao_igual": carga_igual,
                "pacientes_modelo_gravitacional": carga_grav,
                "diferenca_pacientes": carga_grav - carga_igual,
                "colapsa_na_divisao_igual": estoura_igual,
                "colapsa_no_gravitacional": estoura_grav,
            })

        comparativo.sort(key=lambda x: -x["peso_gravitacional"])
        return {
            "ubs_id": ubs_id,
            "ubs_nome": u_info["nome"],
            "distrito": u_info.get("distrito", ""),
            "zona": u_info.get("zona", ""),
            "demanda_remanejada": demanda_u,
            "num_vizinhos": len(vizinhos),
            "colapsos_previstos_divisao_igual": colapsos_igual,
            "colapsos_previstos_gravitacional": colapsos_grav,
            "vizinhos": comparativo,
        }

    def simular_cascata_bfs(
        self,
        ids_falha_inicial: int | list[int] | set[int],
        alpha: float = 1.0,
        beta: float = 2.0,
        max_camadas: int = 12,
    ) -> dict:
        """
        Simula o colapso inicial de um conjunto de UBSs e a propagação do
        EFEITO CASCATA (DOMINÓ) em camadas via Busca em Largura (BFS).

        Mecânica por camada k = 1, 2, ... (Motter & Lai, 2002; Wang et al., 2008):
        - Cada UBS v possui Capacidade C_v, Demanda Programada Local D_v^0 (~70%)
          e Folga Operacional máxima F_v <= 0.30 * C_v (cota de Demanda Espontânea).
        - Quando uma UBS u falha na camada k-1, sua carga desassistida é dividida
          entre suas vizinhas ativas v in N_ativas(u) proporcionalmente ao peso
          gravitacional W_uv (Huff, 1963 / 3SFCA de Wan et al., 2012).
        - Se a carga recebida por v ultrapassar sua folga disponível F_v, a UBS v
          absorve até seu limite operacional e ENTRA EM COLAPSO por sobrecarga,
          propagando o excedente para seus vizinhos na camada k+1 do BFS!
        """
        if isinstance(ids_falha_inicial, int):
            ids_falha_inicial = [ids_falha_inicial]
        iniciais_set = {uid for uid in ids_falha_inicial if uid in self.grafo.distritos}
        if not iniciais_set:
            return {
                "iniciais_removidas": [],
                "total_colapsadas": 0,
                "colapsadas_por_sobrecarga": [],
                "camadas_bfs": [],
                "saltos_maximos_bfs": 0,
                "demanda_inicial_desassistida": 0,
                "demanda_absorvida_total": 0,
                "demanda_isolada_sem_atendimento": 0,
                "estado_final_ubs": {},
            }

        # Estado dinâmico de cada UBS durante a cascata
        folga_restante: dict[int, float] = {
            uid: float(u.get("folga_operacional", 0))
            for uid, u in self.grafo.distritos.items()
        }
        carga_recebida: dict[int, float] = {uid: 0.0 for uid in self.grafo.distritos}
        ativas: set[int] = set(self.grafo.distritos.keys()) - iniciais_set
        colapsadas_cascata: list[dict] = []
        camada_colapso: dict[int, int] = {uid: 0 for uid in iniciais_set}

        # Fila de ondas do BFS: {ubs_id_que_falhou: carga_a_redistribuir}
        onda_atual: dict[int, float] = {
            uid: float(self.grafo.distritos[uid].get("demanda_base", 0))
            for uid in iniciais_set
        }
        demanda_inicial_total = int(round(sum(onda_atual.values())))
        demanda_absorvida_total = 0.0
        demanda_isolada_total = 0.0

        camadas_relatorio: list[dict] = []
        camada_idx = 0
        saltos_maximos = 0

        while onda_atual and camada_idx < max_camadas:
            camada_idx += 1
            fluxos_camada: list[dict] = []
            carga_chegando_vizinho: dict[int, float] = {}
            origens_por_vizinho: dict[int, list[int]] = {}

            for u_falha, carga_u in sorted(onda_atual.items()):
                if carga_u <= 0.5:
                    continue

                # Vizinhos imediatos que ainda estão ativos e com alguma folga ou abertos
                viz_ativos = [
                    v for v in self.grafo.G.neighbors(u_falha)
                    if v in ativas
                ]

                if not viz_ativos:
                    # Sem vizinhos ativos: população fica totalmente isolada!
                    demanda_isolada_total += carga_u
                    fluxos_camada.append({
                        "camada": camada_idx,
                        "origem_id": u_falha,
                        "origem_nome": self.grafo.get_nome(u_falha),
                        "destino_id": None,
                        "destino_nome": "NENHUMA (Região Isolada / Sem Saída Ativa)",
                        "peso_gravitacional_pct": 100.0,
                        "distancia_km": 0.0,
                        "impedancia_topo_km": 0.0,
                        "pacientes_transferidos": int(round(carga_u)),
                        "status_destino": "Isolamento Topológico Total",
                    })
                    continue

                pesos = self.calcular_pesos_gravitacionais(
                    u_falha, viz_ativos, alpha=alpha, beta=beta
                )
                for vid in viz_ativos:
                    w_uv = pesos[vid]["peso_gravitacional"]
                    delta_d = carga_u * w_uv
                    carga_chegando_vizinho[vid] = carga_chegando_vizinho.get(vid, 0.0) + delta_d
                    origens_por_vizinho.setdefault(vid, []).append(u_falha)
                    fluxos_camada.append({
                        "camada": camada_idx,
                        "origem_id": u_falha,
                        "origem_nome": self.grafo.get_nome(u_falha),
                        "destino_id": vid,
                        "destino_nome": self.grafo.get_nome(vid),
                        "peso_gravitacional_pct": pesos[vid]["percentual_gravitacional"],
                        "distancia_km": pesos[vid]["distancia_km"],
                        "impedancia_topo_km": pesos[vid]["impedancia_topografica_km"],
                        "pacientes_transferidos": int(round(delta_d)),
                        "status_destino": "Pendente avaliação da camada",
                    })

            if carga_chegando_vizinho:
                saltos_maximos = camada_idx

            # Avaliar quais vizinhos da Camada k absorvem a demanda e quais estouram os 30%
            proxima_onda: dict[int, float] = {}
            novos_colapsos_camada: list[dict] = []
            status_por_destino: dict[int, str] = {}

            for vid, carga_nova in sorted(carga_chegando_vizinho.items()):
                folga_disp = folga_restante[vid]
                u_info = self.grafo.distritos[vid]

                if carga_nova <= folga_disp:
                    # Vizinho absorve integralmente dentro da sua cota de 30%
                    folga_restante[vid] -= carga_nova
                    carga_recebida[vid] += carga_nova
                    demanda_absorvida_total += carga_nova
                    ocup_nova = (u_info["demanda_base"] + carga_recebida[vid]) / u_info["capacidade"]
                    status_por_destino[vid] = (
                        f"Absorveu ({ocup_nova * 100:.1f}% ocupação)"
                    )
                else:
                    # ESTOURO DE CAPACIDADE (> 100% / estourou os 30% de demanda espontânea!)
                    absorvido_local = folga_disp
                    excedente = carga_nova - absorvido_local
                    folga_restante[vid] = 0.0
                    carga_recebida[vid] += absorvido_local
                    demanda_absorvida_total += absorvido_local

                    # UBS entra em colapso operacional e propaga excedente para a Camada k+1
                    ativas.discard(vid)
                    camada_colapso[vid] = camada_idx
                    proxima_onda[vid] = excedente

                    info_colapso = {
                        "ubs_id": vid,
                        "nome": u_info["nome"],
                        "distrito": u_info.get("distrito", ""),
                        "zona": u_info.get("zona", ""),
                        "camada_bfs": camada_idx,
                        "capacidade": u_info["capacidade"],
                        "demanda_base": u_info["demanda_base"],
                        "folga_inicial_30": u_info["folga_operacional"],
                        "carga_recebida_camada": int(round(carga_nova)),
                        "excedente_repassado": int(round(excedente)),
                        "status_tabela_antes": u_info.get("status_tabela_isolada", ""),
                        "causado_por": [self.grafo.get_nome(oid) for oid in origens_por_vizinho.get(vid, [])],
                    }
                    colapsadas_cascata.append(info_colapso)
                    novos_colapsos_camada.append(info_colapso)
                    status_por_destino[vid] = (
                        f"COLAPSOU EM CASCATA (Excedente: +{int(round(excedente)):,} hab.)"
                    )

            for fl in fluxos_camada:
                dest_id = fl["destino_id"]
                if dest_id is not None and dest_id in status_por_destino:
                    fl["status_destino"] = status_por_destino[dest_id]

            camadas_relatorio.append({
                "camada": camada_idx,
                "num_ubs_origem": len(onda_atual),
                "num_ubs_atingidas": len(carga_chegando_vizinho),
                "novos_colapsos": novos_colapsos_camada,
                "num_novos_colapsos": len(novos_colapsos_camada),
                "fluxos": fluxos_camada,
            })

            onda_atual = proxima_onda

        # Se sobrar carga após max_camadas, contabilizar como desassistida
        if onda_atual:
            demanda_isolada_total += sum(onda_atual.values())

        estado_final: dict[int, dict] = {}
        for uid, u in self.grafo.distritos.items():
            if uid in iniciais_set:
                status_f = "Desativada (Falha Inicial - Camada 0)"
            elif uid in camada_colapso:
                status_f = f"Colapsada em Cascata (Camada {camada_colapso[uid]})"
            elif carga_recebida[uid] > 0:
                status_f = "Pressionada (Absorveu Transbordo)"
            else:
                status_f = "Normal (Sem Alteração)"

            estado_final[uid] = {
                "ubs_id": uid,
                "nome": u["nome"],
                "zona": u["zona"],
                "distrito": u.get("distrito", ""),
                "capacidade": u["capacidade"],
                "demanda_base": u["demanda_base"],
                "carga_extra_recebida": int(round(carga_recebida[uid])),
                "folga_restante": int(round(folga_restante[uid])),
                "status_final": status_f,
                "camada_colapso": camada_colapso.get(uid, None),
            }

        return {
            "iniciais_removidas": [
                {
                    "id": uid,
                    "nome": self.grafo.get_nome(uid),
                    "distrito": self.grafo.distritos[uid].get("distrito", ""),
                    "zona": self.grafo.distritos[uid].get("zona", ""),
                    "demanda_base": self.grafo.distritos[uid].get("demanda_base", 0),
                }
                for uid in sorted(iniciais_set)
            ],
            "num_iniciais": len(iniciais_set),
            "num_colapsadas_cascata": len(colapsadas_cascata),
            "total_colapsadas": len(iniciais_set) + len(colapsadas_cascata),
            "colapsadas_por_sobrecarga": colapsadas_cascata,
            "ids_colapsadas_cascata": [c["ubs_id"] for c in colapsadas_cascata],
            "camadas_bfs": camadas_relatorio,
            "saltos_maximos_bfs": saltos_maximos,
            "demanda_inicial_desassistida": demanda_inicial_total,
            "demanda_absorvida_total": int(round(demanda_absorvida_total)),
            "demanda_isolada_sem_atendimento": int(round(demanda_isolada_total)),
            "percentual_absorvido": round(
                (demanda_absorvida_total / demanda_inicial_total) * 100.0, 2
            ) if demanda_inicial_total > 0 else 100.0,
            "estado_final_ubs": estado_final,
        }

    # ================================================================
    # Algoritmo 4: Simulação Integrada (Topologia + Cascata BFS)
    # ================================================================

    def simular_fechamento(
        self,
        ids_remover: list[int],
        tipo_servico: str = "ubs",
        alpha: float = 1.0,
        beta: float = 2.0,
    ) -> dict:
        """
        Executa o diagnóstico completo de falha combinando:
        1) Fragmentação Topológica (componentes conexas antes e depois); e
        2) Simulação do Efeito Cascata em Dominó por Sobrecarga via BFS e
           Modelo Gravitacional de Huff/3SFCA (Regra 70/30 do SUS).
        """
        ids_set = {uid for uid in ids_remover if uid in self.grafo.distritos}

        # 1. Simular Cascata Gravitacional via BFS
        cascata = self.simular_cascata_bfs(list(ids_set), alpha=alpha, beta=beta)
        ids_todas_caidas = ids_set | set(cascata["ids_colapsadas_cascata"])

        # 2. Medir impacto topológico (antes vs depois considerando todas as UBSs caídas)
        comp_antes = self.grafo.componentes_conexas()
        grafo_pos = self.grafo.copiar_sem_nos(ids_todas_caidas)
        comp_depois = grafo_pos.componentes_conexas()
        distritos_servico_depois = grafo_pos.distritos_com_servico(tipo_servico)

        # Identificar UBSs que ficaram em ilhas totalmente desconectadas da malha principal
        comp_ordenadas = sorted(comp_depois, key=len, reverse=True)
        novos_sem_acesso: set[int] = set()
        if len(comp_ordenadas) > 1:
            for comp_menor in comp_ordenadas[1:]:
                novos_sem_acesso.update(comp_menor)

        pop_novos_sem_acesso = sum(
            grafo_pos.distritos.get(did, {}).get("demanda_base", 0)
            for did in novos_sem_acesso
        )

        # Montar resumo das UBSs que sofreram sobrecarga ou colapso em cascata
        aumento_distancia: dict[int, dict] = {}
        for uid, est in cascata["estado_final_ubs"].items():
            if uid in ids_set:
                continue
            if est["carga_extra_recebida"] > 0 or est["camada_colapso"] is not None:
                u_orig = self.grafo.distritos[uid]
                ocup_antes = round(u_orig["taxa_ocupacao"] * 100.0, 1)
                ocup_depois = round(
                    ((u_orig["demanda_base"] + est["carga_extra_recebida"]) / u_orig["capacidade"]) * 100.0,
                    1,
                )
                aumento_distancia[uid] = {
                    "distrito": u_orig["nome"],
                    "zona": u_orig["zona"],
                    "populacao": u_orig["demanda_base"],
                    "distancia_antes": ocup_antes,
                    "distancia_depois": ocup_depois,
                    "aumento_km": round(ocup_depois - ocup_antes, 1),
                    "carga_extra_recebida": est["carga_extra_recebida"],
                    "status_final": est["status_final"],
                }

        componentes_detalhadas = []
        for comp in comp_ordenadas:
            pop_comp = sum(
                grafo_pos.distritos.get(nid, {}).get("demanda_base", 0)
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
            "distritos_removidos": [
                {"id": did, "nome": self.grafo.get_nome(did)}
                for did in ids_remover if did in self.grafo.distritos
            ],
            "tipo_servico": tipo_servico,
            "componentes_antes": len(comp_antes),
            "media_distancia_antes": 0.0,
            "distritos_sem_acesso_antes": 0,
            "componentes_depois": len(comp_depois),
            "media_distancia_depois": float(cascata["saltos_maximos_bfs"]),
            "distritos_sem_acesso_depois": len(novos_sem_acesso) + cascata["num_colapsadas_cascata"],
            "novos_sem_acesso": sorted(novos_sem_acesso),
            "nomes_novos_sem_acesso": [
                grafo_pos.get_nome(did) for did in sorted(novos_sem_acesso)
            ],
            "pop_removida": cascata["demanda_inicial_desassistida"],
            "pop_novos_sem_acesso": pop_novos_sem_acesso + cascata["demanda_isolada_sem_atendimento"],
            "aumento_medio_distancia": float(cascata["saltos_maximos_bfs"]),
            "distritos_com_aumento": dict(sorted(
                aumento_distancia.items(),
                key=lambda x: -x[1]["carga_extra_recebida"],
            )),
            "componentes": componentes_detalhadas,
            "cascata": cascata,
        }

    def componentes_pos_falha(
        self,
        ids_remover: list[int],
        tipo_servico: str = "ubs",
    ) -> list[dict]:
        """
        Retorna as componentes conexas remanescentes após a falha inicial + cascata.
        """
        cascata = self.simular_cascata_bfs(ids_remover)
        ids_todas_caidas = set(ids_remover) | set(cascata["ids_colapsadas_cascata"])
        grafo_pos = self.grafo.copiar_sem_nos(ids_todas_caidas)
        componentes = sorted(grafo_pos.componentes_conexas(), key=lambda c: -len(c))
        distritos_servico = grafo_pos.distritos_com_servico(tipo_servico)

        resultado = []
        for i, comp in enumerate(componentes, start=1):
            pop = sum(
                grafo_pos.distritos.get(nid, {}).get("demanda_base", 0)
                for nid in comp
            )
            servicos_na_comp = comp & distritos_servico
            isolada = (i > 1) or (len(servicos_na_comp) == 0)

            resultado.append({
                "componente_id": i,
                "distritos_ids": sorted(comp),
                "nomes": sorted(grafo_pos.get_nome(nid) for nid in comp),
                "num_distritos": len(comp),
                "populacao": pop,
                "tem_servico": len(servicos_na_comp) > 0,
                "num_distritos_com_servico": len(servicos_na_comp),
                "isolada": isolada,
            })

        return resultado

    # ================================================================
    # Algoritmo 5: Ranking de Criticidade Topológica e de Cascata
    # ================================================================

    def ranking_criticidade(self, tipo_servico: str = "ubs"):
        """
        Classifica todas as UBSs da rede pelo seu impacto de falha individual:
        - Se é Vértice de Articulação (Tarjan) e se é um "Gargalo Invisível";
        - Quantas UBSs vizinhas derruba em cascata (efeito dominó via BFS);
        - Quantos saltos o BFS precisa expandir até absorver a demanda;
        - População total isolada ou afetada.
        """
        articulacoes, _ = self._executar_tarjan()

        dados: list[dict] = []
        for uid in sorted(self.grafo.distritos.keys()):
            u = self.grafo.distritos[uid]
            cascata = self.simular_cascata_bfs([uid])
            ids_caidas = {uid} | set(cascata["ids_colapsadas_cascata"])
            G_sem = self.grafo.copiar_sem_nos(ids_caidas)
            comps = sorted(G_sem.componentes_conexas(), key=len, reverse=True)
            ubs_isoladas_topo = sum(len(c) for c in comps[1:]) if len(comps) > 1 else 0
            pop_isolada_topo = (
                sum(
                    self.grafo.distritos.get(nid, {}).get("demanda_base", 0)
                    for c in comps[1:]
                    for nid in c
                )
                if len(comps) > 1
                else 0
            )

            num_cascata = cascata["num_colapsadas_cascata"]
            saltos = cascata["saltos_maximos_bfs"]
            pop_desassistida = pop_isolada_topo + cascata["demanda_isolada_sem_atendimento"]

            # Score composto de fragilidade topológica + efeito cascata
            score = 0.0
            score += 25.0 if uid in articulacoes else 0.0
            score += num_cascata * 18.0
            score += ubs_isoladas_topo * 12.0
            score += saltos * 4.0
            score += (u.get("demanda_base", 0) / 10000.0) * 2.0
            score += (pop_desassistida / 10000.0) * 5.0

            dados.append({
                "distrito_id": uid,
                "distrito": u["nome"],
                "distrito_adm": u.get("distrito", ""),
                "zona": u["zona"],
                "populacao": u.get("demanda_base", 0),
                "capacidade": u.get("capacidade", 0),
                "folga_operacional": u.get("folga_operacional", 0),
                "status_tabela_isolada": u.get("status_tabela_isolada", ""),
                "grau": self.grafo.G.degree(uid),
                "eh_articulacao": uid in articulacoes,
                "ubs_colapsadas_cascata": num_cascata,
                "saltos_bfs": saltos,
                "componentes_apos_remocao": len(comps),
                "novos_sem_acesso": ubs_isoladas_topo + num_cascata,
                "pop_sem_acesso": pop_desassistida,
                "aumento_distancia_media": float(saltos),
                "score_criticidade": round(score, 1),
            })

        dados.sort(key=lambda x: -x["score_criticidade"])
        for i, row in enumerate(dados, start=1):
            row["posicao"] = i

        if pd is not None:
            colunas = [
                "posicao", "distrito_id", "distrito", "distrito_adm", "zona",
                "populacao", "capacidade", "folga_operacional", "status_tabela_isolada",
                "grau", "eh_articulacao", "ubs_colapsadas_cascata", "saltos_bfs",
                "componentes_apos_remocao", "novos_sem_acesso",
                "pop_sem_acesso", "aumento_distancia_media", "score_criticidade",
            ]
            return pd.DataFrame(dados)[colunas]
        return dados
