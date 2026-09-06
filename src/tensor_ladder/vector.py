"""
Vectors — contravariant 1-tensors, type (1, 0).

Components transform with P^{-1} under a change of basis (see transforms).
We write components with *upper* indices: v^i.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .basis import Basis, ChangeOfBasis
from .scalar import Scalar

if TYPE_CHECKING:
    from .covector import Covector


@dataclass(frozen=True)
class Vector:
    """
    A vector given by contravariant components in a named basis.

    Parameters
    ----------
    components :
        1-D array ``v^i``, length ``n``.
    basis :
        The basis in which ``components`` are expressed.

    Why "contravariant"?
    --------------------
    If the basis stretches by a factor of 2, the *components* of a fixed
    geometric arrow must shrink by 1/2 so that ``v = v^i e_i`` is unchanged.
    Components transform *contrary* to the basis → "contravariant".
    """

    components: NDArray[np.floating]
    basis: Basis

    def __post_init__(self) -> None:
        c = np.asarray(self.components, dtype=float).reshape(-1)
        if c.ndim != 1:
            raise ValueError("Vector components must be 1-D.")
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
        """Tensor type (p, q) = (1, 0)."""
        return (1, 0)

    @classmethod
    def from_iterable(
        cls, components: ArrayLike, basis: Basis | None = None
    ) -> Vector:
        """Build a Vector; default basis is the standard basis of matching size."""
        c = np.asarray(components, dtype=float).reshape(-1)
        if basis is None:
            basis = Basis.standard(len(c))
        return cls(c, basis)

    def in_basis(self, change: ChangeOfBasis) -> Vector:
        """
        Return the same geometric vector with components in the *new* basis.

        Uses ``v' = P^{-1} v`` (column vector convention).
        """
        from .transforms import transform_vector_components

        if change.dim != self.dim:
            raise ValueError("Dimension mismatch in change of basis.")
        new_components = transform_vector_components(self.components, change)
        new_basis = change.new if change.new is not None else Basis.standard(
            self.dim, name="e'"
        )
        return Vector(new_components, new_basis)

    def __add__(self, other: Vector) -> Vector:
        self._check_same_basis(other)
        return Vector(self.components + other.components, self.basis)

    def __sub__(self, other: Vector) -> Vector:
        self._check_same_basis(other)
        return Vector(self.components - other.components, self.basis)

    def __mul__(self, scalar: float | int | Scalar) -> Vector:
        s = float(scalar)
        return Vector(s * self.components, self.basis)

    def __rmul__(self, scalar: float | int | Scalar) -> Vector:
        return self.__mul__(scalar)

    def __neg__(self) -> Vector:
        return Vector(-self.components, self.basis)

    def dot_euclidean(self, other: Vector) -> Scalar:
        """
        Euclidean dot product of components (teaching helper).

        Prefer pairing a :class:`Covector` with a :class:`Vector`, or using
        a metric / bilinear form, once those ideas are in play.
        """
        self._check_same_basis(other)
        return Scalar(float(np.dot(self.components, other.components)))

    def contract(self, covector: Covector) -> Scalar:
        """⟨ω, v⟩ = ω_i v^i  (Einstein summation on i)."""
        return covector(self)

    def _check_same_basis(self, other: Vector) -> None:
        if self.basis is not other.basis and not np.allclose(
            self.basis.vectors, other.basis.vectors
        ):
            raise ValueError(
                "Vector addition requires the same basis. "
                "Change basis first with .in_basis(...)."
            )

    def __repr__(self) -> str:
        return f"Vector({self.components.tolist()}, basis={self.basis.name!r})"

    def __str__(self) -> str:
        comps = ", ".join(f"{x:.6g}" for x in self.components)
        return f"v^{{{self.basis.name}}} = ({comps})"
