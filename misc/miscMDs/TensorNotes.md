# Tensors (Basics + Foundations + Algebra)

## Scalars (Rank-0 Tensors)

$$s := \text{scalar} \quad [\text{rank } 0]$$

A scalar is a single real number. Examples:
$$s = 1,\quad 20,\quad -50$$

Scalars have magnitude only and remain unchanged under any change of basis or coordinates. Pure magnitudes (mass, temperature, proper time, electric charge, etc.) are scalars and live in $\mathbb{R}$.

**Array view**: a rank-0 tensor is a 0-dimensional array (just a number).

## Vectors (Rank-1 Tensors)

A vector is an element of a vector space $V$.  
A vector space of dimension $n$ is the set of all linear combinations of $n$ basis vectors:
$$V = \operatorname{span}\{\mathbf{e}_1, \mathbf{e}_2, \dots, \mathbf{e}_n\}$$

Every vector $\mathbf{v} \in V$ can be written uniquely as
$$\mathbf{v} = v^i \mathbf{e}_i$$
(Einstein summation convention: a repeated index is summed over).

### Example (2-dimensional Euclidean plane)

For the standard orthonormal basis:
$$\mathbf{e}_1 = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \quad \mathbf{e}_2 = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$$

any vector looks like
$$\mathbf{v} = v^1 \mathbf{e}_1 + v^2 \mathbf{e}_2 = \begin{pmatrix} v^1 \\ v^2 \end{pmatrix}$$

**Array view**: a rank-1 tensor is a 1-dimensional array (a column or row of numbers). Einstein summation is simply the rule that tells you when to sum over a repeated index instead of writing an explicit $\sum$.

(Note: orthonormal bases are convenient for Euclidean space, but most bases used in relativity and continuum mechanics are *not* orthonormal. We drop the orthonormal assumption as soon as a metric appears.)

## Change of Basis and Transformation Law

The geometric vector itself does not change when we change basis; only its components do. The rule that describes how the components must change is the **transformation law**.

Suppose two bases for the same vector space $V$:
- original: $\{\mathbf{e}_i\}$
- new: $\{\tilde{\mathbf{e}}_j\}$

The new basis vectors are linear combinations of the old ones:
$$\tilde{\mathbf{e}}_j = \Lambda^i_{\ j} \mathbf{e}_i$$
($\Lambda^i_{\ j}$ is the change-of-basis matrix.)

Any vector expands in either basis:
$$\mathbf{v} = v^i \mathbf{e}_i = \tilde{v}^j \tilde{\mathbf{e}}_j$$

Substituting the expression for the new basis and equating coefficients immediately yields the **transformation law for vector components**:
$$v^i = \Lambda^i_{\ j} \tilde{v}^j \qquad\text{or equivalently}\qquad \tilde{v}^j = (\Lambda^{-1})^j_{\ i} v^i$$

**Key point**: the components transform with the *inverse* of the matrix that transforms the basis vectors. This opposite behavior keeps the actual geometric vector $\mathbf{v}$ unchanged.

In index notation the pair of rules is:
- basis vectors: $\tilde{\mathbf{e}}_j = \Lambda^i_{\ j} \mathbf{e}_i$
- components: $\tilde{v}^i = (\Lambda^{-1})^i_{\ j} v^j$

Objects whose components transform exactly this way are called *contravariant* vectors (type $(1,0)$ tensors). The law holds for any change of basis; orthonormality is not required.

**Concrete check (2-D rotation by $45^\circ$)**

Let the change-of-basis matrix be
$$
\Lambda^i_{\ j} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix}
$$
so that the new basis vectors are
$$
\tilde{\mathbf{e}}_1 = \Lambda^i_{\ 1}\mathbf{e}_i = \frac{1}{\sqrt{2}}(\mathbf{e}_1 + \mathbf{e}_2), \qquad
\tilde{\mathbf{e}}_2 = \Lambda^i_{\ 2}\mathbf{e}_i = \frac{1}{\sqrt{2}}(-\mathbf{e}_1 + \mathbf{e}_2).
$$

Take the original vector with components $v^i = (1,0)$, i.e.
$$
\mathbf{v} = 1\cdot\mathbf{e}_1 + 0\cdot\mathbf{e}_2.
$$

The components in the new basis are obtained with the inverse matrix:
$$
\tilde{v}^j = (\Lambda^{-1})^j_{\ i}v^i
= \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ -1 & 1 \end{pmatrix}\begin{pmatrix} 1 \\ 0 \end{pmatrix}
= \begin{pmatrix} 1/\sqrt{2} \\ -1/\sqrt{2} \end{pmatrix}.
$$

Now reconstruct the same geometric vector from the new components and the new basis vectors:
$$
\begin{align*}
\tilde{v}^j\tilde{\mathbf{e}}_j
&= \tilde{v}^1\tilde{\mathbf{e}}_1 + \tilde{v}^2\tilde{\mathbf{e}}_2 \\
&= \frac{1}{\sqrt{2}}\cdot\frac{1}{\sqrt{2}}(\mathbf{e}_1 + \mathbf{e}_2)
  + \left(-\frac{1}{\sqrt{2}}\right)\cdot\frac{1}{\sqrt{2}}(-\mathbf{e}_1 + \mathbf{e}_2) \\
&= \frac12(\mathbf{e}_1 + \mathbf{e}_2) - \frac12(-\mathbf{e}_1 + \mathbf{e}_2) \\
&= \frac12\mathbf{e}_1 + \frac12\mathbf{e}_2 + \frac12\mathbf{e}_1 - \frac12\mathbf{e}_2 \\
&= \mathbf{e}_1.
\end{align*}
$$

The components transformed one way and the basis vectors transformed the opposite way; when they are multiplied back together the changes cancel and the original vector $\mathbf{v}$ is recovered unchanged. Only its representation (the pair of numbers that label it) has changed.

## Dual Space and Covectors

Vectors live in $V$. There is a second, equally important space: the **dual space** $V^*$.  
An element of $V^*$ is a linear map that takes a vector and returns a real number. These maps are called ***co*vectors** (or dual vectors, or 1-forms).

Formally,
$$V^* = \{\omega : V \to \mathbb{R} \mid \omega\text{ is linear}\}$$

Given a basis $\{\mathbf{e}_i\}$ of $V$, there is a unique **dual basis** $\{\varepsilon^i\}$ of $V^*$ defined by
$$\varepsilon^i(\mathbf{e}_j) = \delta^i_{\ j}$$

Any covector expands as $\omega = \omega_i \varepsilon^i$.

Under the same change of basis $\tilde{\mathbf{e}}_j = \Lambda^i_{\ j}\mathbf{e}_i$, the dual basis transforms oppositely:
$$\tilde{\varepsilon}^i = (\Lambda^{-1})^i_{\ j} \varepsilon^j$$
Consequently the components of a covector transform with $\Lambda$ itself:
$$\tilde{\omega}_j = \Lambda^i_{\ j} \omega_i$$

**Key point**: covector components transform with the *same* matrix that transforms the basis vectors (the opposite of ordinary vectors). This is exactly what is required so that the pairing $\omega(\mathbf{v})$ is a basis-independent scalar:
$$\omega(\mathbf{v}) = \omega_i v^i = \tilde{\omega}_j \tilde{v}^j$$

Objects whose components transform this way are called covariant vectors (type $(0,1)$ tensors).

**Everyday example**: the gradient of a scalar function is a covector. In coordinates its components are simply the partial derivatives $\partial_i f$, and they transform with $\Lambda$, not $\Lambda^{-1}$.

## Tensors as Multilinear Maps

A **tensor of type $(r,s)$** is a multilinear map that accepts $r$ covectors and $s$ vectors and returns a real number:
$$T : \underbrace{V^*\times\cdots\times V^*}_{r\text{ times}}\times\underbrace{V\times\cdots\times V}_{s\text{ times}}\to\mathbb{R}$$
Multilinear means the map is linear in each argument separately.

The integers $r$ and $s$ are the contravariant and covariant ranks; $r+s$ is the total rank.

**Special cases**
- type $(0,0)$: scalar
- type $(1,0)$: contravariant vector
- type $(0,1)$: covariant vector
- type $(1,1)$: linear map $V\to V$ (ordinary matrix)
- type $(0,2)$: bilinear form (e.g., the metric or a stress tensor)

Given bases $\{\mathbf{e}_i\}$ and $\{\varepsilon^i\}$, the components are obtained by feeding basis elements into the map:
$$T^{i_1\dots i_r}_{\ j_1\dots j_s} = T(\varepsilon^{i_1},\dots,\varepsilon^{i_r},\mathbf{e}_{j_1},\dots,\mathbf{e}_{j_s})$$

Under a change of basis the components transform with one factor of $(\Lambda^{-1})$ for each upper index and one factor of $\Lambda$ for each lower index:
$$\tilde{T}^{i_1\dots i_r}_{\ j_1\dots j_s} = (\Lambda^{-1})^{i_1}_{\ a_1}\cdots(\Lambda^{-1})^{i_r}_{\ a_r}\ \Lambda^{b_1}_{\ j_1}\cdots\Lambda^{b_s}_{\ j_s}\ T^{a_1\dots a_r}_{\ b_1\dots b_s}$$

Any collection of numbers that transforms exactly this way defines a tensor of type $(r,s)$. The multilinear-map definition and the component transformation law are equivalent.

**Concrete examples**
- A matrix $M^i_{\ j}$ is a type $(1,1)$ tensor: it eats one vector and returns a vector (or, equivalently, eats one vector and one covector and returns a scalar).
- The Euclidean dot product is a type $(0,2)$ tensor whose components in an orthonormal basis are simply $\delta_{ij}$.
- In continuum mechanics the stress tensor is a type $(0,2)$ (or $(1,1)$) object that maps a surface normal (covector) to a force density (vector).

## Arrays, Einstein Notation, and Basic Operations

In practice we almost always store and manipulate the *components* of a tensor as a multi-dimensional array:
- rank 0 → number
- rank 1 → 1-D array
- rank 2 → 2-D array (matrix)
- rank 3 → 3-D array
- etc.

Einstein summation is the bookkeeping rule that makes the array operations match the abstract tensor operations. A repeated index is summed; an index that appears only once is free and labels the result.

**Common operations**
- Addition and scalar multiplication: component-wise (same type and rank).
- Tensor (outer) product: if $A$ has rank $r$ and $B$ has rank $s$, then $A\otimes B$ has rank $r+s$ and components $A^{i\dots}B^{j\dots}$.
- Contraction: sum over one upper and one lower index. This lowers the total rank by 2. Example: matrix-vector multiplication $M^i_{\ j}v^j$ is the contraction of a $(1,1)$ tensor with a $(1,0)$ tensor.
- Index raising/lowering (once a metric $g_{ij}$ is available): $v_i = g_{ij}v^j$, $v^i = g^{ij}v_j$. This is how we freely move between covariant and contravariant versions of the same geometric object.

These operations are basis-independent when performed correctly; the transformation laws guarantee that the result is again a tensor.

**Cross-field glimpses**
- *Special/general relativity*: the metric $g_{\mu\nu}$ is a type $(0,2)$ tensor; the electromagnetic field strength $F_{\mu\nu}$ is a type $(0,2)$ tensor; curvature is built from higher-rank tensors.
- *Continuum mechanics / mechanical engineering*: the stress and strain tensors are rank-2 objects; the constitutive law relating them is a rank-4 tensor.
- *Electromagnetism*: Maxwell’s equations can be written in a fully tensorial form using the field-strength tensor.
- *Multivariable calculus*: the Jacobian matrix of a coordinate transformation is precisely the change-of-basis matrix $\Lambda$ we have been using; the gradient, divergence, and curl all acquire clean tensor expressions once we distinguish vectors from covectors.
- (Machine-learning aside: the same multi-dimensional arrays appear as “tensors” in neural-network libraries, but the transformation-law requirement is usually ignored; the objects are simply arrays that happen to carry multiple indices.)

**One-paragraph summary of the array view**  
A tensor is a geometric object that can be represented, once a basis is chosen, by a multi-dimensional array of numbers. When the basis changes, those numbers must be transformed by a specific rule involving the change-of-basis matrix and its inverse (one factor for each index). Einstein summation is the compact notation for the contractions and products we perform on those arrays. The abstract multilinear-map definition guarantees that, no matter which basis we pick, the geometric result stays the same.

This foundation is sufficient to begin working with tensors in relativity, continuum mechanics, electromagnetism, and multivariable calculus. The next natural steps are the metric tensor, index raising/lowering in earnest, and the covariant derivative.