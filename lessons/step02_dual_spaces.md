# Step 2 — Dual spaces (deep)

This lesson goes deeper into \(V^*\) and \(V^{**}\) than Step 1's first look at
covectors.  Work the proofs on paper, then run
`examples/step02_dual_spaces_demo.py` and the notebook
`notebooks/02_dual_spaces.ipynb`.

---

## 1. Dual basis and reconstruction

Fix a basis \(\{e_i\}_{i=1}^n\) of the finite-dimensional real vector space \(V\).
There exists a unique basis \(\{\varepsilon^i\}_{i=1}^n\) of \(V^*\) such that

\[
\varepsilon^i(e_j) = \delta^i_j.
\]

**Existence / uniqueness (sketch).**  Define \(\varepsilon^i\) on basis vectors by
the Kronecker rule and extend linearly; uniqueness follows because a linear
map is determined by its values on a basis.

**Reconstruction.**

\[
v = \varepsilon^i(v)\, e_i,
\qquad
\omega = \omega(e_i)\,\varepsilon^i.
\]

*Proof of the vector formula.*  Write \(v = v^j e_j\).  Then
\(\varepsilon^i(v) = v^j \varepsilon^i(e_j) = v^j\delta^i_j = v^i\), so the right-hand
side is \(v^i e_i = v\).

*Proof of the covector formula.*  Both sides agree on every \(e_k\):
\(\omega(e_k)\) versus \(\omega(e_i)\varepsilon^i(e_k) = \omega(e_i)\delta^i_k = \omega(e_k)\).

```python
from tensor_ladder import Basis, Vector, Covector, dual_basis, reconstruct_vector

e = Basis.standard(2)
db = dual_basis(e)
assert abs(float(db.covector(0)(Vector.from_iterable([1, 0], e))) - 1.0) < 1e-12
```

---

## 2. Bidual and the natural embedding

The **bidual** is \(V^{**} = (V^*)^*\): linear maps \(V^*\to\mathbb{R}\).
Define

\[
\iota: V\to V^{**},
\qquad
\iota(v)(\omega) := \omega(v).
\]

**Linearity of \(\iota\).** Immediate from linearity of evaluation in \(v\).

**Injectivity (finite dim).**  If \(\iota(v)=0\), then \(\omega(v)=0\) for all
\(\omega\in V^*\).  Taking \(\omega=\varepsilon^i\) gives \(v^i=0\) for all \(i\), hence
\(v=0\).

**Isomorphism.**  \(\dim V^{**} = \dim V^* = \dim V\), so an injective linear map
between equal-dimensional spaces is an isomorphism.  In infinite dimensions
\(\iota\) need not be surjective — that is why finite dimensionality matters.

**Naturality under change of basis.**  If \(v'\) and \(\omega'\) are the same
geometric objects in a new basis, then \(\iota(v)(\omega)=\iota(v')(\omega')\)
because both equal the invariant pairing \(\omega(v)\).  The embedding does not
secretly depend on coordinates.

```python
from tensor_ladder import natural_embedding, embedding_commutes_with_change_of_basis
```

---

## 3. Dual of a linear map

Let \(A: V\to W\) be linear.  Its **dual** (transpose on dual spaces) is

\[
A^*: W^*\to V^*,
\qquad
(A^*\eta)(v) := \eta(A v).
\]

**Matrix fact.**  If \(M\) is the matrix of \(A\) in bases of \(V\) and \(W\), and
covector components are columns, then the matrix of \(A^*\) in the dual bases
is \(M^\top\).

*Check.*  \((A^*\eta)(v)=\eta(Av)=\eta\cdot(Mv)=(M^\top\eta)\cdot v\).

```python
from tensor_ladder import LinearMap
A = LinearMap.from_matrix([[2.0, 1.0], [0.0, 3.0]])
assert (A.dual_matrix() == A.matrix.T).all()
```

---

## 4. Annihilators

For a subspace \(U\subseteq V\), the **annihilator** is

\[
U^0 = \{\omega\in V^* : \omega|_U = 0\}.
\]

**Dimension formula.**  \(\dim U^0 = \dim V - \dim U\).

*Sketch.*  Extend a basis of \(U\) to a basis of \(V\).  Dual basis covectors
corresponding to the complementary directions form a basis of \(U^0\).

```python
from tensor_ladder import annihilator, annihilator_dim
```

---

## 5. Musical isomorphism (light bridge)

A nondegenerate bilinear form \(B\) induces

\[
\flat: V\to V^*,\quad v\mapsto v^\flat,\quad (v^\flat)_i = B_{ij}v^j,
\]
\[
\sharp: V^*\to V,\quad \omega\mapsto\omega^\sharp,\quad
(\omega^\sharp)^i = (B^{-1})^{ij}\omega_j,
\]

inverses of each other.  For a metric these are the familiar index-lowering /
raising maps.

```python
from tensor_ladder import BilinearForm
g = BilinearForm.euclidean(2)
# g.flat(v), g.sharp(omega)
```

---

## Exercises

**E1.** Prove that \(\{\varepsilon^i\}\) is linearly independent.  
**Solution.**  If \(a_i\varepsilon^i=0\), evaluate on \(e_k\) to get \(a_k=0\).

**E2.** Show \(\iota\) is surjective when \(\dim V<\infty\) without quoting
“injective + equal dim,” by constructing a preimage for an arbitrary
\(\Phi\in V^{**}\).  
**Solution.**  Set \(v := \Phi(\varepsilon^i)\, e_i\).  Then for any
\(\omega=\omega_j\varepsilon^j\),
\(\iota(v)(\omega)=\omega(v)=\omega_j\Phi(\varepsilon^j)=\Phi(\omega_j\varepsilon^j)=\Phi(\omega)\).

**E3.** If \(A:V\to W\) and \(B:W\to X\), prove \((BA)^*=A^*B^*\).  
**Solution.**  \(((BA)^*\zeta)(v)=\zeta(BAv)=(B^*\zeta)(Av)=(A^*B^*\zeta)(v)\).

**E4.** Compute a basis of \(U^0\) when \(V=\mathbb{R}^3\) and
\(U=\operatorname{span}\{(1,1,0)\}\).  
**Solution.**  \(\omega=(x,y,z)\) annihilates \(U\) iff \(x+y=0\).  Basis e.g.
\(\{(1,-1,0),(0,0,1)\}\).  Check with `annihilator`.

**E5.** For \(B=\begin{pmatrix}2&1\\1&2\end{pmatrix}\), verify
`B.sharp(B.flat(v)) == v` numerically for a nonzero \(v\).  
**Solution.**  See the demo / tests; follows because \(\sharp=\flat^{-1}\) when
\(B\) is invertible.
