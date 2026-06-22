# Guia de Estudo - Refatoracao do Projeto Calculadora IMC

## Objetivo do Estudo

Este documento serve como guia de aprendizado para:
1. **Refatoracao de codigo** - Melhorar a qualidade sem quebrar funcionalidades
2. **Arquitetura de software** - Separar responsabilidades corretamente
3. **Criacao de .exe em Python** - Usando PyInstaller para distribuicao
4. **Preparacao para SDET** - Macros, launchers de testes automatizados

---

## O que Foi Feito

### 1. Estrutura de Pastas Modular

**Antes:** Todos os arquivos na raiz do projeto
```
imc/
├── imc_core.py
├── imc_cli.py
├── launcher_gui.py (714 linhas!)
├── launcher_py.py (codigo morto)
└── test_imc.py
```

**Depois:** Separacao por responsabilidade
```
imc/
├── src/
│   ├── core/
│   │   ├── calculadora.py    # Logica de calculo
│   │   └── modelos.py        # Dataclasses
│   ├── cli/
│   │   └── __init__.py       # Interface CLI
│   ├── gui/
│   │   ├── app.py            # Classe principal
│   │   ├── tema.py           # Cores e constantes
│   │   └── widgets/
│   │       ├── card.py       # Widget Card
│   │       ├── entry.py      # ValidatedEntry
│   │       └── selector.py   # SelectorButton
│   └── main.py               # Entry point
├── tests/
│   └── test_calculadora.py
└── .github/
    └── test.yml
```

**Por que isso importa:**
- Cada modulo tem uma unica responsabilidade (Single Responsibility Principle)
- Facil de encontrar e corrigir bugs
- Componentes reutilizaveis em outros projetos
- Testes mais faceis de escrever e manter

---

### 2. Dataclass para Dados Estruturados

**Antes:** Funcao retornava string formatada
```python
def calcular_imc(nome, idade, altura, peso, ano_atual):
    # ... calculos ...
    return f"Nome: {nome}, IMC: {imc}"
```

**Depois:** Funcao retorna objeto estruturado
```python
@dataclass
class ResultadoIMC:
    nome: str
    idade: int
    imc: float
    categoria: str
    classificacao: str

def calcular_imc(...) -> ResultadoIMC:
    return ResultadoIMC(...)
```

**Por que isso importa para SDET:**
- Possivel acessar dados programaticamente: `resultado.imc`
- Facil de integrar com outros sistemas
- Pode gerar relatorios em diferentes formatos (JSON, CSV, etc.)

---

### 3. Classificacao IMC Padronizada (OMS)

**Antes:** Duas classificacoes diferentes no projeto!
- `imc_core.py`: 3 categorias (errado)
- `launcher_gui.py`: 4 categorias (correto)

**Depois:** Padrao OMS unificado (4 categorias)
```python
if imc < 18.5:
    categoria = "abaixo do peso"
elif imc < 25:
    categoria = "no peso ideal"
elif imc < 30:
    categoria = "com sobrepeso"
else:
    categoria = "com obesidade"
```

**Por que isso importa:**
- Usuarios recebem o mesmo resultado em qualquer interface
- Segue padrao internacional (OMS)
- Elimina gap entre 18.9 e 19.0

---

### 4. Validacao de Entrada no CLI

**Antes:** Conversoes diretas sem validacao
```python
altura = float(sys.argv[3])  # Pode ser negativo!
```

**Depois:** Validacao com limites e mensagens claras
```python
try:
    altura = float(sys.argv[3].replace(",", "."))
except ValueError:
    print("Erro: Altura deve ser um numero.")
    sys.exit(1)

if not (0.5 <= altura <= 2.5):
    print("Erro: Altura deve ser entre 0.5m e 2.5m.")
    sys.exit(1)
```

**Por que isso importa para SDET:**
- Launchers de testes precisam validar inputs
- Mensagens de erro claras facilitam debug
- Codigo defensivo previne crashes

---

### 5. GitHub Actions Corrigido

**Antes:** YAML invalido (faltando dois-pontos)
```yaml
on        # ERRADO - faltando :
  push:
```

**Depois:** YAML valido
```yaml
on:       # CORRETO
  push:
    branches: [ main ]
```

**Por que isso importa:**
- CI/CD e essencial para automacao de testes
- Testes automatizados rodando a cada commit
- Garantia de qualidade antes de entregar

---

### 6. Codigo Morto Removido

**Antes:** `launcher_py.py` com funcao incompleta
```python
def launch_imc_via_cli():
    pass  # Codigo morto
```

**Depois:** Arquivo removido

**Por que isso importa:**
- Codigo morto confunde quem esta aprendendo
- Manutencao mais facil sem lixo no projeto
- Responsavel technical debt

---

## Conceitos Importantes para SDET

### 1. Modularizacao
Separar o codigo em modulos facilita:
- **Reutilizacao**: Usar componentes em outros projetos
- **Manutencao**: Corrigir bugs sem afetar outras partes
- **Testes**: Testar partes isoladas

### 2. Validacao de Entrada
Sempre validar dados em:
- Interfaces de usuario (GUI/CLI)
- Scripts de automacao
- Launchers de testes

### 3. DRY (Don't Repeat Yourself)
- Nunca duplicar logica (como a classificacao IMC)
- Usar funcoes e classes para reutilizar codigo
- Centralizar configuracoes

### 4. Separation of Concerns
- Logica de negocio separada da UI
- Configuracoes separadas do codigo
- Testes separados da implementacao

---

## Como Criar o .exe (PyInstaller)

### Instalacao
```bash
pip install pyinstaller
```

### Criar .exe
```bash
# Modo simples (um arquivo .exe)
pyinstaller --onefile src/main.py

# Escondendo console (apenas para GUI)
pyinstaller --onefile --noconsole src/main.py
```

### Arquivo .spec (Personalizado)
O arquivo `launcher_gui.spec` ja esta configurado para este projeto.

### Estrutura de Saida
```
dist/
└── CalculadoraIMC.exe  # Arquivo executavel final
```

---

## Como Rodar os Testes

```bash
# Descobrir e rodar todos os testes
python -m unittest discover -s tests

# Rodar teste especifico
python -m pytest tests/test_calculadora.py -v
```

---

## Proximos Passos para SDET

1. **Aprender pytest** - Framework de testes mais robusto que unittest
2. **Estudar Page Object Model** - Padrao para testes de UI
3. **Aprender Selenium/Playwright** - Automacao de navegador
4. **Estudar Docker** - Para ambientes de teste isolados
5. **Aprender Jenkins/GitHub Actions** - CI/CD avancado

---

## Recursos Adicionais

- [Documentacao PyInstaller](https://pyinstaller.org/)
- [Tkinter Docs](https://docs.python.org/3/library/tkinter.html)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Pytest](https://docs.pytest.org/)
- [SDET Roadmap](https://roadmap.sh/sdet)

---

**Autor**: Felipe Orlandin  
**Data**: Junho 2026  
**Proposito**: Estudo de refatoracao e criacao de .exe em Python