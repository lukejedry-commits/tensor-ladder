"""
episode_base.py: shared layout/timing helpers for episode files (Episode 1 on).

Episode 0 keeps its own copies (frozen); new episodes import from here:

    from tensor_style import *
    from episode_base import *

Nothing in this module is a Scene subclass, so `manim -a` never renders it.
"""
from __future__ import annotations

from contextlib import contextmanager

from manim import (DOWN, LEFT, RIGHT, UP, FadeIn, FadeOut, MathTex, Mobject, Tex,
                   VGroup, config)

from tensor_style import (AXIS_COLOR, NOT_ALLOWED_COLOR, PAUSE_SHORT, TEXT_COLOR,
                          styled_plane)

__all__ = ["VO_WPM", "CAPTION_SIZE", "words", "ep_plane", "right_panel", "EpisodeMixin"]

VO_WPM = 150          # narration pace used to time every beat
CAPTION_SIZE = 32


def words(text: str, size: float = CAPTION_SIZE, color=TEXT_COLOR) -> Tex:
    return Tex(text, font_size=size, color=color)


def ep_plane(x_range=(-3, 3, 1), y_range=(-1, 4, 1), center=LEFT * 3.6 + UP * 0.05):
    """The standard 2D plane on the left half of the frame (as in Episode 0)."""
    plane = styled_plane(x_range=x_range, y_range=y_range)
    plane.move_to(center)
    return plane


def right_panel(mob: Mobject, y: float = 1.0) -> Mobject:
    """Center a mobject in the right half of the frame."""
    return mob.move_to(RIGHT * 3.4 + UP * y)


class EpisodeMixin:
    """Voice-over-ready pacing: key-phrase captions + beats timed to narration.

    Usage inside construct():
        with self.vo(42):              # 42 narration words for this beat
            self.caption("tip to tail")
            self.play(...)
    On exit the beat waits until it has lasted ~ words / VO_WPM minutes.
    """

    caption_mob = None

    @contextmanager
    def vo(self, n_words: int, min_hold: float = PAUSE_SHORT):
        t0 = self.time
        yield
        remaining = n_words / VO_WPM * 60 - (self.time - t0)
        self.wait(max(min_hold, remaining))

    def caption(self, text: str | None):
        """Swap the bottom key-phrase caption (no hold; vo() does the timing)."""
        anims = []
        if self.caption_mob is not None:
            anims.append(FadeOut(self.caption_mob, shift=UP * 0.15))
            self.caption_mob = None
        if text:
            new = words(text).to_edge(DOWN, buff=0.45)
            if new.width > config.frame_width - 1:
                new.scale_to_fit_width(config.frame_width - 1)
            anims.append(FadeIn(new, shift=UP * 0.15))
            self.caption_mob = new
        if anims:
            self.play(*anims, run_time=0.6)

    def part_title(self, number: int, title: str):
        t = VGroup(
            words(rf"Part {number}", size=24, color=AXIS_COLOR),
            words(rf"\textbf{{{title}}}", size=40),
        ).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.25)
        self.play(FadeIn(t, shift=DOWN * 0.2), run_time=0.8)
        return t

    def clear_all(self, run_time: float = 0.8):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)
        self.caption_mob = None

    @staticmethod
    def cross_mark(size: float = 56):
        return MathTex(r"\times", color=NOT_ALLOWED_COLOR, font_size=size)
