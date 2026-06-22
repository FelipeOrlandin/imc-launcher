"""Aplicacao principal da calculadora IMC.

Gerencia a janela, scroll, e coordena os widgets.
A logica de preview ficou em gui/preview.py.
A logica de validacao ficou em core/validators.py.
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from core.calculadora import calcular_imc
from core.validators import (
    validar_nome, validar_decimal,
    ALTURA_MIN, ALTURA_MAX, PESO_MIN, PESO_MAX, IDADE_MIN, IDADE_MAX,
)
from gui.widgets import Card, ValidatedEntry, SelectorButton
from gui.preview import PreviewCard
from gui.tema import (
    COR_FUNDO, COR_CARD, COR_TEXTO, COR_TEXTO_SEC,
    COR_PRIMARIA, COR_PRIMARIA_HOVER,
    COR_PRIMARIA_GRADIENTE_TOP, COR_PRIMARIA_GRADIENTE_BOTTOM,
    COR_BORDA, COR_INPUT_BG, COR_SLIDER_TRACK,
    JANELA_LARGURA, JANELA_ALTURA, SCROLL_WIDTH, HEADER_HEIGHT,
    FONTE_TITULO, FONTE_SUBTITULO, FONTE_LABEL, FONTE_INPUT,
    FONTE_BOTAO, FONTE_PEQUENA,
)


def criar_gradiente(canvas, x1, y1, x2, y2, cor1, cor2, passo=1):
    """Desenha um gradiente vertical no canvas."""
    r1 = int(cor1[1:3], 16)
    g1 = int(cor1[3:5], 16)
    b1 = int(cor1[5:7], 16)
    r2 = int(cor2[1:3], 16)
    g2 = int(cor2[3:5], 16)
    b2 = int(cor2[5:7], 16)
    alt = y2 - y1
    for i in range(0, alt, passo):
        frac = i / alt
        r = int(r1 + (r2 - r1) * frac)
        g = int(g1 + (g2 - g1) * frac)
        b = int(b1 + (b2 - b1) * frac)
        cor = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(x1, y1 + i, x2, y1 + i, fill=cor, width=passo + 1)


class AppIMC:
    """Aplicacao principal da calculadora IMC."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculadora de IMC")
        self.root.geometry(f"{JANELA_LARGURA}x{JANELA_ALTURA}")
        self.root.resizable(False, False)
        self.root.configure(bg=COR_FUNDO)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        x = (self.root.winfo_screenwidth() - JANELA_LARGURA) // 2
        y = (self.root.winfo_screenheight() - JANELA_ALTURA) // 2
        self.root.geometry(f"{JANELA_LARGURA}x{JANELA_ALTURA}+{x}+{y}")

        self._criar_scrollable()
        self._criar_header()
        self._criar_preview()
        self._criar_nome()
        self._criar_idade_ano()
        self._criar_altura()
        self._criar_peso()
        self._criar_classificacao()
        self._criar_botao()
        self._criar_rodape()

        self._atualizar_preview()

    def _criar_scrollable(self):
        self.molde = tk.Frame(self.root, bg=COR_FUNDO)
        self.molde.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.molde, bg=COR_FUNDO, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.molde, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable = tk.Frame(self.canvas, bg=COR_FUNDO)

        self.scrollable.bind("<Configure>",
                             lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable, anchor="nw", width=SCROLL_WIDTH)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)

        def _mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_enter(event):
            self.canvas.bind_all("<MouseWheel>", _mousewheel)

        def _on_leave(event):
            self.canvas.unbind_all("<MouseWheel>")

        self.canvas.bind("<MouseWheel>", _mousewheel)
        self.canvas.bind("<Enter>", _on_enter)
        self.canvas.bind("<Leave>", _on_leave)

    def _criar_header(self):
        header = tk.Frame(self.scrollable, bg=COR_PRIMARIA, highlightthickness=0)
        header.pack(fill=tk.X, pady=(0, 20))

        h_canvas = tk.Canvas(header, height=HEADER_HEIGHT, bg=COR_PRIMARIA, highlightthickness=0)
        h_canvas.pack(fill=tk.X)
        criar_gradiente(h_canvas, 0, 0, JANELA_LARGURA, HEADER_HEIGHT,
                        COR_PRIMARIA_GRADIENTE_TOP, COR_PRIMARIA_GRADIENTE_BOTTOM)

        tk.Label(header, text="Calculadora de IMC", font=FONTE_TITULO,
                 bg=COR_PRIMARIA, fg="white").place(relx=0.5, rely=0.35, anchor="center")
        tk.Label(header, text="Indice de Massa Corporal", font=FONTE_SUBTITULO,
                 bg=COR_PRIMARIA, fg="#D6E4FF").place(relx=0.5, rely=0.55, anchor="center")

    def _criar_card_layout(self, parent):
        card = Card(parent)
        card.pack(fill=tk.X, padx=15, pady=(0, 12))
        inner = tk.Frame(card, bg=COR_CARD)
        inner.pack(fill=tk.X, padx=15, pady=12)
        return inner

    def _criar_preview(self):
        inner = self._criar_card_layout(self.scrollable)
        self.preview = PreviewCard(inner)

    def _criar_nome(self):
        inner = self._criar_card_layout(self.scrollable)
        tk.Label(inner, text="Nome completo", font=FONTE_LABEL, bg=COR_CARD,
                 fg=COR_TEXTO).pack(anchor=tk.W)
        self.entrada_nome = ValidatedEntry(inner, placeholder="Ex: Joao Silva",
                                           validator=validar_nome, max_chars=50)
        self.entrada_nome.pack(fill=tk.X, pady=(6, 0))

    def _criar_idade_ano(self):
        inner = self._criar_card_layout(self.scrollable)
        grid = tk.Frame(inner, bg=COR_CARD)
        grid.pack(fill=tk.X)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        tk.Label(grid, text="Idade", font=FONTE_LABEL, bg=COR_CARD,
                 fg=COR_TEXTO).grid(row=0, column=0, sticky="w")
        self.seletor_idade = SelectorButton(grid, list(range(IDADE_MIN, IDADE_MAX + 1)), default=25)
        self.seletor_idade.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=(5, 0))

        tk.Label(grid, text="Ano", font=FONTE_LABEL, bg=COR_CARD,
                 fg=COR_TEXTO).grid(row=0, column=1, sticky="w", padx=(5, 0))
        ano_atual = datetime.now().year
        self.seletor_ano = SelectorButton(grid, list(range(ano_atual - 100, ano_atual + 1)),
                                          default=ano_atual)
        self.seletor_ano.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=(5, 0))

    def _criar_altura(self):
        inner = self._criar_card_layout(self.scrollable)
        tk.Label(inner, text="Altura (m)", font=FONTE_LABEL, bg=COR_CARD,
                 fg=COR_TEXTO).pack(anchor=tk.W)

        frame_slider = tk.Frame(inner, bg=COR_CARD)
        frame_slider.pack(fill=tk.X, pady=(5, 0))

        self.altura_var = tk.StringVar(value="1.70")
        self.scale_altura = tk.Scale(frame_slider, from_=ALTURA_MIN, to=ALTURA_MAX, resolution=0.01,
                                     orient=tk.HORIZONTAL, length=300, bg=COR_CARD,
                                     fg=COR_PRIMARIA, highlightthickness=0, bd=0,
                                     troughcolor=COR_SLIDER_TRACK,
                                     activebackground=COR_PRIMARIA,
                                     command=lambda v: self.altura_var.set(f"{float(v):.2f}"))
        self.scale_altura.set(1.70)
        self.scale_altura.pack(side=tk.LEFT, fill=tk.X, expand=True)

        entry = tk.Entry(frame_slider, width=7, font=FONTE_INPUT,
                         textvariable=self.altura_var, justify="center",
                         bg=COR_INPUT_BG, fg=COR_PRIMARIA,
                         relief=tk.FLAT, bd=0, highlightthickness=1,
                         highlightbackground=COR_BORDA,
                         validate="key",
                         validatecommand=(self.root.register(validar_decimal), '%P'))
        entry.pack(side=tk.LEFT, padx=(10, 0), ipady=8)

        def sync_scale(*args):
            try:
                v = float(self.altura_var.get().replace(",", "."))
                if ALTURA_MIN <= v <= ALTURA_MAX:
                    self.scale_altura.set(v)
                    self._atualizar_preview()
            except ValueError:
                pass

        self.altura_var.trace_add("write", sync_scale)
        self.scale_altura.configure(command=lambda v: [
            self.altura_var.set(f"{float(v):.2f}"), self._atualizar_preview()])

    def _criar_peso(self):
        inner = self._criar_card_layout(self.scrollable)
        tk.Label(inner, text="Peso (kg)", font=FONTE_LABEL, bg=COR_CARD,
                 fg=COR_TEXTO).pack(anchor=tk.W)

        frame_slider = tk.Frame(inner, bg=COR_CARD)
        frame_slider.pack(fill=tk.X, pady=(5, 0))

        self.peso_var = tk.StringVar(value="70.0")
        self.scale_peso = tk.Scale(frame_slider, from_=PESO_MIN, to=PESO_MAX, resolution=0.1,
                                   orient=tk.HORIZONTAL, length=300, bg=COR_CARD,
                                   fg=COR_PRIMARIA, highlightthickness=0, bd=0,
                                   troughcolor=COR_SLIDER_TRACK,
                                   activebackground=COR_PRIMARIA,
                                   command=lambda v: self.peso_var.set(f"{float(v):.1f}"))
        self.scale_peso.set(70.0)
        self.scale_peso.pack(side=tk.LEFT, fill=tk.X, expand=True)

        entry = tk.Entry(frame_slider, width=7, font=FONTE_INPUT,
                         textvariable=self.peso_var, justify="center",
                         bg=COR_INPUT_BG, fg=COR_PRIMARIA,
                         relief=tk.FLAT, bd=0, highlightthickness=1,
                         highlightbackground=COR_BORDA,
                         validate="key",
                         validatecommand=(self.root.register(validar_decimal), '%P'))
        entry.pack(side=tk.LEFT, padx=(10, 0), ipady=8)

        def sync_scale(*args):
            try:
                v = float(self.peso_var.get().replace(",", "."))
                if PESO_MIN <= v <= PESO_MAX:
                    self.scale_peso.set(v)
                    self._atualizar_preview()
            except ValueError:
                pass

        self.peso_var.trace_add("write", sync_scale)
        self.scale_peso.configure(command=lambda v: [
            self.peso_var.set(f"{float(v):.1f}"), self._atualizar_preview()])

    def _criar_classificacao(self):
        inner = self._criar_card_layout(self.scrollable)
        tk.Label(inner, text="Classificacao do IMC", font=FONTE_LABEL,
                 bg=COR_CARD, fg=COR_TEXTO).pack(anchor=tk.W, pady=(0, 8))
        self.preview.criar_lista_categorias(inner)

    def _criar_botao(self):
        outer = tk.Frame(self.scrollable, bg=COR_FUNDO)
        outer.pack(pady=(5, 18), fill=tk.X, padx=15)

        self.btn_calc = tk.Button(outer, text="Calcular IMC", command=self._calcular,
                                  font=FONTE_BOTAO, bg=COR_PRIMARIA, fg="white",
                                  relief=tk.FLAT, bd=0, cursor="hand2",
                                  activebackground=COR_PRIMARIA_HOVER,
                                  activeforeground="white",
                                  highlightthickness=0, padx=20, pady=14)
        self.btn_calc.pack(fill=tk.X)

        self.btn_calc.bind("<Enter>", lambda e: self.btn_calc.configure(bg=COR_PRIMARIA_HOVER))
        self.btn_calc.bind("<Leave>", lambda e: self.btn_calc.configure(bg=COR_PRIMARIA))

    def _criar_rodape(self):
        tk.Frame(self.scrollable, bg=COR_BORDA, height=1).pack(fill=tk.X, padx=40, pady=(5, 8))
        tk.Label(self.scrollable, text="\u00a9 2026 Felipe Orlandin", font=FONTE_PEQUENA,
                 bg=COR_FUNDO, fg=COR_TEXTO_SEC).pack(pady=(0, 12))

    def _atualizar_preview(self):
        try:
            altura = float(self.altura_var.get().replace(",", "."))
            peso = float(self.peso_var.get().replace(",", "."))
            if altura <= 0 or peso <= 0:
                raise ValueError
            self.preview.atualizar(altura, peso)
        except (ValueError, ZeroDivisionError):
            self.preview._limpar()

    def _calcular(self):
        self.entrada_nome.set_valid(True)

        nome = self.entrada_nome.get()
        if not nome:
            self.entrada_nome.set_valid(False)
            self.entrada_nome.focus()
            messagebox.showerror("Erro", "Por favor, informe seu nome.")
            return

        try:
            idade = int(self.seletor_idade.get())
            if not (IDADE_MIN <= idade <= IDADE_MAX):
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", f"Idade invalida ({IDADE_MIN}-{IDADE_MAX}).")
            return

        try:
            altura = float(self.altura_var.get().replace(",", "."))
            if not (ALTURA_MIN <= altura <= ALTURA_MAX):
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", f"Altura deve ser entre {ALTURA_MIN} e {ALTURA_MAX} m.")
            return

        try:
            peso = float(self.peso_var.get().replace(",", "."))
            if not (PESO_MIN <= peso <= PESO_MAX):
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", f"Peso deve ser entre {PESO_MIN} e {PESO_MAX} kg.")
            return

        try:
            ano = int(self.seletor_ano.get())
            if ano < 1900 or ano > datetime.now().year:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Ano invalido.")
            return

        resultado = calcular_imc(nome, idade, altura, peso, ano)
        messagebox.showinfo("Resultado do IMC", resultado.formatar())

    def executar(self):
        self.root.mainloop()