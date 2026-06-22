import sys
import os

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

if base_path not in sys.path:
    sys.path.insert(0, base_path)


def main():
    """Entry point principal do projeto."""
    if len(sys.argv) > 1:
        from cli import main as cli_main
        cli_main()
    else:
        from gui.app import AppIMC
        app = AppIMC()
        app.executar()


if __name__ == "__main__":
    main()