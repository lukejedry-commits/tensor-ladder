# Step 1 — Fundamentals: scalars, vectors, covectors, forms, indices, bases

This lesson mirrors the implemented API in `tensor_ladder`.  Work through
the ideas, then run `examples/step01_fundamentals_demo.py` and attempt the
exercises at the end.

---

## 1. Scalars (0-tensors)

A **scalar** is a single real number that does not depend on a choice of
basis.  In index language it has **no free indices**.

Examples: a temperature reading; the number $\omega(v)$ obtained by feeding
a vector into a covector; $\operatorname{tr}(A)$ for an endomorphism.

Under a change of basis, nothing multiplies a scalar — the “empty product”
of transformation matrices.  That is why true scalars are safe observables
across frames.

```python
from tensor_ladder import Scalar
s = Scalar(3.14)
assert float(s) == 3.14
```

---

## 2. Vectors — contravariant components

Fix a finite-dimensional real vector space $V$ with ordered basis
$\{e_1,\ldots,e_n\}$.  Any vector $v\in V$ expands uniquely as

$$
v = v^i\, e_i
\quad\text{(Einstein sum on } i\text{)}.
$$

The numbers $v^i$ are the **contravariant components** of $v$ in that
basis.  We write the index **up**.

### Why “contra-”?

Suppose we stretch every basis vector by a factor of 2: $e'_i = 2 e_i$.
The *geometric* arrow $v$ is unchanged, so its components must **halve**:
$v'^i = v^i / 2$.  Components transform *contrary* to the basis.

In code:

```python
from tensor_ladder import Basis, Vector
e = Basis.standard(2)
v = Vector.from_iterable([3.0, 4.0], e)
```

---

## 3. Covectors — dual vectors / 1-forms

The **dual space** $V^*$ is the set of linear maps $\omega: V\to\mathbb{R}$.
Elements of $V^*$ are **covectors** (also: dual vectors, 1-forms).

Given $\{e_i\}$, the **dual basis** $\{\varepsilon^i\}\subset V^*$ is defined by

$$
\varepsilon^i(e_j) = \delta^i_j.
$$

Any $\omega\in V^*$ expands as $\omega = \omega_i\,\varepsilon^i$ with
$\omega_i = \omega(e_i)$ (index **down**).  Then

$$
\omega(v) = \omega_i v^i.
$$

### Why “co-”?

Covector components transform *with* the basis (same $P$), so that the
pairing $\omega_i v^i$ stays invariant — see §6.

```python
from tensor_ladder import Covector
ω = Covector.from_iterable([1.0, 2.0], e)
print(ω(v))  # Scalar(11.0)
```

---

## 4. Bilinear forms / (0,2) tensors

A **bilinear form** is a map $B: V\times V\to\mathbb{R}$ linear in each
slot.  In components,

$$
B(u,v) = B_{ij}\, u^i v^j.
$$

### Metric (motivation only)

A **metric** is a symmetric, non-degenerate bilinear form $g_{ij}$.  It
provides lengths $g(v,v)$, angles, and the musical maps that raise/lower
indices:

$$
v_i = g_{ij} v^j, \qquad v^i = g^{ij} v_j.
$$

Step 1 keeps this elementary: `BilinearForm` with `.flat(v)` for lowering.

```python
from tensor_ladder import BilinearForm
g = BilinearForm.euclidean(2, e)
print(g(v, v))          # 25
print(g.flat(v))        # Covector([3, 4], ...)
```

---

## 5. Index notation: free vs dummy, Einstein summation

| Appearance of an index | Name | Role |
|------------------------|------|------|
| Once in a term | **free** | Labels a free slot of the result |
| Exactly twice (once up, once down) | **dummy** | Summed over $1\ldots n$ |

**Einstein summation convention:** omit the $\sum$ for dummy indices.

Examples:

- $\omega_i v^i$ — $i$ dummy → scalar  
- $T^i{}_j v^j$ — $i$ free, $j$ dummy → vector  
- $g_{ij} v^i w^j$ — $i,j$ dummy → scalar  

```python
from tensor_ladder import free_and_dummy_indices, einstein_contract
import numpy as np

free, dummy = free_and_dummy_indices("i", "i")
# free=[], dummy=['i']
einstein_contract((np.array([1.,2.]), "i"), (np.array([3.,4.]), "i"))
```

---

## 6. Change of basis — why vectors and covectors differ

Let the new basis be related to the old by

$$
e'_j = e_i\, P^i{}_j
$$

(columns of $P$ = new basis vectors in the old basis).  Then:

$$
\boxed{
v'^i = (P^{-1})^i{}_j\, v^j,
\qquad
\omega'_i = \omega_j\, P^j{}_i.
}
$$

### Short invariance proof

$$
\omega'_i v'^i
= (\omega_j P^j{}_i)\,((P^{-1})^i{}_k v^k)
= \omega_j \delta^j{}_k v^k
= \omega_k v^k.
$$

So the two laws are *forced* if the pairing is geometric (basis-free).

For a bilinear form,

$$
B'_{kl} = P^i{}_k\, P^j{}_l\, B_{ij}
\quad\Leftrightarrow\quad
B' = P^{T} B P.
$$

```python
from tensor_ladder import ChangeOfBasis, Basis
import numpy as np

e = Basis.standard(2, name="e")
e_new = Basis(np.array([[2., 0.], [0., 1.]]), name="ẽ")
chg = ChangeOfBasis.from_bases(e, e_new)
v2 = v.in_basis(chg)
ω2 = ω.in_basis(chg)
assert abs(float(ω2(v2)) - float(ω(v))) < 1e-10
```

---

## Exercises

### Exercise A — Pairing

Let $\omega = (2, -1)$ and $v = (1, 4)$ in the standard basis of
$\mathbb{R}^2$.  Compute $\omega(v)$ by hand and with `Covector`/`Vector`.

### Exercise B — Stretch the basis

Using $P = \operatorname{diag}(2, 1)$, compute new components of
$v = (3, 4)$ and $\omega = (1, 2)$.  Verify $\omega'_i v'^i = \omega_i v^i$.

### Exercise C — Free vs dummy

For the expression $A^i{}_j B^j{}_k v^k$, list free and dummy indices and
state the tensor type of the result.

### Exercise D — Lowering

With $g = \delta_{ij}$ and $v = (3, 4)$, compute $v^\flat = g^\flat(v)$.
What are the covariant components?

---

## Solutions

<details>
<summary>Click to reveal solutions</summary>

**A.** $\omega(v) = 2\cdot 1 + (-1)\cdot 4 = -2$.

```python
from tensor_ladder import Basis, Vector, Covector
e = Basis.standard(2)
print(Covector.from_iterable([2, -1], e)(Vector.from_iterable([1, 4], e)))
# Scalar(-2.0)
```

**B.** $P^{-1} = \operatorname{diag}(1/2, 1)$, so
$v' = (3/2,\ 4)$.  $\omega' = P^{T}\omega = (2,\ 2)$.
Pairing: $2\cdot\tfrac32 + 2\cdot 4 = 3 + 8 = 11$, same as
$1\cdot 3 + 2\cdot 4 = 11$.

**C.** Dummy: $j,k$.  Free: $i$.  Result is a vector (type $(1,0)$).

**D.** $v_i = \delta_{ij} v^j = v^i$, so $v^\flat = (3, 4)$ as a covector.
(In a non-Euclidean metric these would differ.)

</details>
