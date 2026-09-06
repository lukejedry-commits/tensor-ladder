"""
tensor_ladder — teachable tensor mathematics (NumPy only).

Step 1 (implemented): scalars, vectors, covectors, bilinear forms,
index notation, and change of basis.

Later steps (see CURRICULUM.md): manifolds, metrics, Christoffel symbols,
curvature, and the Einstein equation — outlined only for now.
"""

from .basis import Basis, ChangeOfBasis
from .scalar import Scalar
from .vector import Vector
from .covector import Covector
from .tensor import Tensor, BilinearForm
from .index_notation import (
    einstein_contract,
    free_and_dummy_indices,
    validate_index_string,
)
from .transforms import transform_vector_components, transform_covector_components

__version__ = "0.1.0"

__all__ = [
    "Basis",
    "ChangeOfBasis",
    "Scalar",
    "Vector",
    "Covector",
    "Tensor",
    "BilinearForm",
    "einstein_contract",
    "free_and_dummy_indices",
    "validate_index_string",
    "transform_vector_components",
    "transform_covector_components",
    "__version__",
]
