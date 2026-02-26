"""
ORQUESTRADOR — Motor de Auditoria de Políticas de Crédito
==========================================================
Pipeline completo:
  1. Carrega fontes (Notebook + DOCX)       — Múltiplas fontes suportadas
  2. Infere políticas do Notebook           — Componente B
  3. Extrai políticas do DOCX               — Componente C
  4. Matching DOC ↔ Notebook                — Componente D
  5. Validação estática de implementação    — Componente E
  6. Relatório final consolidado

Uso:
  python main.py doc.docx nb.ipynb            → Audita arquivos locais
  python main.py doc.docx --databricks-url URL --token TOKEN --notebook-path /path
  python main.py doc.docx --fico-url URL --fico-token TOKEN
  python main.py                              → Gera mocks e audita (modo teste)
"""

from __future__ import annotations

import os
import sys
import time
import argparse
import tempfile
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
#  Baixar Notebooks de Fontes Remotas
# ═══════════════════════════════════════════════════════════════

def baixar_notebook_databricks(
    workspace_url: str,
    token: str,
    notebook_path: str,
    destino: Optional[str] = None,
) -> str:
    """
    Baixa um notebook do Databricks Workspace via REST API.

    Args:
        workspace_url: URL do workspace (ex: https://adb-xxx.azuredatabricks.net)
        token: Token de acesso pessoal (PAT)
        notebook_path: Caminho do notebook no workspace (ex: /Users/user@co.com/nb)
        destino: Caminho local para salvar (opcional)

    Returns:
        Caminho do arquivo .ipynb local
    """
    import requests
    import base64

    url = f"{workspace_url.rstrip('/')}/api/2.0/workspace/export"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"path": notebook_path, "format": "JUPYTER"}

    print(f"  📥 Baixando notebook do Databricks: {notebook_path}")
    resp = requests.get(url, headers=headers, params=params, timeout=60)
    resp.raise_for_status()

    conteudo_b64 = resp.json().get("content", "")
    conteudo = base64.b64decode(conteudo_b64)

    if destino is None:
        nome = notebook_path.split("/")[-1]
        if not nome.endswith(".ipynb"):
            nome += ".ipynb"
        destino = os.path.join(tempfile.gettempdir(), nome)

    with open(destino, "wb") as f:
        f.write(conteudo)

    print(f"  ✅ Notebook salvo em: {destino}")
    return destino


def baixar_notebook_url(url: str, destino: Optional[str] = None) -> str:
    """
    Baixa um notebook de qualquer URL (FICO, repositório, etc.).

    Args:
        url: URL direta do arquivo .ipynb
        destino: Caminho local para salvar (opcional)

    Returns:
        Caminho do arquivo .ipynb local
    """
    import requests

    print(f"  📥 Baixando notebook de: {url}")
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()

    if destino is None:
        nome = url.split("/")[-1].split("?")[0]
        if not nome.endswith(".ipynb"):
            nome += ".ipynb"
        destino = os.path.join(tempfile.gettempdir(), nome)

    with open(destino, "wb") as f:
        f.write(resp.content)

    print(f"  ✅ Notebook salvo em: {destino}")
    return destino


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
    # ─── Fontes remotas (opcional) ───
    databricks_url: Optional[str] = None,
    databricks_token: Optional[str] = None,
    databricks_notebook_path: Optional[str] = None,
    fico_url: Optional[str] = None,
    fico_token: Optional[str] = None,
    notebook_url: Optional[str] = None,
) -> dict:
    """
    Executa o pipeline completo de auditoria.

    Args:
        caminho_docx:   Caminho do DOCX (se None, gera mock)
        caminho_nb:     Caminho do Notebook local (se None, tenta fontes remotas ou gera mock)
        verbose:        Se True, imprime relatórios intermediários
        databricks_url: URL do workspace Databricks
        databricks_token: Token de acesso Databricks
        databricks_notebook_path: Caminho do notebook no Databricks
        fico_url:       URL direta do notebook no FICO
        fico_token:     Token de acesso FICO (se necessário)
        notebook_url:   URL genérica para baixar notebook

    Returns:
        dict com todos os resultados
    """
    inicio = time.time()

    # ─── ETAPA 1: Obtenção de arquivos ───
    usar_mocks = False

    # Tenta resolver o notebook de fontes remotas se não fornecido localmente
    if caminho_nb is None:
        if databricks_url and databricks_token and databricks_notebook_path:
            print("\n📦 ETAPA 1 — Baixando notebook do Databricks...\n")
            caminho_nb = baixar_notebook_databricks(
                databricks_url, databricks_token, databricks_notebook_path
            )
        elif fico_url:
            print("\n📦 ETAPA 1 — Baixando notebook do FICO...\n")
            headers_extra = {"Authorization": f"Bearer {fico_token}"} if fico_token else {}
            caminho_nb = baixar_notebook_url(fico_url)
        elif notebook_url:
            print("\n📦 ETAPA 1 — Baixando notebook de URL...\n")
            caminho_nb = baixar_notebook_url(notebook_url)

    if caminho_docx is None or caminho_nb is None:
        print("\n📦 ETAPA 1 — Gerando arquivos mock (modo teste)...\n")
        diretorio = os.path.dirname(os.path.abspath(__file__))
        caminho_docx_mock, caminho_nb_mock = gerar_tudo(diretorio)
        caminho_docx = caminho_docx or caminho_docx_mock
        caminho_nb = caminho_nb or caminho_nb_mock
        usar_mocks = True
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
#  Execução via CLI
# ═══════════════════════════════════════════════════════════════

def _parse_args():
    """Parser de argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Motor de Auditoria de Políticas de Crédito",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Modo teste (gera mocks)
  python main.py

  # Arquivos locais
  python main.py doc.docx notebook.ipynb

  # Notebook do Databricks
  python main.py doc.docx --databricks-url https://adb-xxx.azuredatabricks.net \\
      --databricks-token dapi... --databricks-path /Users/user/notebook

  # Notebook de URL genérica (FICO, repositório, etc.)
  python main.py doc.docx --notebook-url https://server/notebook.ipynb

  # Notebook do FICO com autenticação
  python main.py doc.docx --fico-url https://fico.corp/api/notebooks/regras.ipynb \\
      --fico-token "Bearer xxx..."
        """,
    )

    parser.add_argument("docx", nargs="?", default=None,
                        help="Caminho do DOCX com especificações")
    parser.add_argument("notebook", nargs="?", default=None,
                        help="Caminho local do notebook .ipynb")

    # Databricks
    parser.add_argument("--databricks-url", default=None,
                        help="URL do workspace Databricks")
    parser.add_argument("--databricks-token", default=None,
                        help="Token de acesso Databricks (PAT)")
    parser.add_argument("--databricks-path", default=None,
                        help="Caminho do notebook no Databricks")

    # FICO
    parser.add_argument("--fico-url", default=None,
                        help="URL direta do notebook no FICO")
    parser.add_argument("--fico-token", default=None,
                        help="Token de autenticação FICO")

    # URL genérica
    parser.add_argument("--notebook-url", default=None,
                        help="URL genérica para baixar o notebook")

    # Opções
    parser.add_argument("--quiet", action="store_true",
                        help="Reduz output (desativa relatórios intermediários)")

    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    executar_auditoria(
        caminho_docx=args.docx,
        caminho_nb=args.notebook,
        verbose=not args.quiet,
        databricks_url=args.databricks_url,
        databricks_token=args.databricks_token,
        databricks_notebook_path=args.databricks_path,
        fico_url=args.fico_url,
        fico_token=args.fico_token,
        notebook_url=args.notebook_url,
    )
