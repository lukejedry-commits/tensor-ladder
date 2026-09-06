"""
Bases and changes of basis.

Why bases matter
----------------
A vector is a geometric arrow (or more abstractly, an element of a vector
space).  Its *components* are numbers that depend on a chosen basis.
Changing the basis changes the components — but the geometric object stays
the same.  Distinguishing "object" from "components" is the first step
toward tensors.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray


@dataclass(frozen=True)
class Basis:
    """
    An ordered basis for an n-dimensional real vector space.

    Parameters
    ----------
    vectors :
        Shape ``(n, n)``.  Row ``i`` is the components of basis vector
        ``e_i`` in some ambient/reference coordinates.  For a "standard"
        basis, this is the identity matrix.
    name :
        Optional label used in teaching output (e.g. ``"e"``, ``"ẽ"``).

    Notes
    -----
    We store basis vectors as *rows* so that if ``B`` is the matrix whose
    columns are the new basis vectors expressed in the old basis, then
    ``B`` itself is ``vectors.T`` when ``vectors`` uses our row convention
    for a change relative to the standard basis.  See :class:`ChangeOfBasis`.
    """

    vectors: NDArray[np.floating]
    name: str = "e"

    def __post_init__(self) -> None:
        arr = np.asarray(self.vectors, dtype=float)
        if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
            raise ValueError(
                f"Basis must be an (n, n) matrix of basis vectors; got shape {arr.shape}."
            )
        det = np.linalg.det(arr)
        if abs(det) < 1e-12:
            raise ValueError("Basis vectors must be linearly independent (det ≈ 0).")
        object.__setattr__(self, "vectors", arr)

    @property
    def dim(self) -> int:
        """Dimension of the vector space."""
        return self.vectors.shape[0]

    @classmethod
    def standard(cls, dim: int, name: str = "e") -> Basis:
        """Return the standard (orthonormal Cartesian) basis of R^n."""
        if dim < 1:
            raise ValueError("dim must be >= 1")
        return cls(np.eye(dim), name=name)

    def dual_metric_matrix(self) -> NDArray[np.floating]:
        """
        Gram matrix G_{ij} = ⟨e_i, e_j⟩ under the Euclidean inner product
        on ambient coordinates.  Used only as a teaching convenience when
        no separate metric tensor has been introduced yet.
        """
        # rows are basis vectors → G = V V^T
        return self.vectors @ self.vectors.T

    def __repr__(self) -> str:
        return f"Basis(name={self.name!r}, dim={self.dim})"


@dataclass(frozen=True)
class ChangeOfBasis:
    """
    A change of basis from an "old" basis to a "new" basis.

    Convention (physics / GR style)
    -------------------------------
    Let the *new* basis vectors be related to the *old* ones by

        e'_j = e_i  P^i_j

    so the columns of ``P`` are the new basis vectors expressed in the old
    basis.  Then:

    - **Contravariant** (vector) components transform as
      ``v'^i = (P^{-1})^i_j  v^j``  (components "go opposite" to the basis).
    - **Covariant** (covector) components transform as
      ``ω'_i = ω_j  P^j_i``  (same way as the basis).

    Why different?
    --------------
    The pairing ⟨ω, v⟩ must be basis-independent::

        ω'_i v'^i = ω_j P^j_i (P^{-1})^i_k v^k = ω_j δ^j_k v^k = ω_k v^k.

    So covectors must pick up a ``P`` whenever vectors pick up ``P^{-1}``.

    Parameters
    ----------
    P :
        The change-of-basis matrix ``P`` above (shape ``(n, n)``).
    old, new :
        Optional named bases for readable printing.
    """

    P: NDArray[np.floating]
    old: Basis | None = None
    new: Basis | None = None

    def __post_init__(self) -> None:
        P = np.asarray(self.P, dtype=float)
        if P.ndim != 2 or P.shape[0] != P.shape[1]:
            raise ValueError(f"P must be square; got shape {P.shape}.")
        if abs(np.linalg.det(P)) < 1e-12:
            raise ValueError("Change-of-basis matrix P must be invertible.")
        object.__setattr__(self, "P", P)

    @property
    def dim(self) -> int:
        return self.P.shape[0]

    @property
    def P_inv(self) -> NDArray[np.floating]:
        """Inverse of P: used to transform contravariant components."""
        return np.linalg.inv(self.P)

    @classmethod
    def from_bases(cls, old: Basis, new: Basis) -> ChangeOfBasis:
        """
        Build P so that new basis vectors (in ambient coords) equal
        old_ambient @ P, i.e. columns of P are new basis vectors in the
        old basis.

        If ``V_old`` and ``V_new`` have *rows* = basis vectors in ambient
        coordinates, then ``V_new.T = V_old.T @ P``, so
        ``P = V_old.T^{-1} @ V_new.T``.
        """
        if old.dim != new.dim:
            raise ValueError("Bases must have the same dimension.")
        V_old_T = old.vectors.T
        V_new_T = new.vectors.T
        P = np.linalg.solve(V_old_T, V_new_T)
        return cls(P=P, old=old, new=new)

    def __repr__(self) -> str:
        old_n = self.old.name if self.old else "?"
        new_n = self.new.name if self.new else "?"
        return f"ChangeOfBasis({old_n} → {new_n}, dim={self.dim})"
