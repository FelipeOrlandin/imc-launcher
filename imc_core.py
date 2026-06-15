def calcular_imc(nome, idade, altura, peso, ano_atual):
    nascimento = ano_atual - idade
    imc = peso / (altura ** 2)

    if imc <= 18.9:
        resultado = "abaixo do peso"
    elif 19 <= imc <= 24.9:
        resultado = "no peso ideal"
    else:
        resultado = "com sobrepeso"

    texto = (
        f"=======================================\n"
        f"{nome} tem {idade} anos e {altura:.2f}m de altura.\n"
        f"{nome} pesa {peso:.1f}Kg e seu IMC é {imc:.2f}.\n"
        f"{nome} nasceu em {nascimento}.\n\n"
        f"{nome} você está {resultado}.\n"
        f"======================================="
    )
    return texto

# Isso aqui permite testar o módulo diretamente
if __name__ == "__main__":
    print(calcular_imc("Teste", 25, 1.75, 70, 2026))