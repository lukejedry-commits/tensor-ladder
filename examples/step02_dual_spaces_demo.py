#!/usr/bin/env python3
"""
Step 2 teaching demo — dual bases, bidual, dual maps, annihilators, sharp.

Run from the repo root after `pip install -e .`:

    python examples/step02_dual_spaces_demo.py
"""

from __future__ import annotations

import numpy as np

from tensor_ladder import (
    Basis,
    BilinearForm,
    ChangeOfBasis,
    Covector,
    LinearMap,
    Vector,
    annihilator,
    annihilator_dim,
    dual_basis,
    embedding_commutes_with_change_of_basis,
    natural_embedding,
    reconstruct_covector,
    reconstruct_vector,
)


def header(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main() -> None:
    header("1. Dual basis ε^i(e_j) = δ^i_j")
    e = Basis.standard(2, name="e")
    db = dual_basis(e)
    print(f"  {db}")
    print(f"  pairing matrix ε^i(e_j) =\n{db.pairing_matrix()}")

    header("2. Reconstruction v = ε^i(v) e_i  and  ω = ω(e_i) ε^i")
    v = Vector.from_iterable([3.0, 4.0], e)
    omega = Covector.from_iterable([1.0, 2.0], e)
    print(f"  v  = {v}")
    print(f"  reconstructed v = {reconstruct_vector(v)}")
    print(f"  ω  = {omega}")
    print(f"  reconstructed ω = {reconstruct_covector(omega)}")

    header("3. Natural embedding ι : V → V**")
    iota_v = natural_embedding(v)
    print(f"  ι(v)(ω) = {iota_v(omega)}  (same as ω(v) = {omega(v)})")
    e_new = Basis(np.array([[2.0, 0.0], [1.0, 1.0]]), name="e-tilde")
    change = ChangeOfBasis.from_bases(e, e_new)
    ok = embedding_commutes_with_change_of_basis(v, change, omega)
    print(f"  Natural under change of basis? {ok}")

    header("4. Dual of a linear map — matrix is transpose")
    eV = Basis.standard(2, name="eV")
    eW = Basis.standard(3, name="eW")
    M = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    A = LinearMap.from_matrix(M, eV, eW)
    print(f"  {A}")
    print(f"  M =\n{A.matrix}")
    print(f"  matrix of A* = M.T =\n{A.dual_matrix()}")
    eta = Covector.from_iterable([1.0, 0.0, -1.0], eW)
    v2 = Vector.from_iterable([2.0, -1.0], eV)
    left = float(A.apply_dual(eta)(v2))
    right = float(eta(A(v2)))
    print(f"  (A*η)(v) = {left},  η(Av) = {right}, equal? {np.isclose(left, right)}")

    header("5. Annihilator U^0")
    e3 = Basis.standard(3, name="e")
    u = Vector.from_iterable([1.0, 1.0, 0.0], e3)
    ann = annihilator([u], e3)
    print(f"  U = span{{(1,1,0)}}, dim U^0 formula = {annihilator_dim(1, 3)}")
    print(f"  basis of U^0 has {len(ann)} covectors:")
    for w in ann:
        print(f"    {w}  →  ω(u) = {float(w(u)):.2e}")

    header("6. Musical sharp / flat bridge")
    B = BilinearForm.from_matrix([[2.0, 1.0], [1.0, 2.0]], e)
    flat = B.flat(v)
    sharp = B.sharp(flat)
    print(f"  B.flat(v) = {flat}")
    print(f"  B.sharp(flat) = {sharp}")
    print(f"  round-trip OK? {np.allclose(sharp.components, v.components)}")

    header("Done — Step 2 complete")
    print("  Next: CURRICULUM.md Step 3 (multilinear algebra & (p,q) tensors).")
    print()


if __name__ == "__main__":
    main()
