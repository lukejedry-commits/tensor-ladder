"""
tensor_style.py: shared style module for the tensor series.

Usage (in any scene file that sits next to this one):

    from tensor_style import *

    class MyScene(TensorScene):
        def construct(self):
            eq = tmath(rf"{{{{ {VEC} }}}} = {{{{ {vc('i')} }}}} {{{{ {e('i')} }}}}")
            # or, simpler, pass the pieces as separate arguments:
            eq = tmath(VEC, "=", vc("i"), e("i"))

Every symbol has exactly one spelling (the macro helpers below) and exactly
one color (the palette below). See STYLE_GUIDE.md for the rules.

Tested on Manim Community v0.22.1.
"""

from __future__ import annotations

import re
from typing import Iterable, Sequence

import numpy as np
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    UR,
    Arrow,
    Line,
    MathTex,
    NumberPlane,
    Scene,
    ThreeDAxes,
    ThreeDScene,
    VGroup,
    VMobject,
    config,
)

__all__ = [
    # palette
    "BG_COLOR", "TEXT_COLOR", "GRID_COLOR", "AXIS_COLOR",
    "VECTOR_COLOR", "BASIS_COLOR", "NEW_BASIS_COLOR",
    "COMPONENT_COLOR", "NEW_COMPONENT_COLOR",
    "COVECTOR_COLOR", "DUAL_BASIS_COLOR", "NEW_DUAL_BASIS_COLOR",
    "COVECTOR_COMPONENT_COLOR", "NEW_COVECTOR_COMPONENT_COLOR",
    "BETH_COLOR", "NOT_ALLOWED_COLOR", "PALETTE",
    # sizes & pacing
    "VECTOR_STROKE", "BASIS_STROKE", "COVECTOR_STROKE", "TEX_SIZE", "LABEL_SIZE",
    "RUN_TIME", "PAUSE_SHORT", "PAUSE", "PAUSE_LONG",
    # symbols
    "VEC", "BASIS", "NEW_BASIS", "BETH", "BETH_INV", "COVEC",
    "e", "et", "vc", "vct", "eps", "epst", "cc", "cct", "beth", "beth_inv", "bold",
    # tex helpers
    "TEX_COLOR_RULES", "TEX_COLOR_MAP", "classify_tex", "split_groups", "tmath",
    # mobject factories
    "LabeledArrow", "styled_plane", "styled_vector", "basis_vector",
    "new_basis_vector", "covector_stack", "styled_axes_3d",
    # scenes
    "TensorScene", "TensorThreeDScene",
]

# --------------------------------------------------------------------------
# 1. Palette (dark background, colorblind-considerate; see STYLE_GUIDE.md)
# --------------------------------------------------------------------------
# The rule: every OBJECT gets its own hue; every BASIS gets a vivid hue;
# COMPONENTS are a pale tint of the basis they are measured in (never the
# object's color). Old/new bases are complementary pairs: blue/orange on the
# vector side, violet/gold on the dual (covector) side.
# Color is never the *only* cue: bold vs plain, tilde vs none, Latin vs Greek
# and index height carry the same information. Color is a second channel.

BG_COLOR = "#14161C"          # near-black, slightly blue
TEXT_COLOR = "#E8E8E8"        # neutral symbols: = + ( ) numbers
GRID_COLOR = "#3A4152"        # NumberPlane background lines
AXIS_COLOR = "#8A93A6"        # NumberPlane axes

# objects
VECTOR_COLOR = "#FF3EA5"                  # hot pink: the vector       v (bold)
COVECTOR_COLOR = "#2DD4BF"                # teal: the covector         alpha (no index)
# vector side: blue (old) / orange (new)
BASIS_COLOR = "#56B4E9"                   # sky blue: old basis        e_i
COMPONENT_COLOR = "#95D3F8"               # light blue: old comps      v^i (pale tint lerped 1/3 toward e_i)
NEW_BASIS_COLOR = "#FF7F50"               # coral: new basis           ~e_i
NEW_COMPONENT_COLOR = "#FFB8A1"           # pale coral: new comps      ~v^i
# dual side: violet (old) / gold (new)
DUAL_BASIS_COLOR = "#A78BFA"              # violet: old dual basis     eps^i
COVECTOR_COMPONENT_COLOR = "#D6C9FF"      # pale violet: old comps     alpha_i
NEW_DUAL_BASIS_COLOR = "#FFC21A"          # gold: new dual basis       ~eps^i
NEW_COVECTOR_COMPONENT_COLOR = "#FFE88A"  # pale gold: new comps       ~alpha_i
# operators / UI
BETH_COLOR = "#36D86C"                    # green: change of basis     beth, beth^-1

NOT_ALLOWED_COLOR = "#FF5A5A"             # red UI accent: crosses on "not allowed" notation

PALETTE = {
    "background": BG_COLOR,
    "text": TEXT_COLOR,
    "grid": GRID_COLOR,
    "axis": AXIS_COLOR,
    "vector": VECTOR_COLOR,
    "covector": COVECTOR_COLOR,
    "basis": BASIS_COLOR,
    "component": COMPONENT_COLOR,
    "new_basis": NEW_BASIS_COLOR,
    "new_component": NEW_COMPONENT_COLOR,
    "dual_basis": DUAL_BASIS_COLOR,
    "covector_component": COVECTOR_COMPONENT_COLOR,
    "new_dual_basis": NEW_DUAL_BASIS_COLOR,
    "new_covector_component": NEW_COVECTOR_COMPONENT_COLOR,
    "beth": BETH_COLOR,
    "not_allowed": NOT_ALLOWED_COLOR,
}

# --------------------------------------------------------------------------
# 2. Sizes and pacing defaults
# --------------------------------------------------------------------------
VECTOR_STROKE = 6        # the vector v
BASIS_STROKE = 5         # basis arrows (slightly lighter than v)
COVECTOR_STROKE = 3      # covector level lines
TEX_SIZE = 48            # body equations
LABEL_SIZE = 36          # labels attached to arrows

RUN_TIME = 1.0           # default animation length (s)
PAUSE_SHORT = 0.5        # between linked steps
PAUSE = 1.0              # after a new idea appears
PAUSE_LONG = 2.0         # after a key result / before a scene change

# --------------------------------------------------------------------------
# 3. Symbol macros: the ONE spelling of every symbol
# --------------------------------------------------------------------------
VEC = r"\mathbf{v}"
BASIS = r"\mathbf{e}"
NEW_BASIS = r"\tilde{\mathbf{e}}"
BETH = r"\beth"
BETH_INV = r"\beth^{-1}"
COVEC = r"\alpha"


def bold(name: str = "v") -> str:
    """A vector by name, e.g. bold('w') -> \\mathbf{w}."""
    return rf"\mathbf{{{name}}}"


def e(i="i") -> str:
    """Old basis vector  e_i."""
    return rf"\mathbf{{e}}_{{{i}}}"


def et(i="i") -> str:
    """New basis vector  ~e_i."""
    return rf"\tilde{{\mathbf{{e}}}}_{{{i}}}"


def vc(i="i", name: str = "v") -> str:
    """Old vector component  v^i."""
    return rf"{name}^{{{i}}}"


def vct(i="i", name: str = "v") -> str:
    """New vector component  ~v^i."""
    return rf"\tilde{{{name}}}^{{{i}}}"


def eps(i="i") -> str:
    """Old dual basis covector  epsilon^i."""
    return rf"\epsilon^{{{i}}}"


def epst(i="i") -> str:
    """New dual basis covector  ~epsilon^i."""
    return rf"\tilde{{\epsilon}}^{{{i}}}"


def cc(i="i", name: str = r"\alpha") -> str:
    """Old covector component  alpha_i."""
    return rf"{name}_{{{i}}}"


def cct(i="i", name: str = r"\alpha") -> str:
    """New covector component  ~alpha_i."""
    return rf"\tilde{{{name}}}_{{{i}}}"


def beth(i="i", j="j") -> str:
    """Forward change-of-basis entry, staggered:  beth^i{}_j."""
    return rf"\beth^{{{i}}}{{}}_{{{j}}}"


def beth_inv(i="i", j="j") -> str:
    """Backward entry, staggered:  (beth^{-1})^i{}_j."""
    return rf"(\beth^{{-1}})^{{{i}}}{{}}_{{{j}}}"


# --------------------------------------------------------------------------
# 4. Consistent MathTex coloring
# --------------------------------------------------------------------------
# Each *group* of a formula is classified by the first rule that matches its
# LaTeX source. Order matters: specific rules (tilde, beth) come first.
_COVECTOR_LETTERS = r"\\(?:alpha|gamma|omega|sigma|phi|varphi|psi|zeta|eta|xi)"

TEX_COLOR_RULES: list[tuple[str, str]] = [
    (r"\\beth", BETH_COLOR),
    (r"\\tilde\{\s*\\mathbf\{\s*e\s*\}", NEW_BASIS_COLOR),
    (r"\\mathbf\{\s*e\s*\}", BASIS_COLOR),
    (r"\\tilde\{\s*\\(?:var)?epsilon\s*\}", NEW_DUAL_BASIS_COLOR),
    (r"\\(?:var)?epsilon", DUAL_BASIS_COLOR),
    # covector letters: with a lower index = component, bare = the object
    (r"\\tilde\{\s*" + _COVECTOR_LETTERS + r"\s*\}\s*_", NEW_COVECTOR_COMPONENT_COLOR),
    (_COVECTOR_LETTERS + r"(?![A-Za-z])\s*_", COVECTOR_COMPONENT_COLOR),
    (_COVECTOR_LETTERS + r"(?![A-Za-z])", COVECTOR_COLOR),
    (r"\\mathbf\{", VECTOR_COLOR),
    (r"\\tilde\{\s*[A-Za-z]\s*\}\s*\^", NEW_COMPONENT_COLOR),
    (r"^\s*[A-Za-z]\s*\^", COMPONENT_COLOR),
]

# Substring map in Manim's own tex_to_color_map format (coarse: it colors only
# the matched glyphs, so the alpha in alpha_i comes out teal). Prefer tmath().
# For people who
# prefer the stock API: MathTex(..., tex_to_color_map=TEX_COLOR_MAP).
TEX_COLOR_MAP: dict[str, str] = {
    BETH: BETH_COLOR,
    NEW_BASIS: NEW_BASIS_COLOR,
    VEC: VECTOR_COLOR,
    r"\epsilon": DUAL_BASIS_COLOR,
    r"\alpha": COVECTOR_COLOR,
}


def classify_tex(tex: str) -> str | None:
    """Return the series color for one group of LaTeX, or None (default)."""
    for pattern, color in TEX_COLOR_RULES:
        if re.search(pattern, tex):
            return color
    return None


def split_groups(tex: str) -> list[str]:
    """Split a string on depth-0 ``{{ ... }}`` groups, brace-aware.

    ``"{{ \\tilde{\\mathbf{e}}_j }} = {{ \\beth^i{}_j }}"`` ->
    ``[" \\tilde{\\mathbf{e}}_j ", " = ", " \\beth^i{}_j "]``.
    Nested LaTeX braces inside a group (which may contain ``}}``) are safe.
    """
    parts, cur, depth, inside, k = [], "", 0, False, 0
    while k < len(tex):
        two = tex[k:k + 2]
        if tex[k] == "\\" and k + 1 < len(tex) and tex[k + 1] in "{}\\":
            cur += two
            k += 2
            continue
        if not inside:
            if two == "{{" and depth == 0:
                parts.append(cur)
                cur, inside = "", True
                k += 2
                continue
            depth += {"{": 1, "}": -1}.get(tex[k], 0)
        else:
            if two == "}}" and depth == 0:
                parts.append(cur)
                cur, inside = "", False
                k += 2
                continue
            depth += {"{": 1, "}": -1}.get(tex[k], 0)
        cur += tex[k]
        k += 1
    parts.append(cur)
    return [p for p in parts if p.strip()]


def _defuse(tex: str) -> str:
    """Stop Manim from re-splitting a group: '{{' -> '{ {', '}}' -> '} }'."""
    while "{{" in tex or "}}" in tex:
        tex = tex.replace("{{", "{ {").replace("}}", "} }")
    return tex.strip()


def tmath(
    *pieces: str,
    colors: dict[str, str] | None = None,
    font_size: float = TEX_SIZE,
    **kwargs,
) -> MathTex:
    """MathTex with the series coloring applied automatically.

    Pass pieces as separate arguments, or one string with ``{{ }}`` groups,
    or mix both. Each piece/group is colored by ``TEX_COLOR_RULES``;
    unmatched pieces (=, +, numbers) get TEXT_COLOR.

        tmath(et("j"), "=", beth("i", "j"), e("i"))
        tmath(r"{{ \\tilde{v}^i }} = {{ (\\beth^{-1})^i{}_j }} {{ v^j }}")

    ``colors`` overrides by exact piece text, e.g. ``{"x^1": COMPONENT_COLOR}``.
    Index letters inherit their group's color. To color an index separately,
    make it its own group.
    """
    groups: list[str] = []
    for piece in pieces:
        groups.extend(split_groups(str(piece)))
    groups = [_defuse(g) for g in groups]
    if not groups:
        raise ValueError("tmath() needs at least one non-empty piece")

    kwargs.setdefault("color", TEXT_COLOR)
    mob = MathTex(*groups, font_size=font_size, **kwargs)
    overrides = colors or {}
    # One submobject per group (Manim CE >= 0.19 keeps .tex_string on each).
    for part, src in zip(mob.submobjects, groups):
        color = overrides.get(src) or classify_tex(src)
        if color:
            part.set_color(color)
    return mob


# --------------------------------------------------------------------------
# 5. Mobject factories
# --------------------------------------------------------------------------
class LabeledArrow(VGroup):
    """An Arrow with an optional MathTex label. Access .arrow and .label."""

    def __init__(self, arrow: Arrow, label: MathTex | None = None):
        super().__init__(arrow)
        self.arrow = arrow
        self.label = label
        if label is not None:
            self.add(label)


def styled_plane(
    x_range: Sequence[float] = (-7, 7, 1),
    y_range: Sequence[float] = (-4, 4, 1),
    faded: bool = False,
    **kwargs,
) -> NumberPlane:
    """NumberPlane with series defaults: quiet grid, no numbers, no ticks."""
    opacity = 0.35 if faded else 0.8
    kwargs.setdefault(
        "background_line_style",
        {"stroke_color": GRID_COLOR, "stroke_width": 1.5, "stroke_opacity": opacity},
    )
    kwargs.setdefault(
        "axis_config",
        {"stroke_color": AXIS_COLOR, "stroke_width": 2, "include_ticks": False,
         "include_tip": False},
    )
    kwargs.setdefault("faded_line_ratio", 1)
    return NumberPlane(x_range=list(x_range), y_range=list(y_range), **kwargs)


def _to_point(coords, plane: NumberPlane | None) -> np.ndarray:
    c = list(coords) + [0] * (3 - len(coords))
    return plane.c2p(*c[:2]) if plane is not None else np.array(c, dtype=float)


def _arrow(start, end, color, stroke) -> Arrow:
    return Arrow(
        start, end, buff=0, color=color, stroke_width=stroke,
        max_tip_length_to_length_ratio=0.2, max_stroke_width_to_length_ratio=12,
    )


def _place_label(arrow: Arrow, tex: str, color: str | None, direction=None) -> MathTex:
    label = tmath(tex, font_size=LABEL_SIZE)
    if color:
        label.set_color(color)
    vec = arrow.get_end() - arrow.get_start()
    if direction is None:
        # perpendicular-ish offset to the left of the arrow, toward its tip
        n = np.array([-vec[1], vec[0], 0.0])
        n = n / (np.linalg.norm(n) or 1)
        direction = n if np.linalg.norm(n) else UR
    label.move_to(arrow.get_end() + 0.35 * direction + 0.12 * vec / (np.linalg.norm(vec) or 1))
    return label


def styled_vector(
    coords: Sequence[float],
    plane: NumberPlane | None = None,
    label: str | None = VEC,
    color: str = VECTOR_COLOR,
    start: Sequence[float] = (0, 0),
    label_direction=None,
) -> LabeledArrow:
    """The vector itself: thick hot-pink arrow from ``start`` to ``start+coords``.

    Coordinates are in plane units if ``plane`` is given, else scene units.
    """
    s = _to_point(start, plane)
    n = max(len(start), len(coords))
    pad = lambda c: list(c) + [0] * (n - len(c))
    end = _to_point(np.add(pad(start), pad(coords)), plane)
    arrow = _arrow(s, end, color, VECTOR_STROKE)
    lab = _place_label(arrow, label, color, label_direction) if label else None
    return LabeledArrow(arrow, lab)


def basis_vector(
    i, coords: Sequence[float], plane: NumberPlane | None = None,
    label: bool = True, label_direction=None,
) -> LabeledArrow:
    """Old basis arrow e_i, drawn from the origin."""
    arrow = _arrow(_to_point((0, 0), plane), _to_point(coords, plane), BASIS_COLOR, BASIS_STROKE)
    lab = _place_label(arrow, e(i), BASIS_COLOR, label_direction) if label else None
    return LabeledArrow(arrow, lab)


def new_basis_vector(
    i, coords: Sequence[float], plane: NumberPlane | None = None,
    label: bool = True, label_direction=None,
) -> LabeledArrow:
    """New basis arrow ~e_i, drawn from the origin.

    ``coords`` are given in the OLD basis, i.e. column i of beth.
    """
    arrow = _arrow(_to_point((0, 0), plane), _to_point(coords, plane), NEW_BASIS_COLOR, BASIS_STROKE)
    lab = _place_label(arrow, et(i), NEW_BASIS_COLOR, label_direction) if label else None
    return LabeledArrow(arrow, lab)


def _clip_line(p0, d, xmin, xmax, ymin, ymax):
    """Liang-Barsky clip of the infinite line p0 + t d to a rectangle."""
    t0, t1 = -np.inf, np.inf
    for p, q in ((-d[0], p0[0] - xmin), (d[0], xmax - p0[0]),
                 (-d[1], p0[1] - ymin), (d[1], ymax - p0[1])):
        if abs(p) < 1e-12:
            if q < 0:
                return None
            continue
        t = q / p
        if p < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
    if t0 >= t1:
        return None
    return p0 + t0 * d, p0 + t1 * d


def covector_stack(
    alpha: Sequence[float],
    plane: NumberPlane,
    levels: Iterable[int] | None = None,
    color: str = COVECTOR_COLOR,
    show_direction: bool = True,
    region: Sequence[float] | None = None,
    direction_anchor: Sequence[float] | None = None,
) -> VGroup:
    """A 2D covector alpha = (alpha_1, alpha_2) drawn as its level lines.

    Line k is the set { x : alpha_1 x + alpha_2 y = k }, for integer k.
    The zero line is drawn dashed. If ``show_direction``, a small arrow
    crosses the stack in the direction alpha increases. ``region`` is
    (xmin, xmax, ymin, ymax) in plane coordinates (default: whole plane).
    ``direction_anchor`` (plane coords) is where the direction arrow sits
    (default: region center; move it off the origin if basis arrows live there).

    Returns VGroup(lines, direction_arrow?) with attributes .lines, .direction.
    """
    a = np.array(alpha[:2], dtype=float)
    norm2 = float(a @ a)
    if norm2 == 0:
        raise ValueError("covector_stack: the zero covector has no level lines")
    if region is None:
        xr, yr = plane.x_range, plane.y_range
        region = (xr[0], xr[1], yr[0], yr[1])
    xmin, xmax, ymin, ymax = region
    if levels is None:
        corners = [a @ np.array(c) for c in ((xmin, ymin), (xmin, ymax), (xmax, ymin), (xmax, ymax))]
        levels = range(int(np.ceil(min(corners))), int(np.floor(max(corners))) + 1)

    d = np.array([-a[1], a[0]])
    lines = VGroup()
    for k in levels:
        seg = _clip_line(k * a / norm2, d, xmin, xmax, ymin, ymax)
        if seg is None:
            continue
        line = Line(plane.c2p(*seg[0]), plane.c2p(*seg[1]), color=color,
                    stroke_width=COVECTOR_STROKE)
        if k == 0:
            line.set_stroke(opacity=0.55)
        lines.add(line)

    group = VGroup(lines)
    group.lines = lines
    group.direction = None
    if show_direction:
        # spans from the level through `center` to the next level up
        center = (np.array(direction_anchor[:2], dtype=float) if direction_anchor is not None
                  else np.array([(xmin + xmax) / 2, (ymin + ymax) / 2]))
        base = center - ((a @ center) - np.floor(a @ center)) * a / norm2  # on an integer level
        arrow = Arrow(plane.c2p(*base), plane.c2p(*(base + a / norm2)), buff=0,
                      color=color, stroke_width=COVECTOR_STROKE + 1,
                      max_tip_length_to_length_ratio=0.35)
        group.add(arrow)
        group.direction = arrow
    return group


def styled_axes_3d(**kwargs) -> ThreeDAxes:
    """ThreeDAxes with the series axis color (for the 3D episodes)."""
    kwargs.setdefault("axis_config", {"color": AXIS_COLOR, "include_ticks": False})
    return ThreeDAxes(**kwargs)


# --------------------------------------------------------------------------
# 6. Scene bases
# --------------------------------------------------------------------------
class _TensorMixin:
    def beat(self, seconds: float = PAUSE):
        """Pacing pause; use PAUSE_SHORT / PAUSE / PAUSE_LONG."""
        self.wait(seconds)


class TensorScene(_TensorMixin, Scene):
    """Scene with the series background color."""

    def setup(self):
        super().setup()
        self.camera.background_color = BG_COLOR


class TensorThreeDScene(_TensorMixin, ThreeDScene):
    """ThreeDScene with the series background color."""

    def setup(self):
        super().setup()
        self.camera.background_color = BG_COLOR
