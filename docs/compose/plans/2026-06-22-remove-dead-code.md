# Remove Dead Code Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use compose:subagent (recommended) or compose:execute to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove all dead code (unused constants, duplicate constants, unused imports) from the IMC calculator project.

**Architecture:** Simple cleanup - remove 10 identified dead code items across 3 files. No new features, no behavioral changes.

**Tech Stack:** Python, unittest

---

## File Structure

| File | Action | Items to Remove |
|------|--------|-----------------|
| `src/core/validators.py` | Modify | Remove `FAIXA_ALTURA`, `FAIXA_PESO`, `FAIXA_IDADE` (lines 23-25) |
| `src/gui/tema.py` | Modify | Remove entire VALIDACAO section (lines 45-51) |
| `src/gui/widgets/selector.py` | Modify | Remove `COR_TEXTO_SEC` from import (line 3) |

---

### Task 1: Remove unused constants from validators.py

**Covers:** Dead code cleanup

**Files:**
- Modify: `src/core/validators.py:23-25`

- [ ] **Step 1: Remove unused FAIXA constants**

```python
# Before (lines 23-25):
FAIXA_ALTURA = (0.5, 2.5)
FAIXA_PESO = (20, 300)
FAIXA_IDADE = (1, 150)

# After: Delete these 3 lines entirely
```

- [ ] **Step 2: Run tests to verify no breakage**

Run: `python -m unittest discover -s tests -v`
Expected: All 34 tests pass

- [ ] **Step 3: Commit**

```bash
git add src/core/validators.py
git commit -m "chore: remove unused FAIXA constants from validators"
```

---

### Task 2: Remove duplicate constants from tema.py

**Covers:** Dead code cleanup

**Files:**
- Modify: `src/gui/tema.py:45-51`

- [ ] **Step 1: Remove entire VALIDACAO section**

```python
# Before (lines 45-51):
# ==================== VALIDACAO ====================
ALTURA_MIN = 0.5
ALTURA_MAX = 2.5
PESO_MIN = 20
PESO_MAX = 300
IDADE_MIN = 1
IDADE_MAX = 150

# After: Delete these 7 lines (including comment) entirely
```

- [ ] **Step 2: Run tests to verify no breakage**

Run: `python -m unittest discover -s tests -v`
Expected: All 34 tests pass

- [ ] **Step 3: Commit**

```bash
git add src/gui/tema.py
git commit -m "chore: remove duplicate VALIDACAO constants from tema.py"
```

---

### Task 3: Remove unused import from selector.py

**Covers:** Dead code cleanup

**Files:**
- Modify: `src/gui/widgets/selector.py:3`

- [ ] **Step 1: Remove COR_TEXTO_SEC from import**

```python
# Before (line 3):
from gui.tema import (
    COR_CARD, COR_BORDA, COR_TEXTO, COR_TEXTO_SEC,
    COR_PRIMARIA, COR_PRIMARIA_HOVER, COR_PRIMARIA_LIGHT,
    COR_INPUT_BG, FONTE_INPUT, FONTE_LABEL, FONTE_BOTAO_PEQUENO,
)

# After:
from gui.tema import (
    COR_CARD, COR_BORDA, COR_TEXTO,
    COR_PRIMARIA, COR_PRIMARIA_HOVER, COR_PRIMARIA_LIGHT,
    COR_INPUT_BG, FONTE_INPUT, FONTE_LABEL, FONTE_BOTAO_PEQUENO,
)
```

- [ ] **Step 2: Run tests to verify no breakage**

Run: `python -m unittest discover -s tests -v`
Expected: All 34 tests pass

- [ ] **Step 3: Commit**

```bash
git add src/gui/widgets/selector.py
git commit -m "chore: remove unused COR_TEXTO_SEC import from selector"
```

---

### Task 4: Final verification

**Covers:** Dead code cleanup

**Files:** None (verification only)

- [ ] **Step 1: Run full test suite**

Run: `python -m unittest discover -s tests -v`
Expected: All 34 tests pass

- [ ] **Step 2: Verify dead code removed**

Run: `grep -rn "FAIXA_ALTURA\|FAIXA_PESO\|FAIXA_IDADE" src/`
Expected: No output (constants removed)

Run: `grep -rn "ALTURA_MIN\|ALTURA_MAX\|PESO_MIN\|PESO_MAX\|IDADE_MIN\|IDADE_MAX" src/gui/tema.py`
Expected: No output (constants removed from tema.py)

Run: `grep -rn "COR_TEXTO_SEC" src/gui/widgets/selector.py`
Expected: No output (import removed)

- [ ] **Step 3: Final commit (if needed)**

```bash
git status
# If clean, no commit needed
# If changes, commit with appropriate message
```
