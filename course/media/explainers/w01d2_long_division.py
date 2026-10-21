"""Week 1 Day 2 explainer: polynomial long division, the scratch work behind Example 1.3.10."""

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.narration import NarratedScene  # noqa: E402

EXPLAINER = {"id": "w01d2/long-division", "title": "Polynomial long division", "scene": "LongDivision"}

NARRATION = {
    "slick": "In Example 1.3.10, the first line looks almost like magic. Where did z squared minus z plus one "
             "come from? The book's author found it with polynomial long division. Let's see how it works.",
    "numbers": "Start with plain numbers: thirteen seventy one, divided by twelve. Twelve goes into thirteen "
               "once, leaving one. Bring down the seven. Twelve goes into seventeen once, leaving five. Bring "
               "down the one. Twelve goes into fifty one four times, leaving three.",
    "numbers2": "So thirteen seventy one equals twelve times one hundred fourteen, plus a remainder of three. "
                "Polynomials work exactly the same way.",
    "setup": "Divide z to the fourth, minus z cubed, minus z squared, plus two z, plus one, by z squared minus "
             "two. Line up the terms by their power of z, like digits in columns.",
    "step1": "How many times does z squared go into z to the fourth? z squared times. Multiply it back: z "
             "squared times the divisor is z to the fourth, minus two z squared. Subtract, and the leading "
             "term disappears.",
    "step2": "Next, z squared goes into negative z cubed, negative z times. Multiply back: negative z cubed, "
             "plus two z. Subtract again.",
    "step3": "Last, z squared goes into z squared once. Multiply back, subtract, and three is left over. Three "
             "has no z squared in it, so it's the remainder.",
    "result": "So the polynomial equals the divisor, times z squared minus z plus one, plus three. That's "
              "exactly the book's first line.",
    "payoff": "And our fact says z squared minus two is zero. That wipes out the whole first part, so the "
              "answer is just the remainder: three.",
    "outro": "In the proof, you don't show any of this. It's scratch work for finding the identity, and ring "
             "checks it in one step. Try the same trick on exercise fourteen.",
}

QUOT = YELLOW_C     # quotient terms
SUB = BLUE_C        # what gets subtracted
REM = GREEN_C       # the remainder
DIVISOR = TEAL_C


class Grid:
    """Place MathTex pieces in (column, row) cells, so terms of the same degree line up."""

    def __init__(self, origin, col_width, row_height, scale=0.9):
        self.origin = np.array(origin, dtype=float)
        self.cw = col_width
        self.rh = row_height
        self.scale = scale

    def point(self, col, row):
        return self.origin + RIGHT * col * self.cw + DOWN * row * self.rh

    def tex(self, s, col, row, color=WHITE):
        return MathTex(s, color=color).scale(self.scale).move_to(self.point(col, row))

    def underline(self, col_from, col_to, row):
        y = self.point(0, row)[1] - self.rh / 2
        return Line(self.point(col_from, row)[0] * RIGHT + UP * y + LEFT * self.cw * 0.45,
                    self.point(col_to, row)[0] * RIGHT + UP * y + RIGHT * self.cw * 0.45,
                    color=GREY_B, stroke_width=2)

    def bracket(self, col_from, col_to, row, divisor_width):
        """The long-division bracket: a bar over the dividend row and a short stroke on its left."""
        top = self.point(0, row)[1] + self.rh / 2
        left = self.point(col_from, row)[0] - self.cw * 0.55
        right = self.point(col_to, row)[0] + self.cw * 0.5
        bar = Line([left, top, 0], [right, top, 0], color=WHITE, stroke_width=3)
        stroke = ArcBetweenPoints([left, top, 0], [left - 0.12, top - self.rh, 0], angle=-PI / 5,
                                  color=WHITE, stroke_width=3)
        return VGroup(bar, stroke)


class LongDivision(NarratedScene):
    def construct(self):
        slick = MathTex("z^4-z^3-z^2+2z+1", "=", "(z^2-z+1)", "(z^2-2)", "+3").scale(0.95)
        slick[2].set_color(QUOT)
        question = Text("where did this come from?", font_size=28, color=GREY_B).next_to(slick[2], UP, buff=0.5)
        title = Text("Polynomial long division", font_size=40).to_edge(UP, buff=0.6)

        with self.beat("slick") as beat:
            self.play(Write(slick), run_time=beat.until("Where"))
            self.play(Indicate(slick[2], color=QUOT), FadeIn(question, shift=DOWN * 0.2), run_time=beat.until("author"))
            self.play(FadeIn(title, shift=DOWN * 0.2), run_time=beat.until("Let's"))
        self.play(FadeOut(VGroup(slick, question)), run_time=0.5)

        # --- warm-up: 1371 ÷ 12, one digit per column
        g = Grid(origin=[-1.2, 2.2, 0], col_width=0.55, row_height=0.55, scale=0.9)
        divisor = g.tex("12", -1.6, 1, DIVISOR)
        digits = VGroup(*(g.tex(d, c, 1) for c, d in enumerate("1371")))
        bracket = g.bracket(0, 3, 1, 0)
        q = [g.tex("1", 1, 0, QUOT), g.tex("1", 2, 0, QUOT), g.tex("4", 3, 0, QUOT)]
        s1 = VGroup(g.tex("1", 0, 2, SUB), g.tex("2", 1, 2, SUB))
        u1 = g.underline(0, 1, 2)
        r1 = VGroup(g.tex("1", 1, 3), g.tex("7", 2, 3))
        s2 = VGroup(g.tex("1", 1, 4, SUB), g.tex("2", 2, 4, SUB))
        u2 = g.underline(1, 2, 4)
        r2 = VGroup(g.tex("5", 2, 5), g.tex("1", 3, 5))
        s3 = VGroup(g.tex("4", 2, 6, SUB), g.tex("8", 3, 6, SUB))
        u3 = g.underline(2, 3, 6)
        r3 = g.tex("3", 3, 7, REM)
        warmup = VGroup(divisor, digits, bracket, *q, s1, u1, r1, s2, u2, r2, s3, u3, r3)

        with self.beat("numbers") as beat:
            self.play(FadeOut(title), FadeIn(divisor), Write(digits), Create(bracket), run_time=beat.until("Twelve", 2))
            self.play(Write(q[0]), run_time=beat.until("once"))
            self.play(Write(s1), Create(u1), FadeIn(r1[0]), run_time=beat.until("Bring"))
            self.play(TransformFromCopy(digits[2], r1[1]), run_time=beat.until("Twelve", 3))
            self.play(Write(q[1]), Write(s2), Create(u2), FadeIn(r2[0]), run_time=beat.until("Bring", 2))
            self.play(TransformFromCopy(digits[3], r2[1]), run_time=beat.until("Twelve", 4))
            self.play(Write(q[2]), Write(s3), Create(u3), run_time=beat.until("leaving", 3))
            self.play(Write(r3), run_time=beat.until("three"))

        check = MathTex("1371", "=", "12", "\\cdot", "114", "+", "3").scale(1.0).move_to(RIGHT * 3.6 + UP * 0.2)
        check[2].set_color(DIVISOR)
        check[4].set_color(QUOT)
        check[6].set_color(REM)
        with self.beat("numbers2") as beat:
            self.play(Write(check), run_time=beat.until("Polynomials"))
            self.play(Indicate(check, scale_factor=1.05))
        self.play(FadeOut(VGroup(warmup, check)), run_time=0.5)

        # --- z⁴ − z³ − z² + 2z + 1 divided by z² − 2: column c holds the z^(4−c) terms
        p = Grid(origin=[-2.2, 3.1, 0], col_width=1.35, row_height=0.62, scale=0.85)
        pdivisor = p.tex("z^2-2", -1.55, 1, DIVISOR)
        dividend = VGroup(p.tex("z^4", 0, 1), p.tex("-z^3", 1, 1), p.tex("-z^2", 2, 1),
                          p.tex("+2z", 3, 1), p.tex("+1", 4, 1))
        pbracket = p.bracket(0, 4, 1, 0)
        columns = VGroup(*(MathTex(t, color=GREY_C).scale(0.6).move_to(p.point(c, 1) + UP * 1.25)
                           for c, t in enumerate(["z^4", "z^3", "z^2", "z", "1"])))
        pq = [p.tex("z^2", 2, 0, QUOT), p.tex("-z", 3, 0, QUOT), p.tex("+1", 4, 0, QUOT)]
        ps1 = VGroup(p.tex("-(z^4", 0, 2, SUB), p.tex("-2z^2)", 2, 2, SUB))
        pu1 = p.underline(0, 4, 2)
        pr1 = VGroup(p.tex("-z^3", 1, 3), p.tex("+z^2", 2, 3), p.tex("+2z", 3, 3), p.tex("+1", 4, 3))
        ps2 = VGroup(p.tex("-(-z^3", 1, 4, SUB), p.tex("+2z)", 3, 4, SUB))
        pu2 = p.underline(1, 4, 4)
        pr2 = VGroup(p.tex("z^2", 2, 5), p.tex("+1", 4, 5))
        ps3 = VGroup(p.tex("-(z^2", 2, 6, SUB), p.tex("-2)", 4, 6, SUB))
        pu3 = p.underline(2, 4, 6)
        pr3 = p.tex("3", 4, 7, REM)
        division = VGroup(pdivisor, dividend, pbracket, *pq, ps1, pu1, pr1, ps2, pu2, pr2, ps3, pu3, pr3)

        with self.beat("setup") as beat:
            self.play(Write(dividend), run_time=beat.until("by"))
            self.play(FadeIn(pdivisor), Create(pbracket), run_time=beat.until("Line"))
            self.play(LaggedStart(*(FadeIn(c, shift=DOWN * 0.15) for c in columns), lag_ratio=0.2),
                      run_time=beat.until("columns"))

        with self.beat("step1") as beat:
            self.play(Indicate(dividend[0]), Indicate(pdivisor[0][0:2], color=DIVISOR), run_time=beat.until("squared", 2))
            self.play(Write(pq[0]), run_time=beat.until("Multiply"))
            self.play(Write(ps1), run_time=beat.until("Subtract"))
            self.play(Create(pu1), Write(pr1), run_time=beat.until("leading"))
            self.play(Indicate(dividend[0], color=GREY_B), run_time=beat.until("disappears"))

        with self.beat("step2") as beat:
            self.play(Write(pq[1]), run_time=beat.until("Multiply"))
            self.play(Write(ps2), run_time=beat.until("Subtract"))
            self.play(Create(pu2), Write(pr2))

        with self.beat("step3") as beat:
            self.play(Write(pq[2]), run_time=beat.until("Multiply"))
            self.play(Write(ps3), run_time=beat.until("subtract"))
            self.play(Create(pu3), Write(pr3), run_time=beat.until("left"))
            rem_box = SurroundingRectangle(pr3, color=REM, buff=0.12)
            rem_label = Text("remainder", font_size=24, color=REM).next_to(rem_box, RIGHT, buff=0.25)
            self.play(Create(rem_box), FadeIn(rem_label), run_time=beat.until("remainder"))

        result = MathTex("z^4-z^3-z^2+2z+1", "=", "(z^2-2)", "(z^2-z+1)", "+", "3").scale(0.85)
        result[2].set_color(DIVISOR)
        result[3].set_color(QUOT)
        result[5].set_color(REM)
        result.to_edge(DOWN, buff=0.55)
        with self.beat("result") as beat:
            self.play(TransformFromCopy(dividend, result[0]), Write(result[1]), TransformFromCopy(pdivisor, result[2]),
                      run_time=beat.until("times"))
            self.play(TransformFromCopy(VGroup(*pq), result[3]), run_time=beat.until("plus", 2))
            self.play(Write(result[4]), TransformFromCopy(pr3, result[5]), run_time=beat.until("That's"))
            self.play(Indicate(result, scale_factor=1.05))

        with self.beat("payoff") as beat:
            self.play(FadeOut(VGroup(division, columns, rem_box, rem_label)), result.animate.move_to(UP * 1.2),
                      run_time=beat.until("zero"))
            zero = MathTex("0", color=DIVISOR).scale(0.85).move_to(result[2])
            self.play(Transform(result[2], zero), run_time=beat.until("wipes"))
            gone = VGroup(result[2], result[3], result[4])
            self.play(gone.animate.set_opacity(0.25), run_time=beat.until("answer"))
            answer = MathTex("=", "3", color=REM).scale(1.1).next_to(result, DOWN, buff=0.6).align_to(result[1], LEFT)
            self.play(Write(answer), run_time=beat.until("three"))

        with self.beat("outro") as beat:
            lean = Text(":= by ring", font="Noto Sans Mono", font_size=44, color=TEAL_C).move_to(DOWN * 0.3)
            scratch = Text("long division = scratch work", font_size=28, color=GREY_B).next_to(lean, UP, buff=0.6)
            self.play(FadeOut(VGroup(result, answer)), FadeIn(scratch), run_time=beat.until("ring"))
            self.play(Write(lean), run_time=beat.until("Try"))
            ex = MathTex("t^2-4=0", "\\;\\Rightarrow\\;", "t^4+3t^3-3t^2-2t-2=10t+2").scale(0.8).next_to(lean, DOWN, buff=0.8)
            self.play(FadeIn(ex, shift=UP * 0.2), run_time=beat.until("fourteen"))
        self.wait(0.8)
