import sys
from core.calculadora import calcular_imc


def main():
    """Interface de linha de comando com validacao de entrada.
    
    Uso: python -m src.cli Nome Idade Altura Peso AnoAtual
    Exemplo: python -m src.cli Joao 25 1.75 70 2026
    """
    if len(sys.argv) != 6:
        print("Uso: python -m src.cli <nome> <idade> <altura> <peso> <ano_atual>")
        print("Exemplo: python -m src.cli Joao 25 1.75 70 2026")
        sys.exit(1)

    nome = sys.argv[1]

    try:
        idade = int(sys.argv[2])
    except ValueError:
        print("Erro: Idade deve ser um numero inteiro.")
        sys.exit(1)

    try:
        altura = float(sys.argv[3].replace(",", "."))
    except ValueError:
        print("Erro: Altura deve ser um numero (ex: 1.75).")
        sys.exit(1)

    try:
        peso = float(sys.argv[4].replace(",", "."))
    except ValueError:
        print("Erro: Peso deve ser um numero (ex: 70.5).")
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