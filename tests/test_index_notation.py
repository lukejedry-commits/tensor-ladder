"""Tests for free/dummy index helpers and Einstein contraction."""

import numpy as np
import pytest

from tensor_ladder import (
    einstein_contract,
    free_and_dummy_indices,
    validate_index_string,
)


def test_validate_ascii_indices():
    assert validate_index_string("ij") == ["i", "j"]
    assert validate_index_string("i j") == ["i", "j"]


def test_free_and_dummy_pairing():
    free, dummy = free_and_dummy_indices("i", "i")
    assert free == []
    assert dummy == ["i"]


def test_free_and_dummy_mixed():
    free, dummy = free_and_dummy_indices("ij", "j")
    assert free == ["i"]
    assert dummy == ["j"]


def test_triple_index_rejected():
    with pytest.raises(ValueError, match="3 times"):
        free_and_dummy_indices("i", "i", "i")


def test_einstein_scalar_contraction():
    omega = np.array([1.0, 2.0])
    v = np.array([3.0, 4.0])
    result = einstein_contract((omega, "i"), (v, "i"))
    assert result.shape == ()
    assert float(result) == pytest.approx(11.0)


def test_einstein_matrix_vector():
    T = np.array([[1.0, 2.0], [3.0, 4.0]])
    v = np.array([1.0, 1.0])
    out = einstein_contract((T, "ij"), (v, "j"))
    assert np.allclose(out, T @ v)


def test_einstein_out_indices_permutation():
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    # Identity-like: A_ij with free i,j — transpose via out order
    out = einstein_contract((A, "ij"), out_indices="ji")
    assert np.allclose(out, A.T)
