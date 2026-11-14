# Episode 0: How to Read This Series (voice-over script)

> **Audio source of truth:** the generated narration comes from `scripts/episode00_narration.py` (beat ids, ElevenLabs audio tags, spoken spellings like "v super i"). This `.md` stays the human-readable script. If you change a line here, change it there too, then run `python voiceover.py episode00 --only <beat>`. See `VOICEOVER.md`. Paragraphs below that carry two captions are split into two beats in the narration file. The runtimes below are the old caption-timed ones; with narration on, each beat lasts as long as its clip.

Synced to `episode00.py` as it exists now (8 scenes, preview runtime 5:11).
Read rate assumed: **~150 words/min**. The *Read* estimate counts only the narration (the `>` lines).

**How to use this script**
- **On screen** bullets quote the exact captions and equations in the order they appear. Each `>` block is what you say during that beat.
- `[beat]` means let the animation breathe, roughly half a second of silence.
- The captions currently stay up for about 0.25 s per word (`caption()` in `episode00.py`). Narration runs slower than that, so most scenes need longer holds (see the timing table at the end).

---

## Pronunciation and "how to say it" guide

| Written | Say it | Notes |
|---|---|---|
| $\mathbf{v}$ (bold) | "the vector v", or just "v" | Bold means an object. Say "vector" the first time in a scene. |
| $v^i$ | "v-super-i" | Upper index. **Always say "super" or "sub"**. Never "v-i", because later $v_i$ and $v^i$ are different things. |
| $v^1$, $v^2$ | "v-super-one", "v-super-two" | Never "v squared". That is the whole point of Part 3. |
| $(v^2)^2$ | "v-super-two, squared" | |
| $\mathbf{e}_i$ | "e-sub-i" | Basis vector, lower index. |
| $\tilde{\mathbf{e}}_i$ | "e-tilde-sub-i" | |
| $\tilde{v}^i$ | "v-tilde-super-i" | |
| tilde | "TIL-duh" | |
| $\beth$ | "beth" (rhymes with "death") | The LaTeX name and the usual math name. The Hebrew letter itself is *bet*; the Part 6 caption says "(bet)". See open decision #1. |
| $\beth^i{}_j$ | "beth, super-i, sub-j" | Staggered: row first, then column. |
| $\beth^{-1}$ | "beth inverse" | |
| $(\beth^{-1})^i{}_j$ | "beth-inverse, super-i, sub-j" | |
| covector | "CO-vector" | Stress on CO. |
| $\alpha$, $\gamma$, $\omega$ | "alpha", "gamma", "oh-MAY-guh" | |
| $\alpha_i$ | "alpha-sub-i" | |
| $\epsilon^i$ | "epsilon-super-i" ("EP-sih-lon") | The dual basis. |
| $\beta$ | "beta" ("BAY-tuh") | Only said in order to ban it. |
| Einstein summation | "EYEN-stine summation" | |
| $\Sigma$, $\sum$ | "sigma", "the sum over i" | |
| $\mu$, $\nu$ | "myoo", "noo" | Greek spacetime indices (teaser only). |
| contravariant | "CON-truh-VAIR-ee-unt" | |
| $\alpha(\mathbf{v})$ | "alpha of v" | |
| $f'(x)$ | "f-prime of x" | |

---

## E00_01_Intro: cold open (runtime 33.5 s)

**On screen:** the title "**Tensors, from the Ground Up**", then "Episode 0: How to Read This Series".
> Welcome to Tensors, from the Ground Up. This is Episode Zero, the instruction manual for everything that follows.

**On screen:** the grid draws in, a hot-pink arrow grows with its label $\mathbf{v}$. Caption: "Here is an arrow. It exists before anyone picks coordinates."
> Here's an arrow. Notice that nothing about it needs a grid. It points somewhere, it has a length, and it was here before anyone picked coordinates.

**On screen:** the blue $\mathbf{e}_1, \mathbf{e}_2$ arrows appear; the right panel shows "$\mathbf{v} \to (1, 3)$" over "measured with the blue basis". Caption: "Pick a basis, and the arrow becomes two numbers."
> Now pick a basis, these two blue arrows. Measured against them, our arrow becomes a pair of numbers: one, three.

**On screen:** the coral grid draws in, the blue basis fades, the coral $\tilde{\mathbf{e}}_1, \tilde{\mathbf{e}}_2$ grow; "$\mathbf{v} \to (2, 1)$" over "measured with the coral basis". Caption: "Pick a different basis, and you get different numbers."
> Pick a different basis, the coral one, and the very same arrow becomes two, one.

**On screen:** the arrow pulses. Caption: "Same arrow. Different numbers. **That is the whole series.**"
> [beat] The arrow never moved. Only the numbers changed. Same arrow, different numbers. Honestly, that's the whole series in one sentence.

**On screen:** caption "First, a quick guide to how we will write all of this down." Everything fades.
> But before we get there, we need to agree on how to write it all down. So: the house rules.

*Words 120 · Read ≈ 48 s · Runtime 33.5 s → gap +15 s: **lengthen** (≈ +15–20 s).*

---

## E00_02_BoldVsPlain: Part 2 (runtime 32.4 s)

**On screen:** title "Part 2 / **Bold vs. Plain**". The plane with $\mathbf{v}$; a large bold $\mathbf{v}$ on the right with "bold: the object itself". Caption: "A **bold** letter is a geometric object: an arrow, not a list of numbers."
> Rule one. When you see a bold letter, like this bold v, it means an object: the arrow itself, not a list of numbers.

**On screen:** the blue $\mathbf{e}_1, \mathbf{e}_2$ grow. Caption: "Basis vectors are objects too, so they are bold as well: $\mathbf{e}_1$ and $\mathbf{e}_2$."
> Basis vectors are arrows too, so they're bold as well: e-sub-one and e-sub-two.

**On screen:** "$\mathbf{v} = v^1\mathbf{e}_1 + v^2\mathbf{e}_2$"; a dashed blue line climbs from the tip of $\mathbf{e}_1$ up to the tip of $\mathbf{v}$. Caption: "Plain letters are *components*: just numbers, telling us how much of each basis vector to use."
> Now look at the plain letters: v-super-one and v-super-two. They're components, just numbers. They're the recipe: how much of e-sub-one, and how much of e-sub-two, it takes to build v.

**On screen:** "$v^1 = 1, \quad v^2 = 3$". Caption: "Components depend on the basis. Change the basis and they change. The bold arrow stays put."
> Here the recipe is one step along e-sub-one, then three steps along e-sub-two. But these numbers only make sense relative to this basis. Change the basis and the recipe changes. The bold arrow doesn't care.

**On screen:** a boxed card: $\mathbf{v}$ "object", $v^1$ "number". Caption: "Rule #1: **bold** means object, plain means number."
> So: bold means object, plain means number. Hold on to that one. It'll save you a lot of confusion.

*Words 121 · Read ≈ 48 s · Runtime 32.4 s → gap +16 s: **lengthen** (≈ +15–20 s).*

---

## E00_03_IndexHeight: Part 3 (runtime 42.2 s)

**On screen:** title "Part 3 / **Index Height Means Something**". Big $v^i$ with "upper index: vector components". Caption: "Components of a vector carry their index **up high**."
> Rule two: the height of an index means something. Components of a vector carry their index up high. v-super-i.

**On screen:** big $\mathbf{e}_i$ with "lower index: basis vectors". Caption: "Basis vectors carry their index **down low**."
> Basis vectors carry theirs down low. e-sub-i.

**On screen:** caption "Here $i$ is a label that can be 1 or 2 (or 3, once we reach 3D)."
> The letter i is just a label. It can be one or two in the plane, or three once we go 3D.

**On screen:** caption "Latin indices ($i, j, k$) mean space. Greek ($\mu, \nu$) are saved for spacetime."
> And a heads-up for much later: Latin letters like i, j and k count directions in space. Greek letters like mu and nu are reserved for spacetime. We won't need those for a while.

**On screen:** $v^2$ with "component number 2", next to $(v^2)^2$ with "an actual square: always in parentheses". Captions: "Careful: an upper index is *not* an exponent. $v^2$ is component number 2." and then "If we ever mean a square, we will use parentheses. No exceptions."
> Careful, though. An upper index is not an exponent. v-super-two means component number two, not v squared. If we ever do mean a square, you'll see parentheses: v-super-two, squared. No exceptions.

**On screen:** a 2×2 table with columns **vectors** / **covectors** and rows up / down: $v^i$, $\epsilon^i$ / $\mathbf{e}_i$, $\alpha_i$. Captions: "Vectors: components up, basis down." and then "Covectors (Part 7) flip it: components down, basis up. Keep this table handy."
> So for vectors, components go up and the basis goes down. In Part Seven we'll meet covectors, which flip it: components down, basis up. Keep this little table in your back pocket.

*Words 145 · Read ≈ 58 s · Runtime 42.2 s → gap +16 s: **lengthen** (≈ +15–20 s).*

---

## E00_04_Summation: Part 4 (runtime 39.0 s)

**On screen:** title "Part 4 / **Einstein Summation**". "$\mathbf{v} = v^1\mathbf{e}_1 + v^2\mathbf{e}_2$". Caption: "Writing out every term gets old fast, especially in 3D or with more indices."
> Rule three is a shortcut. Writing out every term like this gets old fast, and it only gets worse in 3D or with more indices.

**On screen:** it morphs into "$\mathbf{v} = \sum_{i=1}^{2} v^i\mathbf{e}_i$". Caption: "So first we compress it into a sum over $i$..."
> So first we squeeze it into a sum: v equals the sum over i of v-super-i e-sub-i.

**On screen:** the $\Sigma$ fades, leaving "$\mathbf{v} = v^i\mathbf{e}_i$". Caption: "...and then we drop the $\Sigma$ entirely. The sum is still there, just implied."
> And then we drop the sigma altogether. The sum is still happening. It's just implied.

**On screen:** "up" and "down" arrows point at the two $i$'s. The rule text: "**Rule:** an index repeated once *up* and once *down* in a term is summed." Caption: "This is the Einstein summation convention. From now on it is **always on**."
> How do you know? Look at the index i. It appears twice in the same term, once up and once down. That pattern means "sum over it." This is the Einstein summation convention, and from here on it's always on.

**On screen:** "$\alpha_i v^i$ ✓" with "one up, one down: a sum". Caption: "One up and one down: summed. This one shows up a lot."
> Alpha-sub-i, v-super-i: one down, one up. That's a sum. You'll see this one a lot.

**On screen:** "$v^i v^i$ ×" with "two uppers: not allowed". Caption: "Two uppers (or two lowers) on the same index: a mistake on screen, never a sum."
> But v-super-i, v-super-i, with both indices up? That's not a sum. On this channel, it's a mistake. If you ever see one on screen, call me out in the comments.

*Words 142 · Read ≈ 57 s · Runtime 39.0 s → gap +18 s: **lengthen** (≈ +20 s).*

---

## E00_05_Tilde: Part 5 (runtime 35.7 s)

**On screen:** title "Part 5 / **The Tilde: A New Basis**". The plane with $\mathbf{v}$ and the blue basis; "$\mathbf{v} = v^i\mathbf{e}_i$". Caption: "Here is our vector in the old basis."
> Rule four is about changing your point of view. Here's our vector, written in the old, blue basis: v equals v-super-i e-sub-i.

**On screen:** the coral grid and $\tilde{\mathbf{e}}_1, \tilde{\mathbf{e}}_2$ appear. Caption: "Now choose a **new** basis. We mark everything new with a tilde."
> Now we choose a new basis. Anything that belongs to the new basis gets a little squiggle on top, a tilde.

**On screen:** "$\mathbf{v} = \tilde{v}^i\tilde{\mathbf{e}}_i$". Caption: "New basis vectors get a tilde, and so do the new components."
> The new basis vectors are e-tilde-sub-i, and the new components are v-tilde-super-i.

**On screen:** "$\mathbf{v} = v^i\mathbf{e}_i = \tilde{v}^i\tilde{\mathbf{e}}_i$" in a box. Caption: "Notice that $\mathbf{v}$ has no tilde. The object never changes, only how we describe it."
> Put them together. Notice what's missing: the bold v has no tilde. The vector doesn't belong to either basis. Only our description of it changes.

**On screen:** $\mathbf{e}'_i$ crossed out in red, then $f'(x)$ fades in beside it. Captions: "Why not a prime, like many textbooks use?" and then "Because in tensor calculus a prime looks like a *derivative*. A tilde never does."
> Plenty of textbooks use a prime instead, e-prime-sub-i. We won't. Once we get to tensor calculus, a prime starts to look like a derivative, like f-prime of x. A tilde never does. So: tilde, always.

*Words 115 · Read ≈ 46 s · Runtime 35.7 s → gap +10 s: **lengthen slightly** (≈ +10 s; the two prime beats can absorb some).*

---

## E00_06_Beth: Part 6 (runtime 50.1 s)

**On screen:** title "Part 6 / **Meet ℶ, the Basis-Changer**". A huge green $\beth$. Captions: "This is $\beth$ (*bet*), the second letter of the Hebrew alphabet. It sounds like "b"." and then "B for **basis**: $\beth$ is our change-of-basis matrix."
> Rule five: meet beth. It's the second letter of the Hebrew alphabet, and it makes a "b" sound. B, for basis. Beth is our change-of-basis matrix. Every time we switch bases, beth is the machine that does it.

**On screen:** "$\beth = \begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix}$". Caption: "Each column holds a new basis vector, written in old coordinates."
> For our coral basis, beth is this matrix. Read it column by column. The first column, one, one, is e-tilde-sub-one written in the old basis. The second column, minus one, one, is e-tilde-sub-two.

**On screen:** big $\beth^i{}_j$, with an arrow labeled "row" at the upper $i$ and one labeled "column" at the lower $j$. Caption: "Its entries have **staggered** indices: the first is the row, the second is the column."
> Its entries get staggered indices: beth, super-i, sub-j. The upper index comes first and picks the row. The lower one comes second and picks the column. The stagger tells you which is which.

**On screen:** "$\tilde{\mathbf{e}}_j = \beth^i{}_j\mathbf{e}_i$" with "forward: old basis → new basis". Caption: "$\beth$ builds the new basis out of the old one. Note: $i$ is summed, and $j$ is free on both sides."
> Going forward, beth builds the new basis from the old: e-tilde-sub-j equals beth, super-i, sub-j, e-sub-i. The index i shows up once up and once down, so it's summed. The index j is free, and it sits low on both sides, exactly as it should.

**On screen:** "$\tilde{v}^i = (\beth^{-1})^i{}_j v^j$" with "backward: components use $\beth^{-1}$". Caption: "Components go the *other* way, with the inverse $\beth^{-1}$. Hence "contra"-variant."
> And here's the twist. The components go the other way, with beth inverse: v-tilde-super-i equals beth-inverse, super-i, sub-j, v-super-j. They move against the basis. That's where the word contravariant comes from.

**On screen:** "$\begin{pmatrix}2\\1\end{pmatrix} = \tfrac{1}{2}\begin{pmatrix}1&1\\-1&1\end{pmatrix}\begin{pmatrix}1\\3\end{pmatrix}$". Captions: "Our arrow: old components $(1, 3)$ become new components $(2, 1)$. Same arrow, as promised." and then "We will derive all of this properly in Episode 2. For now, just learn the names."
> Check it with our arrow. Beth inverse takes the old components, one, three, and gives two, one, the exact numbers from the cold open. Same arrow, as promised. We'll derive all of this properly in Episode Two. For today, just learn the names.

*Words 223 · Read ≈ 89 s · Runtime 50.1 s → gap +39 s: **lengthen most** (≈ +40 s), or trim the forward/backward lines.*

---

## E00_07_Covectors: Part 7 (runtime 60.1 s)

**On screen:** title "Part 7 / **Greek Letters Mean Covectors**". Teal "$\alpha, \gamma, \omega$". Caption: "Covectors get Greek letters. They are **never** bold, so they cannot be mistaken for vectors."
> Rule six: Greek letters, like alpha, gamma and omega, mean covectors. They're never bold, so you can't mistake one for a vector.

**On screen:** $\beta$ appears and gets crossed out. Caption: "And never $\beta$: it is too easy to confuse with our $\beth$."
> And we never use beta. It's far too easy to confuse with beth.

**On screen:** the plane with $\mathbf{v}$; a teal stack of slanted lines draws in with a small direction arrow; a teal $\alpha$ on the right. Caption: "Picture a covector as a **stack of lines**, with a direction in which its value grows."
> So what is a covector? Picture a stack of evenly spaced lines, with an arrow showing which way the value goes up.

**On screen:** two teal dots on the arrow, at line 1 and at the tip on line 2; "$\alpha(\mathbf{v}) = 2$". Caption: "Feed it a vector, and you get a number: how many lines the arrow pierces. Here, 2."
> Feed it a vector and it hands you back a number: how many lines the arrow crosses. Our arrow crosses one, and lands right on two. So alpha of v is two.

**On screen:** the teal stack dims, a violet vertical stack draws in with "$\epsilon^1, \epsilon^2$"; it turns into a horizontal stack. Captions: "Covectors have their own basis, the **dual basis** $\epsilon^i$, with the index *up*." and then "$\epsilon^1$ counts steps of $\mathbf{e}_1$, and $\epsilon^2$ counts steps of $\mathbf{e}_2$."
> Covectors get their own basis, called the dual basis: epsilon-super-i, with the index up. Epsilon-super-one counts steps along e-sub-one. Epsilon-super-two counts steps along e-sub-two.

**On screen:** "$\alpha = \alpha_1\epsilon^1 + \alpha_2\epsilon^2$" morphs into "$\alpha = \alpha_i\epsilon^i$". Caption: "Components of a covector carry their index *down*: $\alpha_i$. Exactly the reverse of vectors."
> Any covector is a recipe made of those: alpha equals alpha-sub-i epsilon-super-i. And notice the heights. The components are down this time, exactly the reverse of vectors.

**On screen:** "$\alpha(\mathbf{v}) = \alpha_i v^i = 2$". Caption: "And one up, one down means a sum: $\alpha_i v^i = (-1)(1) + (1)(3) = 2$. It matches the picture."
> Put a covector and a vector together and the indices pair up, one down and one up, so it's a sum. Minus one times one, plus one times three: two. The same number we counted from the picture.

*Words 178 · Read ≈ 71 s · Runtime 60.1 s → gap +11 s: **lengthen slightly** (≈ +10–15 s; the line-drawing beats overlap well with narration).*

---

## E00_08_Recap: Part 8, the legend (runtime 18.1 s)

**On screen:** "**The Legend**: pause here any time". Two columns of swatches (vector side | dual side): vector (object), old basis, old components, new basis, new components, change of basis ($\beth^{-1}$ back) | covector (object), old dual basis, old covector components, new dual basis, new covector components, not allowed. Then the rules and "$\tilde{\mathbf{e}}_j = \beth^i{}_j\mathbf{e}_i$", "$\tilde{v}^i = (\beth^{-1})^i{}_j v^j$", "$\tilde{\alpha}_j = \beth^i{}_j\alpha_i$".
> That's the whole rulebook. Here it is on one card. Every object has its own color, every basis has a bold, vivid color, and components are a paler tint of the basis they're measured in. Pause here any time you get lost. I'll pin it in the description, too.

**On screen:** "Next time / **Episode 1: What Is a Vector, Really?**", and a pink arrow grows.
> Next time, we slow way down and ask a question that sounds too simple to be interesting: what is a vector, really? See you there.

*Words 74 · Read ≈ 30 s · Runtime 18.1 s → gap +12 s: **lengthen** the legend hold (≈ +12 s; the card should stay up anyway).*

---

## Timing summary

| Scene | Runtime now | Narration words | Read @150 wpm | Gap | Action |
|---|---|---|---|---|---|
| E00_01_Intro | 33.5 s | 120 | 48 s | +15 s | lengthen |
| E00_02_BoldVsPlain | 32.4 s | 121 | 48 s | +16 s | lengthen |
| E00_03_IndexHeight | 42.2 s | 145 | 58 s | +16 s | lengthen |
| E00_04_Summation | 39.0 s | 142 | 57 s | +18 s | lengthen |
| E00_05_Tilde | 35.7 s | 115 | 46 s | +10 s | lengthen slightly |
| E00_06_Beth | 50.1 s | 223 | 89 s | +39 s | lengthen most / trim |
| E00_07_Covectors | 60.1 s | 178 | 71 s | +11 s | lengthen slightly |
| E00_08_Recap | 18.1 s | 74 | 30 s | +12 s | lengthen |
| **Total** | **5:11** | **1,118** | **≈ 7:27** | **+≈ 2:16** | |

Read time is pure speaking time. Leave about 10–20% more for the `[beat]` pauses, so a narrated Episode 0 should land around **8–9 minutes**. That matches the 6–8 minute target in the style guide's outline, or runs slightly over it.

**Every scene runs short of its narration.** That's expected, since the captions are timed for silent reading. Recommended fix (no code changed yet): record the voice-over first, then replace each `caption()` hold with that beat's measured VO length. One way to do it is a `wait=` per beat, taken from a small per-scene list of timings. The alternative is trimming the narration by about 30%, which would cost a lot of the warmth.

## Open decisions for Luke
1. **Say "beth" or "bet"?** The script says "beth", the standard math name and the LaTeX name. The Part 6 caption shows "(bet)", the Hebrew name. Either keep both ("beth, in Hebrew *bet*") or pick one and change the caption.
2. **Keep the on-screen captions once there's a voice-over?** Full-sentence captions duplicate the narration. Options: keep them as built-in subtitles, cut them down to key phrases, or turn them off and rely on YouTube CC.
3. **The comments call-out** in Part 4 ("call me out in the comments"): keep it or cut it, depending on how chatty you want the channel to be.
