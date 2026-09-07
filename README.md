# tensor-ladder

**Pedagogical tensor mathematics in pure Python (NumPy only)** — from scalars
and bases up the ladder toward Einstein-style geometric structures.

> **Steps 1–2 are implemented.** Later steps are outlined in [`CURRICULUM.md`](CURRICULUM.md).

## Vision

Tensors are often introduced as “arrays that transform a certain way,” which
is true but opaque.  This package teaches them as **multilinear maps on a
vector space and its dual**, with:

- Explicit classes (`Vector`, `Covector`, `BilinearForm`, `LinearMap`, …) wrapping NumPy
- Change-of-basis that shows *why* vectors and covectors transform differently
- Deep dual-space theory (dual bases, bidual, annihilators, dual maps)
- Index notation (free vs dummy indices, Einstein summation) as a language
  for the same ideas
- Markdown lessons with LaTeX, runnable examples, Jupyter notebooks, and
  exercises with solutions

The long-term ladder (multilinear algebra → manifolds → metrics → connection →
curvature → Einstein equation) is sketched in the curriculum so each step has
a clear destination.

## Install

Requires Python ≥ 3.10.

```bash
git clone https://github.com/lukejedry-commits/tensor-ladder.git
cd tensor-ladder
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev,notebook]"
```

- `.[dev]` — pytest **and** the Jupyter stack (handy default for teaching)
- `.[notebook]` — Jupyter / ipykernel / notebook only
- bare `pip install -e .` — NumPy runtime only

## Quick start

```python
from tensor_ladder import Basis, Vector, Covector, BilinearForm, ChangeOfBasis

e = Basis.standard(2, name="e")
v = Vector.from_iterable([3.0, 4.0], e)
ω = Covector.from_iterable([1.0, 2.0], e)
print(ω(v))  # Scalar(11.0) = ω_i v^i

# Change of basis: stretch the first axis by 2
e_new = Basis([[2.0, 0.0], [0.0, 1.0]], name="ẽ")
change = ChangeOfBasis.from_bases(e, e_new)
v_new = v.in_basis(change)
ω_new = ω.in_basis(change)
print(ω_new(v_new))  # still 11 — pairing is invariant
```

### Step 2 peek — dual basis & natural embedding

```python
from tensor_ladder import dual_basis, natural_embedding, LinearMap

db = dual_basis(e)
print(db.pairing_matrix())  # identity

iota_v = natural_embedding(v)
print(iota_v(ω))  # same as ω(v)

A = LinearMap.from_matrix([[2.0, 1.0], [0.0, 3.0]], e, e)
print(A.dual_matrix())  # transpose
```

## How Steps 1–2 fit the ladder

| Topic | Role on the ladder |
|-------|--------------------|
| Scalars (0-tensors) | Invariants; what contractions produce |
| Vectors (1,0) | Contravariant components; transform with $P^{-1}$ |
| Covectors (0,1) | Linear functionals; transform with $P$ |
| Bilinear forms (0,2) | Motivate the metric $g_{\mu\nu}$; ♭ / ♯ |
| Dual bases & bidual | $\varepsilon^i$, $\iota:V\to V^{**}$, annihilators |
| Dual of a linear map | $A^*$; matrix = transpose |
| Index notation | Bookkeeping for free/dummy indices |
| Change of basis | Why “co-” vs “contra-” exist |

Steps 3+ (multilinear algebra, manifolds, Christoffel symbols, Riemann/Ricci,
Einstein equation) build on this vocabulary — see `CURRICULUM.md`.

## Jupyter / Codespaces

1. Open a Codespace (or local clone) and create a venv.
2. `pip install -e ".[dev,notebook]"`
3. Register the kernel:

   ```bash
   python -m ipykernel install --user --name=tensor-ladder --display-name="Python (tensor-ladder)"
   ```

4. Open `notebooks/01_fundamentals.ipynb` or `notebooks/02_dual_spaces.ipynb`
   and select **Python (tensor-ladder)**.

Details: [`notebooks/README.md`](notebooks/README.md).  A minimal Dev Container
(`.devcontainer/devcontainer.json`) runs the editable install on create.

## Layout

```
tensor-ladder/
├── src/tensor_ladder/     # importable package
├── lessons/               # Markdown + LaTeX lessons
├── examples/              # runnable teaching scripts
├── notebooks/             # Jupyter walkthroughs
├── tests/                 # pytest
├── .devcontainer/         # optional Codespaces / VS Code container
├── CURRICULUM.md
└── pyproject.toml
```

## Run tests & examples

```bash
pytest -q
python examples/step01_fundamentals_demo.py
python examples/step02_dual_spaces_demo.py
```

## License

MIT
