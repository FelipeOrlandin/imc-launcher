import sys
from imc_core import calcular_imc

if len(sys.argv) != 6:
    print("uso: python imc_cli.py <nome> <idade> <altura> <peso> <ano_atual>")
    sys.exit(1)

nome = sys.argv[1]
idade = int(sys.argv[2])
altura = float(sys.argv[3])
peso = float(sys.argv[4])
ano_atual = int(sys.argv[5])

print(calcular_imc(nome, idade, altura, peso, ano_atual))