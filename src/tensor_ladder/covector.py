"""
Covectors — dual vectors / 1-forms, type (0, 1).

A covector ω is a linear map from vectors to scalars: ω : V → ℝ.
Components transform with P under a change of basis (same way as the
basis).  We write components with *lower* indices: ω_i.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .basis import Basis, ChangeOfBasis
from .scalar import Scalar

if TYPE_CHECKING:
    from .vector import Vector


@dataclass(frozen=True)
class Covector:
    """
    A covector (1-form) given by covariant components in a named basis.

    Parameters
    ----------
    components :
        1-D array ``ω_i``, length ``n``.
    basis :
        The basis of V in which these dual components are expressed
        (i.e. relative to the dual basis ε^i with ε^i(e_j) = δ^i_j).

    Dual basis (proof sketch)
    -------------------------
    Given basis {e_j}, there is a unique dual basis {ε^i} of V* such that
    ε^i(e_j) = δ^i_j.  Any ω ∈ V* expands as ω = ω_i ε^i with
    ω_i = ω(e_i).  Then for v = v^j e_j::

        ω(v) = ω_i ε^i(v^j e_j) = ω_i v^j δ^i_j = ω_i v^i.

    Why "covariant"?
    ----------------
    Covector components transform *with* (co-) the basis change, so that
    the pairing ω(v) stays invariant.
    """

    components: NDArray[np.floating]
    basis: Basis

    def __post_init__(self) -> None:
        c = np.asarray(self.components, dtype=float).reshape(-1)
        if c.ndim != 1:
            raise ValueError("Covector components must be 1-D.")
        if c.shape[0] != self.basis.dim:
            raise ValueError(
                f"Expected {self.basis.dim} components for basis {self.basis.name!r}, "
                f"got {c.shape[0]}."
            )
        object.__setattr__(self, "components", c)

    @property
    def dim(self) -> int:
        return self.basis.dim

    @property
    def rank(self) -> tuple[int, int]:
        """Tensor type (p, q) = (0, 1)."""
        return (0, 1)

    @classmethod
    def from_iterable(
        cls, components: ArrayLike, basis: Basis | None = None
    ) -> Covector:
        c = np.asarray(components, dtype=float).reshape(-1)
        if basis is None:
            basis = Basis.standard(len(c))
        return cls(c, basis)

    def __call__(self, vector: Vector) -> Scalar:
        """Evaluate ω(v) = ω_i v^i."""
        from .vector import Vector as VectorType

        if not isinstance(vector, VectorType):
            raise TypeError("Covector acts on Vector.")
        if self.dim != vector.dim:
            raise ValueError("Dimension mismatch.")
        if not np.allclose(self.basis.vectors, vector.basis.vectors):
            raise ValueError(
                "Covector and Vector must share a basis (or change basis first)."
            )
        return Scalar(float(np.dot(self.components, vector.components)))

    def in_basis(self, change: ChangeOfBasis) -> Covector:
        """
        Return the same geometric covector with components in the *new* basis.

        Uses ``ω' = ω @ P`` (row / dual convention), i.e. ω'_i = ω_j P^j_i.
        """
        from .transforms import transform_covector_components

        if change.dim != self.dim:
            raise ValueError("Dimension mismatch in change of basis.")
        new_components = transform_covector_components(self.components, change)
        new_basis = change.new if change.new is not None else Basis.standard(
            self.dim, name="e'"
        )
        return Covector(new_components, new_basis)

    def __add__(self, other: Covector) -> Covector:
        self._check_same_basis(other)
        return Covector(self.components + other.components, self.basis)

    def __sub__(self, other: Covector) -> Covector:
        self._check_same_basis(other)
        return Covector(self.components - other.components, self.basis)

    def __mul__(self, scalar: float | int | Scalar) -> Covector:
        s = float(scalar)
        return Covector(s * self.components, self.basis)

    def __rmul__(self, scalar: float | int | Scalar) -> Covector:
        return self.__mul__(scalar)

    def __neg__(self) -> Covector:
        return Covector(-self.components, self.basis)

    def _check_same_basis(self, other: Covector) -> None:
        if self.basis is not other.basis and not np.allclose(
            self.basis.vectors, other.basis.vectors
        ):
            raise ValueError(
                "Covector addition requires the same basis. "
                "Change basis first with .in_basis(...)."
            )

    def __repr__(self) -> str:
        return f"Covector({self.components.tolist()}, basis={self.basis.name!r})"

    def __str__(self) -> str:
        comps = ", ".join(f"{x:.6g}" for x in self.components)
        return f"ω_{{{self.basis.name}}} = ({comps})"
