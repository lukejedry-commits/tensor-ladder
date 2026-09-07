"""
tensor_ladder — teachable tensor mathematics (NumPy only).

Step 1 (implemented): scalars, vectors, covectors, bilinear forms,
index notation, and change of basis.

Step 2 (implemented): dual bases, bidual / natural embedding, dual of a
linear map, annihilators, and musical sharp/flat.

Later steps (see CURRICULUM.md): multilinear algebra, manifolds, metrics,
Christoffel symbols, curvature, and the Einstein equation — outlined only.
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
from .dual import (
    DualBasis,
    BidualElement,
    dual_basis,
    reconstruct_vector,
    reconstruct_covector,
    natural_embedding,
    embedding_commutes_with_change_of_basis,
    annihilator,
    annihilator_dim,
)
from .linear_map import LinearMap

__version__ = "0.2.0"

__all__ = [
    "Basis",
    "ChangeOfBasis",
    "Scalar",
    "Vector",
    "Covector",
    "Tensor",
    "BilinearForm",
    "DualBasis",
    "BidualElement",
    "dual_basis",
    "reconstruct_vector",
    "reconstruct_covector",
    "natural_embedding",
    "embedding_commutes_with_change_of_basis",
    "annihilator",
    "annihilator_dim",
    "LinearMap",
    "einstein_contract",
    "free_and_dummy_indices",
    "validate_index_string",
    "transform_vector_components",
    "transform_covector_components",
    "__version__",
]
