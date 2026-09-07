"""
Dual spaces (Step 2): dual basis, bidual embedding, annihilators.

Given a finite-dimensional real vector space V with basis {e_i}:

- The dual space V* consists of linear maps ω : V → ℝ (covectors).
- The dual basis {ε^i} ⊂ V* satisfies ε^i(e_j) = δ^i_j.
- Reconstruction: v = ε^i(v) e_i and ω = ω(e_i) ε^i.
- The natural embedding ι : V → V** , ι(v)(ω) = ω(v) is an isomorphism
  in finite dimensions (and natural under change of basis).
- The annihilator of a subspace U ⊆ V is U⁰ = {ω ∈ V* : ω|_U = 0},
  with dim U⁰ = dim V − dim U.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from numpy.typing import NDArray

from .basis import Basis, ChangeOfBasis
from .covector import Covector
from .scalar import Scalar
from .vector import Vector


def _basis_agree(a: Basis, b: Basis) -> bool:
    return a is b or np.allclose(a.vectors, b.vectors)


@dataclass(frozen=True)
class DualBasis:
    """
    The dual basis {ε^i} of V* associated with a primal basis {e_i}.

    By definition ε^i(e_j) = δ^i_j.  In components relative to that same
    primal basis, ε^i is the covector whose components are the i-th
    standard basis row (the Kronecker delta row).

    Parameters
    ----------
    primal :
        The basis {e_i} of V.
    """

    primal: Basis

    @property
    def dim(self) -> int:
        return self.primal.dim

    def covector(self, i: int) -> Covector:
        """Return the dual basis covector ε^i (0-based index)."""
        if not 0 <= i < self.dim:
            raise IndexError(f"Dual basis index {i} out of range for dim {self.dim}.")
        comps = np.zeros(self.dim, dtype=float)
        comps[i] = 1.0
        return Covector(comps, self.primal)

    def as_covectors(self) -> tuple[Covector, ...]:
        """Return (ε^0, …, ε^{n-1}) — 0-based Python indexing for e_1…e_n."""
        return tuple(self.covector(i) for i in range(self.dim))

    def pairing_matrix(self) -> NDArray[np.floating]:
        """
        Matrix M^i_j = ε^i(e_j).  Must equal the identity (teaching check).
        """
        n = self.dim
        # Ambient components of basis vectors are rows of primal.vectors.
        # In the primal basis itself, e_j has components δ^k_j, so
        # ε^i(e_j) = δ^i_j always — compute explicitly for pedagogy.
        M = np.zeros((n, n), dtype=float)
        eye = np.eye(n)
        for i in range(n):
            eps_i = self.covector(i)
            for j in range(n):
                e_j = Vector(eye[j], self.primal)
                M[i, j] = float(eps_i(e_j))
        return M

    def __repr__(self) -> str:
        return f"DualBasis(primal={self.primal.name!r}, dim={self.dim})"


def dual_basis(basis: Basis) -> DualBasis:
    """Construct the dual basis of ``basis``."""
    return DualBasis(primal=basis)


def reconstruct_vector(v: Vector) -> Vector:
    """
    Reconstruct ``v`` via the dual basis: v = ε^i(v) e_i.

    Returns a new :class:`Vector` equal to ``v`` (same basis / components).
    """
    db = DualBasis(v.basis)
    n = v.dim
    comps = np.array([float(db.covector(i)(v)) for i in range(n)], dtype=float)
    return Vector(comps, v.basis)


def reconstruct_covector(omega: Covector) -> Covector:
    """
    Reconstruct ``ω`` via ω = ω(e_i) ε^i.

    Here ω(e_i) is exactly the i-th covariant component.
    """
    n = omega.dim
    eye = np.eye(n)
    coeffs = np.array(
        [float(omega(Vector(eye[i], omega.basis))) for i in range(n)],
        dtype=float,
    )
    # ω = coeffs_i ε^i → components are coeffs
    return Covector(coeffs, omega.basis)


@dataclass(frozen=True)
class BidualElement:
    """
    An element of the bidual V** obtained from the natural embedding ι.

    Conceptually ι(v) ∈ V** is the linear functional on V* given by
    η ↦ η(v).  We store the preimage vector ``v`` and evaluate accordingly.
    """

    vector: Vector

    @property
    def dim(self) -> int:
        return self.vector.dim

    @property
    def basis(self) -> Basis:
        return self.vector.basis

    def __call__(self, omega: Covector) -> Scalar:
        """ι(v)(ω) = ω(v)."""
        if not _basis_agree(self.vector.basis, omega.basis):
            raise ValueError(
                "Bidual evaluation requires covector in the same basis as the vector."
            )
        return omega(self.vector)

    def __repr__(self) -> str:
        return f"BidualElement(ι({self.vector!r}))"


def natural_embedding(v: Vector) -> BidualElement:
    """
    The natural embedding ι : V → V**,  ι(v)(ω) = ω(v).

    In finite dimensions ι is a linear isomorphism.  It is *natural*:
    it does not depend on a choice of basis (see :func:`embedding_commutes_with_change_of_basis`).
    """
    return BidualElement(vector=v)


def embedding_commutes_with_change_of_basis(
    v: Vector, change: ChangeOfBasis, omega: Covector
) -> bool:
    """
    Demonstrate naturality of ι under change of basis.

    Checks that ι(v)(ω) equals ι(v')(ω') where v', ω' are the same
    geometric objects expressed in the new basis.  Returns True iff the
    pairings agree (within floating-point tolerance).
    """
    if change.dim != v.dim:
        raise ValueError("Dimension mismatch.")
    if not _basis_agree(v.basis, omega.basis):
        raise ValueError("v and ω must share a basis before the change.")
    left = float(natural_embedding(v)(omega))
    v_new = v.in_basis(change)
    omega_new = omega.in_basis(change)
    right = float(natural_embedding(v_new)(omega_new))
    return bool(np.isclose(left, right))


def annihilator(
    subspace_vectors: Sequence[Vector],
    ambient_basis: Basis | None = None,
) -> tuple[Covector, ...]:
    """
    Return a basis of the annihilator U⁰ ⊆ V*.

    Parameters
    ----------
    subspace_vectors :
        Vectors spanning U ⊆ V (need not be independent; rank is computed).
    ambient_basis :
        Basis of V.  Defaults to the basis of the first vector.

    Returns
    -------
    tuple of Covector
        A basis of U⁰ = {ω ∈ V* : ω(u) = 0 for all u ∈ U}.
        Length equals ``dim V − rank(U)``.

    Notes
    -----
    If S is the matrix whose *columns* are the spanning vectors' components,
    then ω ∈ U⁰ iff S^T ω = 0, i.e. ω lies in the left nullspace of S
    (nullspace of S^T).
    """
    if not subspace_vectors:
        raise ValueError("Provide at least one spanning vector (or use ambient dim).")
    basis = ambient_basis if ambient_basis is not None else subspace_vectors[0].basis
    for vec in subspace_vectors:
        if vec.dim != basis.dim:
            raise ValueError("All vectors must match ambient dimension.")
        if not _basis_agree(vec.basis, basis):
            raise ValueError("All spanning vectors must be in the ambient basis.")

    # Columns = spanning vectors
    S = np.column_stack([v.components for v in subspace_vectors])
    # Nullspace of S^T via SVD
    # S^T has shape (k, n); nullspace dimension = n - rank(S)
    u, s, vh = np.linalg.svd(S.T, full_matrices=True)
    rank = int(np.sum(s > 1e-10))
    # Right singular vectors corresponding to zero singular values span null(S^T)
    null_basis = vh[rank:].T  # shape (n, n-rank) — columns are null vectors
    n = basis.dim
    codim = n - rank
    if null_basis.size == 0:
        return tuple()
    if null_basis.ndim == 1:
        null_basis = null_basis.reshape(n, 1)
    result = []
    for j in range(codim):
        comps = null_basis[:, j]
        # Normalize sign for stability (optional teaching nicety)
        if comps[np.argmax(np.abs(comps))] < 0:
            comps = -comps
        result.append(Covector(comps, basis))
    return tuple(result)


def annihilator_dim(subspace_dim: int, ambient_dim: int) -> int:
    """
    Dimension formula: dim U⁰ = dim V − dim U.

    Raises if ``subspace_dim`` is out of range.
    """
    if ambient_dim < 1:
        raise ValueError("ambient_dim must be >= 1")
    if not 0 <= subspace_dim <= ambient_dim:
        raise ValueError(
            f"subspace_dim must be in [0, {ambient_dim}]; got {subspace_dim}."
        )
    return ambient_dim - subspace_dim
