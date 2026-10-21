"""Week 1 Day 1 explainer: Brahmagupta's identity, the big first step of Example 1.1.3 / 1.2.3."""

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.narration import NarratedScene  # noqa: E402

EXPLAINER = {"id": "w01d1/brahmagupta", "title": "Brahmagupta's identity", "scene": "Brahmagupta"}

NARRATION = {
    "monster": "In Example 1.1.3, the very first step is a monster. The book calls it Brahmagupta's "
               "identity, after the Indian mathematician who discovered it around the year 628.",
    "left": "Let's check it, one side at a time. Squaring two a n plus b m is like finding the area of a "
            "square with those two lengths along each side. There are four pieces: four a squared n squared, "
            "two copies of two a b m n, and b squared m squared.",
    "right1": "On the right, two times a m plus b n, squared, gives two a squared m squared, plus four a b m "
              "n, plus two b squared n squared.",
    "right2": "The product of the two brackets fills another box: b squared m squared, minus two a squared m "
              "squared, minus two b squared n squared, plus four a squared n squared.",
    "cancel": "Now add up the right side. Two a squared m squared cancels with its negative partner. So does "
              "two b squared n squared. What's left is exactly the left side. So the identity is true for "
              "every a, b, m and n.",
    "why": "So why use it? Because it makes both facts appear. a m plus b n is one, and b squared minus two "
           "a squared is zero. Substitute, and everything collapses to two.",
    "story": "Brahmagupta cared for a different reason. His identity turns one solution of x squared minus two "
             "y squared equals one into a bigger one. Three and two work. Feed them in, and out come "
             "seventeen and twelve. Again, and you get ninety nine and seventy.",
    "sqrt2": "And the fractions seventeen over twelve, then ninety nine over seventy, get closer and closer "
             "to the square root of two.",
    "outro": "In Lean, you don't have to do any of this by hand. ring checks the whole expansion in one step.",
}

# one color per kind of term, so matching terms are easy to follow
A = BLUE_C      # 4a²n²
B = GREEN_C     # 4abmn
C = YELLOW_C    # b²m²
D = PURPLE_B    # 2a²m²  (cancels)
E = ORANGE      # 2b²n²  (cancels)


def box(cols, rows, cells, widths, heights, colors):
    """A labelled multiplication box: column/row labels and one MathTex per cell."""
    group = VGroup()
    x0, y0 = 0.0, 0.0
    ys = [y0]
    for h in heights:
        ys.append(ys[-1] - h)
    xs = [x0]
    for w in widths:
        xs.append(xs[-1] + w)
    for i in range(len(rows)):
        for j in range(len(cols)):
            rect = Rectangle(width=widths[j], height=heights[i], stroke_color=GREY_B, stroke_width=2,
                             fill_color=colors[i][j], fill_opacity=0.18)
            rect.move_to([(xs[j] + xs[j + 1]) / 2, (ys[i] + ys[i + 1]) / 2, 0])
            label = MathTex(cells[i][j], color=colors[i][j]).scale(0.7).move_to(rect)
            group.add(VGroup(rect, label))
    col_labels = VGroup(*(MathTex(c).scale(0.7).move_to([(xs[j] + xs[j + 1]) / 2, y0 + 0.3, 0])
                          for j, c in enumerate(cols)))
    row_labels = VGroup(*(MathTex(r).scale(0.7).move_to([x0 - 0.5, (ys[i] + ys[i + 1]) / 2, 0])
                          for i, r in enumerate(rows)))
    return VGroup(group, col_labels, row_labels)


def align_equals(rows, x):
    for row in rows:
        row.shift(RIGHT * (x - row[1].get_center()[0]))


class Brahmagupta(NarratedScene):
    def construct(self):
        title = Text("Brahmagupta's identity", font_size=40).to_edge(UP, buff=0.5)
        identity = MathTex("(2an+bm)^2", "=", "2(am+bn)^2", "+", "(m^2-2n^2)(b^2-2a^2)").scale(0.95)
        date = Text("Brahmagupta, India, c. 628 CE", font_size=24, color=GREY_B).next_to(identity, DOWN, buff=0.6)

        with self.beat("monster") as beat:
            self.play(Write(identity), run_time=beat.until("calls"))
            self.play(FadeIn(title, shift=DOWN * 0.2), run_time=beat.until("after"))
            self.play(FadeIn(date), run_time=beat.until("discovered"))

        # three expansions, stacked with their "=" signs lined up
        L = MathTex("(2an+bm)^2", "=", "4a^2n^2", "+", "4abmn", "+", "b^2m^2").scale(0.8)
        R1 = MathTex("2(am+bn)^2", "=", "2a^2m^2", "+", "4abmn", "+", "2b^2n^2").scale(0.8)
        R2 = MathTex("(m^2-2n^2)(b^2-2a^2)", "=", "b^2m^2", "-", "2a^2m^2", "-", "2b^2n^2", "+", "4a^2n^2").scale(0.8)
        for tex, part, color in ((L, 2, A), (L, 4, B), (L, 6, C), (R1, 2, D), (R1, 4, B), (R1, 6, E),
                                 (R2, 2, C), (R2, 4, D), (R2, 6, E), (R2, 8, A)):
            tex[part].set_color(color)
        L.move_to(UP * 2.3)
        R1.move_to(UP * 1.4)
        R2.move_to(UP * 0.5)
        align_equals([L, R1, R2], -0.6)

        square = box(["2an", "bm"], ["2an", "bm"], [["4a^2n^2", "2abmn"], ["2abmn", "b^2m^2"]],
                     [2.4, 1.6], [2.4, 1.6], [[A, B], [B, C]]).move_to(DOWN * 1.6)

        with self.beat("left") as beat:
            self.play(FadeOut(title), FadeOut(date), ReplacementTransform(identity[0], L[0]),
                      FadeOut(identity[1:]), run_time=beat.until("Squaring"))
            self.play(Create(square[0]), FadeIn(square[1]), FadeIn(square[2]), run_time=beat.until("four", 1))
            self.play(Write(L[1:]), run_time=beat.until("squared", 3) + 0.8)
        self.play(FadeOut(square), run_time=0.4)

        with self.beat("right1") as beat:
            self.play(Write(R1), run_time=beat.until("plus", 2) + 1.2)

        product = box(["b^2", "-2a^2"], ["m^2", "-2n^2"], [["b^2m^2", "-2a^2m^2"], ["-2b^2n^2", "4a^2n^2"]],
                      [2.2, 2.2], [1.0, 1.0], [[C, D], [E, A]]).move_to(DOWN * 1.9)

        with self.beat("right2") as beat:
            self.play(FadeIn(R2[0]), Create(product[0]), FadeIn(product[1]), FadeIn(product[2]),
                      run_time=beat.until("b"))
            self.play(Write(R2[1:]), run_time=beat.until("squared", 7))
        self.play(FadeOut(product), run_time=0.4)

        total = MathTex("4abmn", "+", "b^2m^2", "+", "4a^2n^2").scale(0.8)
        total[0].set_color(B)
        total[2].set_color(C)
        total[4].set_color(A)
        sum_label = MathTex("\\text{right side} =").scale(0.8)
        sum_line = VGroup(sum_label, total).arrange(RIGHT, buff=0.25).move_to(DOWN * 1.1)
        sum_line.shift(RIGHT * (-0.6 - sum_label.get_right()[0] + 0.25))

        with self.beat("cancel") as beat:
            pair_d = VGroup(R1[2], R2[3], R2[4])
            pair_e = VGroup(R1[6], R2[5], R2[6])
            self.play(Indicate(R1[2], color=D), Indicate(R2[4], color=D), run_time=beat.until("cancels"))
            s1 = Line(R1[2].get_left(), R1[2].get_right(), color=GREY_A, stroke_width=4)
            s2 = Line(R2[3].get_left(), R2[4].get_right(), color=GREY_A, stroke_width=4)
            self.play(Create(s1), Create(s2), pair_d.animate.set_opacity(0.35), run_time=beat.until("So"))
            s3 = Line(R1[6].get_left(), R1[6].get_right(), color=GREY_A, stroke_width=4)
            s4 = Line(R2[5].get_left(), R2[6].get_right(), color=GREY_A, stroke_width=4)
            self.play(Create(s3), Create(s4), pair_e.animate.set_opacity(0.35), run_time=beat.until("What's"))
            self.play(FadeIn(sum_label), TransformFromCopy(R1[4], total[0]), TransformFromCopy(R2[2], total[2]),
                      TransformFromCopy(R2[8], total[4]), FadeIn(total[1]), FadeIn(total[3]),
                      run_time=beat.until("exactly"))
            self.play(Indicate(L[2:], scale_factor=1.08), Indicate(total, scale_factor=1.08), run_time=beat.until("So", 2))
            check = Text("✓ true for every a, b, m, n", font_size=30, color=GREEN_C).next_to(sum_line, DOWN, buff=0.6)
            self.play(FadeIn(check, shift=UP * 0.2))

        self.play(FadeOut(VGroup(L, R1, R2, s1, s2, s3, s4, sum_line, check)), run_time=0.6)

        # why the proof uses it: both facts appear
        ident = MathTex("(2an+bm)^2", "=", "2", "(am+bn)", "^2", "+", "(m^2-2n^2)", "(b^2-2a^2)").scale(0.95).move_to(UP * 1.2)
        f1 = MathTex("am+bn", "=", "1")
        f2 = MathTex("b^2-2a^2", "=", "0")
        f1[0].set_color(BLUE_C)
        f2[0].set_color(YELLOW_C)
        facts = VGroup(f1, f2).arrange(RIGHT, buff=1.2).move_to(UP * 2.7)
        result = MathTex("=", "2", "\\cdot", "1", "^2", "+", "(m^2-2n^2)", "\\cdot", "0", "=", "2").scale(0.95)
        result.next_to(ident, DOWN, buff=0.6).align_to(ident[1], LEFT)

        with self.beat("why") as beat:
            self.play(FadeIn(ident), run_time=beat.until("Because"))
            self.play(Write(f1), ident[3].animate.set_color(BLUE_C), run_time=beat.until("and"))
            self.play(Write(f2), ident[7].animate.set_color(YELLOW_C), run_time=beat.until("Substitute"))
            self.play(Write(result[:3]), TransformFromCopy(f1[2], result[3]), Write(result[4:8]),
                      TransformFromCopy(f2[2], result[8]), run_time=beat.until("collapses"))
            self.play(Write(result[9:]), run_time=beat.until("two", 2) + 0.3)

        self.play(FadeOut(VGroup(ident, facts, result)), run_time=0.6)

        # Brahmagupta's own use: new solutions of x² − 2y² = 1
        pell = MathTex("x^2-2y^2=1").scale(1.1).to_edge(UP, buff=0.7)
        rows = VGroup(
            MathTex("(3,\\,2)", ":", "\\;9-8=1"),
            MathTex("(17,\\,12)", ":", "\\;289-288=1"),
            MathTex("(99,\\,70)", ":", "\\;9801-9800=1"),
        ).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to(RIGHT * 1.2 + DOWN * 0.3)
        for row, color in zip(rows, (BLUE_C, GREEN_C, YELLOW_C)):
            row[0].set_color(color)
        # arrows bulge out to the left of the list, labelled on that side, clear of the arithmetic
        feeds = VGroup(*(CurvedArrow(rows[i][0].get_left() + LEFT * 0.15, rows[i + 1][0].get_left() + LEFT * 0.15,
                                     angle=TAU / 3, color=GREY_B) for i in range(2)))
        feed_label = Text("Brahmagupta's\nidentity", font_size=22, color=GREY_B, line_spacing=1.0)
        feed_label.next_to(feeds, LEFT, buff=0.25)

        with self.beat("story") as beat:
            self.play(Write(pell), run_time=beat.until("Three"))
            self.play(FadeIn(rows[0]), run_time=beat.until("Feed"))
            self.play(Create(feeds[0]), FadeIn(feed_label), run_time=beat.until("seventeen"))
            self.play(FadeIn(rows[1]), run_time=beat.until("Again"))
            self.play(Create(feeds[1]), run_time=beat.until("ninety"))
            self.play(FadeIn(rows[2]))

        line = NumberLine(x_range=[1.410, 1.418, 0.002], length=11, include_numbers=True,
                          decimal_number_config={"num_decimal_places": 3}, font_size=24).move_to(DOWN * 1.5)
        root2 = 2 ** 0.5
        marks = VGroup()
        for value, tex, color, direction in ((17 / 12, "\\tfrac{17}{12}", GREEN_C, UP),
                                             (99 / 70, "\\tfrac{99}{70}", YELLOW_C, UP),
                                             (root2, "\\sqrt2", WHITE, DOWN)):
            dot = Dot(line.n2p(value), color=color)
            label = MathTex(tex, color=color).scale(0.8).next_to(dot, direction, buff=0.35)
            marks.add(VGroup(dot, label))

        with self.beat("sqrt2") as beat:
            self.play(VGroup(pell, rows, feeds, feed_label).animate.scale(0.75).to_edge(UP, buff=0.4),
                      Create(line), run_time=beat.until("seventeen"))
            self.play(FadeIn(marks[0], scale=1.5), run_time=beat.until("ninety"))
            self.play(FadeIn(marks[1], scale=1.5), run_time=beat.until("closer"))
            self.play(FadeIn(marks[2], scale=1.5), run_time=beat.until("square"))

        with self.beat("outro") as beat:
            lean = Text(":= by ring", font="Noto Sans Mono", font_size=48, color=TEAL_C)
            self.play(FadeOut(VGroup(pell, rows, feeds, feed_label, line, marks)), run_time=beat.until("ring"))
            self.play(Write(lean), run_time=beat.until("whole"))
        self.wait(0.8)
