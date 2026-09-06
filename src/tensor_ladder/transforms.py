"""
Change-of-basis formulas for vector and covector components.

Summary
-------
With e'_j = e_i P^i_j:

* Vector (contravariant):   v'^i = (P^{-1})^i_j v^j
* Covector (covariant):     ω'_i = ω_j P^j_i

Mnemonic: *components of vectors transform with P^{-1}; components of
covectors transform with P* — so that ω_i v^i is invariant.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from .basis import ChangeOfBasis


def transform_vector_components(
    components: NDArray[np.floating], change: ChangeOfBasis
) -> NDArray[np.floating]:
    """
    v' = P^{-1} v  (treating components as a column).

    Parameters
    ----------
    components :
        Old contravariant components v^j.
    change :
        The change-of-basis specifying P.
    """
    v = np.asarray(components, dtype=float).reshape(-1)
    if v.shape[0] != change.dim:
        raise ValueError(
            f"Expected {change.dim} components; got {v.shape[0]}."
        )
    return change.P_inv @ v


def transform_covector_components(
    components: NDArray[np.floating], change: ChangeOfBasis
) -> NDArray[np.floating]:
    """
    ω' = P^T ω  if ω is a column, equivalently ω'_i = ω_j P^j_i.

    We store covector components as 1-D arrays; the operation is
    ``P.T @ ω`` when ω is a column vector of components.
    """
    w = np.asarray(components, dtype=float).reshape(-1)
    if w.shape[0] != change.dim:
        raise ValueError(
            f"Expected {change.dim} components; got {w.shape[0]}."
        )
    return change.P.T @ w
