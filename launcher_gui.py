import tkinter as tk
from tkinter import messagebox
from imc_core import calcular_imc

def calcular():
    try:
        nome = entry_nome.get()
        idade = int(entry_idade.get())
        altura = float(entry_altura.get().replace(",", "."))
        peso = float(entry_peso.get().replace(",", "."))
        ano = int(entry_ano.get())
        resultado = calcular_imc(nome, idade, altura, peso, ano)
        messagebox.showinfo("Resultado do IMC", resultado)
    except ValueError:
        messagebox.showerror("Erro", "Preencha todos os campos com números válidos.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Teste se o Tkinter funciona
try:
    janela = tk.Tk()
except Exception as e:
    print("Erro ao criar janela Tkinter:", e)
    exit(1)

janela.title("Calculadora de IMC")
janela.geometry("400x300")

tk.Label(janela, text="Nome:").pack(pady=2)
entry_nome = tk.Entry(janela)
entry_nome.pack(pady=2)

tk.Label(janela, text="Idade:").pack(pady=2)
entry_idade = tk.Entry(janela)
entry_idade.pack(pady=2)

tk.Label(janela, text="Altura (m):").pack(pady=2)
entry_altura = tk.Entry(janela)
entry_altura.pack(pady=2)

tk.Label(janela, text="Peso (kg):").pack(pady=2)
entry_peso = tk.Entry(janela)
entry_peso.pack(pady=2)

tk.Label(janela, text="Ano atual:").pack(pady=2)
entry_ano = tk.Entry(janela)
entry_ano.pack(pady=2)

btn_calcular = tk.Button(janela, text="Calcular IMC", command=calcular)
btn_calcular.pack(pady=20)

print(">>> Iniciando interface gráfica...")
janela.mainloop()