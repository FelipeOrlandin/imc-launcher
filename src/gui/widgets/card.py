import tkinter as tk
from gui.tema import COR_CARD, COR_BORDA


class Card(tk.Frame):
    """Widget de card para agrupar elementos visualmente.
    
    Cria um frame branco com borda leve, comum em interfaces modernas.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COR_CARD, bd=0,
                        highlightthickness=1,
                        highlightbackground=COR_BORDA,
                        highlightcolor=COR_BORDA,
                        **kwargs)