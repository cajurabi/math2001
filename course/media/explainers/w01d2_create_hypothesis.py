"""Week 1 Day 2 explainer: making a fact appear inside the goal (Examples 1.3.2 and 1.3.6)."""

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.narration import NarratedScene  # noqa: E402

EXPLAINER = {"id": "w01d2/create-hypothesis", "title": "Making the facts appear", "scene": "CreateHypothesis"}

NARRATION = {
    "goal": "Here's the fact: x plus four equals two. And here's the goal: show that x equals negative two. "
            "The trouble is, the fact talks about x plus four, but the goal only has x.",
    "create": "So we make x plus four appear. Add four, and take away four. That's adding zero, so it's "
              "still just x.",
    "swap": "Now x plus four sits right inside our expression. Swap it for two, because that's what the "
            "fact says it equals.",
    "finish": "And two minus four is negative two. Done.",
    "system": "The same trick works with two facts at once. To get x from these two, add them up. Group the "
              "x's, the y's, and the number: two x minus x is x, minus y plus y is zero, and there's a plus "
              "one. So the sum is x plus one.",
    "system2": "So x is the first fact, plus the second, minus one. Swap in four and two. Four plus two is "
               "six, and six minus one is five. So x is five.",
    "outro": "Every proof in this section asks the same question: how can I rearrange the goal, so that the "
             "facts appear inside it?",
}

FACT = BLUE_C
FACT2 = YELLOW_C
ZERO = GREY_B


class CreateHypothesis(NarratedScene):
    def construct(self):
        fact = MathTex("x+4", "=", "2")
        fact[0].set_color(FACT)
        fact_box = SurroundingRectangle(fact, color=GREY_B, buff=0.25, corner_radius=0.1)
        fact_label = Text("Fact", font_size=26, color=GREY_B).next_to(fact_box, UP, buff=0.15)
        fact_group = VGroup(fact_label, fact_box, fact).to_corner(UL, buff=0.6)
        goal = MathTex("x", "=", "-2", "\\;?").scale(1.3).move_to(UP * 0.8)

        with self.beat("goal") as beat:
            self.play(FadeIn(fact_label), Create(fact_box), Write(fact), run_time=beat.until("here's", 2))
            self.play(Write(goal), run_time=beat.until("trouble"))
            self.play(Indicate(fact[0], color=FACT), run_time=beat.until("goal", 2))
            self.play(Indicate(goal[0], color=WHITE))

        # build the chain under the goal
        lhs = MathTex("x").scale(1.2)
        r1 = MathTex("=", "(x+4)", "-4").scale(1.2)
        r2 = MathTex("=", "2", "-4").scale(1.2)
        r3 = MathTex("=", "-2").scale(1.2)
        r1.next_to(lhs, RIGHT, buff=0.2)
        r2.next_to(r1, DOWN, buff=0.45, aligned_edge=LEFT)
        r3.next_to(r2, DOWN, buff=0.45, aligned_edge=LEFT)
        chain = VGroup(lhs, r1, r2, r3).move_to(DOWN * 0.9)

        with self.beat("create") as beat:
            self.play(FadeOut(goal[3]), goal[:3].animate.scale(0.75).to_edge(UP, buff=0.7),
                      FadeIn(lhs), run_time=beat.until("Add"))
            self.play(Write(r1), run_time=beat.until("That's"))
            plus = r1[1][2:4]  # "+4" inside the parentheses
            brace = Brace(VGroup(plus, r1[2]), DOWN, color=ZERO)
            zero = MathTex("+4-4=0", color=ZERO).scale(0.8).next_to(brace, DOWN, buff=0.1)
            self.play(GrowFromCenter(brace), FadeIn(zero), run_time=beat.until("still"))
        self.play(FadeOut(brace), FadeOut(zero), run_time=0.4)

        with self.beat("swap") as beat:
            self.play(r1[1].animate.set_color(FACT), Indicate(fact[0], color=FACT), run_time=beat.until("Swap"))
            self.play(Write(r2[0]), TransformFromCopy(fact[2], r2[1]), Write(r2[2]), run_time=beat.until("because"))

        with self.beat("finish") as beat:
            self.play(Write(r3), run_time=beat.until("negative"))
            check = Text("✓", font_size=48, color=GREEN_C).next_to(r3, RIGHT, buff=0.4)
            self.play(FadeIn(check, scale=1.4), run_time=beat.until("Done"))

        self.play(FadeOut(VGroup(fact_group, goal[:3], chain, check)), run_time=0.6)

        # two facts at once (Example 1.3.6)
        f1 = MathTex("2x-y", "=", "4")
        f2 = MathTex("y-x+1", "=", "2")
        f1[0].set_color(FACT)
        f2[0].set_color(FACT2)
        facts = VGroup(f1, f2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        facts_box = SurroundingRectangle(facts, color=GREY_B, buff=0.25, corner_radius=0.1)
        facts_label = Text("Facts", font_size=26, color=GREY_B).next_to(facts_box, UP, buff=0.15)
        known = VGroup(facts_label, facts_box, facts).to_corner(UL, buff=0.6)
        total = MathTex("(", "2x", "-y", ")", "+", "(", "y", "-x+1", ")", "=", "x+1").scale(1.15).move_to(UP * 0.3)
        VGroup(*total[0:4]).set_color(FACT)
        VGroup(*total[5:9]).set_color(FACT2)

        # add the facts, grouping like terms one step at a time
        add = VGroup(
            MathTex("(2x-y)", "+", "(y-x+1)"),
            MathTex("=", "(2x-x)", "+", "(-y+y)", "+1"),
            MathTex("=", "x", "+", "0", "+1"),
            MathTex("=", "x+1"),
        ).scale(1.0).arrange(DOWN, buff=0.3)
        add[0][0].set_color(FACT)
        add[0][2].set_color(FACT2)
        add[1][3].set_color(ZERO)
        add[2][3].set_color(ZERO)
        for row in add[1:]:  # "=" signs lined up, indented under the sum
            row.shift(RIGHT * (add[0].get_left()[0] + 0.5 - row[0].get_left()[0]))
        add.move_to(UP * 0.1 + RIGHT * 0.8)

        with self.beat("system") as beat:
            self.play(FadeIn(facts_label), Create(facts_box), Write(facts), run_time=beat.until("add"))
            self.play(Write(add[0]), run_time=beat.until("Group"))
            self.play(Write(add[1]), run_time=beat.until("two", 3))
            self.play(Write(add[2]), run_time=beat.until("So"))
            self.play(Write(add[3]), run_time=1.0)
        self.play(FadeOut(add), FadeIn(total), run_time=0.7)

        x0 = MathTex("x").scale(1.15)
        s1 = MathTex("=", "(2x-y)", "+", "(y-x+1)", "-1").scale(1.15)
        s2 = MathTex("=", "4", "+", "2", "-1").scale(1.15)
        s3 = MathTex("=", "5").scale(1.15)
        s1[1].set_color(FACT)
        s1[3].set_color(FACT2)
        s1.next_to(x0, RIGHT, buff=0.2)
        s2.next_to(s1, DOWN, buff=0.45, aligned_edge=LEFT)
        s3.next_to(s2, DOWN, buff=0.45, aligned_edge=LEFT)
        chain2 = VGroup(x0, s1, s2, s3).move_to(DOWN * 1.6)

        work = MathTex("4+2-1", "=", "6-1", "=", "5", color=GREY_A).scale(0.8)

        with self.beat("system2") as beat:
            self.play(FadeIn(x0), Write(s1), run_time=beat.until("Swap"))
            self.play(Write(s2[0]), TransformFromCopy(f1[2], s2[1]), Write(s2[2]),
                      TransformFromCopy(f2[2], s2[3]), Write(s2[4]), run_time=beat.until("Four", 2))
            work.next_to(VGroup(s2, s3), RIGHT, buff=1.0)
            self.play(Write(work[:3]), run_time=beat.until("and", 2))
            self.play(Write(work[3:]), run_time=beat.until("So", 2))
            self.play(Write(s3), run_time=beat.until("five", 2))

        with self.beat("outro") as beat:
            question = Text("How can I rearrange the goal\nso that the facts appear inside it?",
                            font_size=36, line_spacing=1.2)
            self.play(FadeOut(VGroup(known, total, chain2, work)), run_time=beat.until("question"))
            self.play(Write(question), run_time=beat.until("facts") + 0.4)
        self.wait(0.8)
