"""Tests for BilinearForm and Tensor."""

import numpy as np
import pytest

from tensor_ladder import Basis, BilinearForm, Tensor, Vector


def test_euclidean_metric():
    e = Basis.standard(2)
    g = BilinearForm.euclidean(2, e)
    v = Vector.from_iterable([3.0, 4.0], e)
    assert float(g(v, v)) == pytest.approx(25.0)
    assert g.is_symmetric()
    assert g.is_nondegenerate()
    assert g.rank == (0, 2)


def test_flat_lowers_index():
    e = Basis.standard(2)
    g = BilinearForm.euclidean(2, e)
    v = Vector.from_iterable([3.0, 4.0], e)
    flat = g.flat(v)
    assert np.allclose(flat.components, [3.0, 4.0])
    assert float(flat(v)) == pytest.approx(25.0)


def test_non_euclidean_form():
    e = Basis.standard(2)
    B = BilinearForm.from_matrix([[2.0, 1.0], [1.0, 2.0]], e)
    u = Vector.from_iterable([1.0, 0.0], e)
    v = Vector.from_iterable([0.0, 1.0], e)
    assert float(B(u, v)) == pytest.approx(1.0)
    assert float(B(u, u)) == pytest.approx(2.0)
    flat = B.flat(u)
    assert np.allclose(flat.components, [2.0, 1.0])


def test_tensor_shape_validation():
    e = Basis.standard(2)
    T = Tensor(np.zeros((2, 2)), p=1, q=1, basis=e)
    assert T.rank == (1, 1)
    with pytest.raises(ValueError):
        Tensor(np.zeros((2, 3)), p=1, q=1, basis=e)


def test_as_tensor_roundtrip():
    e = Basis.standard(2)
    g = BilinearForm.euclidean(2, e)
    T = g.as_tensor()
    assert T.p == 0 and T.q == 2
    assert np.allclose(T.components, g.components)
