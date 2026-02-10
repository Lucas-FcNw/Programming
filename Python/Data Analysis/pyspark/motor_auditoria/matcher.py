"""
COMPONENTE D — Matching DOC ↔ Notebook
========================================
Compara políticas extraídas do DOCX (intenção) com políticas inferidas
do Notebook (implementação), sem assumir correspondência 1:1.

Estratégia:
  - Para cada política do DOC, compara com TODAS do Notebook
  - Calcula score de similaridade multidimensional
  - Seleciona melhor match e avalia confiança
  - Classifica: MATCH_FORTE, MATCH_FRACO, AMBIGUO, NAO_ENCONTRADO
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple

from leitor_docx import PoliticaEspecificada
from leitor_notebook import PoliticaInferida


# ═══════════════════════════════════════════════════════════════
#  Classificação de Match
# ═══════════════════════════════════════════════════════════════

class StatusMatch(Enum):
    MATCH_FORTE = "MATCH_FORTE"
    MATCH_FRACO = "MATCH_FRACO"
    AMBIGUO = "AMBIGUO"
    NAO_ENCONTRADO = "NAO_ENCONTRADO"


@dataclass
class ResultadoMatch:
    """Resultado do matching de uma política do DOC."""
    politica_doc: PoliticaEspecificada
    melhor_match: Optional[PoliticaInferida] = None
    score_similaridade: float = 0.0
    status: StatusMatch = StatusMatch.NAO_ENCONTRADO
    scores_detalhados: dict = field(default_factory=dict)
    candidatos: List[Tuple[PoliticaInferida, float]] = field(default_factory=list)
    motivo: str = ""

    def resumo(self) -> str:
        linhas = [
            f"Política DOC #{self.politica_doc.indice + 1}",
            f"  Texto:    \"{self.politica_doc.texto_original[:70]}{'...' if len(self.politica_doc.texto_original) > 70 else ''}\"",
            f"  Status:   {self.status.value}",
            f"  Score:    {self.score_similaridade:.2%}",
        ]
        if self.melhor_match:
            linhas.append(f"  Match:    célula {self.melhor_match.indice_celula}")
        if self.motivo:
            linhas.append(f"  Motivo:   {self.motivo}")
        if self.scores_detalhados:
            det = self.scores_detalhados
            linhas.append(f"  Detalhe:  campos={det.get('campos', 0):.0%}  ops={det.get('operadores', 0):.0%}  vals={det.get('valores', 0):.0%}  conect={det.get('conectivos', 0):.0%}  strs={det.get('strings', 0):.0%}")
        return "\n".join(linhas)


# ═══════════════════════════════════════════════════════════════
#  Limiares de decisão
# ═══════════════════════════════════════════════════════════════

LIMIAR_MATCH_FORTE = 0.55
LIMIAR_MATCH_FRACO = 0.30
LIMIAR_AMBIGUIDADE = 0.10   # diferença mínima entre 1º e 2º candidato

# Pesos de cada dimensão no score final
PESOS = {
    "campos": 0.35,
    "operadores": 0.20,
    "valores": 0.20,
    "conectivos": 0.10,
    "strings": 0.15,
}


# ═══════════════════════════════════════════════════════════════
#  Normalização de operadores para comparação cruzada
# ═══════════════════════════════════════════════════════════════

# O DOC pode ter ">" e o Notebook ">" — direto.
# Mas o DOC pode ter "isin" e o Notebook "isin" — também direto.
# Precisamos normalizar para comparação justa.

EQUIV_OPERADORES = {
    ">": {">", ">="},
    "<": {"<", "<="},
    ">=": {">=", ">"},
    "<=": {"<=", "<"},
    "==": {"=="},
    "!=": {"!="},
    "isin": {"isin"},
    "when": {"when"},
    "otherwise": {"otherwise"},
    "filter": {"filter", "where"},
    "where": {"where", "filter"},
}


# ═══════════════════════════════════════════════════════════════
#  Funções de similaridade por dimensão
# ═══════════════════════════════════════════════════════════════

def _similaridade_conjuntos(set_a: set, set_b: set) -> float:
    """Similaridade entre dois conjuntos, com suporte a campos compostos.
    Ex: 'tipo' do DOC pode fazer match parcial com 'tipo_contrato' do Notebook."""
    if not set_a and not set_b:
        return 0.0
    if not set_a or not set_b:
        return 0.0

    # Match direto (Jaccard)
    intersecao_direta = set_a & set_b

    # Match composto: 'tipo' do set_a bate com 'tipo_contrato' do set_b
    matches_compostos = set()
    nao_matched_a = set_a - intersecao_direta
    nao_matched_b = set_b - intersecao_direta
    for item_a in nao_matched_a:
        for item_b in nao_matched_b:
            partes_b = item_b.split('_')
            partes_a = item_a.split('_')
            if item_a in partes_b or item_b in partes_a or item_a in item_b or item_b in item_a:
                matches_compostos.add(item_a)
                break

    total_matches = len(intersecao_direta) + len(matches_compostos) * 0.7  # match composto vale 70%
    uniao = set_a | set_b
    return min(total_matches / len(uniao), 1.0)


def _similaridade_operadores(ops_doc: set, ops_nb: set) -> float:
    """Similaridade de operadores com equivalências."""
    if not ops_doc and not ops_nb:
        return 0.0
    if not ops_doc or not ops_nb:
        return 0.0

    # Expande cada operador do DOC com suas equivalências
    matches = 0
    total = len(ops_doc)

    for op_doc in ops_doc:
        equivalentes = EQUIV_OPERADORES.get(op_doc, {op_doc})
        if equivalentes & ops_nb:
            matches += 1

    return matches / total if total > 0 else 0.0


def _similaridade_valores(vals_doc: set, vals_nb: set) -> float:
    """Similaridade de valores numéricos (exata)."""
    if not vals_doc and not vals_nb:
        return 0.0
    if not vals_doc or not vals_nb:
        return 0.0

    # Normaliza valores (remove zeros à direita, trata floats)
    def normalizar(v):
        try:
            f = float(v)
            if f == int(f):
                return str(int(f))
            return str(f)
        except ValueError:
            return v

    norm_doc = {normalizar(v) for v in vals_doc}
    norm_nb = {normalizar(v) for v in vals_nb}

    intersecao = norm_doc & norm_nb
    uniao = norm_doc | norm_nb
    return len(intersecao) / len(uniao)


def _similaridade_strings(strs_doc: set, strs_nb: set) -> float:
    """Similaridade de strings literais (case-insensitive)."""
    if not strs_doc and not strs_nb:
        return 0.0
    if not strs_doc or not strs_nb:
        return 0.0

    norm_doc = {s.upper() for s in strs_doc}
    norm_nb = {s.upper() for s in strs_nb}

    intersecao = norm_doc & norm_nb
    uniao = norm_doc | norm_nb
    return len(intersecao) / len(uniao)


def _similaridade_conectivos(conect_doc: set, conect_nb: set) -> float:
    """Similaridade de conectivos lógicos."""
    if not conect_doc and not conect_nb:
        return 0.5  # ambos sem conectivo → neutro, não penaliza
    if not conect_doc or not conect_nb:
        return 0.0
    return 1.0 if conect_doc == conect_nb else 0.0


# ═══════════════════════════════════════════════════════════════
#  Cálculo de similaridade composta
# ═══════════════════════════════════════════════════════════════

def calcular_similaridade(
    pol_doc: PoliticaEspecificada,
    pol_nb: PoliticaInferida,
) -> Tuple[float, dict]:
    """
    Calcula score de similaridade entre uma política do DOC e uma do Notebook.
    Retorna (score_total, detalhes_por_dimensão).
    """
    scores = {}

    # 1. Campos em comum
    scores["campos"] = _similaridade_conjuntos(pol_doc.campos, pol_nb.campos)

    # 2. Operadores compatíveis
    scores["operadores"] = _similaridade_operadores(pol_doc.operadores, pol_nb.operadores)

    # 3. Valores numéricos
    scores["valores"] = _similaridade_valores(pol_doc.valores, pol_nb.valores)

    # 4. Conectivos
    scores["conectivos"] = _similaridade_conectivos(pol_doc.conectivos, pol_nb.conectivos)

    # 5. Strings literais
    scores["strings"] = _similaridade_strings(pol_doc.strings_literais, pol_nb.strings_literais)

    # Score ponderado
    score_total = sum(
        scores[dim] * PESOS[dim] for dim in PESOS
    )

    # Boost: se campos coincidem fortemente, o match é mais confiável
    if scores["campos"] >= 0.8:
        score_total = min(score_total * 1.15, 1.0)

    return score_total, scores


# ═══════════════════════════════════════════════════════════════
#  Motor de Matching
# ═══════════════════════════════════════════════════════════════

class Matcher:
    """Compara políticas DOC ↔ Notebook e encontra correspondências."""

    def __init__(
        self,
        politicas_doc: List[PoliticaEspecificada],
        politicas_nb: List[PoliticaInferida],
        limiar_forte: float = LIMIAR_MATCH_FORTE,
        limiar_fraco: float = LIMIAR_MATCH_FRACO,
        limiar_ambiguidade: float = LIMIAR_AMBIGUIDADE,
    ):
        self.politicas_doc = politicas_doc
        self.politicas_nb = politicas_nb
        self.limiar_forte = limiar_forte
        self.limiar_fraco = limiar_fraco
        self.limiar_ambiguidade = limiar_ambiguidade
        self.resultados: List[ResultadoMatch] = []

    def executar(self) -> List[ResultadoMatch]:
        """Executa matching de todas as políticas DOC contra o Notebook."""
        self.resultados = []

        for pol_doc in self.politicas_doc:
            resultado = self._match_uma_politica(pol_doc)
            self.resultados.append(resultado)

        return self.resultados

    def _match_uma_politica(self, pol_doc: PoliticaEspecificada) -> ResultadoMatch:
        """Encontra o melhor match no notebook para uma política do DOC."""
        candidatos: List[Tuple[PoliticaInferida, float, dict]] = []

        for pol_nb in self.politicas_nb:
            score, detalhes = calcular_similaridade(pol_doc, pol_nb)
            if score > 0:
                candidatos.append((pol_nb, score, detalhes))

        # Ordena por score decrescente
        candidatos.sort(key=lambda x: x[1], reverse=True)

        resultado = ResultadoMatch(politica_doc=pol_doc)
        resultado.candidatos = [(c[0], c[1]) for c in candidatos]

        if not candidatos:
            resultado.status = StatusMatch.NAO_ENCONTRADO
            resultado.motivo = "Nenhuma política inferida no notebook é compatível."
            return resultado

        melhor = candidatos[0]
        resultado.melhor_match = melhor[0]
        resultado.score_similaridade = melhor[1]
        resultado.scores_detalhados = melhor[2]

        # Classificação
        if melhor[1] >= self.limiar_forte:
            # Verifica ambiguidade: se o 2º candidato é muito próximo
            if len(candidatos) >= 2:
                diff = melhor[1] - candidatos[1][1]
                if diff < self.limiar_ambiguidade:
                    resultado.status = StatusMatch.AMBIGUO
                    resultado.motivo = (
                        f"Duas implementações com score próximo: "
                        f"célula {melhor[0].indice_celula} ({melhor[1]:.0%}) vs "
                        f"célula {candidatos[1][0].indice_celula} ({candidatos[1][1]:.0%})"
                    )
                    return resultado

            resultado.status = StatusMatch.MATCH_FORTE
            resultado.motivo = f"Match confiável com célula {melhor[0].indice_celula}."

        elif melhor[1] >= self.limiar_fraco:
            resultado.status = StatusMatch.MATCH_FRACO
            resultado.motivo = (
                f"Match parcial com célula {melhor[0].indice_celula}. "
                f"Score abaixo do limiar forte ({self.limiar_forte:.0%})."
            )
        else:
            resultado.status = StatusMatch.NAO_ENCONTRADO
            resultado.motivo = (
                f"Melhor candidato (célula {melhor[0].indice_celula}) "
                f"tem score muito baixo ({melhor[1]:.0%})."
            )

        return resultado

    def relatorio(self) -> str:
        """Gera relatório de matching."""
        contagem = {s: 0 for s in StatusMatch}
        for r in self.resultados:
            contagem[r.status] += 1

        linhas = [
            "=" * 55,
            "  COMPONENTE D — Matching DOC ↔ Notebook",
            "=" * 55,
            f"  Políticas DOC:       {len(self.politicas_doc)}",
            f"  Políticas Notebook:  {len(self.politicas_nb)}",
            "",
            f"  ✅ Match forte:      {contagem[StatusMatch.MATCH_FORTE]}",
            f"  ⚠️  Match fraco:      {contagem[StatusMatch.MATCH_FRACO]}",
            f"  🔶 Ambíguo:          {contagem[StatusMatch.AMBIGUO]}",
            f"  ❌ Não encontrado:   {contagem[StatusMatch.NAO_ENCONTRADO]}",
            "",
        ]

        for i, res in enumerate(self.resultados, 1):
            linhas.append(f"─── Match #{i} ───")
            linhas.append(res.resumo())
            linhas.append("")

        return "\n".join(linhas)
