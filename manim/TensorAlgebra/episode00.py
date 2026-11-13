"""
Episode 0: How to Read This Series (the notation primer).

One TensorScene per part of the Episode 0 outline in STYLE_GUIDE.md.
Render one part:   manim -ql episode00.py E00_04_Summation
Render all parts:  manim -ql -a episode00.py

On-screen captions stand in for narration. They use Tex (Computer Modern)
so the video looks the same on any machine, with no system fonts needed.

Running example (used in every part):
    old basis   e_1 = (1, 0),  e_2 = (0, 1)
    new basis   ~e_1 = e_1 + e_2,  ~e_2 = -e_1 + e_2
    so beth = [[1, -1], [1, 1]]   (columns = new basis in old coordinates)
    the vector  v = 1 e_1 + 3 e_2 = 2 ~e_1 + 1 ~e_2
    covector    alpha = -1 eps^1 + 1 eps^2,  so alpha(v) = 2
"""

import re

from manim import *
from tensor_style import *

# --------------------------------------------------------------------------
# Running example numbers
# --------------------------------------------------------------------------
V_OLD = (1, 3)                 # v^1, v^2
V_NEW = (2, 1)                 # ~v^1, ~v^2
E_NEW = ((1, 1), (-1, 1))      # ~e_1, ~e_2 in old coordinates (columns of beth)
ALPHA = (-1, 1)                # alpha_1, alpha_2

CAPTION_SIZE = 32


# --------------------------------------------------------------------------
# Shared layout helpers
# --------------------------------------------------------------------------
def ep_plane() -> NumberPlane:
    """The episode's 2D plane, on the left half of the frame."""
    plane = styled_plane(x_range=(-3, 3, 1), y_range=(-1, 4, 1))
    plane.move_to(LEFT * 3.6 + UP * 0.05)
    return plane


def new_grid(plane: NumberPlane, opacity: float = 0.45) -> VGroup:
    """The new-basis grid: level lines of ~eps^1 and ~eps^2 (rows of beth^-1)."""
    region = (plane.x_range[0], plane.x_range[1], plane.y_range[0], plane.y_range[1])
    g = VGroup(
        covector_stack((0.5, 0.5), plane, color=NEW_BASIS_COLOR, show_direction=False, region=region),
        covector_stack((-0.5, 0.5), plane, color=NEW_BASIS_COLOR, show_direction=False, region=region),
    )
    g.set_stroke(width=1.5, opacity=opacity)
    return g


def right_panel(mob: Mobject, y: float = 1.0) -> Mobject:
    """Center a mobject in the right half of the frame."""
    return mob.move_to(RIGHT * 3.4 + UP * y)


def words(text: str, size: float = CAPTION_SIZE, color=TEXT_COLOR) -> Tex:
    return Tex(text, font_size=size, color=color)


class Ep0Mixin:
    """Adds one caption line at the bottom of the frame (in place of narration)."""

    caption_mob = None

    def caption(self, text: str, wait: float = PAUSE):
        """Swap in a new caption, then hold it long enough to read.

        Hold time = max(wait, reading time), reading time ~0.25 s per word.
        """
        new = words(text).to_edge(DOWN, buff=0.45)
        if new.width > config.frame_width - 1:
            new.scale_to_fit_width(config.frame_width - 1)
        if self.caption_mob is None:
            self.play(FadeIn(new, shift=UP * 0.15), run_time=0.6)
        else:
            self.play(FadeOut(self.caption_mob, shift=UP * 0.15),
                      FadeIn(new, shift=UP * 0.15), run_time=0.6)
        self.caption_mob = new
        n_words = len(re.sub(r"\\[a-zA-Z]+|[${}]", " ", text).split())
        self.beat(max(wait, PAUSE_SHORT + 0.25 * n_words))

    def clear_caption(self):
        if self.caption_mob is not None:
            self.play(FadeOut(self.caption_mob), run_time=0.4)
            self.caption_mob = None

    def part_title(self, number: int, title: str):
        t = VGroup(
            words(rf"Part {number}", size=24, color=AXIS_COLOR),
            words(rf"\textbf{{{title}}}", size=40),
        ).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.25)
        self.play(FadeIn(t, shift=DOWN * 0.2), run_time=0.8)
        return t

    def check(self, mob: Mobject, good: bool) -> Mobject:
        """Checkmark or cross next to a mobject."""
        if good:
            mark = MathTex(r"\checkmark", color=TEXT_COLOR, font_size=48)
        else:
            mark = MathTex(r"\times", color=NOT_ALLOWED_COLOR, font_size=56)
        return mark.next_to(mob, RIGHT, buff=0.35)


# --------------------------------------------------------------------------
# Part 1: Cold open
# --------------------------------------------------------------------------
class E00_01_Intro(Ep0Mixin, TensorScene):
    """Same arrow, two bases, two pairs of numbers: the thesis of the series."""

    def construct(self):
        title = VGroup(
            words(r"\textbf{Tensors, from the Ground Up}", size=60),
            words(r"Episode 0: How to Read This Series", size=36, color=AXIS_COLOR),
        ).arrange(DOWN, buff=0.35)
        self.play(Write(title[0]), run_time=1.5)
        self.play(FadeIn(title[1], shift=UP * 0.2))
        self.beat(PAUSE_LONG)
        self.play(FadeOut(title))

        plane = ep_plane()
        v = styled_vector(V_OLD, plane)
        self.play(Create(plane, lag_ratio=0.05), run_time=1.5)
        self.play(GrowArrow(v.arrow), FadeIn(v.label))
        self.caption(r"Here is an arrow. It exists before anyone picks coordinates.")

        # Old basis: numbers (1, 3)
        e1, e2 = basis_vector(1, (1, 0), plane), basis_vector(2, (0, 1), plane)
        self.play(GrowArrow(e1.arrow), GrowArrow(e2.arrow), FadeIn(e1.label), FadeIn(e2.label))
        old_nums = right_panel(tmath(VEC, r"\;\to\;", "(", "1", ",", "3", ")",
                                     colors={"1": COMPONENT_COLOR, "3": COMPONENT_COLOR}), y=1.2)
        old_tag = words("measured with the blue basis", size=28, color=BASIS_COLOR).next_to(old_nums, DOWN, buff=0.25)
        self.play(Write(old_nums), FadeIn(old_tag))
        self.caption(r"Pick a basis, and the arrow becomes two numbers.")

        # New basis: numbers (2, 1)
        grid = new_grid(plane)
        te1, te2 = new_basis_vector(1, E_NEW[0], plane), new_basis_vector(2, E_NEW[1], plane)
        self.play(plane.background_lines.animate.set_stroke(opacity=0.15),
                  Create(grid, lag_ratio=0.05), run_time=1.5)
        self.play(FadeOut(e1), FadeOut(e2), GrowArrow(te1.arrow), GrowArrow(te2.arrow),
                  FadeIn(te1.label), FadeIn(te2.label))
        new_nums = right_panel(tmath(VEC, r"\;\to\;", "(", "2", ",", "1", ")",
                                     colors={"2": NEW_COMPONENT_COLOR, "1": NEW_COMPONENT_COLOR}), y=-0.4)
        new_tag = words("measured with the coral basis", size=28, color=NEW_BASIS_COLOR).next_to(new_nums, DOWN, buff=0.25)
        self.play(Write(new_nums), FadeIn(new_tag))
        self.caption(r"Pick a different basis, and you get different numbers.")
        self.play(Indicate(v.arrow, color=VECTOR_COLOR, scale_factor=1.05))
        self.caption(r"Same arrow. Different numbers. \textbf{That is the whole series.}", wait=PAUSE_LONG)

        self.caption(r"First, a quick guide to how we will write all of this down.")
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.caption_mob = None


# --------------------------------------------------------------------------
# Part 2: Bold vs plain
# --------------------------------------------------------------------------
class E00_02_BoldVsPlain(Ep0Mixin, TensorScene):
    """Bold = the geometric object; plain = numbers that need a basis."""

    def construct(self):
        title = self.part_title(2, "Bold vs.\\ Plain")
        plane = ep_plane()
        # e_1's label goes below the tip so the dashed 3*e_2 step can't cross it
        e1 = basis_vector(1, (1, 0), plane, label_direction=DOWN)
        e2 = basis_vector(2, (0, 1), plane)
        v = styled_vector(V_OLD, plane)
        self.play(FadeIn(plane), GrowArrow(v.arrow), FadeIn(v.label))

        bold_v = right_panel(tmath(VEC, font_size=96), y=1.3)
        tag_obj = words("bold: the object itself", size=30, color=VECTOR_COLOR).next_to(bold_v, DOWN, buff=0.3)
        self.play(Write(bold_v), FadeIn(tag_obj))
        self.caption(r"A \textbf{bold} letter is a geometric object: an arrow, not a list of numbers.")

        self.play(GrowArrow(e1.arrow), GrowArrow(e2.arrow), FadeIn(e1.label), FadeIn(e2.label))
        self.caption(r"Basis vectors are objects too, so they are bold as well: $\mathbf{e}_1$ and $\mathbf{e}_2$.")

        eq = right_panel(tmath(VEC, "=", vc(1), e(1), "+", vc(2), e(2)), y=1.3)
        self.play(FadeOut(tag_obj), TransformMatchingTex(bold_v, eq))
        # tip-to-tail picture: 1 step of e_1, then 3 steps of e_2
        step2 = DashedLine(plane.c2p(1, 0), plane.c2p(1, 3), color=BASIS_COLOR, stroke_width=3)
        self.play(Create(step2), run_time=1.2)
        self.caption(r"Plain letters are \emph{components}: just numbers, telling us how much of each basis vector to use.")

        nums = right_panel(tmath(vc(1), "= 1,", r"\qquad", vc(2), "= 3"), y=0.0)
        self.play(Write(nums))
        self.caption(r"Components depend on the basis. Change the basis and they change. The bold arrow stays put.", wait=PAUSE_LONG)

        rule = VGroup(
            tmath(r"\mathbf{v}", font_size=60), words("object", size=30),
            tmath(r"v^1", font_size=60), words("number", size=30),
        )
        rule.arrange_in_grid(rows=2, cols=2, col_alignments="cc", buff=(1.2, 0.2), flow_order="dr")
        box = SurroundingRectangle(rule, color=AXIS_COLOR, buff=0.3, corner_radius=0.1)
        card = right_panel(VGroup(rule, box), y=-1.6)
        self.play(FadeIn(card, shift=UP * 0.2))
        self.caption(r"Rule \#1: \textbf{bold} means object, plain means number.", wait=PAUSE_LONG)
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.caption_mob = None


# --------------------------------------------------------------------------
# Part 3: Index height
# --------------------------------------------------------------------------
class E00_03_IndexHeight(Ep0Mixin, TensorScene):
    """Up = components, down = basis vectors; heights are labels, not powers."""

    def construct(self):
        title = self.part_title(3, "Index Height Means Something")

        up = tmath(vc("i"), font_size=90)
        down = tmath(e("i"), font_size=90)
        pair = VGroup(up, down).arrange(RIGHT, buff=3).move_to(UP * 0.9)
        up_tag = words(r"upper index:\\vector components", size=30, color=COMPONENT_COLOR).next_to(up, DOWN, buff=0.4)
        down_tag = words(r"lower index:\\basis vectors", size=30, color=BASIS_COLOR).next_to(down, DOWN, buff=0.4)
        self.play(Write(up), FadeIn(up_tag))
        self.caption(r"Components of a vector carry their index \textbf{up high}.")
        self.play(Write(down), FadeIn(down_tag))
        self.caption(r"Basis vectors carry their index \textbf{down low}.")
        self.caption(r"Here $i$ is a label that can be 1 or 2 (or 3, once we reach 3D).")
        self.caption(r"Latin indices ($i, j, k$) mean space. Greek ($\mu, \nu$) are saved for spacetime.")

        # Heights are not exponents
        self.play(FadeOut(VGroup(up, down, up_tag, down_tag)))
        comp2 = tmath(vc(2), font_size=80)
        sq = tmath("(", vc(2), ")^2", font_size=80)
        row = VGroup(comp2, sq).arrange(RIGHT, buff=3).move_to(UP * 0.9)
        comp2_tag = words(r"``component number 2''", size=30).next_to(comp2, DOWN, buff=0.4)
        sq_tag = words(r"an actual square:\\always in parentheses", size=30).next_to(sq, DOWN, buff=0.4)
        self.play(Write(comp2), FadeIn(comp2_tag))
        self.caption(r"Careful: an upper index is \emph{not} an exponent. $v^2$ is component number 2.")
        self.play(Write(sq), FadeIn(sq_tag))
        self.caption(r"If we ever mean a square, we will use parentheses. No exceptions.", wait=PAUSE_LONG)

        # Preview of the full height table
        self.play(FadeOut(VGroup(comp2, sq, comp2_tag, sq_tag)))
        table = VGroup(
            words(""), words(r"\textbf{vectors}", size=30), words(r"\textbf{covectors}", size=30),
            words("up", size=30, color=AXIS_COLOR), tmath(vc("i")), tmath(eps("i")),
            words("down", size=30, color=AXIS_COLOR), tmath(e("i")), tmath(cc("i")),
        ).arrange_in_grid(rows=3, cols=3, buff=(1.2, 0.5))
        table.move_to(UP * 0.5)
        self.play(FadeIn(table[:5]), FadeIn(table[6:8]))
        self.caption(r"Vectors: components up, basis down.")
        self.play(FadeIn(table[5]), FadeIn(table[8]))
        self.caption(r"Covectors (Part 7) flip it: components down, basis up. Keep this table handy.", wait=PAUSE_LONG)
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.caption_mob = None


# --------------------------------------------------------------------------
# Part 4: Einstein summation
# --------------------------------------------------------------------------
class E00_04_Summation(Ep0Mixin, TensorScene):
    """The explicit sum fades into Einstein's shorthand; valid vs invalid examples."""

    def construct(self):
        title = self.part_title(4, "Einstein Summation")

        full = tmath(VEC, "=", vc(1), e(1), "+", vc(2), e(2), font_size=60).move_to(UP * 0.8)
        self.play(Write(full))
        self.caption(r"Writing out every term gets old fast, especially in 3D or with more indices.")

        sigma = tmath(VEC, "=", r"\sum_{i=1}^{2}", vc("i"), e("i"), font_size=60).move_to(UP * 0.8)
        self.play(TransformMatchingTex(full, sigma), run_time=1.5)
        self.caption(r"So first we compress it into a sum over $i$...")

        short = tmath(VEC, "=", vc("i"), e("i"), font_size=60).move_to(UP * 0.8)
        self.play(sigma[2].animate.set_opacity(0.0), run_time=1.2)
        self.play(TransformMatchingTex(sigma, short), run_time=1.0)
        self.caption(r"...and then we drop the $\Sigma$ entirely. The sum is still there, just implied.")

        # Point at the two i's: one up, one down
        i_up = short[2][1]
        i_down = short[3][1]
        up_lbl = words("up", size=28, color=COMPONENT_COLOR).next_to(i_up, UP, buff=0.55)
        down_lbl = words("down", size=28, color=BASIS_COLOR).next_to(i_down, DOWN, buff=0.55)
        r1 = VGroup(up_lbl, Arrow(up_lbl.get_bottom(), i_up.get_top(), buff=0.08,
                                  color=COMPONENT_COLOR, stroke_width=3,
                                  max_tip_length_to_length_ratio=0.35))
        r2 = VGroup(down_lbl, Arrow(down_lbl.get_top(), i_down.get_bottom(), buff=0.08,
                                    color=BASIS_COLOR, stroke_width=3,
                                    max_tip_length_to_length_ratio=0.35))
        self.play(FadeIn(r1, shift=DOWN * 0.1), FadeIn(r2, shift=UP * 0.1))
        self.play(Indicate(i_up, color=COMPONENT_COLOR), Indicate(i_down, color=BASIS_COLOR))
        rule = words(r"\textbf{Rule:} an index repeated once \emph{up} and once \emph{down} in a term is summed.",
                     size=32).next_to(short, DOWN, buff=1.5)
        self.play(FadeIn(rule, shift=UP * 0.2))
        self.caption(r"This is the Einstein summation convention. From now on it is \textbf{always on}.", wait=PAUSE_LONG)
        self.play(FadeOut(VGroup(r1, r2, rule)), short.animate.scale(0.75).move_to(UP * 1.6))

        # Valid vs invalid
        good = tmath(cc("i"), vc("i"), font_size=56)
        bad = tmath(vc("i"), vc("i"), font_size=56)
        row = VGroup(good, bad).arrange(RIGHT, buff=3.5).move_to(DOWN * 0.2)
        good_m, bad_m = self.check(good, True), self.check(bad, False)
        good_tag = words(r"one up, one down:\\a sum", size=28).next_to(good, DOWN, buff=0.4)
        bad_tag = words(r"two uppers:\\not allowed", size=28).next_to(bad, DOWN, buff=0.4)
        self.play(Write(good), FadeIn(good_m), FadeIn(good_tag))
        self.caption(r"One up and one down: summed. This one shows up a lot.")
        self.play(Write(bad), FadeIn(bad_m), FadeIn(bad_tag))
        self.caption(r"Two uppers (or two lowers) on the same index: a mistake on screen, never a sum.", wait=PAUSE_LONG)
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.caption_mob = None


# --------------------------------------------------------------------------
# Part 5: The tilde
# --------------------------------------------------------------------------
class E00_05_Tilde(Ep0Mixin, TensorScene):
    """Tilde marks the new basis and its components; why not primes."""

    def construct(self):
        title = self.part_title(5, "The Tilde: A New Basis")
        plane = ep_plane()
        v = styled_vector(V_OLD, plane)
        e1, e2 = basis_vector(1, (1, 0), plane), basis_vector(2, (0, 1), plane)
        self.play(FadeIn(plane), GrowArrow(v.arrow), FadeIn(v.label),
                  FadeIn(e1), FadeIn(e2))

        old_eq = right_panel(tmath(VEC, "=", vc("i"), e("i")), y=1.2)
        self.play(Write(old_eq))
        self.caption(r"Here is our vector in the old basis.")

        grid = new_grid(plane)
        te1, te2 = new_basis_vector(1, E_NEW[0], plane), new_basis_vector(2, E_NEW[1], plane)
        self.play(FadeOut(e1), FadeOut(e2),
                  plane.background_lines.animate.set_stroke(opacity=0.15), Create(grid, lag_ratio=0.05))
        self.play(GrowArrow(te1.arrow), GrowArrow(te2.arrow), FadeIn(te1.label), FadeIn(te2.label))
        self.caption(r"Now choose a \textbf{new} basis. We mark everything new with a tilde.")

        new_eq = right_panel(tmath(VEC, "=", vct("i"), et("i")), y=0.0)
        self.play(Write(new_eq))
        self.caption(r"New basis vectors get a tilde, and so do the new components.")

        both = right_panel(tmath(VEC, "=", vc("i"), e("i"), "=", vct("i"), et("i")), y=1.2)
        self.play(FadeOut(new_eq), TransformMatchingTex(old_eq, both))
        box = SurroundingRectangle(both, color=AXIS_COLOR, buff=0.2, corner_radius=0.1)
        self.play(Create(box))
        self.caption(r"Notice that $\mathbf{v}$ has no tilde. The object never changes, only how we describe it.", wait=PAUSE_LONG)

        # Why not primes
        prime = tmath(r"\mathbf{e}'_{i}", font_size=60)
        deriv = MathTex(r"f'(x)", font_size=60, color=TEXT_COLOR)
        why = VGroup(prime, deriv).arrange(RIGHT, buff=1.6)
        right_panel(why, y=-0.8)
        cross = Cross(prime, stroke_color=NOT_ALLOWED_COLOR, stroke_width=6)
        self.play(FadeIn(prime))
        self.play(Create(cross))
        self.caption(r"Why not a prime, like many textbooks use?")
        self.play(FadeIn(deriv, shift=LEFT * 0.2))
        self.caption(r"Because in tensor calculus a prime looks like a \emph{derivative}. A tilde never does.", wait=PAUSE_LONG)
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.caption_mob = None


# --------------------------------------------------------------------------
# Part 6: Beth
# --------------------------------------------------------------------------
class E00_06_Beth(Ep0Mixin, TensorScene):
    """Beth (Hebrew bet) as the change-of-basis matrix, staggered indices, beth^-1."""

    def construct(self):
        title = self.part_title(6, r"Meet $\beth$, the Basis-Changer")

        big = tmath(BETH, font_size=160).move_to(UP * 0.5)
        self.play(Write(big), run_time=1.5)
        self.caption(r"This is $\beth$ (\emph{beth}), the second letter of the Hebrew alphabet. It sounds like ``b''.")
        self.caption(r"B for \textbf{basis}: $\beth$ is our change-of-basis matrix.")

        mat = tmath(BETH, "=", r"\begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix}", font_size=60).move_to(UP * 0.5)
        self.play(TransformMatchingTex(big, mat))
        self.caption(r"Each column holds a new basis vector, written in old coordinates.")

        # Staggered indices
        stag = tmath(beth("i", "j"), font_size=130).move_to(UP * 0.5)
        self.play(FadeOut(mat), FadeIn(stag))
        glyphs = stag[0]
        i_up, j_down = glyphs[1], glyphs[2]
        row_lbl = words("row", size=34, color=AXIS_COLOR).next_to(i_up, RIGHT, buff=1.4).shift(UP * 0.4)
        col_lbl = words("column", size=34, color=AXIS_COLOR).next_to(j_down, RIGHT, buff=1.4).shift(DOWN * 0.4)
        a1 = Arrow(row_lbl.get_left(), i_up.get_right(), buff=0.15, color=AXIS_COLOR, stroke_width=3)
        a2 = Arrow(col_lbl.get_left(), j_down.get_right(), buff=0.15, color=AXIS_COLOR, stroke_width=3)
        self.play(FadeIn(row_lbl), GrowArrow(a1))
        self.play(FadeIn(col_lbl), GrowArrow(a2))
        self.caption(r"Its entries have \textbf{staggered} indices: the first is the row, the second is the column.", wait=PAUSE_LONG)
        self.play(FadeOut(VGroup(stag, row_lbl, col_lbl, a1, a2)))

        # Forward rule for the basis
        fwd = tmath(et("j"), "=", beth("i", "j"), e("i"), font_size=60).move_to(UP * 1.2)
        fwd_tag = words(r"forward: old basis $\to$ new basis", size=30, color=AXIS_COLOR).next_to(fwd, DOWN, buff=0.3)
        self.play(Write(fwd), FadeIn(fwd_tag))
        self.caption(r"$\beth$ builds the new basis out of the old one. Note: $i$ is summed, and $j$ is free on both sides.", wait=PAUSE_LONG)

        # Backward rule for components
        bwd = tmath(vct("i"), "=", beth_inv("i", "j"), vc("j"), font_size=60).move_to(DOWN * 0.6)
        bwd_tag = words(r"backward: components use $\beth^{-1}$", size=30, color=AXIS_COLOR).next_to(bwd, DOWN, buff=0.3)
        self.play(Write(bwd), FadeIn(bwd_tag))
        self.caption(r"Components go the \emph{other} way, with the inverse $\beth^{-1}$. Hence ``contra''-variant.", wait=PAUSE_LONG)

        # Numeric check
        self.play(FadeOut(VGroup(fwd, fwd_tag, bwd_tag)), bwd.animate.move_to(UP * 1.2))
        num = tmath(
            r"\begin{pmatrix} 2 \\ 1 \end{pmatrix}", "=",
            r"\tfrac{1}{2}\begin{pmatrix} 1 & 1 \\ -1 & 1 \end{pmatrix}",
            r"\begin{pmatrix} 1 \\ 3 \end{pmatrix}",
            colors={
                r"\begin{pmatrix} 2 \\ 1 \end{pmatrix}": NEW_COMPONENT_COLOR,
                r"\tfrac{1}{2}\begin{pmatrix} 1 & 1 \\ -1 & 1 \end{pmatrix}": BETH_COLOR,
                r"\begin{pmatrix} 1 \\ 3 \end{pmatrix}": COMPONENT_COLOR,
            },
            font_size=54,
        ).move_to(DOWN * 0.8)
        self.play(Write(num), run_time=1.5)
        self.caption(r"Our arrow: old components $(1, 3)$ become new components $(2, 1)$. Same arrow, as promised.", wait=PAUSE_LONG)
        self.caption(r"We will derive all of this properly in Episode 2. For now, just learn the names.")
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.caption_mob = None


# --------------------------------------------------------------------------
# Part 7: Covectors
# --------------------------------------------------------------------------
class E00_07_Covectors(Ep0Mixin, TensorScene):
    """Greek letters, never bold, never beta; level-line stacks; dual basis eps^i."""

    def construct(self):
        title = self.part_title(7, "Greek Letters Mean Covectors")

        greek = tmath(r"\alpha", ",", r"\gamma", ",", r"\omega", font_size=90).move_to(UP * 0.7)
        self.play(Write(greek))
        self.caption(r"Covectors get Greek letters. They are \textbf{never} bold, so they cannot be mistaken for vectors.")
        beta = MathTex(r"\beta", font_size=90, color=TEXT_COLOR).next_to(greek, RIGHT, buff=1.0)
        cross = Cross(beta, stroke_color=NOT_ALLOWED_COLOR, stroke_width=6)
        self.play(FadeIn(beta))
        self.play(Create(cross))
        self.caption(r"And never $\beta$: it is too easy to confuse with our $\beth$.")
        self.play(FadeOut(VGroup(greek, beta, cross)))

        # The picture: a stack of level lines
        plane = ep_plane()
        v = styled_vector(V_OLD, plane, label_direction=RIGHT)
        alpha = covector_stack(ALPHA, plane, direction_anchor=(1.8, -0.3))
        self.play(FadeIn(plane), GrowArrow(v.arrow), FadeIn(v.label))
        self.play(Create(alpha.lines, lag_ratio=0.1), run_time=1.5)
        self.play(GrowArrow(alpha.direction))
        a_lbl = right_panel(tmath(COVEC, font_size=72), y=1.5)
        self.play(Write(a_lbl))
        self.caption(r"Picture a covector as a \textbf{stack of lines}, with a direction in which its value grows.")

        # alpha(v) = number of lines pierced
        k1 = Dot(plane.c2p(0.5, 1.5), color=COVECTOR_COLOR, radius=0.07)  # on line k=1
        k2 = Dot(plane.c2p(1, 3), color=COVECTOR_COLOR, radius=0.07)      # tip, on line k=2
        self.play(FadeIn(k1, scale=0.5), FadeIn(k2, scale=0.5))
        val = right_panel(tmath(COVEC, "(", VEC, ")", "= 2"), y=0.3)
        self.play(Write(val))
        self.caption(r"Feed it a vector, and you get a number: how many lines the arrow pierces. Here, 2.", wait=PAUSE_LONG)

        # Dual basis
        self.play(FadeOut(VGroup(k1, k2, val)),
                  alpha.lines.animate.set_stroke(opacity=0.25), alpha.direction.animate.set_opacity(0.25))
        region = (-3, 3, -1, 4)
        eps1 = covector_stack((1, 0), plane, color=DUAL_BASIS_COLOR, show_direction=False, region=region)
        eps2 = covector_stack((0, 1), plane, color=DUAL_BASIS_COLOR, show_direction=False, region=region)
        dual = right_panel(tmath(eps(1), ",", r"\quad", eps(2), font_size=60), y=0.3)
        self.play(Create(eps1, lag_ratio=0.1), Write(dual))
        self.caption(r"Covectors have their own basis, the \textbf{dual basis} $\epsilon^i$, with the index \emph{up}.")
        self.play(ReplacementTransform(eps1, eps2), run_time=1.2)
        self.caption(r"$\epsilon^1$ counts steps of $\mathbf{e}_1$, and $\epsilon^2$ counts steps of $\mathbf{e}_2$.")
        self.play(FadeOut(eps2), alpha.lines.animate.set_stroke(opacity=1), alpha.direction.animate.set_opacity(1))

        expand = right_panel(tmath(COVEC, "=", cc(1), eps(1), "+", cc(2), eps(2)), y=0.3)
        self.play(TransformMatchingTex(dual, expand))
        self.caption(r"Components of a covector carry their index \emph{down}: $\alpha_i$. Exactly the reverse of vectors.")
        short = right_panel(tmath(COVEC, "=", cc("i"), eps("i")), y=0.3)
        self.play(TransformMatchingTex(expand, short))
        pair = right_panel(tmath(COVEC, "(", VEC, ")", "=", cc("i"), vc("i"), "= 2"), y=-0.9)
        self.play(Write(pair))
        self.caption(r"And one up, one down means a sum: $\alpha_i v^i = (-1)(1) + (1)(3) = 2$. It matches the picture.", wait=PAUSE_LONG)
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.caption_mob = None


# --------------------------------------------------------------------------
# Part 8: Recap / legend card
# --------------------------------------------------------------------------
class E00_08_Recap(Ep0Mixin, TensorScene):
    """The full legend card to pause on, then the teaser for Episode 1."""

    def construct(self):
        head = words(r"\textbf{The Legend}: pause here any time", size=44).to_edge(UP, buff=0.35)
        self.play(FadeIn(head, shift=DOWN * 0.2))

        # Two parallel columns: vector side | dual side, row by row
        # (object, old basis, old comps, new basis, new comps, operator/UI).
        vec_side = [
            (VEC, "vector (object)", VECTOR_COLOR),
            (e("i"), "old basis", BASIS_COLOR),
            (vc("i"), "old components", COMPONENT_COLOR),
            (et("i"), "new basis", NEW_BASIS_COLOR),
            (vct("i"), "new components", NEW_COMPONENT_COLOR),
            (beth("i", "j"), r"change of basis, $\beth^{-1}$ back", BETH_COLOR),
        ]
        dual_side = [
            (COVEC, "covector (object)", COVECTOR_COLOR),
            (eps("i"), "old dual basis", DUAL_BASIS_COLOR),
            (cc("i"), "old covector components", COVECTOR_COMPONENT_COLOR),
            (epst("i"), "new dual basis", NEW_DUAL_BASIS_COLOR),
            (cct("i"), "new covector components", NEW_COVECTOR_COMPONENT_COLOR),
            (r"\times", "not allowed", NOT_ALLOWED_COLOR),
        ]

        def column(rows):
            cells = []
            for tex, desc, color in rows:
                sw = Square(0.26, fill_color=color, fill_opacity=1, stroke_width=0)
                sym = tmath(tex, font_size=38)
                if tex == r"\times":
                    sym.set_color(NOT_ALLOWED_COLOR)
                cells += [sw, sym, words(desc, size=26)]
            return VGroup(*cells).arrange_in_grid(rows=len(rows), cols=3, buff=(0.3, 0.16),
                                                  col_alignments="ccl")

        col_a, col_b = column(vec_side), column(dual_side)
        cols = VGroup(col_a, col_b).arrange(RIGHT, buff=1.0, aligned_edge=UP)
        cols.next_to(head, DOWN, buff=0.35)
        # rows of the two columns share a baseline
        for k in range(len(vec_side)):
            for c in range(3):
                col_b[3 * k + c].match_y(col_a[3 * k + c])

        hline = Line(LEFT * 6.3, RIGHT * 6.3, color=GRID_COLOR, stroke_width=2).next_to(cols, DOWN, buff=0.25)
        rule_txt = VGroup(
            words(r"bold = object, plain = number", size=24),
            words(r"components: pale tint of their basis", size=24),
            words(r"repeated up + down index = sum", size=24),
            words(r"tilde = new basis (never primes)", size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.8, 0.12), col_alignments="ll")
        rule_eqs = VGroup(
            tmath(et("j"), "=", beth("i", "j"), e("i"), font_size=34),
            tmath(vct("i"), "=", beth_inv("i", "j"), vc("j"), font_size=34),
            tmath(cct("j"), "=", beth("i", "j"), cc("i"), font_size=34),
        ).arrange(RIGHT, buff=0.8)
        rules = VGroup(rule_txt, rule_eqs).arrange(DOWN, buff=0.22).next_to(hline, DOWN, buff=0.2)
        half = (max(cols.width, rules.width) + 0.4) / 2
        hline.put_start_and_end_on(LEFT * half + hline.get_center(), RIGHT * half + hline.get_center())
        hline.set_x(cols.get_x())
        content = VGroup(cols, hline, rules)
        avail_h = head.get_bottom()[1] + config.frame_height / 2 - 0.6
        content.scale(min(1.25, avail_h / content.height, (config.frame_width - 0.8) / content.width))
        content.next_to(head, DOWN, buff=0.35).set_x(0)
        n_rows = len(vec_side)

        self.play(LaggedStart(*[FadeIn(VGroup(*col_a[3 * k:3 * k + 3], *col_b[3 * k:3 * k + 3]), shift=RIGHT * 0.2)
                                for k in range(n_rows)], lag_ratio=0.3), run_time=3.5)
        self.play(Create(hline), LaggedStart(*[FadeIn(r) for r in [*rule_txt, *rule_eqs]], lag_ratio=0.2), run_time=2.5)
        self.beat(PAUSE_LONG * 2.5)

        self.play(*[FadeOut(m) for m in self.mobjects])
        teaser = VGroup(
            words(r"Next time", size=32, color=AXIS_COLOR),
            words(r"\textbf{Episode 1: What Is a Vector, Really?}", size=52),
        ).arrange(DOWN, buff=0.3)
        v = styled_vector((2, 1.2), label=None).move_to(DOWN * 1.6)
        self.play(FadeIn(teaser, shift=UP * 0.2))
        self.play(GrowArrow(v.arrow))
        self.beat(PAUSE_LONG)
        self.play(FadeOut(teaser), FadeOut(v))
