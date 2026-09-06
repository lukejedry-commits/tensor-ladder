#!/usr/bin/env python3
"""
Step 1 teaching demo — scalars through change of basis.

Run from the repo root after `pip install -e .`:

    python examples/step01_fundamentals_demo.py
"""

from __future__ import annotations

import numpy as np

from tensor_ladder import (
    Basis,
    BilinearForm,
    ChangeOfBasis,
    Covector,
    Scalar,
    Vector,
    einstein_contract,
    free_and_dummy_indices,
)


def header(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main() -> None:
    header("1. Scalars (0-tensors)")
    s = Scalar(42.0)
    print(f"  {s!r}  →  float = {float(s)}")
    print("  Scalars are basis-independent: no free indices.")

    header("2. Vectors — contravariant components v^i")
    e = Basis.standard(2, name="e")
    v = Vector.from_iterable([3.0, 4.0], e)
    print(f"  Basis: {e}")
    print(f"  {v}")
    print(f"  rank (p,q) = {v.rank}")
    print("  Reminder: v = v^i e_i  (sum on i).")

    header("3. Covectors — dual vectors / 1-forms ω_i")
    omega = Covector.from_iterable([1.0, 2.0], e)
    print(f"  {omega}")
    pairing = omega(v)
    print(f"  ω(v) = ω_i v^i = {pairing}")
    print("  Proof sketch: ω(v) = ω_i ε^i(v^j e_j) = ω_i v^j δ^i_j = ω_i v^i.")

    header("4. Bilinear forms (0,2) — metric motivation")
    g = BilinearForm.euclidean(2, e)
    print(f"  Euclidean metric g_ij = δ_ij")
    print(f"  g(v,v) = ‖v‖² = {g(v, v)}")
    flat = g.flat(v)
    print(f"  Lower index: v♭ = {flat}")
    print(f"  Symmetric? {g.is_symmetric()}  Nondegenerate? {g.is_nondegenerate()}")

    header("5. Index notation — free vs dummy + Einstein sum")
    free, dummy = free_and_dummy_indices("i", "i")
    print(f"  In ω_i v^i :  free={free}, dummy={dummy}")
    val = float(einstein_contract((omega.components, "i"), (v.components, "i")))
    print(f"  einstein_contract → {val}")

    free2, dummy2 = free_and_dummy_indices("ij", "j")
    print(f"  In T_ij v^j : free={free2}, dummy={dummy2}  → result type (0,1)")
    T = np.array([[1.0, 2.0], [3.0, 4.0]])
    contracted = einstein_contract((T, "ij"), (v.components, "j"))
    print(f"  T_ij v^j = {contracted.tolist()}")

    header("6. Change of basis — vectors vs covectors")
    # New basis: e'_1 = 2 e_1, e'_2 = e_2  →  P = diag(2, 1)
    e_new = Basis(np.array([[2.0, 0.0], [0.0, 1.0]]), name="ẽ")
    change = ChangeOfBasis.from_bases(e, e_new)
    print(f"  {change}")
    print(f"  P =\n{change.P}")
    print(f"  P^{{-1}} =\n{change.P_inv}")

    v_new = v.in_basis(change)
    omega_new = omega.in_basis(change)
    print(f"  Vector transforms with P^{{-1}}: {v_new}")
    print(f"  Covector transforms with P:      {omega_new}")

    old_pair = float(omega(v))
    new_pair = float(omega_new(v_new))
    print(f"  Pairing old basis: {old_pair}")
    print(f"  Pairing new basis: {new_pair}")
    print(f"  Invariant? {np.isclose(old_pair, new_pair)}")

    g_new = g.in_basis(change)
    print(f"  Metric in new basis (P^T g P):\n{g_new.components}")
    print(f"  g'(v',v') = {g_new(v_new, v_new)}  (same length² = 25)")

    header("Done — Step 1 complete")
    print("  Next: see CURRICULUM.md for manifolds → curvature → Einstein.")
    print()


if __name__ == "__main__":
    main()
