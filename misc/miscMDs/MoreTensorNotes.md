# Change-of-basis matrices $\beta$

$$
\beta\in\mathrm{GL}(n)
=\{\,M\in\mathbb{R}^{n\times n}\mid\det M\neq 0\,\}
$$

There exist bases $\{\mathbf{e}_i\}$ and $\{\tilde{\mathbf{e}}_j\}$ such that
$$
\tilde{\mathbf{e}}_j=\beta^i_{\ j}\mathbf{e}_i.
$$
$\beta$ itself is **not** a tensor; it supplies the transformation rule that every tensor must obey.

$\beta$ can be represented as:
$$
\beta=
\underbrace{
    \begin{bmatrix}
        \beta^{1}_{\ \ 1} & \beta^{1}_{\ \ 2} & \cdots & \beta^{1}_{\ \ n} \\
        \beta^{2}_{\ \ 1} & \beta^{2}_{\ \ 2} & \cdots & \beta^{2}_{\ \ n} \\
        \vdots & \vdots & \ddots & \vdots \\
        \beta^{n}_{\ \ 1} & \beta^{n}_{\ \ 2} & \cdots & \beta^{n}_{\ \ n}
\end{bmatrix}
}_{\normalsize{n\text{ columns}}}
\;
\begin{matrix}
    \left.
        \vphantom{
            \begin{bmatrix}
                a \\ a \\ a \\ a
            \end{bmatrix}
        }
    \right\}{n\text{ rows}}
\end{matrix}
$$

## Example
$$
\text{Let } \beta = \begin{bmatrix} a & b \\ c & d \end{bmatrix} $$
$$
\because \mathbf{e}_1 \equiv \begin{bmatrix} 1 \\ 0 \end{bmatrix} \quad \& \quad \mathbf{e}_2 \equiv \begin{bmatrix} 0 \\ 1 \end{bmatrix} \quad \therefore \tilde{\mathbf{e}}_1 \equiv \begin{bmatrix} a \\ c \end{bmatrix} \quad \& \quad \tilde{\mathbf{e}}_2 \equiv \begin{bmatrix} b \\ d \end{bmatrix}
$$
$$\therefore \beta^{-1} = \frac{1}{ad-bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$$

# Linear maps / $(1,1)$-tensors $\Lambda$

$$
\Lambda\in V\otimes V^*
\simeq\mathrm{End}(V)
=\{\,L:V\to V\mid L\text{ is linear}\,\}
$$

In components (any basis)
$$
\Lambda=\Lambda^i_{\ j}\,\mathbf{e}_i\otimes\varepsilon^j,
\qquad
w^i=\Lambda^i_{\ j}v^j.
$$

If the change-of-basis matrix $\beta$ is defined by
$$
\tilde{\mathbf{e}}_j=\beta^i_{\ j}\mathbf{e}_i
$$
(i.e., the new basis row equals the old basis row right-multiplied by $\beta$), then the matrix of the linear map transforms as
$$
\tilde{\Lambda}=\beta^{-1}\Lambda\beta
$$
or, in indices,
$$
\tilde{\Lambda}^i_{\ j}
=(\beta^{-1})^i_{\ a}\,\Lambda^a_{\ b}\,\beta^b_{\ j}.
$$

Left-multiplication by $\beta^{-1}$ and right-multiplication by $\beta$ are exactly what keep the underlying linear map unchanged.

# Bilinear forms / $(0,2)$-tensors $\mathcal{B}$

$$
\mathcal{B}\in V^*\otimes V^*
=\{\,B:V\times V\to\mathbb{R}\mid B\text{ is bilinear}\,\}
$$

In components
$$
\mathcal{B}=\mathcal{B}_{ij}\,\varepsilon^i\otimes\varepsilon^j,
\qquad
\mathcal{B}(\mathbf{v},\mathbf{w})=\mathcal{B}_{ij}v^iw^j.
$$
Under the change of basis given by $\beta$,
$$
\tilde{\mathcal{B}}_{ij}
=\mathcal{B}_{ab}\,\beta^a_{\ i}\,\beta^b_{\ j}.
$$

# $(2,0)$-tensors (for comparison)

$$
T\in V\otimes V
=\{\,T:V^*\times V^*\to\mathbb{R}\mid T\text{ is bilinear}\,\}
$$

They are the “opposite” of $(0,2)$-tensors: they eat two covectors and return a scalar.  
Their components transform with two factors of $\beta^{-1}$:
$$
\tilde{T}^{ij}
=(\beta^{-1})^i_{\ a}\,(\beta^{-1})^j_{\ b}\,T^{ab}.
$$
In the presence of a metric one can freely convert between $(2,0)$, $(1,1)$ and $(0,2)$ versions of the same geometric object by raising or lowering indices; without a metric they remain distinct types.