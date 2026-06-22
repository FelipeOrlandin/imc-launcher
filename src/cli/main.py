"""Interface de linha de comando para o calculo de IMC."""

import sys
from core.calculadora import calcular_imc
from core.validators import ALTURA_MIN, ALTURA_MAX, PESO_MIN, PESO_MAX, IDADE_MIN, IDADE_MAX


def main():
    """Entry point do CLI.

    Uso: python run.py <nome> <idade> <altura> <peso> <ano_atual>
    Exemplo: python run.py Joao 25 1.75 70 2026
    """
    if len(sys.argv) != 6:
        print(f"Uso: {sys.argv[0]} <nome> <idade> <altura> <peso> <ano_atual>")
        print(f"Exemplo: {sys.argv[0]} Joao 25 1.75 70 2026")
        sys.exit(1)

    nome = sys.argv[1]
    if not nome.strip():
        print("Erro: Nome nao pode ser vazio.")
        sys.exit(1)

    try:
        idade = int(sys.argv[2])
        if not (IDADE_MIN <= idade <= IDADE_MAX):
            raise ValueError
    except ValueError:
        print(f"Erro: Idade deve ser entre {IDADE_MIN} e {IDADE_MAX}.")
        sys.exit(1)

    try:
        altura = float(sys.argv[3].replace(",", "."))
        if not (ALTURA_MIN <= altura <= ALTURA_MAX):
            raise ValueError
    except ValueError:
        print(f"Erro: Altura deve ser entre {ALTURA_MIN}m e {ALTURA_MAX}m.")
        sys.exit(1)

    try:
        peso = float(sys.argv[4].replace(",", "."))
        if not (PESO_MIN <= peso <= PESO_MAX):
            raise ValueError
    except ValueError:
        print(f"Erro: Peso deve ser entre {PESO_MIN}kg e {PESO_MAX}kg.")
        sys.exit(1)

    try:
        ano_atual = int(sys.argv[5])
    except ValueError:
        print("Erro: Ano deve ser um numero inteiro.")
        sys.exit(1)

    try:
        resultado = calcular_imc(nome, idade, altura, peso, ano_atual)
        print(resultado.formatar())
    except ValueError as e:
        print(f"Erro: {e}")
        sys.exit(1)