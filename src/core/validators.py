"""Validadores de entrada para o projeto IMC.

Centraliza toda logica de validacao em um modulo reutilizavel,
tanto para GUI quanto para CLI.
"""

ACEITOS = set(
    "aeiouAEIOU"
    "\u00e1\u00e9\u00ed\u00f3\u00fa"
    "\u00e2\u00ea\u00ee\u00f4\u00fb"
    "\u00e3\u00f5"
    "\u00e0\u00e8\u00ec\u00f2\u00f9"
    "\u00e4\u00eb\u00ef\u00f6\u00fc"
    "\u00e7\u00c7"
    "\u00c1\u00c9\u00cd\u00d3\u00da"
    "\u00c2\u00ca\u00ce\u00d4\u00db"
    "\u00c3\u00d5"
    "\u00c0\u00c8\u00cc\u00d2\u00d9"
    "\u00c4\u00cb\u00cf\u00d6\u00dc"
    "'-."
)

MAX_NOME = 50

ALTURA_MIN = 0.5
ALTURA_MAX = 2.5
PESO_MIN = 20
PESO_MAX = 300
IDADE_MIN = 1
IDADE_MAX = 150


def validar_nome(texto):
    """Valida se o texto contem apenas caracteres aceitos para nomes."""
    if len(texto) > MAX_NOME:
        return False
    return all(c.isalpha() or c.isspace() or c in ACEITOS for c in texto)


def validar_decimal(texto):
    """Valida se o texto e um numero decimal valido."""
    if texto == "":
        return True
    if texto in (".", ","):
        return False
    texto = texto.replace(",", ".")
    partes = texto.split(".")
    if len(partes) > 2:
        return False
    return all(p.isdigit() for p in partes)