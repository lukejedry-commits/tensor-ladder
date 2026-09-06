"""Tests for bases and change-of-basis transforms."""

import numpy as np
import pytest

from tensor_ladder import (
    Basis,
    BilinearForm,
    ChangeOfBasis,
    Covector,
    Vector,
    transform_covector_components,
    transform_vector_components,
)


def test_standard_basis():
    e = Basis.standard(3)
    assert e.dim == 3
    assert np.allclose(e.vectors, np.eye(3))


def test_singular_basis_rejected():
    with pytest.raises(ValueError, match="independent"):
        Basis(np.array([[1.0, 2.0], [2.0, 4.0]]))


def test_change_from_bases_diagonal_stretch():
    old = Basis.standard(2, name="e")
    new = Basis(np.array([[2.0, 0.0], [0.0, 1.0]]), name="ẽ")
    chg = ChangeOfBasis.from_bases(old, new)
    assert np.allclose(chg.P, np.diag([2.0, 1.0]))
    assert np.allclose(chg.P_inv, np.diag([0.5, 1.0]))


def test_vector_transforms_with_P_inv():
    old = Basis.standard(2, name="e")
    new = Basis(np.array([[2.0, 0.0], [0.0, 1.0]]), name="ẽ")
    chg = ChangeOfBasis.from_bases(old, new)
    v = Vector.from_iterable([3.0, 4.0], old)
    v_new = v.in_basis(chg)
    assert np.allclose(v_new.components, [1.5, 4.0])
    # Direct helper agrees
    assert np.allclose(
        transform_vector_components(v.components, chg), [1.5, 4.0]
    )


def test_covector_transforms_with_P():
    old = Basis.standard(2, name="e")
    new = Basis(np.array([[2.0, 0.0], [0.0, 1.0]]), name="ẽ")
    chg = ChangeOfBasis.from_bases(old, new)
    omega = Covector.from_iterable([1.0, 2.0], old)
    omega_new = omega.in_basis(chg)
    # ω' = P^T ω = (2, 2)
    assert np.allclose(omega_new.components, [2.0, 2.0])
    assert np.allclose(
        transform_covector_components(omega.components, chg), [2.0, 2.0]
    )


def test_pairing_invariant_under_change():
    old = Basis.standard(2, name="e")
    # General invertible change
    new = Basis(np.array([[1.0, 1.0], [0.0, 2.0]]), name="ẽ")
    chg = ChangeOfBasis.from_bases(old, new)
    v = Vector.from_iterable([3.0, 4.0], old)
    omega = Covector.from_iterable([1.0, 2.0], old)
    assert float(omega.in_basis(chg)(v.in_basis(chg))) == pytest.approx(
        float(omega(v))
    )


def test_metric_transform_preserves_length():
    old = Basis.standard(2, name="e")
    new = Basis(np.array([[1.0, 0.5], [0.0, 1.0]]), name="ẽ")
    chg = ChangeOfBasis.from_bases(old, new)
    g = BilinearForm.euclidean(2, old)
    v = Vector.from_iterable([3.0, 4.0], old)
    g_new = g.in_basis(chg)
    v_new = v.in_basis(chg)
    assert float(g_new(v_new, v_new)) == pytest.approx(float(g(v, v)))
    # Explicit formula B' = P^T B P
    assert np.allclose(g_new.components, chg.P.T @ g.components @ chg.P)


def test_roundtrip_double_change():
    """Changing to new and conceptually back should recover components."""
    old = Basis.standard(2, name="e")
    new = Basis(np.array([[2.0, 1.0], [0.0, 1.0]]), name="ẽ")
    forward = ChangeOfBasis.from_bases(old, new)
    back = ChangeOfBasis.from_bases(new, old)
    v = Vector.from_iterable([5.0, -1.0], old)
    v_back = v.in_basis(forward).in_basis(back)
    assert np.allclose(v_back.components, v.components)
    omega = Covector.from_iterable([2.0, 3.0], old)
    omega_back = omega.in_basis(forward).in_basis(back)
    assert np.allclose(omega_back.components, omega.components)


def test_singular_P_rejected():
    with pytest.raises(ValueError, match="invertible"):
        ChangeOfBasis(P=np.array([[1.0, 2.0], [2.0, 4.0]]))
