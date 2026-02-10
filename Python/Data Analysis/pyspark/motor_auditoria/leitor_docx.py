"""
COMPONENTE C — Leitor de Pseudocódigo (DOCX)
=============================================
Lê um documento Word e extrai sinais semânticos de cada política descrita
em linguagem natural/humana.

Extrai:
  - campos mencionados
  - operadores semânticos (maior, menor, igual, pertence, etc.)
  - valores numéricos e strings
  - conectivos (E, OU)
  - estrutura condicional (SE / SENÃO)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Set, Optional, Tuple

import docx


# ═══════════════════════════════════════════════════════════════
#  Representação de uma Política Especificada
# ═══════════════════════════════════════════════════════════════

@dataclass
class PoliticaEspecificada:
    """Representação de uma política extraída do documento."""
    indice: int
    texto_original: str
    campos: Set[str] = field(default_factory=set)
    operadores: Set[str] = field(default_factory=set)
    valores: Set[str] = field(default_factory=set)
    strings_literais: Set[str] = field(default_factory=set)
    listas: List[set] = field(default_factory=list)
    conectivos: Set[str] = field(default_factory=set)
    tem_condicional: bool = False
    tem_senao: bool = False

    def resumo(self) -> str:
        linhas = [
            f"Política Especificada #{self.indice + 1}",
            f"  Texto:       \"{self.texto_original[:80]}{'...' if len(self.texto_original) > 80 else ''}\"",
            f"  Campos:      {sorted(self.campos) if self.campos else '—'}",
            f"  Operadores:  {sorted(self.operadores) if self.operadores else '—'}",
            f"  Valores:     {sorted(self.valores) if self.valores else '—'}",
            f"  Strings:     {sorted(self.strings_literais) if self.strings_literais else '—'}",
            f"  Conectivos:  {sorted(self.conectivos) if self.conectivos else '—'}",
            f"  Condicional: {'SE/SENÃO' if self.tem_condicional and self.tem_senao else 'SE' if self.tem_condicional else '—'}",
        ]
        return "\n".join(linhas)


# ═══════════════════════════════════════════════════════════════
#  Vocabulário de mapeamento semântico
# ═══════════════════════════════════════════════════════════════

# Campos de negócio conhecidos (podem ser expandidos)
CAMPOS_CONHECIDOS = {
    "score", "renda", "idade", "estado", "codigo", "tipo_contrato",
    "contratos", "prazo", "valor", "taxa", "fator", "categoria",
    "status", "produto", "regiao", "cidade", "cpf", "nome",
    "limite", "parcela", "divida", "saldo", "salario",
    "codigo_produto", "tipo", "contrato", "sobretaxa",
}

# Sinônimos para campos
SINONIMOS_CAMPOS = {
    "pontuação": "score",
    "pontuacao": "score",
    "nota": "score",
    "salário": "renda",
    "salario": "renda",
    "rendimento": "renda",
    "uf": "estado",
    "região": "estado",
    "regiao": "estado",
    "anos": "idade",
    "código": "codigo",
    "codigo": "codigo",
    "código do produto": "codigo",
    "codigo do produto": "codigo",
    "tipo de contrato": "tipo_contrato",
    "contratos ativos": "contratos",
    "fator de risco": "fator_risco",
    "prazo máximo": "prazo_max",
    "prazo maximo": "prazo_max",
    "score final": "score_final",
}

# Mapeamento de operadores textuais para símbolos
OPERADORES_TEXTUAIS = [
    # (padrão regex, operador normalizado)
    (r'\bmaior\s+(?:que|do que|de)\b', '>'),
    (r'\bmaior\b', '>'),
    (r'\bacima\s+de\b', '>'),
    (r'\bsuperior\s+a\b', '>'),
    (r'\bexceder?\b', '>'),
    (r'\bmenor\s+(?:que|do que|de)\b', '<'),
    (r'\bmenor\b', '<'),
    (r'\babaixo\s+de\b', '<'),
    (r'\binferior\s+a\b', '<'),
    (r'\bigual\s+a\b', '=='),
    (r'\bfor\s+igual\b', '=='),
    (r'\bé\b', '=='),
    (r'\bestiver\s+entre\b', 'isin'),
    (r'\bentre\b', 'isin'),
    (r'\bpertenc(?:e|er)\b', 'isin'),
    (r'\bcontém?\b', 'isin'),
    (r'\bpossu[ie]\b', '>'),  # "possui mais de" → >
    (r'\bmais\s+de\b', '>'),
    (r'\bmenos\s+de\b', '<'),
    (r'\bno\s+m[ií]nimo\b', '>='),
    (r'\bno\s+m[aá]ximo\b', '<='),
    (r'\bpelo\s+menos\b', '>='),
    (r'\bat[eé]\b', '<='),
]

# Conectivos
CONECTIVOS_TEXTUAIS = [
    (r'\b[eE]\b(?!\s+(?:o|a|os|as|um|uma)\b)', 'E'),  # "E" mas não "E o/a"
    (r'\bOU\b', 'OU'),
    (r'\bou\b', 'OU'),
]

# Condicionais
CONDICIONAIS = [
    (r'\bSE\b', 'SE'),
    (r'\bse\b', 'SE'),
    (r'\bquando\b', 'SE'),
    (r'\bcaso\b', 'SE'),
]

SENAO_PATTERNS = [
    r'\bcaso\s+contr[aá]rio\b',
    r'\bsen[aã]o\b',
    r'\bpara\s+outros\b',
    r'\bpara\s+as?\s+demais\b',
    r'\boutros\s+estados\b',
    r'\boutros\s+tipos\b',
]


# ═══════════════════════════════════════════════════════════════
#  Extratores semânticos
# ═══════════════════════════════════════════════════════════════

def _normalizar_texto(texto: str) -> str:
    """Normaliza texto para facilitar extração."""
    t = texto.lower().strip()
    # Remove pontuação final
    t = re.sub(r'[.;!]+$', '', t)
    return t


def _extrair_campos_doc(texto: str) -> Set[str]:
    """Extrai campos mencionados no pseudocódigo."""
    campos = set()
    texto_lower = texto.lower()

    # Busca direta por campos conhecidos
    for campo in CAMPOS_CONHECIDOS:
        if re.search(rf'\b{campo}\b', texto_lower):
            campos.add(campo)

    # Busca por sinônimos
    for sinonimo, campo_real in SINONIMOS_CAMPOS.items():
        if sinonimo in texto_lower:
            campos.add(campo_real)

    return campos


def _extrair_operadores_doc(texto: str) -> Set[str]:
    """Extrai operadores semânticos do pseudocódigo."""
    ops = set()
    texto_lower = texto.lower()

    for padrao, op in OPERADORES_TEXTUAIS:
        if re.search(padrao, texto_lower):
            ops.add(op)

    return ops


def _extrair_valores_numericos_doc(texto: str) -> Set[str]:
    """Extrai valores numéricos do pseudocódigo."""
    valores = set()

    # Números com possível % ou "reais"
    for m in re.finditer(r'(\d+\.?\d*)\s*(?:%|reais|pontos|meses|anos)?', texto):
        val = m.group(1)
        # Converte percentuais: "2%" → "0.02"
        seguido_de = texto[m.end():m.end() + 1]
        if '%' in texto[m.start():m.end() + 2]:
            try:
                val_float = float(val) / 100
                valores.add(str(val_float))
            except ValueError:
                pass
        valores.add(val)

    return valores


def _extrair_strings_literais_doc(texto: str) -> Set[str]:
    """Extrai valores string mencionados como categorias ou estados."""
    strings = set()

    # Palavras em MAIÚSCULAS (possíveis categorias/status)
    for m in re.finditer(r'\b([A-Z][A-Z_]+)\b', texto):
        palavra = m.group(1)
        # Ignora conectivos e palavras comuns
        if palavra not in {'SE', 'OU', 'SENÃO', 'SENAO', 'CASO', 'PARA', 'IN', 'COM', 'SEM', 'POR', 'NÃO', 'NAO', 'DO', 'DA', 'DE', 'QUE', 'UM', 'UMA', 'OS', 'AS', 'NO', 'NA', 'AO', 'ÀS', 'DOS', 'DAS'}:
            strings.add(palavra)

    # Siglas de estados (2 letras maiúsculas precedidas de contexto)
    for m in re.finditer(r'\b([A-Z]{2})\b', texto):
        sigla = m.group(1)
        if sigla in {'SP', 'RJ', 'MG', 'BA', 'RS', 'PR', 'SC', 'PE', 'CE', 'DF', 'GO', 'PA', 'MA', 'AM', 'ES', 'PB', 'RN', 'PI', 'AL', 'MT', 'MS', 'TO', 'RO', 'AC', 'AP', 'RR'}:
            strings.add(sigla)

    # Nomes de cidades/estados por extenso
    estados_extenso = {
        "são paulo": "SP", "rio de janeiro": "RJ", "minas gerais": "MG",
        "bahia": "BA", "paraná": "PR", "rio grande do sul": "RS",
    }
    for nome, sigla in estados_extenso.items():
        if nome in texto.lower():
            strings.add(sigla)

    return strings


def _extrair_listas_doc(texto: str) -> List[set]:
    """Extrai listas de valores (ex: '10, 20 ou 30')."""
    listas = []

    # Padrão: números separados por vírgula e/ou "ou"
    m = re.search(r'(\d+(?:\s*[,]\s*\d+)+(?:\s*(?:ou|e)\s*\d+)?)', texto)
    if m:
        nums = set(re.findall(r'\d+', m.group(0)))
        if len(nums) >= 2:
            listas.append(nums)

    return listas


def _extrair_conectivos_doc(texto: str) -> Set[str]:
    """Detecta conectivos E / OU no texto."""
    conectivos = set()
    texto_norm = texto

    # Busca "E" como conectivo lógico (entre condições, não artigo)
    # Ex: "score > 700 E renda > 2000"
    if re.search(r'\b[eE]\b.*\b(?:maior|menor|igual|acima|abaixo|score|renda|idade|estado)\b', texto_norm):
        # Verifica se tem duas condições conectadas por E
        partes = re.split(r'\b[eE]\b', texto_norm)
        if len(partes) >= 2:
            tem_condicao = [bool(re.search(r'(?:maior|menor|igual|acima|abaixo|>|<|==|\d)', p)) for p in partes]
            if sum(tem_condicao) >= 2:
                conectivos.add("E")

    # OU é mais direto
    if re.search(r'\bOU\b|\bou\b', texto):
        # Verifica contexto
        partes_ou = re.split(r'\bOU\b|\bou\b', texto)
        if len(partes_ou) >= 2:
            tem_condicao = [bool(re.search(r'(?:maior|menor|igual|acima|abaixo|>|<|==|\d)', p)) for p in partes_ou]
            if sum(tem_condicao) >= 2:
                conectivos.add("OU")

    return conectivos


def _detectar_condicional(texto: str) -> Tuple[bool, bool]:
    """Detecta se o texto tem estrutura SE/SENÃO."""
    tem_se = False
    tem_senao = False

    for padrao, _ in CONDICIONAIS:
        if re.search(padrao, texto):
            tem_se = True
            break

    for padrao in SENAO_PATTERNS:
        if re.search(padrao, texto, re.IGNORECASE):
            tem_senao = True
            break

    return tem_se, tem_senao


# ═══════════════════════════════════════════════════════════════
#  Motor de Leitura de DOCX
# ═══════════════════════════════════════════════════════════════

class LeitorDocx:
    """Lê um documento DOCX e extrai políticas especificadas."""

    def __init__(self, caminho_docx: str):
        self.caminho = caminho_docx
        self.paragrafos_raw: List[str] = []
        self.politicas: List[PoliticaEspecificada] = []

    def carregar(self):
        """Carrega o documento e extrai parágrafos relevantes."""
        doc = docx.Document(self.caminho)
        self.paragrafos_raw = []

        for para in doc.paragraphs:
            texto = para.text.strip()
            if not texto:
                continue
            # Identifica parágrafos que parecem políticas
            # Heurística: contém "Política" ou tem padrões condicionais
            if self._parece_politica(texto):
                # Remove prefixo "Política N:" se existir
                texto_limpo = re.sub(r'^Pol[ií]tica\s*\d+\s*:\s*', '', texto).strip()
                self.paragrafos_raw.append(texto_limpo)

    def _parece_politica(self, texto: str) -> bool:
        """Heurística para identificar se parágrafo descreve política."""
        indicadores = [
            r'\bPol[ií]tica\s*\d+\b',
            r'\bSE\b',
            r'\bse\b.*\b(?:maior|menor|igual|acima|abaixo)\b',
            r'\bcliente[s]?\b.*\b(?:com|que|do|da)\b',
            r'\b(?:aplicar|classificar|negar|bloquear|encaminhar)\b',
        ]
        return any(re.search(p, texto, re.IGNORECASE) for p in indicadores)

    def extrair_politicas(self) -> List[PoliticaEspecificada]:
        """Extrai sinais semânticos de cada política."""
        self.politicas = []

        for i, texto in enumerate(self.paragrafos_raw):
            campos = _extrair_campos_doc(texto)
            operadores = _extrair_operadores_doc(texto)
            valores = _extrair_valores_numericos_doc(texto)
            strings = _extrair_strings_literais_doc(texto)
            listas = _extrair_listas_doc(texto)
            conectivos = _extrair_conectivos_doc(texto)
            tem_se, tem_senao = _detectar_condicional(texto)

            pol = PoliticaEspecificada(
                indice=i,
                texto_original=texto,
                campos=campos,
                operadores=operadores,
                valores=valores,
                strings_literais=strings,
                listas=listas,
                conectivos=conectivos,
                tem_condicional=tem_se,
                tem_senao=tem_senao,
            )
            self.politicas.append(pol)

        return self.politicas

    def executar(self) -> List[PoliticaEspecificada]:
        """Pipeline completo: carregar → extrair."""
        self.carregar()
        return self.extrair_politicas()

    def relatorio(self) -> str:
        """Gera relatório textual das políticas extraídas."""
        linhas = [
            "=" * 55,
            "  COMPONENTE C — Políticas Extraídas do DOCX",
            "=" * 55,
            f"  Arquivo: {self.caminho}",
            f"  Políticas encontradas: {len(self.politicas)}",
            "",
        ]

        for pol in self.politicas:
            linhas.append(f"─── Política #{pol.indice + 1} ───")
            linhas.append(pol.resumo())
            linhas.append("")

        return "\n".join(linhas)
