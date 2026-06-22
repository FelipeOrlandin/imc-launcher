from core.modelos import ResultadoIMC
from core.validators import ALTURA_MIN, ALTURA_MAX, PESO_MIN, PESO_MAX, IDADE_MIN, IDADE_MAX


def calcular_imc(nome: str, idade: int, altura: float, peso: float, ano_atual: int) -> ResultadoIMC:
    """Calcula o IMC usando padrao OMS (4 categorias).

    Returns:
        ResultadoIMC com dados estruturados
    Raises:
        ValueError: se os dados estiverem fora das faixas validas
    """
    if not (ALTURA_MIN <= altura <= ALTURA_MAX):
        raise ValueError(f"Altura deve ser entre {ALTURA_MIN}m e {ALTURA_MAX}m")
    if not (PESO_MIN <= peso <= PESO_MAX):
        raise ValueError(f"Peso deve ser entre {PESO_MIN}kg e {PESO_MAX}kg")
    if not (IDADE_MIN <= idade <= IDADE_MAX):
        raise ValueError(f"Idade deve ser entre {IDADE_MIN} e {IDADE_MAX} anos")

    nascimento = ano_atual - idade
    imc = peso / (altura ** 2)

    if imc < 18.5:
        categoria = "abaixo do peso"
        classificacao = "Abaixo do peso"
    elif imc < 25:
        categoria = "no peso ideal"
        classificacao = "Peso normal"
    elif imc < 30:
        categoria = "com sobrepeso"
        classificacao = "Sobrepeso"
    else:
        categoria = "com obesidade"
        classificacao = "Obesidade"

    return ResultadoIMC(
        nome=nome,
        idade=idade,
        altura=altura,
        peso=peso,
        imc=imc,
        categoria=categoria,
        classificacao=classificacao,
        ano_nascimento=nascimento,
    )


if __name__ == "__main__":
    print(calcular_imc("Teste", 25, 1.75, 70, 2026))