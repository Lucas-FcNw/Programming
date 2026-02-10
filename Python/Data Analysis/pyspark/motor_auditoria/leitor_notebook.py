"""
COMPONENTE B — Leitor de Notebook (Inferência de Políticas)
============================================================
Lê um notebook Jupyter e infere quais células contêm políticas de crédito,
SEM depender de flags, nomes padronizados ou qualquer marcação explícita.

Cada política inferida contém:
  - índice da célula de origem
  - campos envolvidos (colunas referenciadas)
  - operadores detectados
  - valores literais encontrados
  - conectivos lógicos (E / OU)
  - código-fonte bruto
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from typing import List, Set, Optional

import nbformat


# ═══════════════════════════════════════════════════════════════
#  Representação de uma Política Inferida
# ═══════════════════════════════════════════════════════════════

@dataclass
class PoliticaInferida:
    """Representação interna de uma política descoberta no notebook."""
    indice_celula: int
    campos: Set[str] = field(default_factory=set)
    operadores: Set[str] = field(default_factory=set)
    valores: Set[str] = field(default_factory=set)
    conectivos: Set[str] = field(default_factory=set)
    strings_literais: Set[str] = field(default_factory=set)
    listas: List[set] = field(default_factory=list)
    codigo_fonte: str = ""
    confianca: float = 0.0  # 0.0 a 1.0

    def resumo(self) -> str:
        """Resumo legível da política inferida."""
        linhas = [
            f"Política Inferida (célula {self.indice_celula})",
            f"  Campos:     {sorted(self.campos) if self.campos else '—'}",
            f"  Operadores: {sorted(self.operadores) if self.operadores else '—'}",
            f"  Valores:    {sorted(self.valores) if self.valores else '—'}",
            f"  Strings:    {sorted(self.strings_literais) if self.strings_literais else '—'}",
            f"  Conectivos: {sorted(self.conectivos) if self.conectivos else '—'}",
            f"  Confiança:  {self.confianca:.0%}",
        ]
        return "\n".join(linhas)


# ═══════════════════════════════════════════════════════════════
#  Heurísticas de detecção
# ═══════════════════════════════════════════════════════════════

# Padrões que indicam lógica condicional / política
PADROES_POLITICA = [
    r'\bF\.when\b',
    r'\bF\.col\b',
    r'\.when\s*\(',
    r'\.otherwise\s*\(',
    r'\.filter\s*\(',
    r'\.where\s*\(',
    r'\.isin\s*\(',
    r'\.withColumn\s*\(',
    r'\.between\s*\(',
    r'\.isNull\s*\(',
    r'\.isNotNull\s*\(',
    r'\.like\s*\(',
    r'\.rlike\s*\(',
]

# Operadores relacionais em código
MAPA_OPERADORES = {
    '>': '>',
    '<': '<',
    '>=': '>=',
    '<=': '<=',
    '==': '==',
    '!=': '!=',
}


# ═══════════════════════════════════════════════════════════════
#  Extratores
# ═══════════════════════════════════════════════════════════════

def _extrair_campos(codigo: str) -> Set[str]:
    """Extrai nomes de colunas referenciadas via F.col('nome') ou col('nome'),
    incluindo colunas criadas via withColumn."""
    campos = set()
    # F.col("campo") ou col("campo")
    for m in re.finditer(r"""(?:F\.)?col\s*\(\s*['"]([\w]+)['"]\s*\)""", codigo):
        campos.add(m.group(1))
    # Colunas criadas via withColumn (campo resultante)
    for m in re.finditer(r"""withColumn\s*\(\s*['"]([\w]+)['"]\s*""", codigo):
        campos.add(m.group(1))
    return campos


def _extrair_operadores(codigo: str) -> Set[str]:
    """Extrai operadores relacionais e funções condicionais."""
    ops = set()

    # Operadores simbólicos (cuidado com => e <=)
    for m in re.finditer(r'([><!]=?|==)', codigo):
        op = m.group(1)
        if op in MAPA_OPERADORES:
            ops.add(op)

    # Funções PySpark condicionais
    funcoes = {
        'when': 'when',
        'otherwise': 'otherwise',
        'filter': 'filter',
        'where': 'where',
        'isin': 'isin',
        'between': 'between',
        'isNull': 'isNull',
        'isNotNull': 'isNotNull',
        'like': 'like',
    }
    for func, nome in funcoes.items():
        if re.search(rf'\.{func}\s*\(', codigo):
            ops.add(nome)

    return ops


def _extrair_valores_numericos(codigo: str) -> Set[str]:
    """Extrai valores numéricos usados em comparações."""
    valores = set()

    # Números em comparações: col(...) > 800, == 18, etc.
    for m in re.finditer(
        r"""(?:F\.)?col\s*\([^)]+\)\s*[><=!]+\s*(-?\d+\.?\d*)""", codigo
    ):
        valores.add(m.group(1))

    # Números após operadores dentro de when()
    for m in re.finditer(
        r"""[><=!]+\s*(-?\d+\.?\d*)""", codigo
    ):
        valores.add(m.group(1))

    # Números em withColumn como valor de resultado: literais numéricos soltos
    # Ex: F.col('score') + 50, ou .otherwise(0.1)
    for m in re.finditer(
        r"""(?:otherwise|\.otherwise)\s*\(\s*(-?\d+\.?\d*)""", codigo
    ):
        valores.add(m.group(1))

    # Operações aritméticas com colunas: col('x') + 50
    for m in re.finditer(
        r"""(?:F\.)?col\s*\([^)]+\)\s*[+\-*/]\s*(-?\d+\.?\d*)""", codigo
    ):
        valores.add(m.group(1))

    # Valores dentro de isin()
    for m in re.finditer(r"""\.isin\s*\(([^)]+)\)""", codigo):
        for num in re.findall(r'-?\d+\.?\d*', m.group(1)):
            valores.add(num)

    return valores


def _extrair_strings_literais(codigo: str) -> Set[str]:
    """Extrai strings literais usadas como valores (não nomes de coluna)."""
    strings = set()

    # Encontra todas as strings entre aspas
    todas = re.findall(r"""['"]([^'"]+)['"]""", codigo)

    # Encontra nomes de colunas para excluí-los
    colunas = set()
    for m in re.finditer(r"""(?:F\.)?col\s*\(\s*['"](\w+)['"]\s*\)""", codigo):
        colunas.add(m.group(1))

    # Nomes de colunas em withColumn
    for m in re.finditer(r"""withColumn\s*\(\s*['"](\w+)['"]\s*""", codigo):
        colunas.add(m.group(1))

    for s in todas:
        if s not in colunas and not s.startswith("pyspark"):
            strings.add(s)

    return strings


def _extrair_listas(codigo: str) -> List[set]:
    """Extrai listas usadas em isin() ou arrays."""
    listas = []

    for m in re.finditer(r"""\.isin\s*\(([^)]+)\)""", codigo):
        conteudo = m.group(1)
        # Extrai números e strings
        items = set()
        for num in re.findall(r'-?\d+\.?\d*', conteudo):
            items.add(num)
        for s in re.findall(r"""['"]([^'"]+)['"]""", conteudo):
            items.add(s)
        if items:
            listas.append(items)

    return listas


def _extrair_conectivos(codigo: str) -> Set[str]:
    """Detecta conectivos lógicos E (&) e OU (|)."""
    conectivos = set()
    if re.search(r'\)\s*&\s*\(', codigo) or re.search(r'\s&\s', codigo):
        conectivos.add("E")
    if re.search(r'\)\s*\|\s*\(', codigo) or re.search(r'\s\|\s', codigo):
        conectivos.add("OU")
    return conectivos


def _calcular_confianca(pol: PoliticaInferida) -> float:
    """Calcula grau de confiança de que a célula é uma política real."""
    score = 0.0

    # Tem campos referenciados → +0.2
    if pol.campos:
        score += 0.2

    # Tem operadores condicionais (when, filter, where) → +0.3
    ops_condicionais = {'when', 'filter', 'where', 'otherwise'}
    if pol.operadores & ops_condicionais:
        score += 0.3

    # Tem operadores relacionais (>, <, ==) → +0.2
    ops_relacionais = {'>', '<', '>=', '<=', '==', '!='}
    if pol.operadores & ops_relacionais:
        score += 0.2

    # Tem valores (numéricos ou string) → +0.15
    if pol.valores or pol.strings_literais:
        score += 0.15

    # Tem isin / listas → +0.1
    if pol.listas or 'isin' in pol.operadores:
        score += 0.1

    # Tem conectivos → +0.05
    if pol.conectivos:
        score += 0.05

    return min(score, 1.0)


# ═══════════════════════════════════════════════════════════════
#  Motor de Inferência do Notebook
# ═══════════════════════════════════════════════════════════════

class LeitorNotebook:
    """Lê um notebook e infere quais células contêm políticas."""

    def __init__(self, caminho_nb: str, limiar_confianca: float = 0.35):
        self.caminho = caminho_nb
        self.limiar = limiar_confianca
        self.celulas_codigo: List[dict] = []
        self.politicas: List[PoliticaInferida] = []

    def carregar(self):
        """Carrega o notebook e extrai células de código."""
        with open(self.caminho, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        self.celulas_codigo = []
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == "code":
                self.celulas_codigo.append({
                    "indice_global": i,
                    "codigo": cell.source.strip(),
                })

    def _celula_e_candidata(self, codigo: str) -> bool:
        """Verifica se célula tem padrões indicativos de política."""
        for padrao in PADROES_POLITICA:
            if re.search(padrao, codigo):
                return True
        return False

    def inferir_politicas(self) -> List[PoliticaInferida]:
        """Executa inferência em todas as células do notebook."""
        self.politicas = []

        for cel in self.celulas_codigo:
            codigo = cel["codigo"]
            idx = cel["indice_global"]

            # Filtro rápido: célula precisa ter ao menos um padrão
            if not self._celula_e_candidata(codigo):
                continue

            pol = PoliticaInferida(
                indice_celula=idx,
                campos=_extrair_campos(codigo),
                operadores=_extrair_operadores(codigo),
                valores=_extrair_valores_numericos(codigo),
                strings_literais=_extrair_strings_literais(codigo),
                listas=_extrair_listas(codigo),
                conectivos=_extrair_conectivos(codigo),
                codigo_fonte=codigo,
            )

            pol.confianca = _calcular_confianca(pol)

            # Só inclui se passou no limiar de confiança
            if pol.confianca >= self.limiar:
                self.politicas.append(pol)

        return self.politicas

    def executar(self) -> List[PoliticaInferida]:
        """Pipeline completo: carregar → inferir."""
        self.carregar()
        return self.inferir_politicas()

    def relatorio(self) -> str:
        """Gera relatório textual das políticas inferidas."""
        linhas = [
            "=" * 55,
            "  COMPONENTE B — Políticas Inferidas do Notebook",
            "=" * 55,
            f"  Arquivo: {self.caminho}",
            f"  Células de código: {len(self.celulas_codigo)}",
            f"  Políticas inferidas: {len(self.politicas)}",
            f"  Limiar de confiança: {self.limiar:.0%}",
            "",
        ]

        for i, pol in enumerate(self.politicas, 1):
            linhas.append(f"─── Política Inferida #{i} ───")
            linhas.append(pol.resumo())
            linhas.append("")

        return "\n".join(linhas)
