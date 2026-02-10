"""
ORQUESTRADOR — Motor de Auditoria de Políticas de Crédito
==========================================================
Pipeline completo:
  1. Gera mocks (DOCX + Notebook)          — Componente A
  2. Infere políticas do Notebook           — Componente B
  3. Extrai políticas do DOCX               — Componente C
  4. Matching DOC ↔ Notebook                — Componente D
  5. Validação estática de implementação    — Componente E
  6. Relatório final consolidado

Uso:
  python main.py                    → Gera mocks e audita
  python main.py doc.docx nb.ipynb  → Audita arquivos reais
"""

from __future__ import annotations

import os
import sys
import time
from datetime import datetime
from typing import Optional

# Adiciona diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gerador_mocks import gerar_tudo
from leitor_notebook import LeitorNotebook
from leitor_docx import LeitorDocx
from matcher import Matcher, StatusMatch
from validador import Validador, StatusValidacao


# ═══════════════════════════════════════════════════════════════
#  Relatório Final Consolidado
# ═══════════════════════════════════════════════════════════════

def gerar_relatorio_final(
    resultados_validacao,
    resultados_match,
    politicas_doc,
    politicas_nb,
    caminho_docx: str,
    caminho_nb: str,
    tempo_total: float,
) -> str:
    """Gera relatório consolidado da auditoria."""

    # Contagens
    cont_val = {s: 0 for s in StatusValidacao}
    for r in resultados_validacao:
        cont_val[r.status] += 1

    cont_match = {s: 0 for s in StatusMatch}
    for r in resultados_match:
        cont_match[r.status] += 1

    total_divs = sum(len(r.divergencias) for r in resultados_validacao)

    linhas = [
        "",
        "╔" + "═" * 57 + "╗",
        "║   MOTOR DE AUDITORIA DE POLÍTICAS DE CRÉDITO            ║",
        "║   Relatório Final Consolidado                           ║",
        "╚" + "═" * 57 + "╝",
        "",
        f"  📅 Data:              {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        f"  ⏱️  Tempo execução:    {tempo_total:.2f}s",
        f"  📄 DOCX:              {os.path.basename(caminho_docx)}",
        f"  📓 Notebook:          {os.path.basename(caminho_nb)}",
        "",
        "┌─────────────────────────────────────────────────────────┐",
        "│  RESUMO QUANTITATIVO                                    │",
        "├─────────────────────────────────────────────────────────┤",
        f"│  Políticas especificadas (DOC):    {len(politicas_doc):>3}                  │",
        f"│  Políticas inferidas (Notebook):   {len(politicas_nb):>3}                  │",
        f"│  Total de divergências:            {total_divs:>3}                  │",
        "├─────────────────────────────────────────────────────────┤",
        "│  MATCHING                                               │",
        "├─────────────────────────────────────────────────────────┤",
        f"│  ✅ Match forte:                   {cont_match[StatusMatch.MATCH_FORTE]:>3}                  │",
        f"│  ⚠️  Match fraco:                   {cont_match[StatusMatch.MATCH_FRACO]:>3}                  │",
        f"│  🔶 Ambíguo:                       {cont_match[StatusMatch.AMBIGUO]:>3}                  │",
        f"│  ❌ Não encontrado:                {cont_match[StatusMatch.NAO_ENCONTRADO]:>3}                  │",
        "├─────────────────────────────────────────────────────────┤",
        "│  VALIDAÇÃO                                              │",
        "├─────────────────────────────────────────────────────────┤",
        f"│  ✅ Corretas:                      {cont_val[StatusValidacao.CORRETA]:>3}                  │",
        f"│  ⚠️  Divergentes:                   {cont_val[StatusValidacao.DIVERGENTE]:>3}                  │",
        f"│  🔶 Parciais:                      {cont_val[StatusValidacao.PARCIAL]:>3}                  │",
        f"│  ❌ Não implementadas:             {cont_val[StatusValidacao.NAO_IMPLEMENTADA]:>3}                  │",
        f"│  ❓ Ambíguas:                      {cont_val[StatusValidacao.AMBIGUA]:>3}                  │",
        "└─────────────────────────────────────────────────────────┘",
        "",
        "┌─────────────────────────────────────────────────────────┐",
        "│  DETALHAMENTO POR POLÍTICA                              │",
        "└─────────────────────────────────────────────────────────┘",
        "",
    ]

    for r in resultados_validacao:
        linhas.append(r.resumo())
        linhas.append("")

    # Resumo de decisão
    linhas.append("┌─────────────────────────────────────────────────────────┐")
    linhas.append("│  CONCLUSÃO                                              │")
    linhas.append("└─────────────────────────────────────────────────────────┘")
    linhas.append("")

    taxa_ok = cont_val[StatusValidacao.CORRETA] / len(resultados_validacao) * 100 if resultados_validacao else 0
    taxa_prob = (cont_val[StatusValidacao.DIVERGENTE] + cont_val[StatusValidacao.NAO_IMPLEMENTADA]) / len(resultados_validacao) * 100 if resultados_validacao else 0

    linhas.append(f"  Taxa de conformidade:    {taxa_ok:.0f}%")
    linhas.append(f"  Taxa de problemas:       {taxa_prob:.0f}%")
    linhas.append("")

    if taxa_ok == 100:
        linhas.append("  🎉 Todas as políticas estão implementadas corretamente!")
    elif taxa_ok >= 70:
        linhas.append("  ⚠️  A maioria das políticas está correta, mas existem divergências a corrigir.")
    elif taxa_ok >= 40:
        linhas.append("  🔶 Atenção: várias políticas têm problemas de implementação.")
    else:
        linhas.append("  🚨 Crítico: a maioria das políticas tem divergências ou não está implementada.")

    linhas.append("")
    linhas.append("═" * 59)

    return "\n".join(linhas)


# ═══════════════════════════════════════════════════════════════
#  Pipeline Principal
# ═══════════════════════════════════════════════════════════════

def executar_auditoria(
    caminho_docx: Optional[str] = None,
    caminho_nb: Optional[str] = None,
    verbose: bool = True,
) -> dict:
    """
    Executa o pipeline completo de auditoria.

    Args:
        caminho_docx: Caminho do DOCX (se None, gera mock)
        caminho_nb:   Caminho do Notebook (se None, gera mock)
        verbose:      Se True, imprime relatórios intermediários

    Returns:
        dict com todos os resultados
    """
    inicio = time.time()

    # ─── ETAPA 1: Geração de mocks (se necessário) ───
    if caminho_docx is None or caminho_nb is None:
        print("\n📦 ETAPA 1 — Gerando arquivos mock...\n")
        diretorio = os.path.dirname(os.path.abspath(__file__))
        caminho_docx, caminho_nb = gerar_tudo(diretorio)
    else:
        print(f"\n📦 ETAPA 1 — Usando arquivos fornecidos:")
        print(f"  DOCX:     {caminho_docx}")
        print(f"  Notebook: {caminho_nb}")

    # ─── ETAPA 2: Inferência do Notebook ───
    print("\n🔍 ETAPA 2 — Inferindo políticas do Notebook...\n")
    leitor_nb = LeitorNotebook(caminho_nb)
    politicas_nb = leitor_nb.executar()

    if verbose:
        print(leitor_nb.relatorio())

    # ─── ETAPA 3: Extração do DOCX ───
    print("\n📄 ETAPA 3 — Extraindo políticas do DOCX...\n")
    leitor_doc = LeitorDocx(caminho_docx)
    politicas_doc = leitor_doc.executar()

    if verbose:
        print(leitor_doc.relatorio())

    # ─── ETAPA 4: Matching ───
    print("\n🔗 ETAPA 4 — Matching DOC ↔ Notebook...\n")
    matcher = Matcher(politicas_doc, politicas_nb)
    resultados_match = matcher.executar()

    if verbose:
        print(matcher.relatorio())

    # ─── ETAPA 5: Validação ───
    print("\n🔎 ETAPA 5 — Validação estática...\n")
    validador = Validador(resultados_match)
    resultados_validacao = validador.executar()

    if verbose:
        print(validador.relatorio())

    # ─── ETAPA 6: Relatório Final ───
    tempo_total = time.time() - inicio

    relatorio = gerar_relatorio_final(
        resultados_validacao=resultados_validacao,
        resultados_match=resultados_match,
        politicas_doc=politicas_doc,
        politicas_nb=politicas_nb,
        caminho_docx=caminho_docx,
        caminho_nb=caminho_nb,
        tempo_total=tempo_total,
    )

    print("\n" + relatorio)

    return {
        "politicas_doc": politicas_doc,
        "politicas_nb": politicas_nb,
        "resultados_match": resultados_match,
        "resultados_validacao": resultados_validacao,
        "relatorio": relatorio,
        "tempo": tempo_total,
    }


# ═══════════════════════════════════════════════════════════════
#  Execução
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) == 3:
        # Modo: arquivos reais
        docx_path = sys.argv[1]
        nb_path = sys.argv[2]

        if not os.path.exists(docx_path):
            print(f"❌ Arquivo não encontrado: {docx_path}")
            sys.exit(1)
        if not os.path.exists(nb_path):
            print(f"❌ Arquivo não encontrado: {nb_path}")
            sys.exit(1)

        executar_auditoria(docx_path, nb_path)

    elif len(sys.argv) == 1:
        # Modo: mocks automáticos
        executar_auditoria()

    else:
        print("Uso:")
        print("  python main.py                      → Gera mocks e audita")
        print("  python main.py <doc.docx> <nb.ipynb> → Audita arquivos reais")
        sys.exit(1)
