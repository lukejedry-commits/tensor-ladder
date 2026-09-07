"""
Linear maps and their duals (Step 2).

If A : V → W is linear, the dual (transpose / adjoint on dual spaces) is

    A* : W* → V* ,   (A* η)(v) = η(A v).

In dual bases induced by chosen bases of V and W, the matrix of A* is the
transpose of the matrix of A.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .basis import Basis
from .covector import Covector
from .vector import Vector


def _basis_agree(a: Basis, b: Basis) -> bool:
    return a is b or np.allclose(a.vectors, b.vectors)


@dataclass(frozen=True)
class LinearMap:
    """
    A linear map A : V → W given by its matrix in chosen bases.

    Convention
    ----------
    Components of vectors are columns.  If ``matrix`` is M, then

        (A v)^α = M^α_i v^i    i.e.   Av_components = M @ v_components.

    Columns of M are the components (in the codomain basis) of A(e_i).

    Parameters
    ----------
    matrix :
        Shape ``(dim W, dim V)``.
    domain_basis :
        Basis of V.
    codomain_basis :
        Basis of W.
    """

    matrix: NDArray[np.floating]
    domain_basis: Basis
    codomain_basis: Basis

    def __post_init__(self) -> None:
        M = np.asarray(self.matrix, dtype=float)
        n_out, n_in = self.codomain_basis.dim, self.domain_basis.dim
        if M.shape != (n_out, n_in):
            raise ValueError(
                f"Matrix shape must be (codim, dim) = ({n_out}, {n_in}); got {M.shape}."
            )
        object.__setattr__(self, "matrix", M)

    @property
    def domain_dim(self) -> int:
        return self.domain_basis.dim

    @property
    def codomain_dim(self) -> int:
        return self.codomain_basis.dim

    @classmethod
    def from_matrix(
        cls,
        matrix: ArrayLike,
        domain_basis: Basis | None = None,
        codomain_basis: Basis | None = None,
    ) -> LinearMap:
        """
        Build a linear map from a matrix.

        If bases are omitted, standard bases of matching sizes are used.
        For a square matrix with no bases, one shared standard basis is used
        for domain and codomain.
        """
        M = np.asarray(matrix, dtype=float)
        if M.ndim != 2:
            raise ValueError("matrix must be 2-D.")
        n_out, n_in = M.shape
        if domain_basis is None:
            domain_basis = Basis.standard(n_in, name="e_V")
        if codomain_basis is None:
            if n_in == n_out and domain_basis.dim == n_in:
                # Prefer a single shared basis for endomorphisms when possible
                codomain_basis = domain_basis
            else:
                codomain_basis = Basis.standard(n_out, name="e_W")
        return cls(M, domain_basis, codomain_basis)

    def __call__(self, v: Vector) -> Vector:
        """Apply A to a vector of V."""
        if v.dim != self.domain_dim:
            raise ValueError("Dimension mismatch.")
        if not _basis_agree(v.basis, self.domain_basis):
            raise ValueError("Vector must be expressed in the domain basis.")
        return Vector(self.matrix @ v.components, self.codomain_basis)

    def dual(self) -> LinearMap:
        """
        Return the dual map A* : W* → V*.

        We represent A* by its matrix in the dual bases: that matrix is
        ``M.T`` (shape ``(dim V, dim W)``).  Applying A* to a covector on W
        uses :meth:`apply_dual` (covectors are not identical to vectors).
        The returned :class:`LinearMap` uses the *primal* bases as labels for
        the dual spaces' reference frames (teaching convention: same named
        bases, dual components).
        """
        # A*: W* → V*.  Domain of A* ↔ W, codomain of A* ↔ V.
        return LinearMap(
            matrix=self.matrix.T,
            domain_basis=self.codomain_basis,
            codomain_basis=self.domain_basis,
        )

    def apply_dual(self, eta: Covector) -> Covector:
        """
        Apply A* to η ∈ W*:  (A* η)(v) = η(A v).

        Components: (A* η)_i = (M^T η)_i.
        """
        if eta.dim != self.codomain_dim:
            raise ValueError("Covector must live on the codomain space W.")
        if not _basis_agree(eta.basis, self.codomain_basis):
            raise ValueError("Covector must be expressed in the codomain basis.")
        return Covector(self.matrix.T @ eta.components, self.domain_basis)

    def dual_matrix(self) -> NDArray[np.floating]:
        """Matrix of A* in dual bases — equal to ``matrix.T``."""
        return self.matrix.T.copy()

    def __repr__(self) -> str:
        return (
            f"LinearMap({self.domain_basis.name!r}→{self.codomain_basis.name!r}, "
            f"shape={self.matrix.shape})"
        )
