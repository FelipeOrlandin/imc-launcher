import subprocess

def launch_imc_via_cli(nome, idade, altura, peso, ano_atual):
    comando = [
        "python", "imc_core.py",  
    ]
    pass


from imc_core import calcular_imc

def launch_imc(nome, idade, altura, peso, ano_atual):
    
    return calcular_imc(nome, idade, altura, peso, ano_atual)


if __name__ == "__main__":
    resultado = launch_imc("Maria", 30, 1.68, 68, 2026)
    print(resultado)