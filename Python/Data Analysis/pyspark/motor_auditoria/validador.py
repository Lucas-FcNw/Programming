"""
COMPONENTE E — Validador Estático de Implementação
====================================================
Para cada par (política DOC, política Notebook) que teve match,
verifica se a implementação respeita a especificação.

Valida:
  - Operador correto?
  - Campo correto?
  - Valor correto?
  - Lista completa?
  - Conectivo correto (E vs OU)?

Identifica tipos de erro:
  - Operador diferente
  - Valor faltante / extra
  - Campo errado
  - Lógica diferente
  - Regra parcialmente implementada
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Set

from leitor_docx import PoliticaEspecificada
from leitor_notebook import PoliticaInferida
from matcher import ResultadoMatch, StatusMatch


# ═══════════════════════════════════════════════════════════════
#  Classificação de status da validação
# ═══════════════════════════════════════════════════════════════

class StatusValidacao(Enum):
    CORRETA = "IMPLEMENTAÇÃO CORRETA"
    DIVERGENTE = "IMPLEMENTAÇÃO DIVERGENTE"
    PARCIAL = "IMPLEMENTAÇÃO PARCIAL"
    NAO_IMPLEMENTADA = "NÃO IMPLEMENTADA"
    AMBIGUA = "AMBÍGUA"


class TipoDivergencia(Enum):
    OPERADOR_DIFERENTE = "Operador diferente"
    VALOR_FALTANTE = "Valor faltante no código"
    VALOR_EXTRA = "Valor extra no código (não previsto no DOC)"
    VALOR_DIFERENTE = "Valor diferente"
    CAMPO_ERRADO = "Campo errado ou ausente"
    CAMPO_EXTRA = "Campo extra no código"
    CONECTIVO_DIFERENTE = "Conectivo lógico diferente (E vs OU)"
    LISTA_INCOMPLETA = "Lista de valores incompleta"
    LISTA_COM_EXTRAS = "Lista com valores extras"
    STRING_DIFERENTE = "String/categoria diferente"
    STRING_FALTANTE = "String/categoria faltante"


# ═══════════════════════════════════════════════════════════════
#  Representação de uma divergência
# ═══════════════════════════════════════════════════════════════

@dataclass
class Divergencia:
    """Uma divergência encontrada entre DOC e implementação."""
    tipo: TipoDivergencia
    descricao: str
    valor_esperado: str = ""
    valor_encontrado: str = ""

    def __str__(self) -> str:
        linha = f"  • {self.tipo.value}: {self.descricao}"
        if self.valor_esperado:
            linha += f"\n      Esperado:    {self.valor_esperado}"
        if self.valor_encontrado:
            linha += f"\n      Encontrado:  {self.valor_encontrado}"
        return linha


@dataclass
class ResultadoValidacao:
    """Resultado completo da validação de uma política."""
    politica_doc: PoliticaEspecificada
    politica_nb: Optional[PoliticaInferida]
    status: StatusValidacao
    divergencias: List[Divergencia] = field(default_factory=list)
    score_match: float = 0.0
    celula_notebook: Optional[int] = None

    def resumo(self) -> str:
        emoji = {
            StatusValidacao.CORRETA: "✅",
            StatusValidacao.DIVERGENTE: "⚠️ ",
            StatusValidacao.PARCIAL: "🔶",
            StatusValidacao.NAO_IMPLEMENTADA: "❌",
            StatusValidacao.AMBIGUA: "❓",
        }

        linhas = [
            f"{'─' * 55}",
            f"Política #{self.politica_doc.indice + 1}",
            f"  Texto:   \"{self.politica_doc.texto_original[:70]}{'...' if len(self.politica_doc.texto_original) > 70 else ''}\"",
            f"  Status:  {emoji.get(self.status, '')} {self.status.value}",
        ]

        if self.celula_notebook is not None:
            linhas.append(f"  Célula:  {self.celula_notebook}")
            linhas.append(f"  Match:   {self.score_match:.0%}")

        if self.divergencias:
            linhas.append(f"  Divergências ({len(self.divergencias)}):")
            for div in self.divergencias:
                linhas.append(str(div))

        return "\n".join(linhas)


# ═══════════════════════════════════════════════════════════════
#  Verificadores individuais
# ═══════════════════════════════════════════════════════════════

def _campo_tem_match_composto(campo_doc: str, campos_nb: Set[str]) -> bool:
    """Verifica se um campo do DOC tem correspondência composta no notebook.
    Ex: 'tipo' do DOC pode ser parte de 'tipo_contrato' no notebook.
    Ex: 'fator' do DOC pode ser parte de 'fator_risco' no notebook.
    Ex: 'prazo' do DOC pode ser parte de 'prazo_max' no notebook.
    """
    for campo_nb in campos_nb:
        # Campo do DOC é parte do campo do notebook (prefixo ou sufixo)
        partes = campo_nb.split('_')
        if campo_doc in partes:
            return True
        # Campo do notebook contém o campo do DOC
        if campo_doc in campo_nb:
            return True
    return False


def _verificar_campos(
    pol_doc: PoliticaEspecificada,
    pol_nb: PoliticaInferida,
) -> List[Divergencia]:
    """Verifica se os campos do DOC estão presentes no código."""
    divs = []

    campos_doc = pol_doc.campos
    campos_nb = pol_nb.campos

    # Campos do DOC que faltam no código (com verificação composta)
    faltantes = campos_doc - campos_nb
    for campo in faltantes:
        # Tenta match composto antes de reportar como erro
        if _campo_tem_match_composto(campo, campos_nb):
            continue  # Campo encontrado como parte de campo composto
        divs.append(Divergencia(
            tipo=TipoDivergencia.CAMPO_ERRADO,
            descricao=f"Campo '{campo}' mencionado no DOC não encontrado no código.",
            valor_esperado=campo,
            valor_encontrado=str(sorted(campos_nb)),
        ))

    # Campos no código que não estão no DOC (informativo, não necessariamente erro)
    extras = campos_nb - campos_doc
    for campo in extras:
        divs.append(Divergencia(
            tipo=TipoDivergencia.CAMPO_EXTRA,
            descricao=f"Campo '{campo}' presente no código mas não mencionado no DOC.",
            valor_encontrado=campo,
        ))

    return divs


def _verificar_operadores(
    pol_doc: PoliticaEspecificada,
    pol_nb: PoliticaInferida,
) -> List[Divergencia]:
    """Verifica se os operadores são compatíveis."""
    divs = []

    # Operadores relacionais do DOC (>, <, ==, etc.)
    ops_rel_doc = {op for op in pol_doc.operadores if op in {'>', '<', '>=', '<=', '==', '!='}}
    ops_rel_nb = {op for op in pol_nb.operadores if op in {'>', '<', '>=', '<=', '==', '!='}}

    # Se DOC tem operador relacional e Notebook tem outro diferente
    if ops_rel_doc and ops_rel_nb:
        # Verificar incompatibilidades diretas
        if '>' in ops_rel_doc and '<' in ops_rel_nb and '>' not in ops_rel_nb:
            divs.append(Divergencia(
                tipo=TipoDivergencia.OPERADOR_DIFERENTE,
                descricao="DOC pede '>' mas código implementa '<'.",
                valor_esperado=">",
                valor_encontrado="<",
            ))
        if '<' in ops_rel_doc and '>' in ops_rel_nb and '<' not in ops_rel_nb:
            divs.append(Divergencia(
                tipo=TipoDivergencia.OPERADOR_DIFERENTE,
                descricao="DOC pede '<' mas código implementa '>'.",
                valor_esperado="<",
                valor_encontrado=">",
            ))

    # Verificar isin
    if 'isin' in pol_doc.operadores and 'isin' not in pol_nb.operadores:
        divs.append(Divergencia(
            tipo=TipoDivergencia.OPERADOR_DIFERENTE,
            descricao="DOC exige operador 'pertence a lista' (isin) mas código não usa isin().",
            valor_esperado="isin",
            valor_encontrado=str(sorted(pol_nb.operadores)),
        ))

    return divs


def _normalizar_valor(v: str) -> str:
    """Normaliza valor numérico para comparação."""
    try:
        f = float(v)
        if f == int(f) and '.' not in v:
            return str(int(f))
        return str(f)
    except ValueError:
        return v


def _verificar_valores(
    pol_doc: PoliticaEspecificada,
    pol_nb: PoliticaInferida,
) -> List[Divergencia]:
    """Verifica se os valores numéricos conferem."""
    divs = []

    vals_doc = {_normalizar_valor(v) for v in pol_doc.valores}
    vals_nb = {_normalizar_valor(v) for v in pol_nb.valores}

    # Valores do DOC que não estão no código
    faltantes = vals_doc - vals_nb
    for val in faltantes:
        # Verifica se há um valor próximo (possível divergência sutil)
        proximo = _encontrar_valor_proximo(val, vals_nb)
        if proximo:
            divs.append(Divergencia(
                tipo=TipoDivergencia.VALOR_DIFERENTE,
                descricao=f"Valor '{val}' do DOC difere do valor '{proximo}' no código.",
                valor_esperado=val,
                valor_encontrado=proximo,
            ))
        else:
            divs.append(Divergencia(
                tipo=TipoDivergencia.VALOR_FALTANTE,
                descricao=f"Valor '{val}' do DOC não encontrado no código.",
                valor_esperado=val,
                valor_encontrado=str(sorted(vals_nb)) if vals_nb else "nenhum",
            ))

    # Valores no código que não estão no DOC
    extras = vals_nb - vals_doc
    for val in extras:
        # Só reporta se não é um valor "próximo" já reportado
        if not _encontrar_valor_proximo(val, vals_doc):
            divs.append(Divergencia(
                tipo=TipoDivergencia.VALOR_EXTRA,
                descricao=f"Valor '{val}' presente no código mas não previsto no DOC.",
                valor_encontrado=val,
            ))

    return divs


def _encontrar_valor_proximo(val: str, conjunto: set, tolerancia: float = 0.15) -> Optional[str]:
    """Encontra um valor numericamente próximo no conjunto."""
    try:
        num = float(val)
    except ValueError:
        return None

    for v in conjunto:
        try:
            outro = float(v)
            if num == 0 and outro == 0:
                continue
            # Diferença relativa
            base = max(abs(num), abs(outro), 1)
            diff = abs(num - outro) / base
            if 0 < diff <= tolerancia:
                return v
        except ValueError:
            continue

    return None


def _verificar_strings(
    pol_doc: PoliticaEspecificada,
    pol_nb: PoliticaInferida,
) -> List[Divergencia]:
    """Verifica se strings/categorias conferem."""
    divs = []

    strs_doc = {s.upper() for s in pol_doc.strings_literais}
    strs_nb = {s.upper() for s in pol_nb.strings_literais}

    # Ignora strings muito genéricas
    genericas = {'NORMAL', 'COMUM', 'PADRAO', 'DEFAULT'}

    faltantes = strs_doc - strs_nb - genericas
    for s in faltantes:
        divs.append(Divergencia(
            tipo=TipoDivergencia.STRING_DIFERENTE,
            descricao=f"String '{s}' do DOC não encontrada no código.",
            valor_esperado=s,
            valor_encontrado=str(sorted(strs_nb)) if strs_nb else "nenhum",
        ))

    return divs


def _verificar_conectivos(
    pol_doc: PoliticaEspecificada,
    pol_nb: PoliticaInferida,
) -> List[Divergencia]:
    """Verifica se conectivos lógicos são compatíveis."""
    divs = []

    conect_doc = pol_doc.conectivos
    conect_nb = pol_nb.conectivos

    # Caso mais grave: DOC diz OU, código usa E (ou vice-versa)
    if "OU" in conect_doc and "E" in conect_nb and "OU" not in conect_nb:
        divs.append(Divergencia(
            tipo=TipoDivergencia.CONECTIVO_DIFERENTE,
            descricao="DOC especifica 'OU' (qualquer condição), código implementa 'E' (todas as condições). Lógica invertida!",
            valor_esperado="OU",
            valor_encontrado="E",
        ))
    elif "E" in conect_doc and "OU" in conect_nb and "E" not in conect_nb:
        divs.append(Divergencia(
            tipo=TipoDivergencia.CONECTIVO_DIFERENTE,
            descricao="DOC especifica 'E' (todas as condições), código implementa 'OU' (qualquer condição). Lógica invertida!",
            valor_esperado="E",
            valor_encontrado="OU",
        ))

    return divs


def _verificar_listas(
    pol_doc: PoliticaEspecificada,
    pol_nb: PoliticaInferida,
) -> List[Divergencia]:
    """Verifica se listas de valores são completas."""
    divs = []

    # Compara listas (por posição, se ambos tiverem)
    listas_doc = pol_doc.listas
    listas_nb = pol_nb.listas

    if listas_doc and not listas_nb:
        divs.append(Divergencia(
            tipo=TipoDivergencia.LISTA_INCOMPLETA,
            descricao="DOC especifica lista de valores, mas código não usa isin() com lista.",
            valor_esperado=str(listas_doc[0]),
        ))

    for i, lista_doc in enumerate(listas_doc):
        if i < len(listas_nb):
            lista_nb = listas_nb[i]
            faltam = lista_doc - lista_nb
            extras = lista_nb - lista_doc
            if faltam:
                divs.append(Divergencia(
                    tipo=TipoDivergencia.LISTA_INCOMPLETA,
                    descricao=f"Valores faltantes na lista do código: {sorted(faltam)}",
                    valor_esperado=str(sorted(lista_doc)),
                    valor_encontrado=str(sorted(lista_nb)),
                ))
            if extras:
                divs.append(Divergencia(
                    tipo=TipoDivergencia.LISTA_COM_EXTRAS,
                    descricao=f"Valores extras na lista do código: {sorted(extras)}",
                    valor_esperado=str(sorted(lista_doc)),
                    valor_encontrado=str(sorted(lista_nb)),
                ))

    return divs


# ═══════════════════════════════════════════════════════════════
#  Motor de Validação
# ═══════════════════════════════════════════════════════════════

class Validador:
    """Valida implementações contra especificações."""

    def __init__(self, resultados_match: List[ResultadoMatch]):
        self.resultados_match = resultados_match
        self.resultados_validacao: List[ResultadoValidacao] = []

    def executar(self) -> List[ResultadoValidacao]:
        """Executa validação para todos os matches."""
        self.resultados_validacao = []

        for match in self.resultados_match:
            resultado = self._validar_um(match)
            self.resultados_validacao.append(resultado)

        return self.resultados_validacao

    def _validar_um(self, match: ResultadoMatch) -> ResultadoValidacao:
        """Valida um par DOC↔Notebook."""

        # Caso: não encontrado
        if match.status == StatusMatch.NAO_ENCONTRADO:
            return ResultadoValidacao(
                politica_doc=match.politica_doc,
                politica_nb=None,
                status=StatusValidacao.NAO_IMPLEMENTADA,
            )

        # Caso: ambíguo
        if match.status == StatusMatch.AMBIGUO:
            return ResultadoValidacao(
                politica_doc=match.politica_doc,
                politica_nb=match.melhor_match,
                status=StatusValidacao.AMBIGUA,
                score_match=match.score_similaridade,
                celula_notebook=match.melhor_match.indice_celula if match.melhor_match else None,
            )

        # Caso: tem match (forte ou fraco) → validar detalhes
        pol_doc = match.politica_doc
        pol_nb = match.melhor_match

        divergencias: List[Divergencia] = []

        # Executa todas as verificações
        divergencias.extend(_verificar_campos(pol_doc, pol_nb))
        divergencias.extend(_verificar_operadores(pol_doc, pol_nb))
        divergencias.extend(_verificar_valores(pol_doc, pol_nb))
        divergencias.extend(_verificar_strings(pol_doc, pol_nb))
        divergencias.extend(_verificar_conectivos(pol_doc, pol_nb))
        divergencias.extend(_verificar_listas(pol_doc, pol_nb))

        # Classifica resultado
        # Filtra divergências críticas (ignora campos extras, que são informativos)
        criticas = [d for d in divergencias if d.tipo not in {
            TipoDivergencia.CAMPO_EXTRA,
            TipoDivergencia.VALOR_EXTRA,
        }]

        if not criticas:
            status = StatusValidacao.CORRETA
        elif len(criticas) <= 2 and match.status == StatusMatch.MATCH_FORTE:
            status = StatusValidacao.DIVERGENTE
        elif match.status == StatusMatch.MATCH_FRACO:
            status = StatusValidacao.PARCIAL
        else:
            status = StatusValidacao.DIVERGENTE

        return ResultadoValidacao(
            politica_doc=pol_doc,
            politica_nb=pol_nb,
            status=status,
            divergencias=divergencias,
            score_match=match.score_similaridade,
            celula_notebook=pol_nb.indice_celula,
        )

    def relatorio(self) -> str:
        """Gera relatório final de validação."""
        contagem = {s: 0 for s in StatusValidacao}
        for r in self.resultados_validacao:
            contagem[r.status] += 1

        total_divs = sum(len(r.divergencias) for r in self.resultados_validacao)

        linhas = [
            "=" * 55,
            "  COMPONENTE E — Validação Estática",
            "=" * 55,
            f"  Total de políticas:  {len(self.resultados_validacao)}",
            f"  Total divergências:  {total_divs}",
            "",
            f"  ✅ Corretas:         {contagem[StatusValidacao.CORRETA]}",
            f"  ⚠️  Divergentes:      {contagem[StatusValidacao.DIVERGENTE]}",
            f"  🔶 Parciais:         {contagem[StatusValidacao.PARCIAL]}",
            f"  ❌ Não implementadas: {contagem[StatusValidacao.NAO_IMPLEMENTADA]}",
            f"  ❓ Ambíguas:         {contagem[StatusValidacao.AMBIGUA]}",
            "",
        ]

        for r in self.resultados_validacao:
            linhas.append(r.resumo())
            linhas.append("")

        return "\n".join(linhas)
