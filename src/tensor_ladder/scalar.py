"""
Scalars — 0-tensors.

A scalar is a single number that does not change under a change of basis.
In index language it has *no free indices*.  Examples: temperature at a
point, the result of ω(v) for a covector ω and vector v, the trace of a
(1,1) tensor.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike


@dataclass(frozen=True)
class Scalar:
    """
    A 0-tensor: a basis-independent real number.

    Parameters
    ----------
    value :
        The numerical value.

    Teaching note
    -------------
    Under a change of basis, scalar components transform by the empty
    product of P's — i.e. they are invariant.  That is why physical
    observables that are true scalars (proper time along a worldline,
    Ricci scalar, etc.) are "safe" to compare across frames.
    """

    value: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", float(self.value))

    @property
    def rank(self) -> tuple[int, int]:
        """Tensor type (p, q) = (0, 0)."""
        return (0, 0)

    def __float__(self) -> float:
        return self.value

    def __add__(self, other: Scalar | float | int) -> Scalar:
        if isinstance(other, Scalar):
            return Scalar(self.value + other.value)
        return Scalar(self.value + float(other))

    def __radd__(self, other: float | int) -> Scalar:
        return Scalar(float(other) + self.value)

    def __mul__(self, other: Scalar | float | int) -> Scalar:
        if isinstance(other, Scalar):
            return Scalar(self.value * other.value)
        return Scalar(self.value * float(other))

    def __rmul__(self, other: float | int) -> Scalar:
        return Scalar(float(other) * self.value)

    def __repr__(self) -> str:
        return f"Scalar({self.value})"

    def __str__(self) -> str:
        return f"{self.value}"
