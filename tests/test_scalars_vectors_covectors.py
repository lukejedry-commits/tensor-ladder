"""Unit tests for Scalar, Vector, Covector, and pairings."""

import numpy as np
import pytest

from tensor_ladder import Basis, Covector, Scalar, Vector


def test_scalar_arithmetic():
    s = Scalar(2.5)
    assert float(s) == 2.5
    assert s.rank == (0, 0)
    assert float(s + Scalar(1.5)) == 4.0
    assert float(s * 2) == 5.0
    assert float(3 * s) == 7.5


def test_vector_basics():
    e = Basis.standard(3, name="e")
    v = Vector.from_iterable([1.0, 2.0, 3.0], e)
    assert v.dim == 3
    assert v.rank == (1, 0)
    assert np.allclose(v.components, [1, 2, 3])
    w = 2 * v
    assert np.allclose(w.components, [2, 4, 6])
    assert np.allclose((v + w).components, [3, 6, 9])


def test_vector_dim_mismatch():
    e = Basis.standard(2)
    with pytest.raises(ValueError):
        Vector.from_iterable([1.0, 2.0, 3.0], e)


def test_covector_pairing():
    e = Basis.standard(2)
    v = Vector.from_iterable([3.0, 4.0], e)
    omega = Covector.from_iterable([1.0, 2.0], e)
    assert omega.rank == (0, 1)
    assert float(omega(v)) == pytest.approx(11.0)
    assert float(v.contract(omega)) == pytest.approx(11.0)


def test_covector_basis_mismatch():
    e = Basis.standard(2, name="e")
    f = Basis(np.eye(2) * 1.0, name="f")  # same vectors numerically — ok
    # Force a genuinely different basis
    g = Basis(np.array([[1.0, 0.0], [1.0, 1.0]]), name="g")
    omega = Covector.from_iterable([1.0, 0.0], e)
    v = Vector.from_iterable([1.0, 0.0], g)
    with pytest.raises(ValueError, match="basis"):
        omega(v)


def test_default_basis_from_iterable():
    v = Vector.from_iterable([1.0, 0.0])
    assert v.basis.dim == 2
    assert np.allclose(v.basis.vectors, np.eye(2))
