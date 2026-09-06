"""
Tensors and bilinear forms.

A (p, q)-tensor is a multilinear map

    T : (V*)^p × V^q → ℝ

or equivalently an element of V^{⊗p} ⊗ (V*)^{⊗q}.

Step 1 focuses on:
- rank (0,0) → Scalar
- rank (1,0) → Vector
- rank (0,1) → Covector
- rank (0,2) → BilinearForm (motivates the metric)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .basis import Basis, ChangeOfBasis
from .covector import Covector
from .scalar import Scalar
from .vector import Vector


@dataclass(frozen=True)
class Tensor:
    """
    A general (p, q)-tensor stored as a NumPy array of components.

    Index convention for the array axes
    -----------------------------------
    The first ``p`` axes are *contravariant* (upper indices);
    the remaining ``q`` axes are *covariant* (lower indices).

    Example: a (1,1) tensor has components ``T^i_j`` with array shape
    ``(n, n)``; axis 0 ↔ i, axis 1 ↔ j.

    Parameters
    ----------
    components :
        ndarray of shape ``(n,) * (p + q)``.
    p, q :
        Numbers of upper / lower indices.
    basis :
        Basis for V in which components are expressed.
    """

    components: NDArray[np.floating]
    p: int
    q: int
    basis: Basis

    def __post_init__(self) -> None:
        if self.p < 0 or self.q < 0:
            raise ValueError("p and q must be non-negative.")
        c = np.asarray(self.components, dtype=float)
        expected_ndim = self.p + self.q
        if expected_ndim == 0:
            c = np.asarray(c, dtype=float).reshape(())
        elif c.ndim != expected_ndim:
            raise ValueError(
                f"Expected ndim={expected_ndim} for type ({self.p},{self.q}); got {c.ndim}."
            )
        n = self.basis.dim
        if expected_ndim > 0 and any(s != n for s in c.shape):
            raise ValueError(
                f"Each axis must have length dim={n}; got shape {c.shape}."
            )
        object.__setattr__(self, "components", c)

    @property
    def dim(self) -> int:
        return self.basis.dim

    @property
    def rank(self) -> tuple[int, int]:
        return (self.p, self.q)

    def __repr__(self) -> str:
        return (
            f"Tensor(type=({self.p},{self.q}), shape={self.components.shape}, "
            f"basis={self.basis.name!r})"
        )


@dataclass(frozen=True)
class BilinearForm:
    """
    A bilinear form — a (0, 2)-tensor: B : V × V → ℝ.

    Components ``B_{ij}`` satisfy ``B(u, v) = B_{ij} u^i v^j``.

    Motivation for the metric
    -------------------------
    A *metric* is a symmetric, non-degenerate bilinear form g_{μν}.
    It lets you:

    1. Measure lengths: ‖v‖² = g(v, v)
    2. Raise/lower indices: v_i = g_{ij} v^j  (turn vectors into covectors)
    3. Define angles, orthogonality, and (later) the Levi-Civita connection

    In Step 1 we keep B elementary: any bilinear form, with helpers for
    the symmetric / Euclidean cases.
    """

    components: NDArray[np.floating]
    basis: Basis

    def __post_init__(self) -> None:
        c = np.asarray(self.components, dtype=float)
        n = self.basis.dim
        if c.shape != (n, n):
            raise ValueError(f"Bilinear form needs shape ({n}, {n}); got {c.shape}.")
        object.__setattr__(self, "components", c)

    @property
    def dim(self) -> int:
        return self.basis.dim

    @property
    def rank(self) -> tuple[int, int]:
        return (0, 2)

    @classmethod
    def euclidean(cls, dim: int, basis: Basis | None = None) -> BilinearForm:
        """Standard Euclidean metric δ_{ij} in the given (or standard) basis."""
        if basis is None:
            basis = Basis.standard(dim)
        if basis.dim != dim:
            raise ValueError("basis.dim must equal dim.")
        return cls(np.eye(dim), basis)

    @classmethod
    def from_matrix(
        cls, matrix: ArrayLike, basis: Basis | None = None
    ) -> BilinearForm:
        m = np.asarray(matrix, dtype=float)
        if m.ndim != 2 or m.shape[0] != m.shape[1]:
            raise ValueError("matrix must be square.")
        if basis is None:
            basis = Basis.standard(m.shape[0])
        return cls(m, basis)

    def __call__(self, u: Vector, v: Vector) -> Scalar:
        """Evaluate B(u, v) = B_{ij} u^i v^j."""
        for vec, label in ((u, "u"), (v, "v")):
            if vec.dim != self.dim:
                raise ValueError(f"Dimension mismatch for {label}.")
            if not np.allclose(vec.basis.vectors, self.basis.vectors):
                raise ValueError(f"{label} must be expressed in the form's basis.")
        val = float(u.components @ self.components @ v.components)
        return Scalar(val)

    def is_symmetric(self, tol: float = 1e-10) -> bool:
        return bool(np.allclose(self.components, self.components.T, atol=tol))

    def is_nondegenerate(self, tol: float = 1e-12) -> bool:
        return abs(np.linalg.det(self.components)) > tol

    def flat(self, v: Vector) -> Covector:
        """
        Lower an index: v ↦ v♭ with (v♭)_i = B_{ij} v^j.

        For a metric, this is the musical isomorphism "flat".
        """
        if v.dim != self.dim:
            raise ValueError("Dimension mismatch.")
        if not np.allclose(v.basis.vectors, self.basis.vectors):
            raise ValueError("Vector must be in the form's basis.")
        return Covector(self.components @ v.components, self.basis)

    def in_basis(self, change: ChangeOfBasis) -> BilinearForm:
        """
        Transform (0,2) components: B'_{kl} = P^i_k P^j_l B_{ij},
        i.e. ``B' = P^T B P``.
        """
        if change.dim != self.dim:
            raise ValueError("Dimension mismatch.")
        P = change.P
        new_components = P.T @ self.components @ P
        new_basis = change.new if change.new is not None else Basis.standard(
            self.dim, name="e'"
        )
        return BilinearForm(new_components, new_basis)

    def as_tensor(self) -> Tensor:
        """View as a generic (0, 2) Tensor."""
        return Tensor(self.components, p=0, q=2, basis=self.basis)

    def __repr__(self) -> str:
        return f"BilinearForm(shape={self.components.shape}, basis={self.basis.name!r})"

    def __str__(self) -> str:
        return f"B_{{{self.basis.name}}} =\n{self.components}"
