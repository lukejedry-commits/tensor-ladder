"""
Episode 1: What Is a Vector, Really?   (2D only)

Built from scripts/episode01_outline_and_script.md. One TensorScene per scene:
    manim -ql episode01.py E01_05_ComponentsAsRecipe
    manim -ql -a episode01.py

Voice-over ready: captions are key phrases only. Every beat is wrapped in
`with self.vo(n):` where n is that beat's narration word count from the
script, so each beat lasts about as long as it takes to read (150 wpm).

Running example (same as Episode 0):
    old basis  e_1 = (1, 0), e_2 = (0, 1);   v = 1 e_1 + 3 e_2,  [v]_e  = (1, 3)
    new basis  ~e_1 = e_1 + e_2, ~e_2 = -e_1 + e_2;  v = 2 ~e_1 + 1 ~e_2,  [v]_~e = (2, 1)
    doubled    ~e_i = 2 e_i;  [v]_~e = (1/2, 3/2)   (basis x2 -> components x1/2)
"""

import numpy as np
from manim import *

from tensor_style import *
from episode_base import *

V = (1, 3)
E_OLD = ((1, 0), (0, 1))
E_NEW = ((1, 1), (-1, 1))
E_DOUBLE = ((2, 0), (0, 2))

# narration word counts per beat, from scripts/episode01_outline_and_script.md
VO_WORDS = {
    "E01_01": [47, 42],
    "E01_02": [18, 48, 13, 42],
    "E01_03": [23, 31, 40, 40, 48],
    "E01_04": [30, 42, 21, 42, 28],
    "E01_05": [36, 19, 34, 32, 53],
    "E01_06": [27, 31, 22, 23, 50],
    "E01_07": [36, 33, 48, 34],
    "E01_08": [38, 49, 5],
}


def label_near_tip(arrow: Arrow, mob: Mobject, side: float = 1.0, dist: float = 0.38) -> Mobject:
    """Place a label just past an arrow tip, offset to its left (side=1) or right (-1)."""
    d = arrow.get_end() - arrow.get_start()
    d = d / (np.linalg.norm(d) or 1)
    n = side * np.array([-d[1], d[0], 0.0])
    return mob.move_to(arrow.get_end() + dist * n + 0.15 * d)


def scene_arrow(start, vec, color=VECTOR_COLOR, stroke=VECTOR_STROKE) -> Arrow:
    """A plain arrow in scene units (for the coordinate-free scenes)."""
    s = np.array([*start, 0.0])
    return Arrow(s, s + np.array([*vec, 0.0]), buff=0, color=color, stroke_width=stroke,
                 max_tip_length_to_length_ratio=0.2, max_stroke_width_to_length_ratio=12)


def grow_walk(walk, run_time_per_step=0.5):
    """Animations that lay a recipe walk down step by step."""
    anims = []
    labels = list(walk.labels)
    li = 0
    for arr in walk.steps:
        group = [GrowArrow(arr)]
        # numbered walks have one label per full step, in order
        if li < len(labels) and np.linalg.norm(labels[li].get_center() - arr.get_center()) < 0.6:
            group.append(FadeIn(labels[li]))
            li += 1
        anims.append(AnimationGroup(*group, run_time=run_time_per_step))
    return Succession(*anims)


class Ep1Scene(EpisodeMixin):
    """Mixin marker for Episode 1 scenes (not a Scene, so -a skips it)."""


# --------------------------------------------------------------------------
class E01_01_ColdOpen(Ep1Scene, TensorScene):
    """List? Arrow? Something else? Three views of one object."""

    def construct(self):
        w = VO_WORDS["E01_01"]
        with self.vo(w[0]):
            heads = VGroup(*[words(t, size=30, color=AXIS_COLOR) for t in
                             ("a list of numbers?", "an arrow?", "something else?")])
            lst = Tex(r"\texttt{[1, 3]}", font_size=60, color=TEXT_COLOR)
            arrow = scene_arrow((-0.7, -1.1), (1.4, 2.0))
            other = words(r"``anything you can\\add and scale''", size=30)
            contents = VGroup(lst, arrow, other)
            for k, x in enumerate((-4.6, 0.0, 4.6)):
                heads[k].move_to([x, 1.9, 0])
                contents[k].move_to([x, -0.1, 0])
            self.caption("three answers")
            for k in range(3):
                self.play(FadeIn(heads[k], shift=DOWN * 0.2),
                          GrowArrow(arrow) if k == 1 else FadeIn(contents[k]), run_time=1.0)
                self.wait(1.2)
        with self.vo(w[1]):
            self.caption("one object, three views")
            self.play(lst.animate.move_to(arrow).scale(0.3).set_opacity(0),
                      other.animate.move_to(arrow).scale(0.3).set_opacity(0),
                      FadeOut(heads), run_time=1.5)
            self.play(arrow.animate.scale(1.3).move_to(DOWN * 0.6), run_time=1.0)
            title = words(r"\textbf{Episode 1: What Is a Vector, Really?}", size=52).to_edge(UP, buff=0.8)
            self.play(Write(title), run_time=1.5)
        self.clear_all()


# --------------------------------------------------------------------------
class E01_02_TheArrowItself(Ep1Scene, TensorScene):
    """Coordinate-free arrow: direction + length, free to slide, invariant."""

    def construct(self):
        w = VO_WORDS["E01_02"]
        self.part_title(2, "The Arrow Itself")
        start, vec = (-1.5, -1.3), (3.0, 1.6)
        arrow = scene_arrow(start, vec)
        lab = label_near_tip(arrow, tmath(VEC, font_size=LABEL_SIZE))
        v = VGroup(arrow, lab)
        with self.vo(w[0]):
            self.caption("just an arrow")
            self.play(GrowArrow(arrow), FadeIn(lab))
        with self.vo(w[1]):
            self.caption("direction + length")
            s3 = np.array([*start, 0.0])
            ref = DashedLine(s3, s3 + RIGHT * 1.6, color=AXIS_COLOR, stroke_width=2)
            ang = Angle(Line(s3, s3 + RIGHT), Line(s3, arrow.get_end()), radius=0.75, color=AXIS_COLOR)
            ang_lab = words("direction", size=26, color=AXIS_COLOR).next_to(ang, RIGHT, buff=0.15).shift(DOWN * 0.15)
            brace = Brace(arrow, direction=rotate_vector(UP, angle_of_vector(arrow.get_end() - arrow.get_start())),
                          color=AXIS_COLOR)
            br_lab = words("length", size=26, color=AXIS_COLOR)
            brace.put_at_tip(br_lab)
            self.play(Create(ref), Create(ang), FadeIn(ang_lab))
            self.play(GrowFromCenter(brace), FadeIn(br_lab))
            self.wait(1.0)
            self.play(FadeOut(VGroup(ref, ang, ang_lab, brace, br_lab)))
            self.caption("slide it: same vector")
            shifts = [LEFT * 3.9 + UP * 1.45, RIGHT * 3.9 + DOWN * 0.9, LEFT * 3.9 + DOWN * 1.1]
            copies = [v.copy() for _ in shifts]
            for c, sh in zip(copies, shifts):
                self.add(c)
                self.play(c.animate.shift(sh), run_time=1.0)
        with self.vo(w[2]):
            self.caption("tilt it: a different vector")
            tilted = copies[1]
            self.play(Rotate(tilted, angle=28 * DEGREES, about_point=tilted[0].get_start()), run_time=1.0)
            cross = Cross(tilted, stroke_color=NOT_ALLOWED_COLOR, stroke_width=6)
            self.play(Create(cross))
        with self.vo(w[3]):
            self.caption("no coordinates needed")
            self.play(FadeOut(VGroup(*copies, cross)))
            self.play(Indicate(arrow, color=VECTOR_COLOR, scale_factor=1.04))
        self.clear_all()


# --------------------------------------------------------------------------
class E01_03_AddAndScale(Ep1Scene, TensorScene):
    """Tip-to-tail addition, the parallelogram, scaling, a linear combination."""

    def construct(self):
        w = VO_WORDS["E01_03"]
        self.part_title(3, "Adding and Scaling")
        O = (-4.2, -1.9)
        vv, ww = np.array([3.0, 1.0]), np.array([-1.0, 2.0])
        v = scene_arrow(O, vv)
        wa = scene_arrow(O, ww, color=VECTOR_2_COLOR)
        v_lab = label_near_tip(v, tmath(VEC, font_size=LABEL_SIZE), side=-1)
        w_lab = label_near_tip(wa, tmath(bold("w"), font_size=LABEL_SIZE))
        with self.vo(w[0]):
            self.caption("add and scale")
            self.play(GrowArrow(v), FadeIn(v_lab), GrowArrow(wa), FadeIn(w_lab))

        with self.vo(w[1]):
            self.caption("tip to tail")
            w_moved = wa.copy()  # arrow only: labels stay at the tails' originals
            self.play(w_moved.animate.shift(np.array([*vv, 0.0])), run_time=1.2)
            s = scene_arrow(O, vv + ww)
            s_lab = label_near_tip(s, tmath(VEC, "+", bold("w"), font_size=LABEL_SIZE))
            self.play(GrowArrow(s), FadeIn(s_lab))

        with self.vo(w[2]):
            self.caption("either order: same tip")
            v_moved = v.copy().set_opacity(0.85)
            self.play(v_moved.animate.shift(np.array([*ww, 0.0])), run_time=1.2)
            comm = right_panel(tmath(VEC, "+", bold("w"), "=", bold("w"), "+", VEC), y=1.4)
            self.play(Write(comm))

        with self.vo(w[3]):
            self.play(FadeOut(VGroup(v, wa, v_lab, w_lab, w_moved, v_moved, s, s_lab, comm)))
            self.caption("stretch, shrink, flip")
            O2 = np.array([-2.6, -0.6])
            u = np.array([2.0, 1.0])
            base = scene_arrow(O2, u)
            lab = label_near_tip(base, tmath(VEC, font_size=LABEL_SIZE))
            self.play(GrowArrow(base), FadeIn(lab))
            col = VGroup().move_to(RIGHT * 4.2 + UP * 1.0)
            ghosts = VGroup()
            for k_, tex in ((2.0, ["2", VEC]), (0.5, [r"\tfrac{1}{2}", VEC]), (-1.0, ["-", VEC])):
                new = scene_arrow(O2, k_ * u)
                new_lab = label_near_tip(new, tmath(*tex, font_size=LABEL_SIZE), side=1 if k_ > 0 else -1)
                ghost = base.copy().set_opacity(0.25)
                self.add(ghost)
                ghosts.add(ghost)
                self.play(Transform(base, new), Transform(lab, new_lab), run_time=1.0)
                entry = tmath(*tex, font_size=40)
                col.add(entry)
                col.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 4.2 + UP * 0.6)
                self.add(entry)
                self.wait(0.6)
            ghost = base.copy().set_opacity(0.25)
            self.add(ghost)
            ghosts.add(ghost)
            zero = Dot([*O2, 0], color=VECTOR_COLOR, radius=0.09)
            zero_lab = tmath(r"\mathbf{0}", font_size=LABEL_SIZE).next_to(zero, DOWN, buff=0.15)
            self.play(ReplacementTransform(base, zero), ReplacementTransform(lab, zero_lab))
            entry = tmath("0", VEC, "=", r"\mathbf{0}", font_size=40)
            col.add(entry)
            col.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 4.2 + UP * 0.4)
            self.add(entry)

        with self.vo(w[4]):
            self.play(FadeOut(VGroup(zero, zero_lab, col, ghosts)))
            self.caption("add + scale = a vector space")
            O3 = np.array([-4.5, -1.2])
            two_v = scene_arrow(O3, 2 * u)
            minus_w = scene_arrow(O3 + 2 * u, -ww, color=VECTOR_2_COLOR)
            res = scene_arrow(O3, 2 * u - ww)
            two_v_lab = label_near_tip(two_v, tmath("2", VEC, font_size=LABEL_SIZE))
            mw_lab = tmath("-", bold("w"), font_size=LABEL_SIZE).next_to(minus_w.get_center(), RIGHT, buff=0.3)
            res_lab = tmath("2", VEC, "-", bold("w"), font_size=LABEL_SIZE).next_to(res, DOWN, buff=0.25)
            self.play(GrowArrow(two_v), FadeIn(two_v_lab))
            self.play(GrowArrow(minus_w), FadeIn(mw_lab))
            self.play(GrowArrow(res), FadeIn(res_lab))
            vs = right_panel(words(r"\textbf{vector space}:\\anything you can\\add and scale", size=34), y=1.0)
            self.play(FadeIn(vs, shift=UP * 0.2))
        self.clear_all()


# --------------------------------------------------------------------------
class E01_04_ChoosingABasis(Ep1Scene, TensorScene):
    """Pick e_1, e_2; every arrow is a combination; a parallel pair fails."""

    def construct(self):
        w = VO_WORDS["E01_04"]
        self.part_title(4, "Choosing a Basis")
        plane = ep_plane()
        v = styled_vector(V, plane)
        with self.vo(w[0]):
            self.caption("a basis: our reference")
            self.play(GrowArrow(v.arrow), FadeIn(v.label))
            self.play(FadeIn(plane), run_time=1.2)
            self.bring_to_back(plane)

        e1, e2 = basis_vector(1, E_OLD[0], plane), basis_vector(2, E_OLD[1], plane)
        with self.vo(w[1]):
            self.caption(r"$\mathbf{e}_1, \mathbf{e}_2$: bold and blue")
            self.play(GrowArrow(e1.arrow), FadeIn(e1.label), GrowArrow(e2.arrow), FadeIn(e2.label))
            self.play(Indicate(v.arrow, color=VECTOR_COLOR, scale_factor=1.04))
            note = right_panel(words(r"$\mathbf{v}$ didn't move:\\we only added a ruler", size=32), y=1.2)
            self.play(FadeIn(note))

        with self.vo(w[2]):
            self.caption(r"some $\mathbf{e}_1$ + some $\mathbf{e}_2$")
            demos = VGroup()
            for comps in ((2, 1), (-2, 2)):
                a = styled_vector(comps, plane, label=None, color=VECTOR_2_COLOR)
                walk = recipe_walk(comps, E_OLD, plane)
                walk.set_opacity(0.7)
                demos.add(VGroup(a, walk))
                self.play(GrowArrow(a.arrow), run_time=0.6)
                self.play(grow_walk(walk, 0.35))
            self.wait(0.5)
            self.play(FadeOut(demos))

        with self.vo(w[3]):
            self.caption("parallel pair: only a line")
            self.play(FadeOut(VGroup(e1, e2, note)))
            a = Arrow(plane.c2p(0, 0), plane.c2p(1, 0.5), buff=0, color=BASIS_COLOR, stroke_width=BASIS_STROKE)
            b = Arrow(plane.c2p(0, 0), plane.c2p(-2, -1), buff=0, color=BASIS_COLOR, stroke_width=BASIS_STROKE)
            span = Line(plane.c2p(-2, -1), plane.c2p(3, 1.5), color=BASIS_COLOR, stroke_width=10,
                        stroke_opacity=0.3)
            self.play(GrowArrow(a), GrowArrow(b))
            self.play(Create(span), run_time=1.2)
            span_lab = right_panel(words(r"every combination\\stays on this line", size=32), y=1.2)
            miss = self.cross_mark(48).next_to(v.label, RIGHT, buff=0.15)
            miss_lab = right_panel(words(r"$\mathbf{v}$ is unreachable", size=32), y=0.0)
            self.play(FadeIn(span_lab))
            self.play(FadeIn(miss), FadeIn(miss_lab))

        with self.vo(w[4]):
            self.caption("basis: two non-parallel arrows")
            self.play(FadeOut(VGroup(a, b, span, span_lab, miss, miss_lab)))
            self.play(FadeIn(e1), FadeIn(e2))
            rule = right_panel(words(r"\textbf{basis} (in 2D):\\two non-parallel arrows\\reach every arrow,\\exactly one way", size=32), y=0.8)
            self.play(FadeIn(rule, shift=UP * 0.2))
        self.clear_all()


# --------------------------------------------------------------------------
class E01_05_ComponentsAsRecipe(Ep1Scene, TensorScene):
    """v = v^1 e_1 + v^2 e_2 = v^i e_i; the recipe (1, 3), tagged with its basis."""

    def construct(self):
        w = VO_WORDS["E01_05"]
        self.part_title(5, "Components Are a Recipe")
        plane = ep_plane()
        v = styled_vector(V, plane)
        # e_1 label below-right: the walk's first step and its counter sit on/below e_1
        e1 = basis_vector(1, E_OLD[0], plane, label_direction=DOWN + RIGHT * 0.6)
        e2 = basis_vector(2, E_OLD[1], plane)
        with self.vo(w[0]):
            self.caption("the recipe")
            self.play(FadeIn(plane), GrowArrow(v.arrow), FadeIn(v.label), FadeIn(e1), FadeIn(e2))
            q = right_panel(words(r"how many steps of $\mathbf{e}_1$?\\how many of $\mathbf{e}_2$?", size=32), y=1.3)
            self.play(FadeIn(q))

        walk = recipe_walk(V, E_OLD, plane, numbered=True, number_side=-1)
        with self.vo(w[1]):
            self.caption("1 step, then 3")
            self.play(v.arrow.animate.set_opacity(0.45))
            self.play(grow_walk(walk, 0.7))
            self.play(v.arrow.animate.set_opacity(1))

        with self.vo(w[2]):
            self.caption("components: plain, index up")
            eq1 = right_panel(tmath(VEC, "=", "1", e(1), "+", "3", e(2)), y=1.4)
            self.play(FadeOut(q), Write(eq1))
            self.wait(1.0)
            eq2 = right_panel(tmath(VEC, "=", vc(1), e(1), "+", vc(2), e(2)), y=1.4)
            nums = right_panel(tmath(vc(1), "= 1,", r"\qquad", vc(2), "= 3"), y=0.4)
            self.play(TransformMatchingTex(eq1, eq2))
            self.play(Write(nums))

        with self.vo(w[3]):
            self.caption("Einstein: one up, one down")
            eq3 = right_panel(tmath(VEC, "=", vc("i"), e("i")), y=1.4)
            self.play(TransformMatchingTex(eq2, eq3))
            self.play(Indicate(eq3[2][1], color=COMPONENT_COLOR), Indicate(eq3[3][1], color=BASIS_COLOR))

        with self.vo(w[4]):
            self.caption("one recipe, tagged with its basis")
            tag = right_panel(tagged_components(V), y=-1.0)
            self.play(Write(tag))
            box = SurroundingRectangle(tag.tag, color=BASIS_COLOR, buff=0.06, corner_radius=0.06)
            self.play(Create(box))
            self.play(Indicate(tag.tag, color=BASIS_COLOR, scale_factor=1.1))
        self.clear_all()


# --------------------------------------------------------------------------
class E01_06_SameArrowNewBasis(Ep1Scene, TensorScene):
    """Coral basis as an overlay; the same arrow is 2 ~e_1 + 1 ~e_2."""

    def construct(self):
        w = VO_WORDS["E01_06"]
        self.part_title(6, "Same Arrow, New Basis")
        plane = ep_plane()
        v = styled_vector(V, plane)
        e1, e2 = basis_vector(1, E_OLD[0], plane), basis_vector(2, E_OLD[1], plane)
        te1, te2 = new_basis_vector(1, E_NEW[0], plane), new_basis_vector(2, E_NEW[1], plane)
        with self.vo(w[0]):
            self.caption(r"a new basis: $\tilde{\mathbf{e}}_1, \tilde{\mathbf{e}}_2$")
            self.play(FadeIn(plane), GrowArrow(v.arrow), FadeIn(v.label), FadeIn(e1), FadeIn(e2))
            self.play(e1.animate.set_opacity(0.3), e2.animate.set_opacity(0.3))
            self.play(GrowArrow(te1.arrow), FadeIn(te1.label), GrowArrow(te2.arrow), FadeIn(te2.label))

        grid = basis_grid(plane, *E_NEW)
        with self.vo(w[1]):
            self.caption("same vector, new ruler")
            # overlay only: the plane and v are never transformed
            self.play(plane.background_lines.animate.set_stroke(opacity=0.15),
                      Create(grid, lag_ratio=0.05), run_time=1.5)
            self.bring_to_front(te1, te2, v)
            self.play(Indicate(v.arrow, color=VECTOR_COLOR, scale_factor=1.04))

        walk = recipe_walk(V_NEW := (2, 1), E_NEW, plane, colors=[NEW_BASIS_COLOR] * 2,
                           numbered=True, number_color=NEW_COMPONENT_COLOR)
        with self.vo(w[2]):
            self.caption("2 steps, then 1")
            self.play(v.arrow.animate.set_opacity(0.45))
            self.play(grow_walk(walk, 0.8))
            self.play(v.arrow.animate.set_opacity(1))

        with self.vo(w[3]):
            self.caption("new components")
            eq1 = right_panel(tmath(VEC, "=", "2", et(1), "+", "1", et(2)), y=1.4)
            self.play(Write(eq1))
            self.wait(0.8)
            eq2 = right_panel(tmath(VEC, "=", vct("i"), et("i")), y=1.4)
            nums = right_panel(tmath(vct(1), "= 2,", r"\qquad", vct(2), "= 1"), y=0.4)
            self.play(TransformMatchingTex(eq1, eq2))
            self.play(Write(nums))

        with self.vo(w[4]):
            self.caption("two lists, one arrow")
            tags = VGroup(tagged_components(V, font_size=40),
                          tagged_components(V_NEW, new=True, font_size=40)).arrange(RIGHT, buff=0.6)
            right_panel(tags, y=0.9)
            inv = right_panel(tmath(VEC, "=", vc("i"), e("i"), "=", vct("i"), et("i")), y=-1.0)
            box = SurroundingRectangle(inv, color=AXIS_COLOR, buff=0.2, corner_radius=0.1)
            self.play(FadeOut(VGroup(eq2, nums)), FadeIn(tags))
            self.play(Write(inv), Create(box))
            self.play(Indicate(inv[0], color=VECTOR_COLOR, scale_factor=1.15))
        self.clear_all()


# --------------------------------------------------------------------------
class E01_07_ListVsArrow(Ep1Scene, TensorScene):
    """A list needs its basis; doubling the basis halves the components."""

    def construct(self):
        w = VO_WORDS["E01_07"]
        self.part_title(7, "The List Is Not the Arrow")
        with self.vo(w[0]):
            self.caption("a list alone: which vector?")
            bare = tmath(VEC, "=", r"\begin{pmatrix} 1 \\ 3 \end{pmatrix}",
                         colors={r"\begin{pmatrix} 1 \\ 3 \end{pmatrix}": TEXT_COLOR}, font_size=60)
            bare.move_to(UP * 0.4)
            self.play(Write(bare))
            cross = Cross(bare, stroke_color=NOT_ALLOWED_COLOR, stroke_width=6)
            self.play(Create(cross))
            q = words("which basis?", size=34, color=AXIS_COLOR).next_to(bare, DOWN, buff=0.5)
            self.play(FadeIn(q))

        with self.vo(w[1]):
            self.caption("always tag the basis")
            tags = VGroup(tagged_components(V), tagged_components((2, 1), new=True)).arrange(RIGHT, buff=1.4)
            tags.move_to(UP * 0.4)
            self.play(FadeOut(VGroup(bare, cross, q)), FadeIn(tags, shift=UP * 0.2))
            rule = words(r"never a bare list for a vector", size=32, color=AXIS_COLOR).next_to(tags, DOWN, buff=0.6)
            self.play(FadeIn(rule))

        plane = ep_plane()
        v = styled_vector(V, plane)
        e1, e2 = basis_vector(1, E_OLD[0], plane), basis_vector(2, E_OLD[1], plane)
        te1, te2 = new_basis_vector(1, E_DOUBLE[0], plane), new_basis_vector(2, E_DOUBLE[1], plane)
        grid = basis_grid(plane, *E_DOUBLE)
        walk = recipe_walk((0.5, 1.5), E_DOUBLE, plane, colors=[NEW_BASIS_COLOR] * 2)
        with self.vo(w[2]):
            self.caption("double the basis")
            self.play(FadeOut(VGroup(tags, rule)))
            self.play(FadeIn(plane), GrowArrow(v.arrow), FadeIn(v.label), FadeIn(e1), FadeIn(e2))
            old_tag = right_panel(tagged_components(V, font_size=44), y=1.2)
            self.play(FadeIn(old_tag))
            self.play(e1.arrow.animate.set_opacity(0.3), e2.arrow.animate.set_opacity(0.3),
                      FadeOut(e1.label), FadeOut(e2.label),
                      plane.background_lines.animate.set_stroke(opacity=0.15),
                      Create(grid, lag_ratio=0.05), run_time=1.2)
            self.play(GrowArrow(te1.arrow), FadeIn(te1.label), GrowArrow(te2.arrow), FadeIn(te2.label))
            dbl = right_panel(tmath(et("i"), "=", "2", e("i"), font_size=40), y=2.25)
            self.play(FadeIn(dbl))
            self.play(v.arrow.animate.set_opacity(0.45))
            self.play(grow_walk(walk, 0.8))
            self.play(v.arrow.animate.set_opacity(1))
            new_tag = right_panel(tagged_components((r"\tfrac{1}{2}", r"\tfrac{3}{2}"), new=True,
                                                    font_size=44), y=-0.4)
            self.play(FadeIn(new_tag))

        with self.vo(w[3]):
            self.caption("components go the opposite way")
            rule = right_panel(words(r"basis $\times 2$ \;$\Rightarrow$\; components $\times \tfrac{1}{2}$",
                                     size=32), y=-1.85)
            self.play(Write(rule))
            contra = words(r"\textbf{contra}-variant", size=36, color=AXIS_COLOR).next_to(rule, DOWN, buff=0.3)
            self.play(FadeIn(contra, shift=UP * 0.2))
            self.play(Indicate(new_tag.column, color=NEW_COMPONENT_COLOR))
        self.clear_all()


# --------------------------------------------------------------------------
class E01_08_NextTime(Ep1Scene, TensorScene):
    """Three-line recap, then the Episode 2 hook (beth forward, components = ?)."""

    def construct(self):
        w = VO_WORDS["E01_08"]
        with self.vo(w[0]):
            head = words(r"\textbf{Recap}", size=44).to_edge(UP, buff=0.5)
            texts = [words(r"the vector is the arrow: basis-independent", size=34),
                     words(r"components: a recipe in a chosen basis", size=34),
                     words(r"change basis: components change, arrow doesn't", size=34)]
            maths = [scene_arrow((0, 0), (1.2, 0.6)),
                     tmath(VEC, "=", vc("i"), e("i"), font_size=44),
                     tmath(vc("i"), e("i"), "=", vct("i"), et("i"), font_size=44)]
            rows = VGroup()
            for k, (t, m) in enumerate(zip(texts, maths)):
                y = 1.3 - 1.25 * k
                t.move_to([0, y, 0]).to_edge(LEFT, buff=0.6)
                m.move_to([0, y, 0]).align_to([2.6, 0, 0], LEFT)
                rows.add(VGroup(t, m))
            self.play(FadeIn(head))
            for r in rows:
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.9)
                self.wait(0.8)

        with self.vo(w[1]):
            self.play(FadeOut(VGroup(head, rows)))
            big = tmath(BETH, font_size=120).move_to(UP * 1.9)
            fwd = tmath(et("j"), "=", beth("i", "j"), e("i"), font_size=56).move_to(UP * 0.4)
            bwd = tmath(vct("i"), "=", r"\;?", font_size=56).next_to(fwd, DOWN, buff=0.5)
            self.play(Write(big))
            self.play(Write(fwd))
            self.wait(0.8)
            self.play(Write(bwd))
            self.play(Indicate(bwd[2], scale_factor=1.4))
            nxt = VGroup(
                words("Next time", size=30, color=AXIS_COLOR),
                words(r"\textbf{Episode 2: Changing Basis (and Why Components Go Backwards)}", size=40),
            ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
            if nxt.width > config.frame_width - 0.6:
                nxt.scale_to_fit_width(config.frame_width - 0.6)
            self.play(FadeIn(nxt, shift=UP * 0.2))

        with self.vo(w[2], min_hold=1.5):
            pass
        self.clear_all()
