"""Widget de preview do IMC.

Exibe icone, valor, classificacao e barra de progresso.
Separa a logica de preview do AppIMC principal.
"""

import tkinter as tk
from gui.tema import (
    COR_CARD, COR_TEXTO, COR_TEXTO_SEC, COR_PRIMARIA,
    COR_SUCESSO, COR_ATENCAO, COR_ERRO,
    COR_SLIDER_BG,
    FONTE_PEQUENA, FONTE_VALOR_GRANDE, FONTE_CLASSIFICACAO,
    BARRA_PROGRESSO_MAX,
)


CATEGORIAS = [
    {"nome": "Abaixo do peso", "faixa": "< 18,5", "cor": COR_ATENCAO,
     "icone": "\u26a0", "descricao": "Voce esta abaixo do peso recomendado."},
    {"nome": "Peso normal", "faixa": "18,5 - 24,9", "cor": COR_SUCESSO,
     "icone": "\u2713", "descricao": "Parabens! Seu peso esta ideal."},
    {"nome": "Sobrepeso", "faixa": "25 - 29,9", "cor": COR_ATENCAO,
     "icone": "\u25b2", "descricao": "Atencao: voce esta com sobrepeso."},
    {"nome": "Obesidade", "faixa": "\u2265 30", "cor": COR_ERRO,
     "icone": "\u25cf", "descricao": "Procure um profissional de saude."},
]


def classificar_imc(imc):
    """Retorna indice, cor, icone e descricao para um valor de IMC."""
    if imc < 18.5:
        return 0
    elif imc < 25:
        return 1
    elif imc < 30:
        return 2
    else:
        return 3


class PreviewCard:
    """Card de preview com icone, valor, classificacao e barra de progresso."""

    def __init__(self, parent):
        self.parent = parent
        self.categoria_frames = []
        self.categoria_widgets = []
        self._criar_widgets()

    def _criar_widgets(self):
        topo = tk.Frame(self.parent, bg=COR_CARD)
        topo.pack(fill=tk.X)

        self.icone_label = tk.Label(topo, text="?",
                                    font=FONTE_VALOR_GRANDE,
                                    bg=COR_CARD, fg=COR_TEXTO_SEC)
        self.icone_label.pack(side=tk.LEFT, padx=(0, 15))

        centro = tk.Frame(topo, bg=COR_CARD)
        centro.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(centro, text="SEU IMC", font=FONTE_PEQUENA,
                 bg=COR_CARD, fg=COR_TEXTO_SEC).pack(anchor=tk.W)

        self.imc_var = tk.StringVar(value="--")
        self.imc_label = tk.Label(centro, textvariable=self.imc_var,
                                  font=FONTE_VALOR_GRANDE, bg=COR_CARD, fg=COR_PRIMARIA)
        self.imc_label.pack(anchor=tk.W)

        dir_frame = tk.Frame(topo, bg=COR_CARD)
        dir_frame.pack(side=tk.RIGHT)

        tk.Label(dir_frame, text="CLASSIFICACAO", font=FONTE_PEQUENA,
                 bg=COR_CARD, fg=COR_TEXTO_SEC).pack(anchor=tk.E)

        self.class_var = tk.StringVar(value="---")
        self.class_label = tk.Label(dir_frame, textvariable=self.class_var,
                                    font=FONTE_CLASSIFICACAO, bg=COR_CARD, fg=COR_TEXTO_SEC)
        self.class_label.pack(anchor=tk.E)

        self.desc_var = tk.StringVar(value="Preencha altura e peso")
        tk.Label(self.parent, textvariable=self.desc_var, font=FONTE_PEQUENA,
                 bg=COR_CARD, fg=COR_TEXTO_SEC).pack(anchor=tk.W, pady=(8, 0))

        barra_frame = tk.Frame(self.parent, bg=COR_CARD)
        barra_frame.pack(fill=tk.X, pady=(12, 0))

        barra_bg = tk.Frame(barra_frame, bg=COR_SLIDER_BG, height=6, highlightthickness=0)
        barra_bg.pack(fill=tk.X)

        barra_container = tk.Frame(barra_bg, bg=COR_SLIDER_BG, height=6, highlightthickness=0)
        barra_container.pack(fill=tk.X)

        self.barra_preenchimento = tk.Frame(barra_container, bg=COR_SLIDER_BG, width=0, height=6, highlightthickness=0)
        self.barra_preenchimento.place(x=0, y=0)

    def criar_lista_categorias(self, parent):
        """Cria a lista visual de categorias OMS."""
        for cat in CATEGORIAS:
            row = tk.Frame(parent, bg=COR_CARD)
            row.pack(fill=tk.X, pady=2, ipady=5)

            indicador = tk.Frame(row, bg=cat["cor"], width=4, height=20, highlightthickness=0)
            indicador.pack(side=tk.LEFT, padx=(12, 8))

            lbl_cat = tk.Label(row, text=cat["nome"], font=FONTE_PEQUENA,
                               bg=COR_CARD, fg=COR_TEXTO)
            lbl_cat.pack(side=tk.LEFT)

            lbl_faixa = tk.Label(row, text=cat["faixa"], font=FONTE_PEQUENA,
                                 bg=COR_CARD, fg=COR_TEXTO_SEC)
            lbl_faixa.pack(side=tk.RIGHT, padx=(0, 12))

            self.categoria_frames.append(row)
            self.categoria_widgets.append((lbl_cat, lbl_faixa, indicador))

    def atualizar(self, altura, peso):
        """Atualiza preview com base na altura e peso."""
        try:
            imc = peso / (altura ** 2)
        except (ValueError, ZeroDivisionError):
            self._limpar()
            return

        idx = classificar_imc(imc)
        cat = CATEGORIAS[idx]

        self.imc_var.set(f"{imc:.1f}")
        self.class_var.set(cat["nome"])
        self.imc_label.configure(fg=cat["cor"])
        self.class_label.configure(fg=cat["cor"])
        self.icone_label.configure(text=cat["icone"], fg=cat["cor"])
        self.desc_var.set(cat["descricao"])

        self._destacar(idx)
        self._atualizar_barra(imc)

    def _limpar(self):
        self.imc_var.set("--")
        self.class_var.set("---")
        self.icone_label.configure(text="?", fg=COR_TEXTO_SEC)
        self.desc_var.set("Preencha altura e peso")
        self.imc_label.configure(fg=COR_PRIMARIA)
        self._limpar_destaques()
        self.barra_preenchimento.configure(width=0)

    def _atualizar_barra(self, imc):
        imc_clamped = max(10, min(50, imc))
        frac = (imc_clamped - 10) / 40.0
        width = int(frac * BARRA_PROGRESSO_MAX)
        idx = classificar_imc(imc)
        cor = CATEGORIAS[idx]["cor"]
        self.barra_preenchimento.configure(bg=cor, width=width)

    def _destacar(self, indice):
        for i, frame in enumerate(self.categoria_frames):
            lbl_cat, lbl_faixa, dot = self.categoria_widgets[i]
            if i == indice:
                frame.configure(bg="#E8EDFD")
                lbl_cat.configure(bg="#E8EDFD", fg="#4A6CF7")
                lbl_faixa.configure(bg="#E8EDFD", fg="#4A6CF7")
                dot.configure(bg="#E8EDFD")
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