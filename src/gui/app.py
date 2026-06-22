import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from core.calculadora import calcular_imc
from gui.widgets import Card, ValidatedEntry, SelectorButton
from gui.tema import (
    COR_FUNDO, COR_CARD, COR_TEXTO, COR_TEXTO_SEC, COR_TEXTO_TERCIARIO,
    COR_PRIMARIA, COR_PRIMARIA_HOVER, COR_PRIMARIA_LIGHT,
    COR_PRIMARIA_GRADIENTE_TOP, COR_PRIMARIA_GRADIENTE_BOTTOM,
    COR_SUCESSO, COR_ATENCAO, COR_ERRO,
    COR_BORDA, COR_INPUT_BG, COR_SLIDER_TRACK, COR_SLIDER_BG,
    FONTE_TITULO, FONTE_SUBTITULO, FONTE_LABEL, FONTE_INPUT,
    FONTE_BOTAO, FONTE_PEQUENA, FONTE_VALOR_GRANDE, FONTE_CLASSIFICACAO,
)


def criar_gradiente(canvas, x1, y1, x2, y2, cor1, cor2, passo=1):
    """Desenha um gradiente vertical no canvas."""
    r1 = int(cor1[1:3], 16); g1 = int(cor1[3:5], 16); b1 = int(cor1[5:7], 16)
    r2 = int(cor2[1:3], 16); g2 = int(cor2[3:5], 16); b2 = int(cor2[5:7], 16)
    altura = y2 - y1
    for i in range(0, altura, passo):
        frac = i / altura
        r = int(r1 + (r2 - r1) * frac)
        g = int(g1 + (g2 - g1) * frac)
        b = int(b1 + (b2 - b1) * frac)
        cor = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(x1, y1 + i, x2, y1 + i, fill=cor, width=passo+1)


def validar_nome(texto):
    if len(texto) > 50:
        return False
    return all(c.isalpha() or c.isspace() or c in "aeiouAEIOUaeiou '^.'-_/" for c in texto)


def validar_decimal(texto):
    if texto == "":
        return True
    texto = texto.replace(",", ".")
    partes = texto.split(".")
    if len(partes) > 2:
        return False
    return all(p.isdigit() for p in partes)


class AppIMC:
    """Aplicacao principal da calculadora IMC.
    
    Interface grafica com:
    - Preview ao vivo do IMC
    - Sliders para altura e peso
    - Classificacao OMS padronizada
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculadora de IMC")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.root.configure(bg=COR_FUNDO)

        w, h = 500, 700
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        self.categoria_frames = []
        self.categoria_widgets = []

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

        self.scrollable.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable, anchor="nw", width=480)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,10), pady=10)

        def _mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _mousewheel)

    def _criar_header(self):
        header = tk.Frame(self.scrollable, bg=COR_PRIMARIA, highlightthickness=0)
        header.pack(fill=tk.X, pady=(0, 20))

        h_canvas = tk.Canvas(header, height=130, bg=COR_PRIMARIA, highlightthickness=0)
        h_canvas.pack(fill=tk.X)
        criar_gradiente(h_canvas, 0, 0, 500, 130,
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
        inner_preview = self._criar_card_layout(self.scrollable)

        preview_topo = tk.Frame(inner_preview, bg=COR_CARD)
        preview_topo.pack(fill=tk.X)

        self.preview_icone_label = tk.Label(preview_topo, text="?",
                                  font=FONTE_VALOR_GRANDE,
                                  bg=COR_CARD, fg=COR_TEXTO_SEC)
        self.preview_icone_label.pack(side=tk.LEFT, padx=(0, 15))

        preview_centro = tk.Frame(preview_topo, bg=COR_CARD)
        preview_centro.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(preview_centro, text="SEU IMC", font=FONTE_PEQUENA,
                 bg=COR_CARD, fg=COR_TEXTO_SEC).pack(anchor=tk.W)

        self.preview_imc_var = tk.StringVar(value="--")
        self.preview_imc_label = tk.Label(preview_centro, textvariable=self.preview_imc_var,
                                font=FONTE_VALOR_GRANDE, bg=COR_CARD, fg=COR_PRIMARIA)
        self.preview_imc_label.pack(anchor=tk.W)

        preview_dir = tk.Frame(preview_topo, bg=COR_CARD)
        preview_dir.pack(side=tk.RIGHT)

        tk.Label(preview_dir, text="CLASSIFICACAO", font=FONTE_PEQUENA,
                 bg=COR_CARD, fg=COR_TEXTO_SEC).pack(anchor=tk.E)

        self.preview_class_var = tk.StringVar(value="---")
        self.preview_class_label = tk.Label(preview_dir, textvariable=self.preview_class_var,
                                  font=FONTE_CLASSIFICACAO, bg=COR_CARD, fg=COR_TEXTO_SEC)
        self.preview_class_label.pack(anchor=tk.E)

        self.preview_desc_var = tk.StringVar(value="Preencha altura e peso")
        tk.Label(inner_preview, textvariable=self.preview_desc_var, font=FONTE_PEQUENA,
                 bg=COR_CARD, fg=COR_TEXTO_SEC).pack(anchor=tk.W, pady=(8, 0))

        progresso_frame = tk.Frame(inner_preview, bg=COR_CARD)
        progresso_frame.pack(fill=tk.X, pady=(12, 0))

        progresso_bg = tk.Frame(progresso_frame, bg=COR_SLIDER_BG, height=6, highlightthickness=0)
        progresso_bg.pack(fill=tk.X)

        progresso_barra = tk.Frame(progresso_bg, bg=COR_SLIDER_BG, height=6, highlightthickness=0)
        progresso_barra.pack(fill=tk.X)

        self.progresso_max_width = 440
        self.progresso_preenchimento = tk.Frame(progresso_barra, bg=COR_SLIDER_BG, width=0, height=6, highlightthickness=0)
        self.progresso_preenchimento.place(x=0, y=0)

    def _criar_nome(self):
        inner_nome = self._criar_card_layout(self.scrollable)
        tk.Label(inner_nome, text="Nome completo", font=FONTE_LABEL, bg=COR_CARD,
                 fg=COR_TEXTO).pack(anchor=tk.W)
        self.entrada_nome = ValidatedEntry(inner_nome, placeholder="Ex: Joao Silva",
                                  validator=validar_nome, max_chars=50)
        self.entrada_nome.pack(fill=tk.X, pady=(6, 0))

    def _criar_idade_ano(self):
        inner_idade_ano = self._criar_card_layout(self.scrollable)
        grid = tk.Frame(inner_idade_ano, bg=COR_CARD)
        grid.pack(fill=tk.X)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        tk.Label(grid, text="Idade", font=FONTE_LABEL, bg=COR_CARD,
                 fg=COR_TEXTO).grid(row=0, column=0, sticky="w")
        self.seletor_idade = SelectorButton(grid, list(range(1, 111)), default=25)
        self.seletor_idade.grid(row=1, column=0, sticky="ew", padx=(0,5), pady=(5,0))

        tk.Label(grid, text="Ano", font=FONTE_LABEL, bg=COR_CARD,
                 fg=COR_TEXTO).grid(row=0, column=1, sticky="w", padx=(5,0))
        ano_atual = datetime.now().year
        self.seletor_ano = SelectorButton(grid, list(range(ano_atual-100, ano_atual+1)), default=ano_atual)
        self.seletor_ano.grid(row=1, column=1, sticky="ew", padx=(5,0), pady=(5,0))

    def _criar_altura(self):
        inner_alt = self._criar_card_layout(self.scrollable)
        tk.Label(inner_alt, text="Altura (m)", font=FONTE_LABEL, bg=COR_CARD,
                 fg=COR_TEXTO).pack(anchor=tk.W)

        frame_slider_alt = tk.Frame(inner_alt, bg=COR_CARD)
        frame_slider_alt.pack(fill=tk.X, pady=(5,0))

        self.altura_var = tk.StringVar(value="1.70")
        self.scale_altura = tk.Scale(frame_slider_alt, from_=0.5, to=2.5, resolution=0.01,
                           orient=tk.HORIZONTAL, length=300, bg=COR_CARD,
                           fg=COR_PRIMARIA, highlightthickness=0, bd=0,
                           troughcolor=COR_SLIDER_TRACK,
                           activebackground=COR_PRIMARIA,
                           command=lambda v: self.altura_var.set(f"{float(v):.2f}"))
        self.scale_altura.set(1.70)
        self.scale_altura.pack(side=tk.LEFT, fill=tk.X, expand=True)

        entry_altura = tk.Entry(frame_slider_alt, width=7, font=FONTE_INPUT,
                           textvariable=self.altura_var, justify="center",
                           bg=COR_INPUT_BG, fg=COR_PRIMARIA,
                           relief=tk.FLAT, bd=0, highlightthickness=1,
                           highlightbackground=COR_BORDA,
                           validate="key",
                           validatecommand=(self.root.register(validar_decimal), '%P'))
        entry_altura.pack(side=tk.LEFT, padx=(10,0), ipady=8)

        def sync_altura_scale(*args):
            try:
                v = float(self.altura_var.get().replace(",","."))
                if 0.5 <= v <= 2.5:
                    self.scale_altura.set(v)
                    self._atualizar_preview()
            except ValueError:
                pass
        self.altura_var.trace_add("write", sync_altura_scale)
        self.scale_altura.configure(command=lambda v: [self.altura_var.set(f"{float(v):.2f}"), self._atualizar_preview()])

    def _criar_peso(self):
        inner_pes = self._criar_card_layout(self.scrollable)
        tk.Label(inner_pes, text="Peso (kg)", font=FONTE_LABEL, bg=COR_CARD,
                 fg=COR_TEXTO).pack(anchor=tk.W)

        frame_slider_pes = tk.Frame(inner_pes, bg=COR_CARD)
        frame_slider_pes.pack(fill=tk.X, pady=(5,0))

        self.peso_var = tk.StringVar(value="70.0")
        self.scale_peso = tk.Scale(frame_slider_pes, from_=30, to=200, resolution=0.1,
                         orient=tk.HORIZONTAL, length=300, bg=COR_CARD,
                         fg=COR_PRIMARIA, highlightthickness=0, bd=0,
                         troughcolor=COR_SLIDER_TRACK,
                         activebackground=COR_PRIMARIA,
                         command=lambda v: self.peso_var.set(f"{float(v):.1f}"))
        self.scale_peso.set(70.0)
        self.scale_peso.pack(side=tk.LEFT, fill=tk.X, expand=True)

        entry_peso = tk.Entry(frame_slider_pes, width=7, font=FONTE_INPUT,
                         textvariable=self.peso_var, justify="center",
                         bg=COR_INPUT_BG, fg=COR_PRIMARIA,
                         relief=tk.FLAT, bd=0, highlightthickness=1,
                         highlightbackground=COR_BORDA,
                         validate="key",
                         validatecommand=(self.root.register(validar_decimal), '%P'))
        entry_peso.pack(side=tk.LEFT, padx=(10,0), ipady=8)

        def sync_peso_scale(*args):
            try:
                v = float(self.peso_var.get().replace(",","."))
                if 30 <= v <= 200:
                    self.scale_peso.set(v)
                    self._atualizar_preview()
            except ValueError:
                pass
        self.peso_var.trace_add("write", sync_peso_scale)
        self.scale_peso.configure(command=lambda v: [self.peso_var.set(f"{float(v):.1f}"), self._atualizar_preview()])

    def _criar_classificacao(self):
        inner_class = self._criar_card_layout(self.scrollable)
        tk.Label(inner_class, text="Classificacao do IMC", font=FONTE_LABEL,
                 bg=COR_CARD, fg=COR_TEXTO).pack(anchor=tk.W, pady=(0,8))

        categorias = [
            ("Abaixo do peso", "< 18,5", COR_ATENCAO),
            ("Peso normal", "18,5 - 24,9", COR_SUCESSO),
            ("Sobrepeso", "25 - 29,9", COR_ATENCAO),
            ("Obesidade", ">= 30", COR_ERRO),
        ]

        for cat, faixa, cor in categorias:
            row = tk.Frame(inner_class, bg=COR_CARD)
            row.pack(fill=tk.X, pady=2, ipady=5)

            indicador = tk.Frame(row, bg=cor, width=4, height=20, highlightthickness=0)
            indicador.pack(side=tk.LEFT, padx=(12,8))

            lbl_cat = tk.Label(row, text=cat, font=FONTE_INPUT, bg=COR_CARD, fg=COR_TEXTO)
            lbl_cat.pack(side=tk.LEFT)

            lbl_faixa = tk.Label(row, text=faixa, font=FONTE_INPUT, bg=COR_CARD, fg=COR_TEXTO_SEC)
            lbl_faixa.pack(side=tk.RIGHT, padx=(0,12))

            self.categoria_frames.append(row)
            self.categoria_widgets.append((lbl_cat, lbl_faixa, indicador))

    def _criar_botao(self):
        btn_outer = tk.Frame(self.scrollable, bg=COR_FUNDO)
        btn_outer.pack(pady=(5, 18), fill=tk.X, padx=15)

        self.btn_calc = tk.Button(btn_outer, text="Calcular IMC", command=self._calcular,
                            font=FONTE_BOTAO, bg=COR_PRIMARIA, fg="white",
                            relief=tk.FLAT, bd=0, cursor="hand2",
                            activebackground=COR_PRIMARIA_HOVER,
                            activeforeground="white",
                            highlightthickness=0,
                            padx=20, pady=14)
        self.btn_calc.pack(fill=tk.X)

        def btn_enter(e):
            self.btn_calc.configure(bg=COR_PRIMARIA_HOVER)
        def btn_leave(e):
            self.btn_calc.configure(bg=COR_PRIMARIA)
        self.btn_calc.bind("<Enter>", btn_enter)
        self.btn_calc.bind("<Leave>", btn_leave)

    def _criar_rodape(self):
        tk.Frame(self.scrollable, bg=COR_BORDA, height=1).pack(fill=tk.X, padx=40, pady=(5,8))
        tk.Label(self.scrollable, text="\u00a9 2026 Felipe Orlandin", font=FONTE_PEQUENA,
                 bg=COR_FUNDO, fg=COR_TEXTO_SEC).pack(pady=(0,12))

    def _atualizar_preview(self):
        try:
            altura = float(self.altura_var.get().replace(",", "."))
            peso = float(self.peso_var.get().replace(",", "."))
            if altura <= 0 or peso <= 0:
                raise ValueError
            imc = peso / (altura ** 2)
            self.preview_imc_var.set(f"{imc:.1f}")

            if imc < 18.5:
                classificacao = "Abaixo do peso"
                cor = COR_ATENCAO
                icone = "\u26a0"
                descricao = "Voce esta abaixo do peso recomendado."
                faixa_idx = 0
            elif imc < 25:
                classificacao = "Peso normal"
                cor = COR_SUCESSO
                icone = "\u2713"
                descricao = "Parabens! Seu peso esta ideal."
                faixa_idx = 1
            elif imc < 30:
                classificacao = "Sobrepeso"
                cor = COR_ATENCAO
                icone = "\u25b2"
                descricao = "Atencao: voce esta com sobrepeso."
                faixa_idx = 2
            else:
                classificacao = "Obesidade"
                cor = COR_ERRO
                icone = "\u25cf"
                descricao = "Procure um profissional de saude."
                faixa_idx = 3

            self.preview_class_var.set(classificacao)
            self.preview_class_label.configure(fg=cor)
            self.preview_imc_label.configure(fg=cor)
            self.preview_icone_label.configure(text=icone, fg=cor)
            self.preview_desc_var.set(descricao)
            self._destacar_categoria(faixa_idx)
            self._atualizar_barra_imc(imc)

        except (ValueError, ZeroDivisionError):
            self.preview_imc_var.set("--")
            self.preview_class_var.set("---")
            self.preview_icone_label.configure(text="?", fg=COR_TEXTO_SEC)
            self.preview_desc_var.set("Preencha altura e peso")
            self.preview_imc_label.configure(fg=COR_PRIMARIA)
            self._limpar_destaques()
            self.progresso_preenchimento.configure(width=0)

    def _atualizar_barra_imc(self, imc):
        imc_clamped = max(10, min(50, imc))
        frac = (imc_clamped - 10) / 40.0
        width = int(frac * self.progresso_max_width)
        if imc < 18.5:
            cor = COR_ATENCAO
        elif imc < 25:
            cor = COR_SUCESSO
        elif imc < 30:
            cor = COR_ATENCAO
        else:
            cor = COR_ERRO
        self.progresso_preenchimento.configure(bg=cor, width=width)

    def _destacar_categoria(self, indice):
        for i, frame in enumerate(self.categoria_frames):
            lbl_cat, lbl_faixa, dot = self.categoria_widgets[i]
            if i == indice:
                frame.configure(bg=COR_PRIMARIA_LIGHT)
                lbl_cat.configure(bg=COR_PRIMARIA_LIGHT, fg=COR_PRIMARIA)
                lbl_faixa.configure(bg=COR_PRIMARIA_LIGHT, fg=COR_PRIMARIA)
                dot.configure(bg=COR_PRIMARIA_LIGHT)
            else:
                frame.configure(bg=COR_CARD)
                lbl_cat.configure(bg=COR_CARD, fg=COR_TEXTO)
                lbl_faixa.configure(bg=COR_CARD, fg=COR_TEXTO_SEC)
                dot.configure(bg=COR_CARD)

    def _limpar_destaques(self):
        for i, frame in enumerate(self.categoria_frames):
            lbl_cat, lbl_faixa, dot = self.categoria_widgets[i]
            frame.configure(bg=COR_CARD)
            lbl_cat.configure(bg=COR_CARD, fg=COR_TEXTO)
            lbl_faixa.configure(bg=COR_CARD, fg=COR_TEXTO_SEC)
            dot.configure(bg=COR_CARD)

    def _calcular(self):
        self.entrada_nome.set_valid(True)

        nome = self.entrada_nome.get()
        if not nome:
            self.entrada_nome.set_valid(False)
            self.entrada_nome.focus()
            messagebox.showerror("Erro", "Por favor, informe seu nome.")
            return

        idade_str = self.seletor_idade.get()
        try:
            idade = int(idade_str)
            if idade < 1 or idade > 110:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Idade invalida (1-110).")
            return

        altura_str = self.altura_var.get().replace(",", ".")
        try:
            altura = float(altura_str)
            if altura < 0.5 or altura > 2.5:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Altura deve ser entre 0.5 e 2.5 m.")
            return

        peso_str = self.peso_var.get().replace(",", ".")
        try:
            peso = float(peso_str)
            if peso < 20 or peso > 300:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Peso deve ser entre 20 e 300 kg.")
            return

        ano_str = self.seletor_ano.get()
        try:
            ano = int(ano_str)
            if ano < 1900 or ano > datetime.now().year:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Ano invalido.")
            return

        resultado = calcular_imc(nome, idade, altura, peso, ano)
        messagebox.showinfo("Resultado do IMC", resultado.formatar())

    def executar(self):
        self.root.mainloop()