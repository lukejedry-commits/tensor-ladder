"""Tests for Step 2: dual bases, bidual, linear-map dual, annihilators, sharp."""

import numpy as np
import pytest

from tensor_ladder import (
    Basis,
    BilinearForm,
    ChangeOfBasis,
    Covector,
    DualBasis,
    LinearMap,
    Vector,
    annihilator,
    annihilator_dim,
    dual_basis,
    embedding_commutes_with_change_of_basis,
    natural_embedding,
    reconstruct_covector,
    reconstruct_vector,
)


def test_dual_basis_kronecker():
    e = Basis.standard(3, name="e")
    db = dual_basis(e)
    assert isinstance(db, DualBasis)
    M = db.pairing_matrix()
    assert np.allclose(M, np.eye(3))
    for i in range(3):
        for j in range(3):
            eps_i = db.covector(i)
            e_j = Vector(np.eye(3)[j], e)
            assert float(eps_i(e_j)) == pytest.approx(float(i == j))


def test_reconstruct_vector_and_covector():
    e = Basis.standard(2)
    v = Vector.from_iterable([3.0, -1.5], e)
    v2 = reconstruct_vector(v)
    assert np.allclose(v2.components, v.components)

    omega = Covector.from_iterable([2.0, 7.0], e)
    omega2 = reconstruct_covector(omega)
    assert np.allclose(omega2.components, omega.components)


def test_natural_embedding_evaluates_as_pairing():
    e = Basis.standard(2)
    v = Vector.from_iterable([3.0, 4.0], e)
    omega = Covector.from_iterable([1.0, 2.0], e)
    iota_v = natural_embedding(v)
    assert float(iota_v(omega)) == pytest.approx(11.0)
    assert float(omega(v)) == pytest.approx(11.0)


def test_embedding_naturality_under_change_of_basis():
    e = Basis.standard(2, name="e")
    e_new = Basis(np.array([[2.0, 0.0], [1.0, 1.0]]), name="e-tilde")
    change = ChangeOfBasis.from_bases(e, e_new)
    v = Vector.from_iterable([3.0, 4.0], e)
    omega = Covector.from_iterable([1.0, 2.0], e)
    assert embedding_commutes_with_change_of_basis(v, change, omega)


def test_embedding_is_injective_finite_dim():
    e = Basis.standard(2)
    for comps in ([0.0, 0.0], [1.0, -2.0], [0.0, 3.0]):
        v = Vector.from_iterable(comps, e)
        iota_v = natural_embedding(v)
        db = dual_basis(e)
        recovered = [float(iota_v(db.covector(i))) for i in range(2)]
        assert np.allclose(recovered, comps)


def test_linear_map_apply():
    e = Basis.standard(2, name="e")
    A = LinearMap.from_matrix([[2.0, 1.0], [0.0, 3.0]], e, e)
    v = Vector.from_iterable([1.0, 1.0], e)
    Av = A(v)
    assert np.allclose(Av.components, [3.0, 3.0])


def test_dual_map_is_transpose():
    eV = Basis.standard(2, name="eV")
    eW = Basis.standard(3, name="eW")
    M = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    A = LinearMap.from_matrix(M, eV, eW)
    assert np.allclose(A.dual_matrix(), M.T)
    A_star = A.dual()
    assert np.allclose(A_star.matrix, M.T)

    eta = Covector.from_iterable([1.0, 0.0, -1.0], eW)
    A_star_eta = A.apply_dual(eta)
    v = Vector.from_iterable([2.0, -1.0], eV)
    left = float(A_star_eta(v))
    right = float(eta(A(v)))
    assert left == pytest.approx(right)


def test_annihilator_dimension_formula():
    assert annihilator_dim(1, 3) == 2
    assert annihilator_dim(0, 2) == 2
    assert annihilator_dim(2, 2) == 0
    with pytest.raises(ValueError):
        annihilator_dim(3, 2)


def test_annihilator_of_line():
    e = Basis.standard(3, name="e")
    u = Vector.from_iterable([1.0, 0.0, 0.0], e)
    ann = annihilator([u], e)
    assert len(ann) == annihilator_dim(1, 3)
    for omega in ann:
        assert float(omega(u)) == pytest.approx(0.0)
    mat = np.stack([w.components for w in ann])
    assert np.linalg.matrix_rank(mat) == 2


def test_annihilator_full_space():
    e = Basis.standard(2)
    u = Vector.from_iterable([1.0, 0.0], e)
    w = Vector.from_iterable([0.0, 1.0], e)
    ann = annihilator([u, w], e)
    assert len(ann) == 0


def test_sharp_inverse_of_flat():
    e = Basis.standard(2)
    B = BilinearForm.from_matrix([[2.0, 1.0], [1.0, 2.0]], e)
    v = Vector.from_iterable([3.0, -1.0], e)
    flat = B.flat(v)
    sharp = B.sharp(flat)
    assert np.allclose(sharp.components, v.components)
    omega = Covector.from_iterable([1.0, 4.0], e)
    assert np.allclose(B.flat(B.sharp(omega)).components, omega.components)


def test_sharp_requires_nondegenerate():
    e = Basis.standard(2)
    B = BilinearForm.from_matrix([[1.0, 0.0], [0.0, 0.0]], e)
    omega = Covector.from_iterable([1.0, 0.0], e)
    with pytest.raises(ValueError, match="non-degenerate"):
        B.sharp(omega)
