## Tensors (Basics + Foundations + Algebra)

### Scalars (Rank-0 Tensors)

$$s := \text{scalar} \quad [\text{rank } 0]$$

A scalar is a single real number. Examples:
$$s = 1,\quad 20,\quad -50$$

Scalars have magnitude only. In the tensor hierarchy they are the objects that remain unchanged under any change of basis or coordinates. All measurements of pure magnitude (mass, temperature, proper time, etc.) are scalars and live in $\mathbb{R}$.

### Vectors (Rank-1 Tensors)

A vector is an element of a vector space $V$.  
A vector space of dimension $n$ is the set of all linear combinations of $n$ basis vectors:

$$V = \operatorname{span}\{\mathbf{e}_1, \mathbf{e}_2, \dots, \mathbf{e}_n\}$$

Every vector $\mathbf{v} \in V$ can be written uniquely as
$$\mathbf{v} = v^i \mathbf{e}_i$$
(Einstein summation convention: repeated index is summed).

**Example (2-dimensional Euclidean plane)**  
For a simple orthonormal basis:
$$\mathbf{e}_1 = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \quad \mathbf{e}_2 = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$$

Any vector then looks like
$$\mathbf{v} = v^1 \mathbf{e}_1 + v^2 \mathbf{e}_2 = \begin{pmatrix} v^1 \\ v^2 \end{pmatrix}$$

(Note: orthonormal bases are convenient for Euclidean space, but most bases used in relativity are *not* orthonormal. We will drop the orthonormal assumption as soon as we introduce the metric.)

### Change of Basis and Transformation Law

So far we have written a vector in one fixed basis.  
In practice we often change bases. The geometric vector itself does not change; only its components do. The rule that tells us how the components must change is called the **transformation law**.

Suppose we have two bases for the same vector space $V$:
- original basis: $\{\mathbf{e}_i\}$
- new basis: $\{\tilde{\mathbf{e}}_j\}$

The new basis vectors can be expressed as linear combinations of the old ones:
$$
\tilde{\mathbf{e}}_j = \Lambda^i_{\ j} \mathbf{e}_i
$$
(The matrix $\Lambda^i_{\ j}$ is the change-of-basis matrix.)

Any vector $\mathbf{v}$ can be expanded in either basis:
$$
\mathbf{v} = v^i \mathbf{e}_i = \tilde{v}^j \tilde{\mathbf{e}}_j
$$

Substitute the expression for the new basis vectors:
$$
v^i \mathbf{e}_i = \tilde{v}^j (\Lambda^i_{\ j} \mathbf{e}_i)
$$

Because the basis vectors are linearly independent, the coefficients of each $\mathbf{e}_i$ must match. This gives the **transformation law for vector components**:
$$
v^i = \Lambda^i_{\ j} \tilde{v}^j
$$
or, equivalently (solving for the new components),
$$
\tilde{v}^j = (\Lambda^{-1})^j_{\ i} v^i
$$

**Key point**: the components transform with the *inverse* of the matrix that transforms the basis vectors. This opposite behavior is what keeps the actual vector $\mathbf{v}$ unchanged.

In index notation we often write the two transformation rules side by side:
- basis vectors: $\tilde{\mathbf{e}}_j = \Lambda^i_{\ j} \mathbf{e}_i$
- components: $\tilde{v}^i = (\Lambda^{-1})^i_{\ j} v^j$

This pair of rules is the prototype for all later tensor transformation laws. Objects whose components transform exactly this way are called *contra*variant vectors (type $(1,0)$ tensors).

**Note**: We have not yet assumed the bases are orthonormal. The transformation law above is completely general; it holds for any change of basis.

### Dual Space and Covectors

Vectors live in a vector space $V$.  
There is a second space that is equally important: the **dual space** $V^*$.  
An element of $V^*$ is a linear map that takes a vector and returns a real number.  
These maps are called ***co*vectors** (or dual vectors, or 1-forms).

Formally,
$$
V^* = \{\omega : V \to \mathbb{R} \mid \omega \text{ is linear}\}
$$

Given a basis $\{\mathbf{e}_i\}$ of $V$, there exists a unique **dual basis** $\{\varepsilon^{i}\}$ of $V^*$ defined by the relation
$$
\varepsilon^{\ i}(\mathbf{e}_j) = \delta^{\ i}_{\ \ j}
$$
(The Kronecker delta is 1 when the indices match and 0 otherwise.)

Any covector $\omega \in V^*$ can be expanded in this dual basis:
$$
\omega = \omega_i \ \varepsilon^i
$$
The numbers $\omega_i$ are the components of the covector.

When we change basis, the dual basis transforms in the opposite way from the original basis.  
If the new basis is related to the old one by
$$
\tilde{\mathbf{e}}_j = \Lambda^i_{\ j} \ \mathbf{e}_i
$$
then the dual basis transforms as
$$
\tilde{\varepsilon}^{\ i} = (\Lambda^{-1})^i_{\ j} \ \varepsilon^{\ j}
$$

The components of a covector therefore transform with the matrix $\Lambda$ itself (not its inverse):
$$
\tilde{\varepsilon}_j = \Lambda^i_{\ j} \ \varepsilon_i
$$
or, written the other way,
$$
\varepsilon_i = (\Lambda^{-1})^j_{\ i} \ \tilde{\varepsilon}_j
$$

**Key point**: the components of a covector transform with the *same* matrix that transforms the basis vectors. This is the opposite of the rule for ordinary vectors. The opposite behavior is exactly what is required so that the number $\varepsilon(\mathbf{v})$ stays the same no matter which basis we use:
$$
\varepsilon(\mathbf{v}) = \varepsilon_i v^i = \tilde{\varepsilon}_j \tilde{v}^j
$$
The pairing of a covector and a vector is a basis-independent scalar.

Objects whose components transform this way are called covariant vectors (type $(0,1)$ tensors).  
Together with the contravariant vectors of the previous section, they form the two building blocks from which all higher-rank tensors are constructed.

### Tensors as Multilinear Maps

We now have two kinds of objects:
- contravariant vectors (type $(1,0)$), which live in $V$
- covariant vectors (type $(0,1)$), which live in $V^*$

A general tensor combines both.  
A **tensor of type $(r,s)$** is a multilinear map that accepts $r$ covectors and $s$ vectors and returns a real number:
$$
T : \underbrace{V^* \times \cdots \times V^*}_{r \text{ times}} \times \underbrace{V \times \cdots \times V}_{s \text{ times}} \to \mathbb{R}
$$
Multilinear means the map is linear in each argument separately when the others are held fixed.

The integers $r$ and $s$ are called the contravariant and covariant ranks.  
Their sum $r+s$ is the total rank of the tensor.

**Special cases already seen**
- type $(0,0)$: a scalar (no arguments)
- type $(1,0)$: a contravariant vector (eats one covector)
- type $(0,1)$: a covariant vector (eats one vector)
- type $(1,1)$: a linear map $V \to V$ (or $V^* \to V^*$)
- type $(0,2)$: a bilinear form (eats two vectors)

Given a basis $\{\mathbf{e}_i\}$ of $V$ and its dual basis $\{\varepsilon^i\}$ of $V^*$, the components of $T$ are the numbers obtained by feeding basis elements into the map:
$$
T^{i_1 \dots i_r}_{\ \ j_1 \dots j_s} = T(\varepsilon^{i_1}, \dots, \varepsilon^{i_r}, \mathbf{e}_{j_1}, \dots, \mathbf{e}_{j_s})
$$

Under a change of basis
$$
\tilde{\mathbf{e}}_j = \Lambda^i_{\ j} \ \mathbf{e}_i
$$
the components transform with one factor of $(\Lambda^{-1})$ for each upper index and one factor of $\Lambda$ for each lower index:
$$
\tilde{T}^{i_1 \dots i_r}_{\ \ j_1 \dots j_s} = (\Lambda^{-1})^{i_1}_{\ a_1} \cdots (\Lambda^{-1})^{i_r}_{\ a_r} \ \Lambda^{b_1}_{\ j_1} \cdots \Lambda^{b_s}_{\ j_s} \ T^{a_1 \dots a_r}_{\ \ b_1 \dots b_s}
$$

This is the full tensor transformation law.  
Any collection of numbers that transforms exactly this way under every change of basis defines a tensor of type $(r,s)$.

**Key point**: the multilinear-map definition and the component transformation law are equivalent. One can start from either description and recover the other. In practice we usually work with the components, but the map definition makes clear why the transformation law must look the way it does: it is the unique rule that keeps the output scalar independent of the basis we chose.