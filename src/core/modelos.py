from dataclasses import dataclass


@dataclass
class ResultadoIMC:
    """Armazena o resultado estruturado do calculo de IMC.
    
    Usar dataclass permite acessar dados programaticamente
    (ex: resultado.imc, resultado.categoria) em vez de
    apenas uma string formatada.
    """
    nome: str
    idade: int
    altura: float
    peso: float
    imc: float
    categoria: str
    classificacao: str
    ano_nascimento: int

    def formatar(self) -> str:
        """Retorna texto formatado para exibicao."""
        return (
            f"=======================================\n"
            f"{self.nome} tem {self.idade} anos e {self.altura:.2f}m de altura.\n"
            f"{self.nome} pesa {self.peso:.1f}Kg e seu IMC e {self.imc:.2f}.\n"
            f"{self.nome} nasceu em {self.ano_nascimento}.\n\n"
            f"{self.nome} voce esta {self.classificacao}.\n"
            f"======================================="
        )