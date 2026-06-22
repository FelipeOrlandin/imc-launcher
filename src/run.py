"""Entry point para PyInstaller.

Forca imports de todos os modulos para que PyInstaller
os encontre durante a analise estatica.
"""

import sys
import os

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

if base_path not in sys.path:
    sys.path.insert(0, base_path)

import core.modelos
import core.calculadora
import core.validators
import gui.tema
import gui.preview
import gui.widgets.card
import gui.widgets.entry
import gui.widgets.selector
import gui.widgets
import gui.app
import cli

from main import main
main()