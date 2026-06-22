import tkinter as tk
from ..tema import (
    COR_CARD, COR_BORDA, COR_TEXTO, COR_TEXTO_SEC,
    COR_TEXTO_TERCIARIO, COR_PRIMARIA, COR_ERRO,
    COR_ERRO_LIGHT, COR_INPUT_BG, FONTE_INPUT, FONTE_PEQUENA,
)


class ValidatedEntry(tk.Frame):
    """Entry com placeholder e validacao visual.
    
    Recursos:
    - Placeholder que desaparece ao focar
    - Borda muda de cor com validacao
    - Helper text opcional
    """
    def __init__(self, parent, placeholder="", validator=None,
                 max_chars=None, helper_text=None, **kwargs):
        super().__init__(parent, bg=COR_CARD)
        self.placeholder = placeholder
        self.validator = validator
        self.max_chars = max_chars
        self.has_placeholder = bool(placeholder)
        self.valid = True

        self.border = tk.Frame(self, bg=COR_BORDA, bd=0,
                               highlightthickness=1,
                               highlightbackground=COR_BORDA)
        self.border.pack(fill=tk.X)

        self.entry = tk.Entry(self.border, font=FONTE_INPUT,
                              bg=COR_INPUT_BG, fg=COR_TEXTO,
                              insertbackground=COR_PRIMARIA,
                              insertwidth=2,
                              relief=tk.FLAT, bd=0, **kwargs)
        self.entry.pack(fill=tk.X, ipady=10, padx=12, pady=1)

        if placeholder:
            self.entry.insert(0, placeholder)
            self.entry.configure(fg=COR_TEXTO_SEC)
            self.entry.bind("<FocusIn>", self._clear_placeholder)
            self.entry.bind("<FocusOut>", self._restore_placeholder)

        if validator:
            vcmd = (self.register(self._validate), '%P')
            self.entry.configure(validate="key", validatecommand=vcmd)

        self.entry.bind("<FocusIn>", self._on_focus_in, add="+")
        self.entry.bind("<FocusOut>", self._on_focus_out, add="+")

        if helper_text:
            help_frame = tk.Frame(self, bg=COR_CARD)
            help_frame.pack(fill=tk.X, pady=(3,0))
            tk.Label(help_frame, text="\u2139", font=FONTE_PEQUENA,
                    bg=COR_CARD, fg=COR_TEXTO_TERCIARIO).pack(side=tk.LEFT, padx=(0,3))
            tk.Label(help_frame, text=helper_text, font=FONTE_PEQUENA,
                    bg=COR_CARD, fg=COR_TEXTO_TERCIARIO).pack(side=tk.LEFT)

    def _clear_placeholder(self, event):
        if self.has_placeholder and self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.configure(fg=COR_TEXTO)
            self.has_placeholder = False

    def _restore_placeholder(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.configure(fg=COR_TEXTO_SEC)
            self.has_placeholder = True

    def _on_focus_in(self, event):
        self.border.configure(highlightbackground=COR_PRIMARIA, bg=COR_PRIMARIA)

    def _on_focus_out(self, event):
        if not self.valid:
            self.border.configure(highlightbackground=COR_ERRO, bg=COR_ERRO)
        else:
            self.border.configure(highlightbackground=COR_BORDA, bg=COR_BORDA)

    def _validate(self, text):
        if self.max_chars and len(text) > self.max_chars:
            return False
        if self.validator and text:
            return self.validator(text)
        return True

    def get(self):
        text = self.entry.get().strip()
        return "" if text == self.placeholder else text

    def set_valid(self, valid):
        self.valid = valid
        if valid:
            self.border.configure(highlightbackground=COR_BORDA, bg=COR_BORDA)
        else:
            self.border.configure(highlightbackground=COR_ERRO, bg=COR_ERRO)
            self.after(100, lambda: self.border.configure(bg=COR_ERRO_LIGHT))
            self.after(300, lambda: self.border.configure(highlightbackground=COR_ERRO, bg=COR_ERRO))

    def focus(self):
        self.entry.focus_set()