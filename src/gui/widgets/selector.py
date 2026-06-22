import tkinter as tk
from ..tema import (
    COR_CARD, COR_BORDA, COR_TEXTO, COR_TEXTO_SEC,
    COR_PRIMARIA, COR_PRIMARIA_HOVER, COR_PRIMARIA_LIGHT,
    COR_INPUT_BG, FONTE_INPUT, FONTE_LABEL, FONTE_BOTAO_PEQUENO,
)


class SelectorButton(tk.Frame):
    """Botao seletor com pop-up de lista.
    
    Exibe um botao que, ao clicar, abre uma janela popup
    com lista de opcoes para selecionar.
    """
    def __init__(self, parent, values, default, command=None, width=12, label=""):
        super().__init__(parent, bg=COR_CARD)
        self.values = list(values)
        self.command = command
        self.var = tk.StringVar(value=str(default))
        self.width = width
        self.label = label

        self.btn = tk.Button(self, textvariable=self.var,
                             font=FONTE_INPUT, bg=COR_INPUT_BG, fg=COR_TEXTO,
                             relief=tk.FLAT, bd=0, cursor="hand2",
                             activebackground=COR_PRIMARIA_LIGHT,
                             activeforeground=COR_PRIMARIA,
                             command=self._open_popup,
                             highlightthickness=1,
                             highlightbackground=COR_BORDA,
                             anchor="center")
        self.btn.pack(fill=tk.X, ipady=10)

    def _open_popup(self):
        popup = tk.Toplevel(self)
        popup.title("")
        popup.geometry("260x320")
        popup.configure(bg=COR_CARD)
        popup.resizable(False, False)
        popup.transient(self.winfo_toplevel())
        popup.grab_set()
        popup.overrideredirect(True)

        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        if x + 260 > screen_w:
            x = screen_w - 270
        if y + 320 > screen_h:
            y = self.winfo_rooty() - 320
        popup.geometry(f"+{x}+{y}")

        outer = tk.Frame(popup, bg=COR_CARD,
                        highlightthickness=1,
                        highlightbackground=COR_BORDA)
        outer.pack(fill=tk.BOTH, expand=True)

        header_frame = tk.Frame(outer, bg=COR_PRIMARIA)
        header_frame.pack(fill=tk.X)
        titulo = self.label if self.label else "Selecione"
        tk.Label(header_frame, text=titulo, font=FONTE_LABEL,
                bg=COR_PRIMARIA, fg="white").pack(ipady=10)

        frame_lista = tk.Frame(outer, bg=COR_CARD)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll = tk.Scrollbar(frame_lista, width=8, bg=COR_BORDA,
                             troughcolor=COR_CARD, bd=0)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(frame_lista, font=FONTE_INPUT,
                            bg=COR_INPUT_BG, fg=COR_TEXTO,
                            selectmode=tk.SINGLE,
                            yscrollcommand=scroll.set,
                            relief=tk.FLAT, bd=0,
                            activestyle="none",
                            selectbackground=COR_PRIMARIA,
                            selectforeground="white",
                            cursor="hand2",
                            highlightthickness=0)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.configure(command=listbox.yview)

        for v in self.values:
            listbox.insert(tk.END, str(v))

        current = self.var.get()
        for i, v in enumerate(self.values):
            if str(v) == current:
                listbox.selection_set(i)
                listbox.see(i)
                break

        def confirm():
            sel = listbox.curselection()
            if sel:
                value = str(self.values[sel[0]])
                self.var.set(value)
                if self.command:
                    self.command(value)
            popup.destroy()

        btn_frame = tk.Frame(outer, bg=COR_CARD)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0,10))

        tk.Button(btn_frame, text="Cancelar",
                 font=FONTE_BOTAO_PEQUENO,
                 bg=COR_INPUT_BG, fg=COR_TEXTO,
                 relief=tk.FLAT, bd=0, cursor="hand2",
                 activebackground=COR_BORDA,
                 command=popup.destroy).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0,4))

        tk.Button(btn_frame, text="OK",
                 font=FONTE_BOTAO_PEQUENO,
                 bg=COR_PRIMARIA, fg="white",
                 relief=tk.FLAT, bd=0, cursor="hand2",
                 activebackground=COR_PRIMARIA_HOVER,
                 command=confirm).pack(side=tk.RIGHT, fill=tk.X, expand=True, ipady=8, padx=(4,0))

        listbox.bind("<Double-Button-1>", lambda e: confirm())
        popup.bind("<Return>", lambda e: confirm())
        popup.bind("<Escape>", lambda e: popup.destroy())
        listbox.focus_set()

    def get(self):
        return self.var.get()