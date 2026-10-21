"""Week 1 Day 3 explainer: chains of inequalities and the direction of substitution (1.4.1, 1.4.6)."""

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.narration import NarratedScene  # noqa: E402

EXPLAINER = {"id": "w01d3/inequality-chains", "title": "Which way does a substitution push?", "scene": "InequalityChains"}

NARRATION = {
    "facts": "Here are our facts: x plus three is at most two, and y plus two x is at least three. We want "
             "to show that y is bigger than three.",
    "chain": "We build a chain, just like with equalities. But now each link can be equals, at least, or "
             "bigger than.",
    "first": "First, y equals y plus two x, minus two x. Then substitute: y plus two x is at least three, so "
             "the whole thing is at least three minus two x.",
    "flip": "Next we want x plus three to appear. Three minus two x is the same as nine, minus two times x "
            "plus three. Now, careful. x plus three is at most two, but it's multiplied by negative two. "
            "Making it smaller makes the whole expression bigger. So this link is at least, not at most.",
    "end": "Nine minus four is five, which is bigger than three. Every link points the same way, so y is "
           "bigger than three.",
    "mixed": "Here's what goes wrong when the links disagree. n squared is at least twenty five, which is "
             "bigger than twenty one, which is at most two n plus eleven. Up, up, then down. That tells us "
             "nothing at all.",
    "outro": "In Lean, rel makes each substitution and checks its direction for you. Push the wrong way, "
             "and it refuses.",
}

FACT_A = BLUE_C     # x + 3 ≤ 2
FACT_B = YELLOW_C   # y + 2x ≥ 3
GOOD = GREEN_C
BAD = RED_C


class InequalityChains(NarratedScene):
    def construct(self):
        fa = MathTex("x+3", "\\le", "2")
        fb = MathTex("y+2x", "\\ge", "3")
        fa[0].set_color(FACT_A)
        fb[0].set_color(FACT_B)
        facts = VGroup(fa, fb).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        box = SurroundingRectangle(facts, color=GREY_B, buff=0.25, corner_radius=0.1)
        label = Text("Facts", font_size=26, color=GREY_B).next_to(box, UP, buff=0.15)
        known = VGroup(label, box, facts).to_corner(UL, buff=0.6)
        goal = MathTex("y", ">", "3", "\\;?").scale(1.2).to_corner(UR, buff=0.9)

        with self.beat("facts") as beat:
            self.play(FadeIn(label), Create(box), Write(fa), run_time=beat.until("and"))
            self.play(Write(fb), run_time=beat.until("We"))
            self.play(Write(goal), run_time=beat.until("bigger"))

        lhs = MathTex("y").scale(1.1)
        r1 = MathTex("=", "y+2x", "-2x").scale(1.1)
        r2 = MathTex("\\ge", "3", "-2x").scale(1.1)
        r3 = MathTex("=", "9", "-2", "(x+3)").scale(1.1)
        r4 = MathTex("\\ge", "9", "-2", "\\cdot 2").scale(1.1)
        r5 = MathTex(">", "3").scale(1.1)
        r1[1].set_color(FACT_B)
        r3[3].set_color(FACT_A)
        r1.next_to(lhs, RIGHT, buff=0.2)
        rows = [r1, r2, r3, r4, r5]
        for above, row in zip(rows, rows[1:]):
            row.next_to(above, DOWN, buff=0.32, aligned_edge=LEFT)
        chain = VGroup(lhs, *rows).move_to(DOWN * 0.45 + LEFT * 1.2)

        with self.beat("chain") as beat:
            self.play(FadeIn(lhs), run_time=beat.until("But"))
            symbols = VGroup(MathTex("="), MathTex("\\ge"), MathTex(">")).arrange(RIGHT, buff=0.6)
            symbols.next_to(chain, RIGHT, buff=1.6).shift(UP * 1.2)
            self.play(LaggedStart(*(FadeIn(s, shift=UP * 0.2) for s in symbols), lag_ratio=0.4),
                      run_time=beat.until("than") + 0.3)

        with self.beat("first") as beat:
            self.play(FadeOut(symbols), Write(r1), run_time=beat.until("Then"))
            self.play(Indicate(fb[0], color=FACT_B), Indicate(r1[1], color=FACT_B), run_time=beat.until("so"))
            self.play(Write(r2[0]), TransformFromCopy(fb[2], r2[1]), Write(r2[2]), run_time=beat.until("minus", 2) + 0.3)

        with self.beat("flip") as beat:
            self.play(Write(r3), run_time=beat.until("careful"))
            self.play(Indicate(fa, color=FACT_A), Indicate(r3[3], color=FACT_A), run_time=beat.until("multiplied"))
            # small seesaw: (x + 3) goes down, −2(x + 3) goes up
            down = VGroup(MathTex("x+3", color=FACT_A).scale(0.8), Arrow(UP * 0.4, DOWN * 0.4, color=FACT_A, buff=0))
            down.arrange(RIGHT, buff=0.15)
            up = VGroup(MathTex("-2(x+3)", color=GOOD).scale(0.8), Arrow(DOWN * 0.4, UP * 0.4, color=GOOD, buff=0))
            up.arrange(RIGHT, buff=0.15)
            seesaw = VGroup(down, up).arrange(DOWN, buff=0.5, aligned_edge=LEFT).next_to(chain, RIGHT, buff=1.4)
            self.play(FadeIn(down, shift=DOWN * 0.2), run_time=beat.until("Making"))
            self.play(FadeIn(up, shift=UP * 0.2), Indicate(r3[2], color=GOOD), run_time=beat.until("So"))
            self.play(Write(r4[0]), Write(r4[1]), Write(r4[2]), TransformFromCopy(fa[2], r4[3]),
                      run_time=beat.until("not") + 0.3)
            self.play(Indicate(r4[0], color=GOOD))

        with self.beat("end") as beat:
            self.play(FadeOut(seesaw), Write(r5), run_time=beat.until("Every"))
            links = VGroup(*(row[0] for row in rows))
            self.play(LaggedStart(*(Indicate(s, color=GOOD) for s in links), lag_ratio=0.25),
                      run_time=beat.until("so") + 0.3)
            done = MathTex("y", ">", "3", color=GOOD).scale(1.2).move_to(goal[:3])
            self.play(FadeOut(goal), FadeIn(done))

        self.play(FadeOut(VGroup(known, chain, done)), run_time=0.6)

        bad = VGroup(
            MathTex("n^2"), MathTex("\\ge", "25"), MathTex(">", "21"), MathTex("\\le", "2n+11"),
        ).arrange(RIGHT, buff=0.3).scale(1.2).move_to(UP * 0.5)
        arrows = VGroup()
        with self.beat("mixed") as beat:
            self.play(Write(bad[0]), Write(bad[1]), run_time=beat.until("bigger"))
            self.play(Write(bad[2]), run_time=beat.until("most"))
            self.play(Write(bad[3]), run_time=beat.until("Up"))
            for part, direction, color in ((bad[1], UP, GOOD), (bad[2], UP, GOOD), (bad[3], DOWN, BAD)):
                arrows.add(Arrow(ORIGIN, direction * 0.6, color=color, buff=0).next_to(part[0], DOWN, buff=0.35))
            self.play(LaggedStart(*(GrowArrow(a) for a in arrows), lag_ratio=0.5), run_time=beat.until("That"))
            cross = Cross(bad, stroke_color=BAD, stroke_width=6)
            self.play(Create(cross), run_time=beat.until("nothing"))

        with self.beat("outro") as beat:
            lean = Text("by rel [h]", font="Noto Sans Mono", font_size=40, color=GOOD)
            note = Text("substitutes and checks the direction", font_size=30, color=GREY_A).next_to(lean, DOWN, buff=0.4)
            self.play(FadeOut(VGroup(bad, arrows, cross)), FadeIn(lean), run_time=beat.until("checks"))
            self.play(FadeIn(note), run_time=beat.until("Push"))
        self.wait(0.8)
