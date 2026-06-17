import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from imc_core import calcular_imc
import math

# ========== CONFIGURAÇÃO DE TEMA ==========
COR_FUNDO = "#F0F2F5"
COR_CARD = "#FFFFFF"
COR_TEXTO = "#1A202C"
COR_TEXTO_SEC = "#718096"
COR_TEXTO_TERCIARIO = "#A0AEC0"
COR_PRIMARIA = "#4A6CF7"
COR_PRIMARIA_HOVER = "#3B5DE7"
COR_PRIMARIA_ATIVO = "#2D4FD7"
COR_PRIMARIA_LIGHT = "#E8EDFD"
COR_PRIMARIA_GRADIENTE_TOP = "#5B7BFA"
COR_PRIMARIA_GRADIENTE_BOTTOM = "#3A5BD9"
COR_SUCESSO = "#38A169"
COR_SUCESSO_LIGHT = "#C6F6D5"
COR_SUCESSO_BG = "#F0FFF4"
COR_ATENCAO = "#DD6B20"
COR_ATENCAO_LIGHT = "#FEEBC8"
COR_ATENCAO_BG = "#FFFAF0"
COR_ERRO = "#E53E3E"
COR_ERRO_LIGHT = "#FED7D7"
COR_ERRO_BG = "#FFF5F5"
COR_BORDA = "#E2E8F0"
COR_BORDA_CLARA = "#EDF2F7"
COR_INPUT_BG = "#F7FAFC"
COR_SLIDER_TRACK = "#CBD5E0"
COR_SLIDER_BG = "#E2E8F0"

FONTE_FAMILY = "Segoe UI"
FONTE_TITULO = (FONTE_FAMILY, 20, "bold")
FONTE_SUBTITULO = (FONTE_FAMILY, 10)
FONTE_LABEL = (FONTE_FAMILY, 10, "bold")
FONTE_INPUT = (FONTE_FAMILY, 10)
FONTE_BOTAO = (FONTE_FAMILY, 12, "bold")
FONTE_BOTAO_PEQUENO = (FONTE_FAMILY, 9)
FONTE_PEQUENA = (FONTE_FAMILY, 8)
FONTE_VALOR_GRANDE = (FONTE_FAMILY, 28, "bold")
FONTE_VALOR_MEDIO = (FONTE_FAMILY, 18, "bold")
FONTE_CLASSIFICACAO = (FONTE_FAMILY, 12, "bold")


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


# ========== WIDGETS CUSTOMIZADOS ==========
class Card(tk.Frame):
    """Card com cantos e borda leve - usando pack tradicional."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COR_CARD, bd=0,
                        highlightthickness=1,
                        highlightbackground=COR_BORDA,
                        highlightcolor=COR_BORDA,
                        **kwargs)


class ValidatedEntry(tk.Frame):
    """Entry com placeholder e validação visual."""
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
            tk.Label(help_frame, text="ⓘ", font=FONTE_PEQUENA,
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


class SelectorButton(tk.Frame):
    """Botão seletor com pop-up."""
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

        # Posicionar
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

        # Título
        header_frame = tk.Frame(outer, bg=COR_PRIMARIA)
        header_frame.pack(fill=tk.X)
        titulo = self.label if self.label else "Selecione"
        tk.Label(header_frame, text=titulo, font=FONTE_LABEL,
                bg=COR_PRIMARIA, fg="white").pack(ipady=10)

        # Lista com scroll
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


# ========== VALIDAÇÕES ==========
def validar_nome(texto):
    if len(texto) > 50:
        return False
    return all(c.isalpha() or c.isspace() or c in "áéíóúâêîôûãõàèìòùäëïöüçÁÉÍÓÚÂÊÎÔÛÃÕÀÈÌÒÙÄËÏÖÜÇ'." for c in texto)

def validar_decimal(texto):
    if texto == "":
        return True
    texto = texto.replace(",", ".")
    partes = texto.split(".")
    if len(partes) > 2:
        return False
    return all(p.isdigit() for p in partes)


# ========== FUNÇÃO DE ATUALIZAÇÃO AO VIVO ==========
def atualizar_preview(*args):
    try:
        altura = float(altura_var.get().replace(",", "."))
        peso = float(peso_var.get().replace(",", "."))
        if altura <= 0 or peso <= 0:
            raise ValueError
        imc = peso / (altura ** 2)
        preview_imc_var.set(f"{imc:.1f}")

        if imc < 18.5:
            classificacao = "Abaixo do peso"
            cor = COR_ATENCAO
            icone = "\u26a0"
            descricao = "Voc\u00ea est\u00e1 abaixo do peso recomendado."
            faixa_idx = 0
        elif 18.5 <= imc <= 24.9:
            classificacao = "Peso normal"
            cor = COR_SUCESSO
            icone = "\u2713"
            descricao = "Parab\u00e9ns! Seu peso est\u00e1 ideal."
            faixa_idx = 1
        elif 25 <= imc <= 29.9:
            classificacao = "Sobrepeso"
            cor = COR_ATENCAO
            icone = "\u25b2"
            descricao = "Aten\u00e7\u00e3o: voc\u00ea est\u00e1 com sobrepeso."
            faixa_idx = 2
        else:
            classificacao = "Obesidade"
            cor = COR_ERRO
            icone = "\u25cf"
            descricao = "Procure um profissional de sa\u00fade."
            faixa_idx = 3

        preview_class_var.set(classificacao)
        preview_class_label.configure(fg=cor)
        preview_imc_label.configure(fg=cor)
        preview_icone_label.configure(text=icone, fg=cor)
        preview_desc_var.set(descricao)
        destacar_categoria(faixa_idx)
        atualizar_barra_imc(imc)

    except (ValueError, ZeroDivisionError):
        preview_imc_var.set("--")
        preview_class_var.set("---")
        preview_icone_label.configure(text="?", fg=COR_TEXTO_SEC)
        preview_desc_var.set("Preencha altura e peso")
        preview_imc_label.configure(fg=COR_PRIMARIA)
        limpar_destaques()
        progresso_preenchimento.configure(width=0)


def atualizar_barra_imc(imc):
    imc_clamped = max(10, min(50, imc))
    frac = (imc_clamped - 10) / 40.0
    width = int(frac * progresso_max_width)
    if imc < 18.5:
        cor = COR_ATENCAO
    elif imc <= 24.9:
        cor = COR_SUCESSO
    elif imc <= 29.9:
        cor = COR_ATENCAO
    else:
        cor = COR_ERRO
    progresso_preenchimento.configure(bg=cor, width=width)


def destacar_categoria(indice):
    for i, frame in enumerate(categoria_frames):
        lbl_cat, lbl_faixa, dot = categoria_widgets[i]
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


def limpar_destaques():
    for i, frame in enumerate(categoria_frames):
        lbl_cat, lbl_faixa, dot = categoria_widgets[i]
        frame.configure(bg=COR_CARD)
        lbl_cat.configure(bg=COR_CARD, fg=COR_TEXTO)
        lbl_faixa.configure(bg=COR_CARD, fg=COR_TEXTO_SEC)
        dot.configure(bg=COR_CARD)


# ========== FUNÇÃO PRINCIPAL ==========
def calcular():
    entrada_nome.set_valid(True)

    nome = entrada_nome.get()
    if not nome:
        entrada_nome.set_valid(False)
        entrada_nome.focus()
        messagebox.showerror("Erro", "Por favor, informe seu nome.")
        return

    idade_str = seletor_idade.get()
    try:
        idade = int(idade_str)
        if idade < 1 or idade > 110:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Idade inv\u00e1lida (1-110).")
        return

    altura_str = altura_var.get().replace(",", ".")
    try:
        altura = float(altura_str)
        if altura < 0.5 or altura > 2.5:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Altura deve ser entre 0.5 e 2.5 m.")
        return

    peso_str = peso_var.get().replace(",", ".")
    try:
        peso = float(peso_str)
        if peso < 20 or peso > 300:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Peso deve ser entre 20 e 300 kg.")
        return

    ano_str = seletor_ano.get()
    try:
        ano = int(ano_str)
        if ano < 1900 or ano > datetime.now().year:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Ano inv\u00e1lido.")
        return

    resultado = calcular_imc(nome, idade, altura, peso, ano)
    messagebox.showinfo("Resultado do IMC", resultado)


# ========== CRIAÇÃO DA JANELA ==========
janela = tk.Tk()
janela.title("Calculadora de IMC")
janela.geometry("500x700")
janela.resizable(False, False)
janela.configure(bg=COR_FUNDO)

w, h = 500, 700
x = (janela.winfo_screenwidth() - w) // 2
y = (janela.winfo_screenheight() - h) // 2
janela.geometry(f"{w}x{h}+{x}+{y}")

# ========== MOLDE PRINCIPAL COM SCROLL ==========
molde = tk.Frame(janela, bg=COR_FUNDO)
molde.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(molde, bg=COR_FUNDO, highlightthickness=0)
scrollbar = tk.Scrollbar(molde, orient=tk.VERTICAL, command=canvas.yview)
scrollable = tk.Frame(canvas, bg=COR_FUNDO)

scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable, anchor="nw", width=480)

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0), pady=10)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,10), pady=10)

def _mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
canvas.bind_all("<MouseWheel>", _mousewheel)

# ========== CABEÇALHO ==========
header = tk.Frame(scrollable, bg=COR_PRIMARIA, highlightthickness=0)
header.pack(fill=tk.X, pady=(0, 20))

# Gradiente
h_canvas = tk.Canvas(header, height=130, bg=COR_PRIMARIA, highlightthickness=0)
h_canvas.pack(fill=tk.X)
criar_gradiente(h_canvas, 0, 0, 500, 130,
                COR_PRIMARIA_GRADIENTE_TOP, COR_PRIMARIA_GRADIENTE_BOTTOM)

# Texto do cabeçalho usando Label posicionado sobre o canvas
tk.Label(header, text="Calculadora de IMC", font=FONTE_TITULO,
         bg=COR_PRIMARIA, fg="white").place(relx=0.5, rely=0.35, anchor="center")
tk.Label(header, text="\u00cdndice de Massa Corporal", font=FONTE_SUBTITULO,
         bg=COR_PRIMARIA, fg="#D6E4FF").place(relx=0.5, rely=0.55, anchor="center")

# ========== FUNÇÃO AUXILIAR PARA CRIAR CARDS ==========
def criar_card_layout(parent):
    """Cria um frame card com padding."""
    card = Card(parent)
    card.pack(fill=tk.X, padx=15, pady=(0, 12))
    inner = tk.Frame(card, bg=COR_CARD)
    inner.pack(fill=tk.X, padx=15, pady=12)
    return inner

# ========== PRÉVIA DO IMC ==========
inner_preview = criar_card_layout(scrollable)

# Topo: ícone + valor + classificação
preview_topo = tk.Frame(inner_preview, bg=COR_CARD)
preview_topo.pack(fill=tk.X)

preview_icone_label = tk.Label(preview_topo, text="?",
                              font=FONTE_VALOR_GRANDE,
                              bg=COR_CARD, fg=COR_TEXTO_SEC)
preview_icone_label.pack(side=tk.LEFT, padx=(0, 15))

preview_centro = tk.Frame(preview_topo, bg=COR_CARD)
preview_centro.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tk.Label(preview_centro, text="SEU IMC", font=FONTE_PEQUENA,
         bg=COR_CARD, fg=COR_TEXTO_SEC).pack(anchor=tk.W)

preview_imc_var = tk.StringVar(value="--")
preview_imc_label = tk.Label(preview_centro, textvariable=preview_imc_var,
                            font=FONTE_VALOR_GRANDE, bg=COR_CARD, fg=COR_PRIMARIA)
preview_imc_label.pack(anchor=tk.W)

# Classificação à direita
preview_dir = tk.Frame(preview_topo, bg=COR_CARD)
preview_dir.pack(side=tk.RIGHT)

tk.Label(preview_dir, text="CLASSIFICA\u00c7\u00c3O", font=FONTE_PEQUENA,
         bg=COR_CARD, fg=COR_TEXTO_SEC).pack(anchor=tk.E)

preview_class_var = tk.StringVar(value="---")
preview_class_label = tk.Label(preview_dir, textvariable=preview_class_var,
                              font=FONTE_CLASSIFICACAO, bg=COR_CARD, fg=COR_TEXTO_SEC)
preview_class_label.pack(anchor=tk.E)

# Descrição
preview_desc_var = tk.StringVar(value="Preencha altura e peso")
tk.Label(inner_preview, textvariable=preview_desc_var, font=FONTE_PEQUENA,
         bg=COR_CARD, fg=COR_TEXTO_SEC).pack(anchor=tk.W, pady=(8, 0))

# Barra de progresso
progresso_frame = tk.Frame(inner_preview, bg=COR_CARD)
progresso_frame.pack(fill=tk.X, pady=(12, 0))

progresso_bg = tk.Frame(progresso_frame, bg=COR_SLIDER_BG, height=6, highlightthickness=0)
progresso_bg.pack(fill=tk.X)

progresso_barra = tk.Frame(progresso_bg, bg=COR_SLIDER_BG, height=6, highlightthickness=0)
progresso_barra.pack(fill=tk.X)

progresso_max_width = 440
progresso_preenchimento = tk.Frame(progresso_barra, bg=COR_SLIDER_BG, width=0, height=6, highlightthickness=0)
progresso_preenchimento.place(x=0, y=0)

# ========== NOME ==========
inner_nome = criar_card_layout(scrollable)
tk.Label(inner_nome, text="Nome completo", font=FONTE_LABEL, bg=COR_CARD,
         fg=COR_TEXTO).pack(anchor=tk.W)
entrada_nome = ValidatedEntry(inner_nome, placeholder="Ex: Jo\u00e3o Silva",
                             validator=validar_nome, max_chars=50)
entrada_nome.pack(fill=tk.X, pady=(6, 0))

# ========== IDADE E ANO ==========
inner_idade_ano = criar_card_layout(scrollable)
grid = tk.Frame(inner_idade_ano, bg=COR_CARD)
grid.pack(fill=tk.X)
grid.columnconfigure(0, weight=1)
grid.columnconfigure(1, weight=1)

tk.Label(grid, text="Idade", font=FONTE_LABEL, bg=COR_CARD,
         fg=COR_TEXTO).grid(row=0, column=0, sticky="w")
seletor_idade = SelectorButton(grid, list(range(1, 111)), default=25)
seletor_idade.grid(row=1, column=0, sticky="ew", padx=(0,5), pady=(5,0))

tk.Label(grid, text="Ano", font=FONTE_LABEL, bg=COR_CARD,
         fg=COR_TEXTO).grid(row=0, column=1, sticky="w", padx=(5,0))
ano_atual = datetime.now().year
seletor_ano = SelectorButton(grid, list(range(ano_atual-100, ano_atual+1)), default=ano_atual)
seletor_ano.grid(row=1, column=1, sticky="ew", padx=(5,0), pady=(5,0))

# ========== ALTURA ==========
inner_alt = criar_card_layout(scrollable)
tk.Label(inner_alt, text="Altura (m)", font=FONTE_LABEL, bg=COR_CARD,
         fg=COR_TEXTO).pack(anchor=tk.W)

frame_slider_alt = tk.Frame(inner_alt, bg=COR_CARD)
frame_slider_alt.pack(fill=tk.X, pady=(5,0))

altura_var = tk.StringVar(value="1.70")
scale_altura = tk.Scale(frame_slider_alt, from_=0.5, to=2.5, resolution=0.01,
                       orient=tk.HORIZONTAL, length=300, bg=COR_CARD,
                       fg=COR_PRIMARIA, highlightthickness=0, bd=0,
                       troughcolor=COR_SLIDER_TRACK,
                       activebackground=COR_PRIMARIA,
                       command=lambda v: altura_var.set(f"{float(v):.2f}"))
scale_altura.set(1.70)
scale_altura.pack(side=tk.LEFT, fill=tk.X, expand=True)

entry_altura = tk.Entry(frame_slider_alt, width=7, font=FONTE_INPUT,
                       textvariable=altura_var, justify="center",
                       bg=COR_INPUT_BG, fg=COR_PRIMARIA,
                       relief=tk.FLAT, bd=0, highlightthickness=1,
                       highlightbackground=COR_BORDA,
                       validate="key",
                       validatecommand=(janela.register(validar_decimal), '%P'))
entry_altura.pack(side=tk.LEFT, padx=(10,0), ipady=8)

def sync_altura_scale(*args):
    try:
        v = float(altura_var.get().replace(",","."))
        if 0.5 <= v <= 2.5:
            scale_altura.set(v)
            atualizar_preview()
    except ValueError:
        pass
altura_var.trace_add("write", sync_altura_scale)
scale_altura.configure(command=lambda v: [altura_var.set(f"{float(v):.2f}"), atualizar_preview()])

# ========== PESO ==========
inner_pes = criar_card_layout(scrollable)
tk.Label(inner_pes, text="Peso (kg)", font=FONTE_LABEL, bg=COR_CARD,
         fg=COR_TEXTO).pack(anchor=tk.W)

frame_slider_pes = tk.Frame(inner_pes, bg=COR_CARD)
frame_slider_pes.pack(fill=tk.X, pady=(5,0))

peso_var = tk.StringVar(value="70.0")
scale_peso = tk.Scale(frame_slider_pes, from_=30, to=200, resolution=0.1,
                     orient=tk.HORIZONTAL, length=300, bg=COR_CARD,
                     fg=COR_PRIMARIA, highlightthickness=0, bd=0,
                     troughcolor=COR_SLIDER_TRACK,
                     activebackground=COR_PRIMARIA,
                     command=lambda v: peso_var.set(f"{float(v):.1f}"))
scale_peso.set(70.0)
scale_peso.pack(side=tk.LEFT, fill=tk.X, expand=True)

entry_peso = tk.Entry(frame_slider_pes, width=7, font=FONTE_INPUT,
                     textvariable=peso_var, justify="center",
                     bg=COR_INPUT_BG, fg=COR_PRIMARIA,
                     relief=tk.FLAT, bd=0, highlightthickness=1,
                     highlightbackground=COR_BORDA,
                     validate="key",
                     validatecommand=(janela.register(validar_decimal), '%P'))
entry_peso.pack(side=tk.LEFT, padx=(10,0), ipady=8)

def sync_peso_scale(*args):
    try:
        v = float(peso_var.get().replace(",","."))
        if 30 <= v <= 200:
            scale_peso.set(v)
            atualizar_preview()
    except ValueError:
        pass
peso_var.trace_add("write", sync_peso_scale)
scale_peso.configure(command=lambda v: [peso_var.set(f"{float(v):.1f}"), atualizar_preview()])

# ========== CLASSIFICAÇÃO ==========
inner_class = criar_card_layout(scrollable)
tk.Label(inner_class, text="Classifica\u00e7\u00e3o do IMC", font=FONTE_LABEL,
         bg=COR_CARD, fg=COR_TEXTO).pack(anchor=tk.W, pady=(0,8))

categorias = [
    ("Abaixo do peso", "< 18,5", COR_ATENCAO),
    ("Peso normal", "18,5 - 24,9", COR_SUCESSO),
    ("Sobrepeso", "25 - 29,9", COR_ATENCAO),
    ("Obesidade", "\u2265 30", COR_ERRO),
]

categoria_frames = []
categoria_widgets = []

for cat, faixa, cor in categorias:
    row = tk.Frame(inner_class, bg=COR_CARD)
    row.pack(fill=tk.X, pady=2, ipady=5)

    indicador = tk.Frame(row, bg=cor, width=4, height=20, highlightthickness=0)
    indicador.pack(side=tk.LEFT, padx=(12,8))

    lbl_cat = tk.Label(row, text=cat, font=FONTE_INPUT, bg=COR_CARD, fg=COR_TEXTO)
    lbl_cat.pack(side=tk.LEFT)

    lbl_faixa = tk.Label(row, text=faixa, font=FONTE_INPUT, bg=COR_CARD, fg=COR_TEXTO_SEC)
    lbl_faixa.pack(side=tk.RIGHT, padx=(0,12))

    categoria_frames.append(row)
    categoria_widgets.append((lbl_cat, lbl_faixa, indicador))

# ========== BOTÃO ==========
btn_outer = tk.Frame(scrollable, bg=COR_FUNDO)
btn_outer.pack(pady=(5, 18), fill=tk.X, padx=15)

def calcular_click():
    calcular()

btn_calc = tk.Button(btn_outer, text="Calcular IMC", command=calcular_click,
                    font=FONTE_BOTAO, bg=COR_PRIMARIA, fg="white",
                    relief=tk.FLAT, bd=0, cursor="hand2",
                    activebackground=COR_PRIMARIA_HOVER,
                    activeforeground="white",
                    highlightthickness=0,
                    padx=20, pady=14)
btn_calc.pack(fill=tk.X)

# Efeitos hover
def btn_enter(e):
    btn_calc.configure(bg=COR_PRIMARIA_HOVER)
def btn_leave(e):
    btn_calc.configure(bg=COR_PRIMARIA)
btn_calc.bind("<Enter>", btn_enter)
btn_calc.bind("<Leave>", btn_leave)

# ========== RODAPÉ ==========
tk.Frame(scrollable, bg=COR_BORDA, height=1).pack(fill=tk.X, padx=40, pady=(5,8))
tk.Label(scrollable, text="\u00a9 2026 Felipe Orlandin", font=FONTE_PEQUENA,
         bg=COR_FUNDO, fg=COR_TEXTO_SEC).pack(pady=(0,12))

# Inicializar
atualizar_preview()

janela.mainloop()