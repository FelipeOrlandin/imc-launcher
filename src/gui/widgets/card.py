import tkinter as tk
from ..tema import COR_CARD, COR_BORDA


class Card(tk.Frame):
    """Widget de card para agrupar elementos visualmente."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COR_CARD, bd=0,
                        highlightthickness=1,
                        highlightbackground=COR_BORDA,
                        highlightcolor=COR_BORDA,
                        **kwargs)