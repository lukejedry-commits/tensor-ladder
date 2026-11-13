# Tensor Series: Notation & Style Guide

This is the internal rulebook, not an episode. **Every symbol has one spelling, one color, and one meaning, starting in Episode 0.** If a new symbol is needed, add it here first, then to `tensor_style.py`.

Sources: eigenchris *Tensors for Beginners* (backbone: mechanics and index placement), cross-checked against 3Blue1Brown *Essence of Linear Algebra* (visual intuition for bases and change of basis) and Pavel Grinfeld / MathTheBeautiful (rigor of index notation). Tone: fun, but every equation on screen is correct and consistent.

Tested on **Manim Community v0.22.1**.

---

## 1. Symbol table

| Object | Written | LaTeX (`tensor_style` helper) | Color role |
|---|---|---|---|
| Vector (the geometric object) | $\mathbf{v}$, $\mathbf{u}$, … | `\mathbf{v}` (`VEC`, `bold("u")`) | vector |
| Second vector (when two appear together) | $\mathbf{w}$ | `bold("w")` | vector_2 |
| Component list *in a named basis* | $[\mathbf{v}]_{\mathbf{e}}$, $[\mathbf{v}]_{\tilde{\mathbf{e}}}$ | `tagged_components((1,3))`, `tagged_components((2,1), new=True)` | tag in text/vector/basis, column in component |
| Old basis vector | $\mathbf{e}_i$ | `\mathbf{e}_{i}` (`e("i")`) | basis |
| New basis vector | $\tilde{\mathbf{e}}_i$ | `\tilde{\mathbf{e}}_{i}` (`et("i")`) | new_basis |
| Vector component, old basis | $v^i$ | `v^{i}` (`vc("i")`) | component |
| Vector component, new basis | $\tilde{v}^i$ | `\tilde{v}^{i}` (`vct("i")`) | new_component |
| Covector (the object) | $\alpha$, $\gamma$, $\omega$ | `\alpha` (`COVEC`) | covector |
| Dual basis, old | $\epsilon^i$ | `\epsilon^{i}` (`eps("i")`) | dual_basis |
| Covector component, old | $\alpha_i$ | `\alpha_{i}` (`cc("i")`) | covector_component |
| Dual basis, new | $\tilde{\epsilon}^i$ | `\tilde{\epsilon}^{i}` (`epst("i")`) | new_dual_basis |
| Covector component, new | $\tilde{\alpha}_i$ | `\tilde{\alpha}_{i}` (`cct("i")`) | new_covector_component |
| Change-of-basis matrix (forward) | $\beth$, entries $\beth^i{}_j$ | `\beth`, `beth("i","j")` | beth |
| Backward matrix | $\beth^{-1}$, entries $(\beth^{-1})^i{}_j$ | `BETH_INV`, `beth_inv("i","j")` | beth |

**Hard rules**
- **Bold = object, plain = number.** $\mathbf{v}$ is an arrow; $v^1$ is a number that depends on a chosen basis. Components are never bold.
- **Tilde = "belongs to the new basis".** Never use primes ($\mathbf{e}'$): primes will mean derivatives in the tensor calculus episodes.
- **$\beth$** (Hebrew *beth*, said "beth", "b for basis", from `amssymb`) is only the change-of-basis matrix. Backward is always $\beth^{-1}$, never a new letter.
- **Covectors use Greek letters and are never bold.** Allowed: $\alpha, \gamma, \omega$ (and $\sigma, \phi, \psi$ if needed). **Never $\beta$** (too close to $\beth$, both visually and as a pun). $\epsilon$ is reserved for the dual basis.
- **General indices are $i, j, k$** (then $l, m$). Use explicit 1, 2, 3 only when computing a concrete example.
- **Index alphabets.** Latin indices $i, j, k, \dots$ are **spatial coordinates only**. Greek indices $\mu, \nu, \rho, \sigma$ are **spacetime** indices, with index $0$ = time (Minkowski 1+3; more spatial dimensions are possible later). Greek indices are introduced properly only when spacetime arrives. Until then, Episode 0 only teases them.
- **Never use a letter that already names an object or basis as an index.** That rules out $\alpha, \beta, \gamma, \epsilon, \omega$ (covectors, the dual basis, the banned $\beta$) and $e, v$, plus any letter we assign to an object later.
- Matrices are named with plain letters ($\beth$). Their entries carry staggered indices.
- **Never show a bare list for a vector.** A list of numbers is only meaningful with its basis, so every component list on screen is tagged: $[\mathbf{v}]_{\mathbf{e}} = \begin{pmatrix}1\\3\end{pmatrix}$, $[\mathbf{v}]_{\tilde{\mathbf{e}}} = \begin{pmatrix}2\\1\end{pmatrix}$ (use `tagged_components`). Writing $\mathbf{v} = \begin{pmatrix}1\\3\end{pmatrix}$ is allowed only as a crossed-out anti-example (Episode 1, Part 7). Generic programming-style lists like `[1, 3]` in typewriter font are not vectors and may appear as "what people think a vector is" (Episode 1 cold open).

## 2. Index rules

1. **Height means something.** Vector components go up ($v^i$). Basis vectors go down ($\mathbf{e}_i$). Covector components go down ($\alpha_i$). The dual basis goes up ($\epsilon^i$).
2. **Einstein summation.** An index that appears once up and once down in the same term is summed: $v^i\mathbf{e}_i \equiv \sum_i v^i\mathbf{e}_i$. Episode 0 shows the $\sum$ once, then fades it out, and it never comes back. Two uppers or two lowers on the same index is a mistake on screen. Fix it, don't sum it.
3. **Free indices must match on both sides** of every equation, at the same height.
4. **Staggered indices.** Write $\beth^i{}_j$ (LaTeX `\beth^{i}{}_{j}`). The first (upper) index is the **row** and the second (lower) is the **column**. Never stack them as $\beth^i_j$.
5. **Core transformation rules** (shown in this form every time):
   - basis (covariant): $\tilde{\mathbf{e}}_j = \beth^i{}_j\,\mathbf{e}_i$, so column $j$ of $\beth$ holds the old-basis coordinates of $\tilde{\mathbf{e}}_j$.
   - components (contravariant): $\tilde{v}^i = (\beth^{-1})^i{}_j\,v^j$
   - Later, for covectors: $\tilde{\alpha}_j = \beth^i{}_j\,\alpha_i$ and $\tilde{\epsilon}^i = (\beth^{-1})^i{}_j\,\epsilon^j$.
6. **Invariance statement** (the series thesis): $\mathbf{v} = v^i\mathbf{e}_i = \tilde{v}^i\tilde{\mathbf{e}}_i$. The object stays the same; its components change.

## 3. Color palette (dark background)

**The color rule.** Every **object** gets its own hue. Every **basis** gets a vivid hue. **Components are a pale tint of the basis they're measured in**, never the object's color, so "these numbers belong to those arrows" is visible at a glance. Old and new bases are **complementary pairs**: blue/orange on the vector side, violet/gold on the dual (covector) side.

| Role | Hex | Used for |
|---|---|---|
| background | `#14161C` | every scene |
| text | `#E8E8E8` | =, +, parentheses, numbers, ✓ |
| grid | `#3A4152` | NumberPlane lines |
| axis | `#8A93A6` | axes |
| **vector** (object) | `#FF3EA5` (hot pink) | $\mathbf{v}$ (and any other bold vector except $\mathbf{w}$), its arrow |
| **vector_2** (second vector) | `#C4378A` (dim hot pink) | $\mathbf{w}$ and its arrow, whenever a second vector shares the screen with $\mathbf{v}$ (sums, linear combinations, example arrows). Same hue family as the vector, darker (L≈47), so it still reads as "a vector" but is distinguishable; it is far from coral and red. `tmath` colors `\mathbf{w}` this way automatically, and `styled_vector(..., label=bold("w"))` picks it up as the default arrow color. Results like $\mathbf{v}+\mathbf{w}$ or $2\mathbf{v}-\mathbf{w}$ are drawn in the main vector pink. |
| **covector** (object) | `#2DD4BF` (teal) | $\alpha$ (no index), its level-line stack |
| **basis** | `#56B4E9` (sky blue) | $\mathbf{e}_i$ and their arrows |
| **component** | `#95D3F8` (light blue) | $v^i$. This is the pale tint `#B5E3FF` lerped 1/3 toward the basis blue `#56B4E9` (comp + (basis − comp)/3), so it reads clearly against white text. |
| **new_basis** | `#FF7F50` (coral/orange) | $\tilde{\mathbf{e}}_i$, their arrows, the new grid |
| **new_component** | `#FFB8A1` (pale coral) | $\tilde{v}^i$ |
| **dual_basis** | `#A78BFA` (violet) | $\epsilon^i$ and their stacks |
| **covector_component** | `#D6C9FF` (pale violet) | $\alpha_i$ |
| **new_dual_basis** | `#FFC21A` (gold) | $\tilde{\epsilon}^i$ and their stacks |
| **new_covector_component** | `#FFE88A` (pale gold) | $\tilde{\alpha}_i$ |
| **beth** | `#36D86C` (green) | $\beth$, $\beth^{-1}$, matrix entries |
| not_allowed | `#FF5A5A` (red, UI accent) | crosses / $\times$ on notation we never use |

`tmath` applies this automatically: $\mathbf{w}$ → vector_2, any other bold letter → vector, $\alpha$ with no index → covector (teal), $\alpha_i$ → covector_component, $\tilde{\alpha}_i$ → new_covector_component, $\epsilon^i$ → dual_basis, $\tilde{\epsilon}^i$ → new_dual_basis (same idea for $\gamma, \omega, \dots$). A group is colored by its first matching rule, so keep each symbol in its own group (e.g. write `COVEC, "(", VEC, ")"`, not one `\alpha(\mathbf{v})` group).

**Colorblind note.** A simulated color-vision check (Machado 2009 model; deuteranopia, protanopia, tritanopia) finds these near-collisions:
- **Deuteranopia:** $v^i$ (`#95D3F8`) vs $\alpha_i$ (`#D6C9FF`) are **nearly identical**. This is the closest pair in the whole palette, and the 1/3 lerp made it slightly closer than the old pale tint. Also hot-pink $\mathbf{v}$ vs teal $\alpha$. Not-allowed red vs beth green (only ever an × or a cross).
- **Protanopia:** $v^i$ vs $\alpha_i$ are again **nearly identical** (the closest pair), and pale gold $\tilde{\alpha}_i$ vs beth green.
- **Tritanopia** (rare): teal $\alpha$ vs beth green, and pale coral $\tilde{v}^i$ vs gold $\tilde{\epsilon}^i$.

With typical color vision, $v^i$ is now a bit closer to its basis blue $\mathbf{e}_i$ than before. Bold vs plain still separates them. None of these pairs is ever separated by color alone. $v^i$ vs $\alpha_i$ **must always be told apart by the letter (Latin vs Greek) and the index height (up vs down)**, and never by color alone. $\mathbf{v}$ vs $\alpha$ differ as bold Latin vs plain Greek, and $\beth$ is a unique glyph. So **color is always a second cue, never the only one**. Keep it that way: never introduce two symbols that differ *only* by color.

## 4. Typography (MathTex)

- Build every formula with **`tmath(...)`**, never a bare `MathTex`. It colors each piece by rule:
  `tmath(et("j"), "=", beth("i","j"), e("i"))` or
  `tmath(r"{{ \tilde{v}^i }} = {{ (\beth^{-1})^i{}_j }} {{ v^j }}")`.
- One **group** (argument or `{{ }}` block) = one symbol with its indices. Index letters take their symbol's color. To color something on its own (for example, to flash an index), put it in its own group.
- `tmath` splits groups itself (aware of brace depth) and passes them to `MathTex` as separate arguments, so nested braces like `\tilde{\mathbf{e}}` (which contain `}}`) never confuse Manim's double-brace splitter. Don't split `\left( … \right)` or `\frac{…}{…}` across groups.
- Use the same group structure in successive equations, so `TransformMatchingTex` can morph them cleanly.
- Sizes: `TEX_SIZE = 48` for equations and `LABEL_SIZE = 36` for arrow labels. Use `\,` before a summed partner when it helps readability ($\beth^i{}_j\,\mathbf{e}_i$).
- Plain words on screen use `Text`/`Tex` in `TEXT_COLOR`. Only math goes in `tmath`.

## 5. Animation conventions

**2D first.** Every concept gets a 2D episode or segment before its 3D version.

- **Plane:** `styled_plane()`: quiet grid (`GRID_COLOR`, width 1.5), muted axes, no ticks or numbers. Use `faded=True` when the plane is a backdrop for equations. The plane is the coordinate-free "space", and the basis arrows define coordinates.
- **Arrows:** the vector is thickest (`VECTOR_STROKE = 6`), basis arrows `5`, and covector lines `3`. Always use `buff=0`, from the origin unless the point is that vectors are free (`styled_vector(..., start=...)`).
- **Labels** sit just past the tip, offset perpendicular to the arrow (`label_direction` to override).
- **Covectors** are stacks of level lines (eigenchris's picture): `covector_stack((α1, α2), plane)` (teal by default) draws $\alpha_1x+\alpha_2y=k$ for integer $k$. The $k=0$ line is dimmed, and a small arrow shows the direction of increase. $\alpha(\mathbf{v})$ = the number of lines the arrow pierces. Denser stack = larger covector. Dual-basis stacks use `color=DUAL_BASIS_COLOR` (violet) or `NEW_DUAL_BASIS_COLOR` (gold).
- **Recipe walks:** `recipe_walk(components, basis_coords, plane, numbered=True)` draws $v^i\mathbf{e}_i$ tip-to-tail: whole steps of each basis vector (partial last step for fractions, backwards for negatives), optionally counted 1, 2, 3 in the component color (`number_color=NEW_COMPONENT_COLOR` for a new basis; `number_side=-1` puts counters on the right of the walk).
- **New-basis grid as an overlay (preferred from Episode 1):** `basis_grid(plane, b1, b2)` draws the coral lines of constant $\tilde{v}^1$ and $\tilde{v}^2$ on top of the (dimmed) old grid. Nothing is transformed, so the vector visibly stays put. Use this whenever the point is "same arrow, new ruler".
- **Change of basis:** draw $\tilde{\mathbf{e}}_j$ from the columns of $\beth$. To warp the grid, use `ApplyMatrix(B, plane)` where `B` is $\beth$ as a numpy array. The vector arrow **never moves** during a change of basis, only the grid, the basis, and the components do.
- **Voice-over timing (Episode 1 on):** captions are key phrases only. Each beat is wrapped in `with self.vo(n_words):` (`episode_base.EpisodeMixin`), which holds until the beat lasts about `n_words / 150` minutes, so the picture matches the narration paragraph it illustrates.
- **Pacing:** `RUN_TIME = 1.0`. `self.beat()` waits `PAUSE = 1.0` after a new idea, `PAUSE_SHORT = 0.5` between linked steps, and `PAUSE_LONG = 2.0` after a key result. Introduce one new symbol at a time and color-flash it (`Indicate`) the first time it appears.
- **3D:** `TensorThreeDScene` + `styled_axes_3d()`. Use `Arrow3D` for 3D vectors, with the same colors. Pin equations with `add_fixed_in_frame_mobjects`. Rotate the camera slowly (ambient rate ≤ 0.1 rad/s).
- **Fun, but grounded:** humor goes in narration, small character moments, and visual gags (like a vector "refusing" to move when the basis changes), never in the notation itself.

## 6. Episode 0: "How to read this series" (notation primer, ~6–8 min)

1. **Cold open (30 s):** one hot-pink arrow, two different grids snapping in beneath it, and two different pairs of numbers. "Same arrow. Different numbers. That's the whole series."
2. **Bold vs plain:** $\mathbf{v}$ (the arrow) vs $v^1, v^2$ (numbers that need a basis). Show $\mathbf{v} = v^1\mathbf{e}_1 + v^2\mathbf{e}_2$ with the color legend.
3. **Index height:** up for components, down for basis vectors. "Heights aren't exponents": $v^2$ means *component number 2*. State the rule once: an actual power always gets parentheses, $(v^2)^2$.
4. **Einstein summation:** $\sum_i v^i\mathbf{e}_i$ → the $\sum$ fades → $v^i\mathbf{e}_i$. Show a valid and an invalid (two uppers) example.
5. **The tilde:** a new basis $\tilde{\mathbf{e}}_i$ and new components $\tilde{v}^i$. Explain why we never use primes (a nod to derivatives later).
6. **Meet $\beth$:** Hebrew *beth*, "the **b**asis-changer". Staggered indices $\beth^i{}_j$ (row up, column down), and $\beth^{-1}$ going back. Preview $\tilde{\mathbf{e}}_j = \beth^i{}_j\mathbf{e}_i$ without deriving it.
7. **Greek = covector:** $\alpha, \gamma, \omega$ as stacks of lines and $\epsilon^i$ as the dual basis. "Never bold, never $\beta$."
8. **Legend card (end screen):** every color role in two parallel columns (vector side | dual side), plus the rules and the three transformation laws, to pause on. Pin it as a reference.

Episode 1 then builds "what a vector really is". Episode 2 derives $\beth$ (forward/backward transforms), and the rest follows eigenchris's order.

## 7. Episode 1: "What Is a Vector, Really?" (2D, ~7.5 min)

Script: `scripts/episode01_outline_and_script.md`. Code: `episode01.py` (scenes `E01_01_ColdOpen` … `E01_08_NextTime`, shared helpers in `episode_base.py`). Running example: $[\mathbf{v}]_{\mathbf{e}} = (1, 3)$, $[\mathbf{v}]_{\tilde{\mathbf{e}}} = (2, 1)$ with $\tilde{\mathbf{e}}_1 = \mathbf{e}_1 + \mathbf{e}_2$, $\tilde{\mathbf{e}}_2 = -\mathbf{e}_1 + \mathbf{e}_2$; then the doubled basis $\tilde{\mathbf{e}}_i = 2\mathbf{e}_i$ giving $(\tfrac12, \tfrac32)$, the contravariance hook into Episode 2, "Changing Basis (and Why Components Go Backwards)".
