import sys
import os

if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, base_path)


def main():
    """Entry point principal do projeto.
    
    Detecta automaticamente se deve usar CLI ou GUI:
    - Com argumentos: CLI (python -m src.main Nome Idade Altura Peso Ano)
    - Sem argumentos: GUI (python -m src.main)
    """
    if len(sys.argv) > 1:
        from cli import main as cli_main
        cli_main()
    else:
        from gui.app import AppIMC
        app = AppIMC()
        app.executar()


if __name__ == "__main__":
    main()