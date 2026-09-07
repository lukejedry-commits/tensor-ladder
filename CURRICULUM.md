# Curriculum — the tensor ladder

Steps 1–2 are **implemented** in code and lessons.  Steps 3–N are **outlines
only** (no implementation yet).  Each step lists prerequisites, learning goals,
and the mathematical objects that will appear in a future package release.

---

## Step 1 — Fundamentals *(implemented)*

**Objects:** scalars, vectors, covectors, bilinear forms, bases, index notation.

**Goals:**

- Distinguish geometric objects from components
- Evaluate $\omega(v) = \omega_i v^i$
- Transform vector vs covector components correctly under a change of basis
- Use free/dummy indices and Einstein summation
- See bilinear forms as the elementary home of a metric $g_{ij}$

**Code:** `Scalar`, `Vector`, `Covector`, `BilinearForm`, `Basis`, `ChangeOfBasis`,
`einstein_contract`, transform helpers.

**Lesson:** `lessons/step01_fundamentals.md`

---

## Step 2 — Dual spaces (deep) *(implemented)*

**Prerequisites:** Step 1.

**Goals:**

- Dual basis $\varepsilon^i$ dual to $e_i$: $\varepsilon^i(e_j)=\delta^i_j$;
  reconstruct $v = \varepsilon^i(v)\, e_i$ and $\omega = \omega(e_i)\,\varepsilon^i$
- Bidual $V^{**}$ and the **natural embedding** $\iota: V\to V^{**}$,
  $\iota(v)(\omega)=\omega(v)$; finite-dimensional isomorphism; naturality
  under change of basis
- Dual of a linear map: if $A: V\to W$, then $A^*: W^*\to V^*$,
  $(A^*\eta)(v)=\eta(A v)$; matrix of $A^*$ is the transpose (in dual bases)
- Annihilator of a subspace: $U^0 = \{\omega\in V^*:\omega|_U=0\}$; dimension
  formula $\dim U^0 = \dim V - \dim U$
- Light bridge: nondegenerate bilinear form induces musical isomorphisms
  $V\cong V^*$ via flat ♭ / sharp ♯

**Code:** `DualBasis`, `dual_basis`, `reconstruct_vector`, `reconstruct_covector`,
`natural_embedding`, `BidualElement`, `annihilator`, `annihilator_dim`,
`LinearMap`, `BilinearForm.sharp`.

**Lesson:** `lessons/step02_dual_spaces.md`

---

## Step 3 — Multilinear algebra & (p,q) tensors *(outline)*

**Prerequisites:** Steps 1–2.

**Goals:**

- Define $(p,q)$-tensors as multilinear maps $(V^*)^p \times V^q \to \mathbb{R}$
- Tensor product, contraction, symmetries (sym / skew)
- Raising and lowering with a non-degenerate metric (full mixed-tensor API)
- Fully general change-of-basis for mixed tensors:
  $$
  T'^{i_1\ldots i_p}{}_{j_1\ldots j_q}
  = (P^{-1})^{i_1}{}_{a_1}\cdots P^{b_1}{}_{j_1}\cdots\,
    T^{a_1\ldots}{}_{b_1\ldots}
  $$

**Future modules:** `tensor_product`, `contract`, extended musical isomorphisms.

---

## Step 4 — Manifolds & tangent spaces *(outline)*

**Prerequisites:** Steps 1–3; multivariable calculus.

**Goals:**

- Smooth manifolds, charts, and atlases (intuitive + precise)
- Tangent vectors as derivations / equivalence classes of curves
- Cotangent space $T_p^*M$; differentials $df$
- Coordinate bases $\partial/\partial x^\mu$ and $dx^\mu$
- Pushforward and pullback

**Future modules:** `Chart`, `Manifold` (lightweight), `TangentVector`, `OneForm`.

---

## Step 5 — Riemannian / Lorentzian metrics *(outline)*

**Prerequisites:** Step 4.

**Goals:**

- Metric tensor field $g_{\mu\nu}(x)$
- Lengths of curves; causal character in Lorentzian signature
- Orthonormal / null frames; Minkowski space as local model
- Volume form $\sqrt{|\det g|}\,d^n x$

**Future modules:** `Metric`, `line_element`, signature helpers.

---

## Step 6 — Connections & Christoffel symbols *(outline)*

**Prerequisites:** Step 5.

**Goals:**

- Affine connection $\nabla$; covariant derivative of tensors
- Torsion and metric compatibility
- Levi-Civita connection uniquely fixed by $g$
- Christoffel symbols
  $$
  \Gamma^\sigma_{\mu\nu}
  = \tfrac12 g^{\sigma\rho}(\partial_\mu g_{\nu\rho}
  + \partial_\nu g_{\mu\rho} - \partial_\rho g_{\mu\nu})
  $$
- Geodesic equation $\ddot x^\sigma + \Gamma^\sigma_{\mu\nu}\dot x^\mu\dot x^\nu = 0$

**Future modules:** `Connection`, `christoffel`, `geodesic_rhs`.

---

## Step 7 — Curvature *(outline)*

**Prerequisites:** Step 6.

**Goals:**

- Riemann tensor from $[\nabla_U, \nabla_V] - \nabla_{[U,V]}$
- Component formula in terms of $\Gamma$ and $\partial\Gamma$
- Symmetries of $R^\rho{}_{\sigma\mu\nu}$; Ricci $R_{\mu\nu}$; scalar $R$
- Bianchi identities; geodesic deviation

**Future modules:** `riemann`, `ricci`, `scalar_curvature`.

---

## Step 8 — Einstein equation *(outline)*

**Prerequisites:** Step 7; stress-energy as a symmetric $(0,2)$ tensor.

**Goals:**

- Einstein tensor $G_{\mu\nu} = R_{\mu\nu} - \tfrac12 R g_{\mu\nu}$
- Field equation $G_{\mu\nu} + \Lambda g_{\mu\nu} = \kappa T_{\mu\nu}$
- Conservation $\nabla^\mu G_{\mu\nu} = 0$ ↔ $\nabla^\mu T_{\mu\nu} = 0$
- Classic solutions at a glance: Minkowski, Schwarzschild, FLRW (read-only)

**Future modules:** `einstein_tensor`, example metrics as fixtures — still
pedagogical, not a full GR simulator.

---

## Step 9+ — Optional extensions *(outline)*

- Differential forms, exterior derivative, Stokes
- Hodge dual; Maxwell in form language
- Cartan formalism (tetrads, spin connection)
- Linearized gravity and gravitational waves (weak field)

---

## Design principles (all steps)

1. **NumPy only** for numerics unless a later step explicitly justifies otherwise
   (Jupyter is an optional teaching frontend, not a math dependency).
2. **Objects before index soup** — then show indices as efficient notation.
3. **Invariants first** — every transform demo checks a scalar pairing.
4. **Lessons + examples + tests** for each implemented step.
