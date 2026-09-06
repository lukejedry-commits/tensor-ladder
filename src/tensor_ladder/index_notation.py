"""
Index notation helpers: free vs dummy indices and Einstein summation.

Einstein summation convention
-----------------------------
When an index appears twice in a monomial — once up, once down — it is a
*dummy* (bound) index and is summed over its range.  Indices that appear
once are *free* and label the free slots of the resulting tensor.

Examples
--------
- ``ω_i v^i``           → scalar (i dummy)
- ``T^i_j v^j``         → vector (i free, j dummy)
- ``g_{ij} v^i w^j``    → scalar (i, j dummy)
- ``R^ρ_{σμν}``         → (1,3) tensor (all free)

This module provides small teaching utilities; for heavy numeric work use
``numpy.einsum`` directly (which we wrap pedagogically below).
"""

from __future__ import annotations

import re
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray


_INDEX_TOKEN = re.compile(r"[A-Za-zΑ-Ωα-ω][0-9]*|[μνρσλκξη]")


def validate_index_string(indices: str) -> list[str]:
    """
    Split an index string like ``'i'``, ``'ij'``, ``'μν'`` into tokens.

    For Latin letters we treat each character as an index (``'ij'`` → i, j).
    Whitespace is ignored.  Raises ``ValueError`` on empty / invalid input.
    """
    s = indices.replace(" ", "")
    if not s:
        raise ValueError("Index string must be non-empty.")
    # Prefer char-by-char for simple ASCII teaching strings
    if all(c.isalpha() and ord(c) < 128 for c in s):
        return list(s)
    tokens = _INDEX_TOKEN.findall(s)
    if "".join(tokens) != s:
        raise ValueError(f"Could not parse index string {indices!r}.")
    return tokens


def free_and_dummy_indices(*index_groups: str) -> tuple[list[str], list[str]]:
    """
    Classify indices appearing in one or more index groups.

    An index that appears **exactly twice** across all groups is dummy;
    one that appears **once** is free.  Appearing more than twice is an
    error (ambiguous / not standard Einstein convention).

    Returns
    -------
    free, dummy :
        Ordered lists (first occurrence order).
    """
    counts: dict[str, int] = {}
    order: list[str] = []
    for group in index_groups:
        for idx in validate_index_string(group):
            if idx not in counts:
                order.append(idx)
                counts[idx] = 0
            counts[idx] += 1

    free: list[str] = []
    dummy: list[str] = []
    for idx in order:
        c = counts[idx]
        if c == 1:
            free.append(idx)
        elif c == 2:
            dummy.append(idx)
        else:
            raise ValueError(
                f"Index {idx!r} appears {c} times; Einstein convention "
                "allows a dummy index to appear exactly twice."
            )
    return free, dummy


def einstein_contract(
    *operands: tuple[ArrayLike, str],
    out_indices: str | None = None,
) -> NDArray[np.floating]:
    """
    Pedagogical wrapper around ``numpy.einsum`` for Einstein contraction.

    Parameters
    ----------
    operands :
        Pairs ``(array, index_string)``, e.g. ``(omega, 'i'), (v, 'i')``.
    out_indices :
        Explicit free-index order for the result.  If omitted, free indices
        appear in first-occurrence order.

    Examples
    --------
    >>> import numpy as np
    >>> from tensor_ladder import einstein_contract
    >>> ω = np.array([1.0, 2.0])
    >>> v = np.array([3.0, 4.0])
    >>> float(einstein_contract((ω, 'i'), (v, 'i')))
    11.0
    """
    if not operands:
        raise ValueError("Need at least one operand.")

    arrays: list[NDArray[np.floating]] = []
    groups: list[str] = []
    for arr, idx in operands:
        a = np.asarray(arr, dtype=float)
        toks = validate_index_string(idx)
        if a.ndim != len(toks):
            raise ValueError(
                f"Array ndim {a.ndim} does not match index count {len(toks)} for {idx!r}."
            )
        arrays.append(a)
        groups.append(idx)

    free, dummy = free_and_dummy_indices(*groups)
    if out_indices is None:
        out = "".join(free)
    else:
        out_toks = validate_index_string(out_indices) if out_indices else []
        if sorted(out_toks) != sorted(free):
            raise ValueError(
                f"out_indices {out_indices!r} must be a permutation of free indices {free}."
            )
        out = out_indices

    # Build einsum subscripts with single-letter labels
    # Map each index token to a unique einsum letter
    all_idxs = []
    for g in groups:
        for t in validate_index_string(g):
            if t not in all_idxs:
                all_idxs.append(t)
    if out:
        for t in validate_index_string(out):
            if t not in all_idxs:
                all_idxs.append(t)

    letters = "ijklmnopqrstuvwxyzabcdefgh"
    if len(all_idxs) > len(letters):
        raise ValueError("Too many distinct indices for this teaching helper.")
    label = {idx: letters[k] for k, idx in enumerate(all_idxs)}

    parts = []
    for g in groups:
        parts.append("".join(label[t] for t in validate_index_string(g)))
    left = ",".join(parts)
    right = "".join(label[t] for t in validate_index_string(out)) if out else ""
    subscripts = f"{left}->{right}"

    return np.asarray(np.einsum(subscripts, *arrays, optimize=True), dtype=float)


def demonstrate_pairing(
    omega_components: ArrayLike, vector_components: ArrayLike
) -> dict[str, float | list[str]]:
    """
    Worked numeric demo: free/dummy analysis + contraction for ω_i v^i.
    """
    free, dummy = free_and_dummy_indices("i", "i")
    value = float(
        einstein_contract(
            (omega_components, "i"),
            (vector_components, "i"),
        )
    )
    return {"free": free, "dummy": dummy, "value": value}
