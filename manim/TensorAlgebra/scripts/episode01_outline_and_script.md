# Episode 1: What Is a Vector, Really? (outline and voice-over script)

**Status:** an outline plus a narration draft only. No `episode01.py` exists yet.
**Target runtime:** about 9–10 minutes. That's ~1,125 narration words (≈ 7.5 min at 150 wpm) plus animation beats such as the recipe walks and grid fades. **2D only.**
**Continuity with Ep 0:** the same running example. $\mathbf{v}$ has old components $(1, 3)$ and new components $(2, 1)$, with $\beth = \begin{pmatrix}1&-1\\1&1\end{pmatrix}$, so $\tilde{\mathbf{e}}_1 = \mathbf{e}_1 + \mathbf{e}_2$ and $\tilde{\mathbf{e}}_2 = -\mathbf{e}_1 + \mathbf{e}_2$. Check: $2\tilde{\mathbf{e}}_1 + 1\tilde{\mathbf{e}}_2 = (2,2) + (-1,1) = (1,3)$ ✓.

## Sources and how they map to this episode
- **eigenchris, *Tensors for Beginners*,** the early episodes ("Tensor Definition", "Forward and Backward Transformations", "Vector definition", "Vector Transformation Rules"). He argues that a vector is an *invariant* object and that its components are *not* the vector. He builds the new basis from the old one with a forward matrix $F$ ($\tilde{\mathbf{e}}_j = F_{ij}\mathbf{e}_i$, whose columns are the new basis in old coordinates) and recovers the old basis with a backward matrix $B = F^{-1}$. **Our translation:** $F \to \beth$ (entries $\beth^i{}_j$, staggered) and $B \to \beth^{-1}$. His result that components transform with the *backward* matrix is Episode 2's payoff. Ep 1 only motivates it.
- **3Blue1Brown, *Essence of Linear Algebra*:** ch. 1 gives the three views of a vector (physics arrow, CS list, maths "anything you can add and scale"). Ch. 2 covers linear combinations, span and basis vectors, including the "bad basis" of two parallel vectors that only span a line. Ch. 3 reminds us that a *linear transformation* moves vectors. We do the opposite here (a *passive* change of description), and the script says so explicitly to head off a common confusion. (His later ch. 13, "Change of basis", is the natural cross-reference for Ep 2.)
- **Pavel Grinfeld (MathTheBeautiful), the geometric-vector viewpoint:** vectors are directed segments with geometric addition and scaling, defined *before* any coordinates. Coordinates are a convenience we choose, and invariant statements are the ones worth trusting. This shapes scenes 2 and 3.

## Visual vocabulary (from `tensor_style.py`, unchanged)
- `styled_vector(...)`: the vector, `VECTOR_COLOR` hot pink `#FF3EA5`, stroke 6. `start=` slides it (free vectors). Use `label=bold("w")` for a second vector $\mathbf{w}$.
- `basis_vector(i, ...)`: old basis, `BASIS_COLOR` `#56B4E9`. `new_basis_vector(i, ...)`: new basis, `NEW_BASIS_COLOR` coral `#FF7F50`.
- Components: `COMPONENT_COLOR` `#95D3F8` for $v^i$ and `NEW_COMPONENT_COLOR` `#FFB8A1` for $\tilde{v}^i$, via `tmath(vc("i"))` / `tmath(vct("i"))`.
- `styled_plane()` / `ep_plane()` (Ep 0 layout: plane on the left, equations on the right, captions at the bottom). `new_grid(plane)` from `episode00.py` draws the coral grid.
- `BETH_COLOR` green, used only in the closing teaser. `NOT_ALLOWED_COLOR` red for the "bad basis" cross.
- No covectors in this episode, except for one callback line in the cold open (optional).

---

## Scene list

| # | Class | Summary | Target |
|---|---|---|---|
| 1 | `E01_01_ColdOpen` | A list of numbers? An arrow? Something else? Three answers, one object. | 0:50 |
| 2 | `E01_02_TheArrowItself` | The vector as a coordinate-free arrow: direction plus length, free to slide, invariant. | 1:00 |
| 3 | `E01_03_AddAndScale` | Tip-to-tail addition, the parallelogram, and stretching/flipping/shrinking, all with no grid. | 1:30 |
| 4 | `E01_04_ChoosingABasis` | Pick $\mathbf{e}_1, \mathbf{e}_2$. Every arrow is a combination. The bad (parallel) basis fails. | 1:20 |
| 5 | `E01_05_ComponentsAsRecipe` | $\mathbf{v} = v^1\mathbf{e}_1 + v^2\mathbf{e}_2 = v^i\mathbf{e}_i$. Components as recipe amounts, $(1, 3)$, unique. | 1:30 |
| 6 | `E01_06_SameArrowNewBasis` | The coral basis from Ep 0. The same arrow is reached by $2\tilde{\mathbf{e}}_1 + 1\tilde{\mathbf{e}}_2$, giving $(2, 1)$. The arrow never moves. | 1:40 |
| 7 | `E01_07_ListVsArrow` | The punchline: a list means nothing without its basis. Double the basis and the components halve. | 1:20 |
| 8 | `E01_08_NextTime` | Recap in three lines, then the Episode 2 teaser: how exactly do components change? ($\beth$ vs $\beth^{-1}$) | 0:50 |
| | | **Total** | **≈ 10:00** |

---

## E01_01_ColdOpen (≈ 0:50)

**Visuals:** Three panels fade in left to right on `BG_COLOR`, each with a small heading (`Tex`, `AXIS_COLOR`):
1. "a list?": a column $\begin{pmatrix}1\\3\end{pmatrix}$ in `COMPONENT_COLOR`.
2. "an arrow?": a hot-pink `styled_vector` with no grid.
3. "something else?": $\mathbf{v}$, with "anything you can add and scale" in small text.

Then the column and the "something else" panel slide toward the arrow and merge into it. Title card: "**Episode 1: What Is a Vector, Really?**".

**Narration**
> Ask three people what a vector is and you'll get three answers. A computer scientist says it's a list of numbers. A physicist says it's an arrow, a direction with a length. And a mathematician says something slippery, like "it's anything you can add together and scale."
>
> [beat] Here's the thing. For what we're building, these aren't three different objects. They're three views of one object, and only one of them is the object itself. Today we figure out which one. And it's the reason tensors exist at all.

*89 words · read ≈ 36 s*

---

## E01_02_TheArrowItself (≈ 1:00)

**Visuals:** No plane and no grid, just the dark background. A pink $\mathbf{v}$ grows from a point. Then:
- A faint brace or arc labels "direction" and a measure line labels "length" (`Tex`, `AXIS_COLOR`).
- Copies of the same arrow slide around the screen with `styled_vector(..., start=...)`, unrotated and unstretched. Each copy gets a small "$=\mathbf{v}$" tag.
- One copy is rotated slightly and is crossed out in `NOT_ALLOWED_COLOR`: "different direction, different vector".
- End with one arrow and the caption "no coordinates required".

**Narration**
> Let's start with the arrow and strip everything else away. No grid. No axes. No numbers. Just this.
>
> An arrow like this is fully described by two things: which way it points, and how long it is. That's it. Where you draw it doesn't matter. Slide it over here, or over here. As long as you don't rotate it or stretch it, it's the same vector.
>
> [beat] But tilt it, even a little, and now it's a different vector.
>
> Notice what we haven't needed yet: coordinates. This arrow is a perfectly good geometric object all by itself. That's the heart of the matter. The vector exists first. Any numbers we attach to it come later, and they're our choice, not its.

*121 words · read ≈ 48 s*

**Note:** in this episode, vectors in the plane are *free* arrows (displacements), not points. Leave the curved-space subtlety (where you *can't* slide freely) for the tensor calculus arc. At most, add one line: "on a flat plane, at least. Hold that thought for much later."

---

## E01_03_AddAndScale (≈ 1:30)

**Visuals:** Still no grid. Two vectors: $\mathbf{v}$ in pink and $\mathbf{w}$ (`styled_vector(..., label=bold("w"))`). Pink is the "vector" role, so both are pink. They are told apart by their labels; optionally draw $\mathbf{w}$ at 70% opacity.
1. **Tip-to-tail:** $\mathbf{w}$ slides so its tail sits on $\mathbf{v}$'s tip, and the sum $\mathbf{v}+\mathbf{w}$ is drawn from $\mathbf{v}$'s tail to $\mathbf{w}$'s tip. Label it with `tmath(VEC, "+", bold("w"))`.
2. **Parallelogram:** the other order, $\mathbf{w}+\mathbf{v}$, lands on the same tip. Dashed sides complete the parallelogram. Show "$\mathbf{v}+\mathbf{w} = \mathbf{w}+\mathbf{v}$".
3. **Scaling:** $\mathbf{v}$ stretches to $2\mathbf{v}$, shrinks to $\tfrac12\mathbf{v}$, flips to $-\mathbf{v}$, and collapses to the zero vector, a dot labeled $\mathbf{0}$. The labels are `tmath("2", VEC)`, etc. The scalar is in `TEXT_COLOR`, because a scalar is a plain number, *not* a component.
4. **Linear combination:** $2\mathbf{v} - \mathbf{w}$ built tip-to-tail. Caption: "add and scale: that's all a vector space needs".

**Narration**
> So what can you do with arrows, before any numbers show up? Two things. You can add them, and you can scale them.
>
> To add v and w, slide w over so its tail sits on v's tip. The sum is the arrow from the very start to the very end. Tip to tail.
>
> Do it in the other order, w first and then v, and you land in exactly the same spot. The two routes trace out a parallelogram. So v plus w equals w plus v. No arithmetic required. It's just geometry.
>
> Scaling is even simpler. Two v is the same direction, twice as long. One-half v, half as long. Minus v points the opposite way. And zero times v shrinks all the way down to the zero vector, a single point.
>
> [beat] Put those together and you can build things like two v minus w. Adding and scaling: that's really all a vector needs to do. Mathematicians call any collection you can add and scale like this a *vector space*. Arrows in the plane are our first, friendliest example.

*182 words · read ≈ 73 s*

**Note:** in "two v", the 2 is a *scalar*, not a component. Keep it in `TEXT_COLOR` and say it out loud once. Viewers will otherwise blur scalars and components together, and Episode 2 depends on keeping them apart.

---

## E01_04_ChoosingABasis (≈ 1:20)

**Visuals:** `ep_plane()` fades in *underneath* the existing pink $\mathbf{v}$, which stays put. Two blue arrows, `basis_vector(1, (1,0))` and `basis_vector(2, (0,1))`, grow from the origin.
1. A few random pink arrows each decompose into "some $\mathbf{e}_1$" + "some $\mathbf{e}_2$" (dashed blue legs, as in Ep 0 Part 2).
2. **Bad basis:** replace $\mathbf{e}_2$ with an arrow parallel to $\mathbf{e}_1$. Every combination stays on one line, a highlighted `Line` labeled "span: just a line". $\mathbf{v}$ sits off that line and is unreachable. The parallel pair gets a red cross.
3. Restore $\mathbf{e}_2$. Caption: "a basis: two arrows that aren't parallel, which together reach everything".

**Narration**
> Now, arrows are lovely, but at some point you want to calculate. To calculate, you need a reference, a couple of arrows everyone agrees to measure against. That's a basis.
>
> Let's pick two, and call them e-sub-one and e-sub-two. They're bold, because they're arrows too. They're blue, because blue is our basis color. And notice what didn't happen: our pink vector didn't move. We just set up a ruler next to it.
>
> Any arrow in the plane can now be built from these two: some amount of e-sub-one, plus some amount of e-sub-two.
>
> [beat] But not every pair of arrows works. Suppose the second one is parallel to the first. Every combination of them lies on this one line. Our vector is off the line, so it can't be built at all. That pair fails.
>
> So, the rule: in the plane, a basis is two arrows that aren't parallel. Together they can reach everything, and there's exactly one way to reach each arrow.

*163 words · read ≈ 65 s*

---

## E01_05_ComponentsAsRecipe (≈ 1:30)

**Visuals:** The plane, blue basis and pink $\mathbf{v}$ = (1, 3) from Ep 0.
1. A "recipe walk": one copy of $\mathbf{e}_1$ is laid down from the origin, then three copies of $\mathbf{e}_2$ are stacked tip to tail. Each step ticks a counter in `COMPONENT_COLOR` ("1", then "1, 2, 3"). The walk ends exactly on $\mathbf{v}$'s tip.
2. The right panel builds in sequence (use `TransformMatchingTex` between them):
   - `tmath(VEC, "=", "1", e(1), "+", "3", e(2))`
   - `tmath(VEC, "=", vc(1), e(1), "+", vc(2), e(2))` with `tmath(vc(1), "= 1,", r"\qquad", vc(2), "= 3")` below it
   - `tmath(VEC, "=", vc("i"), e("i"))`, with the Ep 0 "up/down" arrows flashing briefly on the paired $i$'s
3. A component column $\begin{pmatrix}1\\3\end{pmatrix}$ in `COMPONENT_COLOR`, with a small blue tag "in the basis $\mathbf{e}_i$" attached beneath it.

**Narration**
> So how do we turn our arrow into numbers? Think of it as a recipe. How many steps of e-sub-one, and how many steps of e-sub-two, does it take to get to the tip of v?
>
> Watch: one step along e-sub-one. Then one, two, three steps along e-sub-two. And we land exactly on the tip.
>
> So v equals one e-sub-one plus three e-sub-two. Those amounts are the components. In our notation they're plain, not bold, because they're numbers, and their index goes up: v-super-one equals one, v-super-two equals three.
>
> Write the recipe in general, and it's v equals v-super-one e-sub-one plus v-super-two e-sub-two. Or, with Einstein's shortcut from Episode Zero, just v equals v-super-i e-sub-i. One index up, one down, summed.
>
> [beat] And because e-sub-one and e-sub-two aren't parallel, this recipe is the only one that works. So it's fair to stack the two numbers into a list: one, three. But look at that little tag underneath. These numbers are the recipe *in this basis*. Remember that tag. It's about to matter a lot.

*174 words · read ≈ 70 s*

---

## E01_06_SameArrowNewBasis (≈ 1:40)

**Visuals:**
1. The plane, $\mathbf{v}$, the blue basis, and the $(1, 3)$ column move to the upper right.
2. The coral basis from Ep 0 grows: `new_basis_vector(1, (1, 1))` and `new_basis_vector(2, (-1, 1))`, with `new_grid(plane)` fading in and the blue grid dimming. **Don't use `ApplyMatrix` on the plane** if $\mathbf{v}$ or the old arrows are part of it, since that would move them. Overlay the new grid instead (this matches the style guide's rule that the vector never moves).
3. A coral recipe walk: two copies of $\tilde{\mathbf{e}}_1$ tip to tail, then one copy of $\tilde{\mathbf{e}}_2$. It lands on the same tip.
4. The right panel shows `tmath(VEC, "=", "2", et(1), "+", "1", et(2))`, then `tmath(VEC, "=", vct("i"), et("i"))` with $\tilde{v}^1 = 2$, $\tilde{v}^2 = 1$, and a coral-tagged column $\begin{pmatrix}2\\1\end{pmatrix}$ "in the basis $\tilde{\mathbf{e}}_i$".
5. The boxed invariance line from Ep 0: `tmath(VEC, "=", vc("i"), e("i"), "=", vct("i"), et("i"))`.
6. Optional side note: "$\tilde{\mathbf{e}}_1 = \mathbf{e}_1 + \mathbf{e}_2$, $\tilde{\mathbf{e}}_2 = -\mathbf{e}_1 + \mathbf{e}_2$", with each new arrow decomposed in blue dashed legs. This is the first glimpse of what $\beth$'s columns mean, but don't name $\beth$ yet.

**Narration**
> Now, nothing forces us to use the blue basis. Somebody else might prefer these coral arrows, e-tilde-sub-one and e-tilde-sub-two. The tilde is our mark for "new basis."
>
> First, an important point. We're not moving the vector. We're not rotating or stretching the plane. We're only changing the ruler we hold up next to it. Same vector, new description.
>
> So what's the recipe now? Two steps along e-tilde-sub-one. Then one step along e-tilde-sub-two. And we land in exactly the same place.
>
> So in the new basis, v equals two e-tilde-sub-one plus one e-tilde-sub-two. The new components are v-tilde-super-one equals two, and v-tilde-super-two equals one.
>
> [beat] Put both descriptions side by side. v equals v-super-i e-sub-i, and v equals v-tilde-super-i e-tilde-sub-i. Two completely different lists, one and three versus two and one, and both of them describe the very same arrow. Notice the bold v: still no tilde. The vector didn't change. Our description did.

*153 words · read ≈ 61 s*

---

## E01_07_ListVsArrow (≈ 1:20)

**Visuals:**
1. The two columns, $(1, 3)$ with a blue tag and $(2, 1)$ with a coral tag, sit side by side. The tags fade out, and a big "?" appears between the untagged columns.
2. Show $\mathbf{v} = (1, 3)$ crossed out in `NOT_ALLOWED_COLOR`. Replace it with $\mathbf{v} \to (1, 3)$ in the blue basis (the Ep 0 "→" notation). See open decision #2.
3. **Contravariance teaser:** restore the blue basis and double it: $\tilde{\mathbf{e}}_i = 2\mathbf{e}_i$, so the coral arrows are twice as long. The recipe walk now needs half the steps: $\tilde{v}^1 = \tfrac12$, $\tilde{v}^2 = \tfrac32$. Show "basis ×2 → components ×½". The arrow, again, never moves.

**Narration**
> So here's the punchline. If I hand you the list "one, three" and nothing else, what vector did I give you? You can't know. Without the basis, those two numbers are a recipe without the ingredients.
>
> That's why, on this channel, we won't write "v equals one, three." The arrow and the list are not the same thing. The list is the arrow *as seen from* a particular basis.
>
> [beat] And here's something strange. Take the blue basis and double it, so every basis arrow is twice as long. Now how many steps does it take to reach v? Only half as many. The basis got bigger, and the components got smaller. They moved in opposite directions.
>
> Hold on to that. Components don't just change when the basis changes. They change the *opposite* way. That one observation is where the word "contravariant" comes from, and it's exactly where we're headed next.

*151 words · read ≈ 60 s*

---

## E01_08_NextTime (≈ 0:50)

**Visuals:**
1. A recap card with three lines (`Tex` plus `tmath`):
   - "the vector is the arrow: basis-independent" next to a pink arrow
   - "components are a recipe in a chosen basis: $\mathbf{v} = v^i\mathbf{e}_i$"
   - "change the basis, the components change; the arrow doesn't: $v^i\mathbf{e}_i = \tilde{v}^i\tilde{\mathbf{e}}_i$"
2. Teaser: the green $\beth$ fades in, with "$\tilde{\mathbf{e}}_j = \beth^i{}_j\,\mathbf{e}_i$" and "$\tilde{v}^i = \;?$" (a question mark in place of the right-hand side), then "**Episode 2: Changing Basis (and Why Components Go Backwards)**".

**Narration**
> Let's recap. A vector is the arrow itself. It doesn't depend on any basis. Its components are a recipe, written in a basis we choose. And when we change the basis, the recipe changes, but the arrow doesn't.
>
> Next time we make that precise. Remember beth, the basis-changer from Episode Zero? We'll see exactly how beth builds the new basis out of the old one. Then we'll answer the question we just ran into: if the basis changes by beth, how do the components change? Spoiler: backwards.
>
> See you in Episode Two.

*92 words · read ≈ 37 s*

---

## Narration total
**1,125 words ≈ 7.5 min** of speaking. With animation beats (recipe walks, the parallelogram, grid fades), the episode should land around **9–10 minutes**, inside the 8–12 minute target. If it runs short, the best places to expand are scene 3 (one more linear-combination example) and scene 6 (the optional decomposition of $\tilde{\mathbf{e}}_i$ in blue legs).

## New helpers worth adding to `tensor_style.py` (not implemented)
1. **`tip_to_tail(v_coords, w_coords, plane=None, start=(0,0))`:** returns the two arrows placed tip to tail plus the sum arrow (scene 3). It could also return the dashed parallelogram sides.
2. **`recipe_walk(components, basis_coords, plane, color)`:** lays down $\lfloor v^i \rfloor$ copies of each basis arrow tip to tail, and partial copies for fractional amounts (½, 3/2 in scene 7). Each step comes with a tick label for the counter. This is the core visual of scenes 5–7, and of Episode 2 too.
3. **`basis_grid(plane, b1, b2, color)`:** a general grid for any basis, promoting `new_grid()` out of `episode00.py` into the module (scenes 4, 6 and 7, including the doubled basis).
4. **`component_column(values, basis_tag, color)`:** a column vector $\begin{pmatrix}\cdot\\\cdot\end{pmatrix}$ in component color with a small attached "in the basis …" tag in basis color (scenes 5–7). This makes it hard to show a list without its basis.
5. **`span_line(plane, direction)`:** a highlighted infinite line for the "bad basis" span (scene 4).
6. *(Optional)* **`scalar_tex(...)`:** forces a coefficient to `TEXT_COLOR` inside `tmath`, so scalars like "2" in $2\mathbf{v}$ never inherit component color. Today, a bare "2" piece already stays `TEXT_COLOR`, so this is only for safety.
7. *(Optional)* Promote `ep_plane()`, `Ep0Mixin.caption()` and `part_title()` into a shared `episode_base.py`, so Episode 1 doesn't copy and paste them.

## Open decisions for Luke
1. **Whose components are "true"?** Ep 0 used "$\mathbf{v} \to (1,3)$". Ep 1 proposes banning "$\mathbf{v} = (1,3)$" on screen and always tagging a list with its basis. Do you like the `→` plus basis-tag convention, or would you prefer a bracket notation such as $[\mathbf{v}]_{\mathbf{e}} = (1,3)$? The bracket introduces a new symbol, which would need a style-guide entry.
2. **The doubled-basis teaser (scene 7):** keep it in Ep 1 as a cliffhanger, or save it for Ep 2? Keeping it makes the "contra" idea land a week earlier. Saving it gives Ep 2 a stronger cold open.
3. **The mathematician's "anything you can add and scale" in the cold open:** keep it as a one-liner (current plan), or skip abstract vector spaces until later?
4. **Two vectors in one color:** the "vector" role has one color, so $\mathbf{v}$ and $\mathbf{w}$ are both hot pink. Is a dimmer pink for $\mathbf{w}$ OK, or do you want a second-vector color (a new palette role)?
5. **Episode 2's title:** proposed "Changing Basis (and Why Components Go Backwards)". Rename if you like.
6. **Free vectors vs. points:** add the one-line "on a flat plane, at least" foreshadowing in scene 2, or leave curvature unmentioned for now?
