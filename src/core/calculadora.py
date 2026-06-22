from core.modelos import ResultadoIMC


def calcular_imc(nome: str, idade: int, altura: float, peso: float, ano_atual: int) -> ResultadoIMC:
    """Calcula o IMC usando padrao OMS (4 categorias).
    
    Antes havia inconsistencia entre core (3 categorias) e GUI (4 categorias).
    Agora ambos usam o padrao OMS:
      - Abaixo do peso: < 18.5
      - Peso normal: 18.5 - 24.9
      - Sobrepeso: 25 - 29.9
      - Obesidade: >= 30
    
    Returns:
        ResultadoIMC com dados estruturados
    Raises:
        ValueError: se os dados estiverem fora das faixas validas
    """
    if not (0.5 <= altura <= 2.5):
        raise ValueError("Altura deve ser entre 0.5m e 2.5m")
    if not (20 <= peso <= 300):
        raise ValueError("Peso deve ser entre 20kg e 300kg")
    if not (1 <= idade <= 150):
        raise ValueError("Idade deve ser entre 1 e 150 anos")

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