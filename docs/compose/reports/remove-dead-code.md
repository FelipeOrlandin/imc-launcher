---
feature: remove-dead-code
status: delivered
specs: []
plans:
  - docs/compose/plans/2026-06-22-remove-dead-code.md
branch: main
commits: ee0aaf2..ecba50a
---

# Remove Dead Code — Final Report

## What Was Built

Remocao de codigo morto do projeto Calculadora IMC. Foram identificados e removidos 10 itens de codigo nao utilizado: 3 constantes FAIXA duplicadas, 6 constantes de validacao duplicadas, e 1 import nao utilizado. Nenhuma funcionalidade foi alterada - apenas limpeza de codigo.

## Architecture

**Arquivos modificados:**
- `src/core/validators.py` — Removidas constantes `FAIXA_ALTURA`, `FAIXA_PESO`, `FAIXA_IDADE`
- `src/gui/tema.py` — Removida secao inteira `VALIDACAO` (6 constantes duplicadas)
- `src/gui/widgets/selector.py` — Removido import `COR_TEXTO_SEC`

**Constantes removidas de `validators.py`:**
```python
# Estas constantes nao eram usadas em nenhum lugar:
FAIXA_ALTURA = (0.5, 2.5)
FAIXA_PESO = (20, 300)
FAIXA_IDADE = (1, 150)
```

**Constantes removidas de `tema.py`:**
```python
# Estas duplicavam as constantes de validators.py:
ALTURA_MIN = 0.5
ALTURA_MAX = 2.5
PESO_MIN = 20
PESO_MAX = 300
IDADE_MIN = 1
IDADE_MAX = 150
```

**Import removido de `selector.py`:**
```python
# COR_TEXTO_SEC era importado mas nunca usado
from gui.tema import (
    COR_CARD, COR_BORDA, COR_TEXTO,  # COR_TEXTO_SEC removido
    ...
)
```

## Usage

Nenhuma mudanca de uso. O projeto continua funcionando exatamente como antes. As constantes removidas nao eram usadas por nenhum modulo.

## Verification

- **Testes:** 34/34 passando apos cada alteracao
- **Verificacao manual:** `grep` confirmou que nenhum dos simbolos removidos aparece no codigo
- **Commits:** 4 commits (3 de limpeza + 1 do plano)

## Journey Log

- [lesson] Constantes duplicadas entre `validators.py` e `tema.py` - fonte unica da verdade em `validators.py`
- [lesson] Imports nao detectados por testes - necessario verificacao manual com grep
