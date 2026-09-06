# tensor-ladder

**Pedagogical tensor mathematics in pure Python (NumPy only)** — from scalars
and bases up the ladder toward Einstein-style geometric structures.

> **Step 1 is implemented.** Later steps are outlined in [`CURRICULUM.md`](CURRICULUM.md).

## Vision

Tensors are often introduced as “arrays that transform a certain way,” which
is true but opaque.  This package teaches them as **multilinear maps on a
vector space and its dual**, with:

- Explicit classes (`Vector`, `Covector`, `BilinearForm`, …) wrapping NumPy
- Change-of-basis that shows *why* vectors and covectors transform differently
- Index notation (free vs dummy indices, Einstein summation) as a language
  for the same ideas
- Markdown lessons with LaTeX, runnable examples, and exercises with solutions

The long-term ladder (manifolds → metrics → connection → curvature → Einstein
equation) is sketched in the curriculum so each step has a clear destination.

## Install

Requires Python ≥ 3.10.

```bash
git clone https://github.com/lukejedry-commits/tensor-ladder.git
cd tensor-ladder
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Quick start

```python
from tensor_ladder import Basis, Vector, Covector, BilinearForm, ChangeOfBasis

e = Basis.standard(2, name="e")
v = Vector.from_iterable([3.0, 4.0], e)
ω = Covector.from_iterable([1.0, 2.0], e)
print(ω(v))  # Scalar(11.0) = ω_i v^i

# Change of basis: stretch the first axis by 2
P = [[2.0, 0.0], [0.0, 1.0]]
e_new = Basis([[2.0, 0.0], [0.0, 1.0]], name="ẽ")
change = ChangeOfBasis.from_bases(e, e_new)
v_new = v.in_basis(change)
ω_new = ω.in_basis(change)
print(ω_new(v_new))  # still 11 — pairing is invariant
```

## How Step 1 fits the ladder

| Topic | Role on the ladder |
|-------|--------------------|
| Scalars (0-tensors) | Invariants; what contractions produce |
| Vectors (1,0) | Contravariant components; transform with \(P^{-1}\) |
| Covectors (0,1) | Linear functionals; transform with \(P\) |
| Bilinear forms (0,2) | Motivate the metric \(g_{\mu\nu}\) |
| Index notation | Bookkeeping for free/dummy indices |
| Change of basis | Why “co-” vs “contra-” exist |

Steps 2+ (manifolds, Christoffel symbols, Riemann/Ricci, Einstein equation)
build on this vocabulary — see `CURRICULUM.md`.

## Layout

```
tensor-ladder/
├── src/tensor_ladder/     # importable package
├── lessons/               # Markdown + LaTeX lessons
├── examples/              # runnable teaching scripts
├── tests/                 # pytest
├── CURRICULUM.md
└── pyproject.toml
```

## Run tests & example

```bash
cd /workspace/tensor-ladder
pytest -q
python examples/step01_touramentals_demo.py
```

## License

MIT
