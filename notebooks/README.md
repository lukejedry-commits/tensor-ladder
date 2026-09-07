# Notebooks

Interactive walkthroughs that **import** `tensor_ladder` (they do not reimplement the math).

| Notebook | Step |
|----------|------|
| `01_fundamentals.ipynb` | Step 1 |
| `02_dual_spaces.ipynb` | Step 2 |

## Codespaces / local Jupyter

1. Open the repo in a GitHub Codespace (or clone locally).
2. Create a venv and install editable extras:

   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -e ".[dev,notebook]"
   ```

   (`dev` already includes the Jupyter stack; `.[notebook]` alone is enough for kernels without pytest.)

3. Register a named kernel:

   ```bash
   python -m ipykernel install --user --name=tensor-ladder --display-name="Python (tensor-ladder)"
   ```

4. Open a notebook → **Kernel → Select Kernel → Python (tensor-ladder)**.

If you use the included Dev Container, the post-create command runs
`pip install -e ".[dev,notebook]"`; you still need step 3 once to register the
kernel display name (or select the Codespace Python environment directly).
