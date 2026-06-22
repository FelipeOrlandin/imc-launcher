import sys


def main():
    """Entry point principal do projeto.
    
    Detecta automaticamente se deve usar CLI ou GUI:
    - Com argumentos: CLI (python -m src.main Nome Idade Altura Peso Ano)
    - Sem argumentos: GUI (python -m src.main)
    """
    if len(sys.argv) > 1:
        from .cli import main as cli_main
        cli_main()
    else:
        from .gui.app import AppIMC
        app = AppIMC()
        app.executar()


if __name__ == "__main__":
    main()