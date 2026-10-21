"""Week 1 Day 1 explainer: Brahmagupta's identity, the big first step of Example 1.1.3 / 1.2.3.

Story: who Brahmagupta was, the old puzzle of doubling a square, near misses x² − 2y² = ±1, a way a
student could find Brahmagupta's rule with conjugates, the book's identity as that rule in disguise,
the expansion check, and the chain of near misses that reaches the Śulba-sūtra value 577/408.

Every algebra and arithmetic step is shown on screen (see CLAUDE.md: never hide steps).
All equations here are checked with Lean (ring / linear_combination / numbers) before rendering.
Brahmagupta's book states the rule without a derivation, so the discovery path is presented as
"one way you could have found it", not as his method.
"""

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.narration import NarratedScene  # noqa: E402

EXPLAINER = {"id": "w01d1/brahmagupta", "title": "Brahmagupta's identity", "scene": "Brahmagupta"}

NARRATION = {
    "monster": "In Example 1.1.3, the very first step is a monster. The book calls it Brahmagupta's "
               "identity, after the Indian mathematician who discovered it around the year 628.",
    "bio": "Brahmagupta was born in India in 598. He was an astronomer, and predicting where the planets will "
           "be takes a lot of arithmetic, including square roots. In 628, at the age of thirty, he finished a "
           "huge book of astronomy and mathematics, the Brahma-sphuta-siddhanta, in the city of Bhillamala. "
           "Later he led the observatory at Ujjain. His book is the oldest we know that treats zero as a number "
           "with rules of its own. It also has rules for positive and negative numbers, which he called "
           "fortunes and debts. One of those rules matters today: a debt times a debt is a fortune.",
    "altar": "Here's a puzzle that was already old in his day. Indian altar builders, in texts called the "
             "Shulba Sutras, needed a square with twice the area of another square. The trick is the diagonal. "
             "Cut a square in half along its diagonal. The square built on that diagonal is made of four of "
             "those halves, which is two whole squares. So the doubled square's side is the diagonal. And the "
             "diagonal is the square root of two times the side, because the square root of two, squared, is two.",
    "tiles": "But no fraction is exactly the square root of two, so builders needed good approximations. Look "
             "for whole numbers where one square is almost exactly two copies of another. A single tile is one "
             "short of two tiles. A three by three square is nine tiles, and two squares of two by two make "
             "eight: one tile over. In symbols, one squared minus two times one squared is one minus two, which "
             "is negative one. Three squared minus two times two squared is nine minus eight, which is positive "
             "one. Call these near misses. Each one gives a fraction near the square root of two: one over one, "
             "and three over two.",
    "question": "Here's the question anyone in his day could have asked: from the near misses you have, can you "
                "build a bigger one? A bigger square that misses by just one tile gives a fraction even closer "
                "to the square root of two. Brahmagupta found a rule that does exactly that. His book states "
                "the rule in verse, and doesn't say how he found it. So here's one way you could have found it "
                "yourself, using a tool from Algebra 2.",
    "conj": "In Algebra 2 you multiply by a conjugate to clear a square root. Multiply three plus two root two "
            "by three minus two root two, one pair at a time. You get nine, minus six root two, plus six root "
            "two, minus two root two times two root two, which is four times two, because root two times root "
            "two is two. The root twos cancel, leaving nine minus eight, which is one. That's our near miss, "
            "three squared minus two times two squared, hiding inside the product.",
    "square3": "Now square both of them. Three plus two root two, squared, is nine, plus six root two, plus six "
               "root two, plus four times two. Group the plain numbers and the root twos: seventeen plus twelve "
               "root two. Three minus two root two, squared, comes out the same way with minus signs: seventeen "
               "minus twelve root two.",
    "product": "Multiply those two results together. Their product is the square of the product we already "
               "found, so it's one squared, which is one. But a number times its conjugate always follows one "
               "pattern: x plus y root two, times x minus y root two, is x squared minus two y squared. So the "
               "same product is seventeen squared minus two times twelve squared. That makes seventeen and "
               "twelve a new near miss, still just one tile off, out of 289.",
    "gen1": "Does this work for any two near misses? Multiply x one plus y one root two by x two plus y two "
            "root two. You get four products, and the last is y one root two times y two root two, which is "
            "y one y two times two. Gather the plain parts and the root two parts. Call the plain part capital "
            "X, and the root two part capital Y. Now put minus signs in both brackets. The same four products "
            "come out, but the root two parts are subtracted. The last product stays positive, because a debt "
            "times a debt is a fortune. You get capital X minus capital Y root two.",
    "gen2": "Now multiply capital X plus capital Y root two by capital X minus capital Y root two. The "
            "conjugate pattern says that's X squared minus two Y squared. But it's also all four brackets "
            "multiplied together, and you can multiply them in any order. Pair each bracket with its own "
            "conjugate. The first pair gives x one squared minus two y one squared. The second gives x two "
            "squared minus two y two squared. So: put in two near misses, and you get a new pair whose miss "
            "is the two misses multiplied. That's Brahmagupta's rule.",
    "book": "And here is the monster from the book, in disguise. Rename x one, y one, x two and y two as b, a, "
            "m and n. Write the terms in the book's order. Then add two times a m plus b n, squared, to both "
            "sides. That's exactly Brahmagupta's identity.",
    "left": "The book checks it a different way, by expanding both sides. Let's do that too, one side at a "
            "time. Squaring two a n plus b m is like finding the area of a "
            "square with those two lengths along each side. It splits into four pieces. Two a n times two "
            "a n is four a squared n squared. Each side piece is two a n times b m, which is two a b m n. "
            "And b m times b m is b squared m squared.",
    "left2": "Now add the four pieces. The two middle pieces are the same, so two a b m n plus two a b m n "
             "is four a b m n. The left side is four a squared n squared, plus four a b m n, plus b squared "
             "m squared.",
    "right1": "Now the first part of the right side. Square a m plus b n the same way: a m squared, plus two "
              "times a m times b n, plus b n squared. That's a squared m squared, plus two a b m n, plus b "
              "squared n squared. Then multiply every term by two.",
    "right2": "The second part multiplies two brackets, so fill a box with every pair. m squared times b "
              "squared is b squared m squared. m squared times negative two a squared is negative two a "
              "squared m squared. Negative two n squared times b squared is negative two b squared n squared. "
              "And negative two n squared times negative two a squared is positive four a squared n squared, "
              "because a negative times a negative is positive.",
    "cancel": "Now add the two parts of the right side, and group the matching terms. Two a squared m squared "
              "minus two a squared m squared is zero. Two b squared n squared minus two b squared n squared is "
              "zero too. What's left is four a b m n, plus b squared m squared, plus four a squared n squared. "
              "Put those in the same order as the left side, and they match exactly. So the identity is true "
              "for every a, b, m and n.",
    "why": "So why use it? Because it makes both facts appear. a m plus b n is one, and b squared minus two "
           "a squared is zero. Substitute them in. One squared is one, so the first part is two times one. "
           "Anything times zero is zero. And two plus zero is two.",
    "chain1": "Now let's use the rule to build near misses. Start with the smallest, one and one, which misses "
              "by negative one: a debt of one tile. Use it for both pairs. The new x is one times one, plus two "
              "times one times one: one plus two, three. The new y is one times one, plus one times one: one "
              "plus one, two. The new miss is negative one times negative one. A debt times a debt is a "
              "fortune: positive one. Three and two, nine tiles against eight.",
    "chain2": "Now use three and two for both pairs. The new x is three times three, plus two times two times "
              "two: nine plus eight, seventeen. The new y is three times two, plus two times three: six plus "
              "six, twelve. The miss is one times one, which is one. Check it: seventeen squared minus two "
              "times twelve squared is 289 minus two times 144, which is 289 minus 288, which is one. The same "
              "pair the conjugates gave.",
    "chain3": "Do it again, with seventeen and twelve as the first pair, and three and two as the second. The "
              "new x is seventeen times three, plus two times twelve times two: fifty one plus forty eight, "
              "ninety nine. The new y is seventeen times two, plus twelve times three: thirty four plus thirty "
              "six, seventy. Ninety nine squared minus two times seventy squared is 9801 minus two times 4900, "
              "which is 9801 minus 9800: one again.",
    "chain4": "Once more, with ninety nine and seventy. The new x is ninety nine times three, plus two times "
              "seventy times two: two hundred ninety seven plus two hundred eighty, five hundred seventy seven. "
              "The new y is ninety nine times two, plus seventy times three: one hundred ninety eight plus two "
              "hundred ten, four hundred eight. And five hundred seventy seven squared minus two times four "
              "hundred eight squared works out, step by step, to one, yet again.",
    "sulba": "Look at that pair: five hundred seventy seven over four hundred eight. The Shulba Sutras give the "
             "diagonal of a square with side one as one, plus a third, plus a fourth of that third, minus a "
             "thirty fourth of that fourth. A fourth of a third is a twelfth, and a thirty fourth of a twelfth "
             "is one over four hundred eight. Over the common denominator, four hundred eight, that's four "
             "hundred eight, plus one hundred thirty six, plus thirty four, minus one, which is exactly five "
             "hundred seventy seven over four hundred eight. Whether the altar builders found it this way, no "
             "one knows. But with near misses and Brahmagupta's rule, you could have found it yourself.",
    "sqrt2": "Why do these fractions get close to the square root of two? Divide both sides of x squared "
             "minus two y squared equals one by y squared. That gives x over y, squared, minus two, equals one "
             "over y squared. So x over y, squared, is two plus one over y squared. For seventeen over twelve, "
             "that's two plus one over 144. For ninety nine over seventy, two plus one over 4900. And for five "
             "hundred seventy seven over four hundred eight, two plus one over one hundred sixty six thousand, "
             "four hundred sixty four. As y grows, the extra bit shrinks toward zero, so x over y gets closer "
             "and closer to the square root of two.",
    "outro": "In Lean, you don't have to do any of this by hand. ring checks the whole expansion in one step. "
             "But now you know where the monster comes from: an old puzzle about doubling a square, and a debt "
             "times a debt.",
}


# one color per kind of term, so matching terms are easy to follow
A = BLUE_C      # 4a²n²
B = GREEN_C     # abmn terms
C = YELLOW_C    # b²m²
D = PURPLE_B    # 2a²m²  (cancels)
E = ORANGE      # 2b²n²  (cancels)
R = TEAL_C      # √2 parts
NOTE = GREY_B


def chain(rows, scale=0.75, buff=0.32):
    """Equation rows with their "=" signs lined up.

    rows: list of (eq_index, [(tex, color), ...]); eq_index is the position of the "=" part.
    """
    mobs = []
    for eq_index, parts in rows:
        tex = MathTex(*(t for t, _ in parts)).scale(scale)
        for part, (_, color) in zip(tex, parts):
            part.set_color(color)
        tex.eq_index = eq_index
        mobs.append(tex)
    group = VGroup(*mobs).arrange(DOWN, buff=buff)
    x = mobs[0][mobs[0].eq_index].get_center()[0]
    for tex in mobs[1:]:
        tex.shift(RIGHT * (x - tex[tex.eq_index].get_center()[0]))
    return group


def cell_box(cols, rows, first, then, widths, heights, colors, scale=0.62):
    """Multiplication box. Each cell first shows its product (`first`), then its simplified value (`then`)."""
    rects, labels, finals = VGroup(), VGroup(), VGroup()
    ys = [0.0]
    for h in heights:
        ys.append(ys[-1] - h)
    xs = [0.0]
    for w in widths:
        xs.append(xs[-1] + w)
    for i in range(len(rows)):
        for j in range(len(cols)):
            rect = Rectangle(width=widths[j], height=heights[i], stroke_color=GREY_B, stroke_width=2,
                             fill_color=colors[i][j], fill_opacity=0.16)
            rect.move_to([(xs[j] + xs[j + 1]) / 2, (ys[i] + ys[i + 1]) / 2, 0])
            rects.add(rect)
            labels.add(MathTex(first[i][j], color=WHITE).scale(scale).move_to(rect))
            finals.add(MathTex(then[i][j], color=colors[i][j]).scale(scale + 0.06).move_to(rect))
    col_labels = VGroup(*(MathTex(c).scale(0.7).move_to([(xs[j] + xs[j + 1]) / 2, 0.32, 0]) for j, c in enumerate(cols)))
    row_labels = VGroup(*(MathTex(r).scale(0.7).move_to([-0.6, (ys[i] + ys[i + 1]) / 2, 0]) for i, r in enumerate(rows)))
    frame = VGroup(rects, col_labels, row_labels)
    return frame, labels, finals


def tiles(n, size, color):
    """An n-by-n square of unit tiles."""
    squares = VGroup(*(Square(size, stroke_color=GREY_B, stroke_width=2, fill_color=color, fill_opacity=0.55)
                       for _ in range(n * n)))
    return squares.arrange_in_grid(rows=n, cols=n, buff=0)


class Brahmagupta(NarratedScene):
    def summary_line(self, tex_parts, colors, index):
        line = MathTex(*tex_parts).scale(0.55)
        for part, color in zip(line, colors):
            part.set_color(color)
        line.to_corner(UL, buff=0.35).shift(DOWN * 0.42 * index)
        return line

    def show(self, beat, word, *animations, occurrence=1, run_time=0.9):
        """Play `animations` briskly, then hold until `word` is spoken."""
        self.play(*animations, run_time=min(run_time, beat.until(word, occurrence)))
        rest = beat.until(word, occurrence, minimum=0.0)
        if rest > 0.02:
            self.wait(rest)

    def construct(self):
        title = Text("Brahmagupta's identity", font_size=40).to_edge(UP, buff=0.5)
        identity = MathTex("(2an+bm)^2", "=", "2(am+bn)^2", "+", "(m^2-2n^2)(b^2-2a^2)").scale(0.95)
        date = Text("Brahmagupta, India, 628 CE", font_size=24, color=NOTE).next_to(identity, DOWN, buff=0.6)

        with self.beat("monster") as beat:
            self.play(Write(identity), run_time=beat.until("calls"))
            self.play(FadeIn(title, shift=DOWN * 0.2), run_time=beat.until("after"))
            self.play(FadeIn(date), run_time=beat.until("discovered"))

        # ---- who he was
        name = Text("Brahmagupta", font_size=46).to_edge(UP, buff=0.55)
        dates = Text("born 598, died around 670, India", font_size=24, color=NOTE).next_to(name, DOWN, buff=0.18)
        life = VGroup(
            Text("an astronomer: predicting the planets takes a lot of arithmetic", font_size=26),
            Text("628, age 30: finished the Brāhmasphuṭasiddhānta in Bhillamala", font_size=26),
            Text("later: head of the observatory at Ujjain", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(dates, DOWN, buff=0.55)
        zero = VGroup(Text("zero is a number:", font_size=26),
                      MathTex("a-a=0", ",\\quad", "a+0=a").scale(0.8)).arrange(RIGHT, buff=0.25)
        signs = Text("fortunes (positive) and debts (negative)", font_size=26)
        debt = Text("debt × debt = fortune", font_size=32, color=A)
        rules = VGroup(zero, signs, debt).arrange(DOWN, buff=0.28).to_edge(DOWN, buff=0.6)

        with self.beat("bio") as beat:
            self.show(beat, "astronomer", FadeOut(VGroup(title, date, identity)), FadeIn(name, shift=DOWN * 0.2), FadeIn(dates))
            self.show(beat, "finished", FadeIn(life[0], shift=RIGHT * 0.2))
            self.show(beat, "Later", FadeIn(life[1], shift=RIGHT * 0.2))
            self.show(beat, "oldest", FadeIn(life[2], shift=RIGHT * 0.2))
            self.show(beat, "fortunes", FadeIn(zero))
            self.show(beat, "One", FadeIn(signs))
            self.show(beat, "fortune", FadeIn(debt, scale=1.1))
            self.play(Indicate(debt, color=A))
        self.play(FadeOut(VGroup(name, dates, life, rules)), run_time=0.6)

        # ---- the old puzzle: a square with twice the area
        u = 1.25
        grid = VGroup(*(Square(u, stroke_color=GREY_B, stroke_width=2) for _ in range(4))).arrange_in_grid(rows=2, cols=2, buff=0)
        grid.move_to(LEFT * 3.4 + DOWN * 0.35)
        c = grid.get_center()
        corner = grid[0].copy().set_stroke(width=0).set_fill(BLUE_C, 0.45)
        corner_label = MathTex("1").scale(0.8).move_to(grid[0].get_center() + UL * 0.3)
        diag = Line(c + UP * u, c + LEFT * u, color=YELLOW_C, stroke_width=5)
        halves = VGroup(*(Polygon(c + p, c + q, c, stroke_width=0, fill_color=YELLOW_C, fill_opacity=0.4)
                          for p, q in ((UP * u, LEFT * u), (LEFT * u, DOWN * u), (DOWN * u, RIGHT * u), (RIGHT * u, UP * u))))
        tilted = Polygon(c + UP * u, c + LEFT * u, c + DOWN * u, c + RIGHT * u, color=YELLOW_C, stroke_width=5)
        altar_head = Text("Śulba-sūtras: a square with twice the area", font_size=30).to_edge(UP, buff=0.5)
        altar_notes = VGroup(
            Text("small square: area 1", font_size=26, color=BLUE_C),
            Text("tilted square: 4 halves = area 2", font_size=26, color=YELLOW_C),
            Text("its side is the diagonal", font_size=26),
            MathTex("\\text{diagonal} = \\sqrt{2}\\times\\text{side}").scale(0.8),
            MathTex("\\text{because } (\\sqrt{2})^2 = 2", color=NOTE).scale(0.7),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(RIGHT * 3.0 + DOWN * 0.35)

        with self.beat("altar") as beat:
            self.show(beat, "trick", FadeIn(altar_head), Create(grid), run_time=1.5)
            self.show(beat, "Cut", FadeIn(corner), FadeIn(corner_label), FadeIn(altar_notes[0]))
            self.show(beat, "built", Create(diag), FadeIn(halves[0]))
            self.show(beat, "which", Create(tilted), FadeIn(halves[1:]), run_time=1.5)
            self.show(beat, "So", FadeIn(altar_notes[1]))
            self.show(beat, "And", FadeIn(altar_notes[2]))
            self.show(beat, "because", FadeIn(altar_notes[3]))
            self.play(FadeIn(altar_notes[4]))
        self.play(FadeOut(VGroup(altar_head, grid, corner, corner_label, diag, halves, tilted, altar_notes)), run_time=0.6)

        # ---- near misses, in tiles
        t = 0.42
        tiles_head = Text("whole numbers: one square ≈ two copies of another", font_size=28).to_edge(UP, buff=0.5)
        small = VGroup(tiles(1, t, BLUE_C), Text("vs", font_size=24, color=NOTE),
                       VGroup(tiles(1, t, YELLOW_C), tiles(1, t, YELLOW_C)).arrange(RIGHT, buff=0.12)).arrange(RIGHT, buff=0.3)
        nine = tiles(3, t, BLUE_C)
        eights = VGroup(tiles(2, t, YELLOW_C), tiles(2, t, YELLOW_C)).arrange(RIGHT, buff=0.15)
        big = VGroup(nine, Text("vs", font_size=24, color=NOTE), eights).arrange(RIGHT, buff=0.3)
        VGroup(small, big).arrange(RIGHT, buff=1.6).move_to(UP * 1.45)
        cap_y = big.get_bottom()[1] - 0.4
        small_cap = MathTex("1 \\text{ vs } 2", "\\text{: one short}").scale(0.65).move_to([small.get_x(), cap_y, 0])
        small_cap[1].set_color(RED_C)
        big_cap = MathTex("9 \\text{ vs } 4+4=8", "\\text{: one over}").scale(0.65).move_to([big.get_x(), cap_y, 0])
        big_cap[1].set_color(GREEN_C)
        extra = nine[8].copy().set_fill(GREEN_C, 0.9)
        misses = chain([
            (1, [("1^2-2\\cdot 1^2", WHITE), ("=", WHITE), ("1-2", WHITE), ("=", WHITE), ("-1", RED_C)]),
            (1, [("3^2-2\\cdot 2^2", WHITE), ("=", WHITE), ("9-8", WHITE), ("=", WHITE), ("1", GREEN_C)]),
        ], scale=0.8, buff=0.35).move_to(DOWN * 1.45)
        miss_label = Text("near misses", font_size=24, color=NOTE).next_to(misses, LEFT, buff=0.6)
        fracs = VGroup(MathTex("\\tfrac{1}{1} = 1").scale(0.7), MathTex("\\tfrac{3}{2} = 1.5").scale(0.7))
        for frac, row in zip(fracs, misses):
            frac.move_to([misses.get_right()[0] + 1.4, row.get_y(), 0])
        root_ref = MathTex("\\sqrt{2}\\approx 1.414", color=NOTE).scale(0.6).next_to(fracs, DOWN, buff=0.3)

        with self.beat("tiles") as beat:
            self.show(beat, "single", FadeIn(tiles_head))
            self.show(beat, "three", FadeIn(small), FadeIn(small_cap))
            self.show(beat, "two", FadeIn(nine), occurrence=4)
            self.show(beat, "one", FadeIn(eights), occurrence=3)
            self.show(beat, "In", FadeIn(extra), FadeIn(big_cap))
            self.play(Write(misses[0]), run_time=beat.until("Three", 3))
            self.play(Write(misses[1]), run_time=beat.until("Call"))
            self.show(beat, "Each", FadeIn(miss_label))
            self.show(beat, "and", FadeIn(fracs[0]), occurrence=2)
            self.play(FadeIn(fracs[1]), FadeIn(root_ref))
        self.play(FadeOut(VGroup(tiles_head, small, small_cap, big, big_cap, extra, misses, miss_label, fracs, root_ref)),
                  run_time=0.6)

        # ---- the question, and an honest note about what history records
        q1 = Text("From the near misses you have,\ncan you build a bigger one?", font_size=34, line_spacing=1.2).move_to(UP * 1.6)
        q_note = Text("Brahmagupta's book gives the rule in verse, not how he found it.", font_size=24, color=NOTE).move_to(DOWN * 0.3)
        q_path = Text("One way you could find it: conjugates, from Algebra 2", font_size=28, color=GREEN_C).move_to(DOWN * 1.6)

        with self.beat("question") as beat:
            self.show(beat, "Brahmagupta", FadeIn(q1))
            self.show(beat, "So", FadeIn(q_note))
            self.play(FadeIn(q_path))
        self.play(FadeOut(VGroup(q1, q_note, q_path)), run_time=0.6)

        # ---- conjugates: the near miss 9 − 8 = 1 hides inside a product
        conj_head = Text("Conjugates (Algebra 2)", font_size=30).to_edge(UP, buff=0.5)
        cj = chain([
            (1, [("(3+2\\sqrt{2})(3-2\\sqrt{2})", WHITE), ("=", WHITE), ("3\\cdot 3", WHITE), ("-3\\cdot 2\\sqrt{2}", R),
                 ("+2\\sqrt{2}\\cdot 3", R), ("-2\\sqrt{2}\\cdot 2\\sqrt{2}", YELLOW_C)]),
            (0, [("=", WHITE), ("9", WHITE), ("-6\\sqrt{2}", R), ("+6\\sqrt{2}", R), ("-4\\cdot 2", YELLOW_C)]),
            (0, [("=", WHITE), ("9-8", WHITE)]),
            (0, [("=", WHITE), ("1", GREEN_C)]),
        ], scale=0.78, buff=0.4).move_to(UP * 0.5)
        rr = MathTex("\\sqrt{2}\\cdot\\sqrt{2} = 2", color=YELLOW_C).scale(0.65).next_to(cj[1], RIGHT, buff=0.6)
        cancel_note = Text("the √2 parts cancel", font_size=22, color=R).next_to(cj[2], RIGHT, buff=0.6)
        hidden = MathTex("3^2-2\\cdot 2^2", "=", "1", color=GREEN_C).scale(0.8).next_to(cj, DOWN, buff=0.6)
        hidden_note = Text("our near miss, hiding inside", font_size=22, color=NOTE).next_to(hidden, DOWN, buff=0.15)

        with self.beat("conj") as beat:
            self.show(beat, "Multiply", FadeIn(conj_head))
            self.play(Write(cj[0]), run_time=beat.until("You", 2))
            self.play(Write(cj[1]), run_time=beat.until("because"))
            self.show(beat, "The", FadeIn(rr))
            self.show(beat, "leaving", Indicate(cj[1][2], color=R), Indicate(cj[1][3], color=R), FadeIn(cancel_note), run_time=1.2)
            self.play(Write(cj[2]), run_time=beat.until("which", 2))
            self.play(Write(cj[3]), run_time=beat.until("That's"))
            self.show(beat, "hiding", FadeIn(hidden))
            self.play(FadeIn(hidden_note))
        sum0 = self.summary_line(["(3+2\\sqrt{2})(3-2\\sqrt{2})", "=", "1"], [WHITE, WHITE, GREEN_C], 0)
        self.play(FadeOut(VGroup(conj_head, cj[:3], rr, cancel_note, hidden, hidden_note)),
                  ReplacementTransform(cj[3], sum0), run_time=0.7)

        # ---- square both conjugates
        sq_plus = chain([
            (1, [("(3+2\\sqrt{2})^2", WHITE), ("=", WHITE), ("(3+2\\sqrt{2})(3+2\\sqrt{2})", WHITE)]),
            (0, [("=", WHITE), ("9", WHITE), ("+6\\sqrt{2}", R), ("+6\\sqrt{2}", R), ("+4\\cdot 2", YELLOW_C)]),
            (0, [("=", WHITE), ("(9+8)", WHITE), ("+", WHITE), ("(6\\sqrt{2}+6\\sqrt{2})", R)]),
            (0, [("=", WHITE), ("17", BLUE_C), ("+", WHITE), ("12\\sqrt{2}", BLUE_C)]),
        ], scale=0.62, buff=0.34)
        sq_minus = chain([
            (1, [("(3-2\\sqrt{2})^2", WHITE), ("=", WHITE), ("(3-2\\sqrt{2})(3-2\\sqrt{2})", WHITE)]),
            (0, [("=", WHITE), ("9", WHITE), ("-6\\sqrt{2}", R), ("-6\\sqrt{2}", R), ("+4\\cdot 2", YELLOW_C)]),
            (0, [("=", WHITE), ("(9+8)", WHITE), ("-", WHITE), ("(6\\sqrt{2}+6\\sqrt{2})", R)]),
            (0, [("=", WHITE), ("17", BLUE_C), ("-", WHITE), ("12\\sqrt{2}", BLUE_C)]),
        ], scale=0.62, buff=0.34)
        VGroup(sq_plus, sq_minus).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to(DOWN * 0.4)

        with self.beat("square3") as beat:
            self.play(Write(sq_plus[0]), run_time=beat.until("is"))
            self.play(Write(sq_plus[1]), run_time=beat.until("Group"))
            self.play(Write(sq_plus[2]), run_time=beat.until("seventeen"))
            self.play(Write(sq_plus[3]), run_time=beat.until("Three", 2))
            self.play(Write(sq_minus[0]), run_time=beat.until("comes"))
            self.play(Write(sq_minus[1]), run_time=beat.until("seventeen", 2))
            self.play(Write(sq_minus[2]), run_time=1.0)
            self.play(Write(sq_minus[3]), run_time=1.0)
        sum1 = self.summary_line(["(3+2\\sqrt{2})^2", "=", "17+12\\sqrt{2}"], [WHITE, WHITE, BLUE_C], 1)
        sum2 = self.summary_line(["(3-2\\sqrt{2})^2", "=", "17-12\\sqrt{2}"], [WHITE, WHITE, BLUE_C], 2)
        self.play(FadeOut(VGroup(sq_plus[:3], sq_minus[:3])), ReplacementTransform(sq_plus[3], sum1),
                  ReplacementTransform(sq_minus[3], sum2), run_time=0.7)

        # ---- multiply the two results
        pr = chain([
            (1, [("(17+12\\sqrt{2})(17-12\\sqrt{2})", BLUE_C), ("=", WHITE), ("(3+2\\sqrt{2})^2(3-2\\sqrt{2})^2", WHITE)]),
            (0, [("=", WHITE), ("[(3+2\\sqrt{2})(3-2\\sqrt{2})]^2", WHITE)]),
            (0, [("=", WHITE), ("1^2", GREEN_C)]),
            (0, [("=", WHITE), ("1", GREEN_C)]),
        ], scale=0.68, buff=0.28).move_to(UP * 0.45 + RIGHT * 1.2)
        pattern = chain([
            (1, [("(x+y\\sqrt{2})(x-y\\sqrt{2})", NOTE), ("=", NOTE), ("x^2-xy\\sqrt{2}+xy\\sqrt{2}-y^2\\cdot 2", NOTE)]),
            (0, [("=", NOTE), ("x^2-2y^2", NOTE)]),
        ], scale=0.6, buff=0.22).move_to(DOWN * 1.55)
        pr2 = MathTex("(17+12\\sqrt{2})(17-12\\sqrt{2})", "=", "17^2-2\\cdot 12^2").scale(0.68).move_to(DOWN * 2.75)
        pr2[0].set_color(BLUE_C)
        new_miss = MathTex("17^2-2\\cdot 12^2", "=", "1", color=GREEN_C).scale(0.9).move_to(DOWN * 0.6)
        new_note = Text("a new near miss: 289 tiles vs 288", font_size=24, color=GREEN_C).next_to(new_miss, DOWN, buff=0.25)

        with self.beat("product") as beat:
            self.play(Write(pr[0]), run_time=beat.until("so"))
            self.play(Write(pr[1]), run_time=beat.until("one"))
            self.play(Write(pr[2]), run_time=beat.until("which"))
            self.play(Write(pr[3]), run_time=beat.until("But"))
            self.play(Write(pattern[0]), run_time=beat.until("is", 3))
            self.play(Write(pattern[1]), run_time=beat.until("So", 2))
            self.play(Write(pr2), run_time=beat.until("That"))
            self.show(beat, "still", FadeOut(VGroup(pr[:3], pattern)), pr[3].animate.next_to(new_miss, UP, buff=1.2),
                      pr2.animate.move_to(UP * 1.6), Write(new_miss), run_time=1.5)
            self.play(FadeIn(new_note))
        self.play(FadeOut(VGroup(pr[3], pr2, new_miss, new_note, sum0, sum1, sum2)), run_time=0.6)

        # ---- any two near misses
        defs = VGroup(MathTex("X", "=", "x_1x_2+2y_1y_2"), MathTex("Y", "=", "x_1y_2+y_1x_2")).arrange(RIGHT, buff=1.2)
        defs.scale(0.7).to_edge(UP, buff=0.4)
        defs[0].set_color(BLUE_C)
        defs[1].set_color(GREEN_C)
        g = chain([
            (1, [("(x_1+y_1\\sqrt{2})(x_2+y_2\\sqrt{2})", WHITE), ("=", WHITE), ("x_1x_2", WHITE), ("+x_1y_2\\sqrt{2}", R),
                 ("+y_1x_2\\sqrt{2}", R), ("+y_1y_2\\cdot 2", YELLOW_C)]),
            (0, [("=", WHITE), ("(x_1x_2+2y_1y_2)", BLUE_C), ("+", WHITE), ("(x_1y_2+y_1x_2)", GREEN_C), ("\\sqrt{2}", R)]),
            (0, [("=", WHITE), ("X", BLUE_C), ("+", WHITE), ("Y", GREEN_C), ("\\sqrt{2}", R)]),
            (1, [("(x_1-y_1\\sqrt{2})(x_2-y_2\\sqrt{2})", WHITE), ("=", WHITE), ("x_1x_2", WHITE), ("-x_1y_2\\sqrt{2}", R),
                 ("-y_1x_2\\sqrt{2}", R), ("+y_1y_2\\cdot 2", YELLOW_C)]),
            (0, [("=", WHITE), ("(x_1x_2+2y_1y_2)", BLUE_C), ("-", WHITE), ("(x_1y_2+y_1x_2)", GREEN_C), ("\\sqrt{2}", R)]),
            (0, [("=", WHITE), ("X", BLUE_C), ("-", WHITE), ("Y", GREEN_C), ("\\sqrt{2}", R)]),
        ], scale=0.62, buff=0.3).move_to(DOWN * 0.35)
        g[3].shift(DOWN * 0.2)
        g[4:].shift(DOWN * 0.2)
        fortune = MathTex("(-y_1\\sqrt{2})(-y_2\\sqrt{2}) = +y_1y_2\\cdot 2", "\\quad\\text{debt}\\times\\text{debt} = \\text{fortune}",
                          color=A).scale(0.55).to_edge(DOWN, buff=0.3)

        with self.beat("gen1") as beat:
            self.play(Write(g[0]), run_time=beat.until("Gather"))
            self.play(Write(g[1]), run_time=beat.until("Call"))
            self.play(Write(g[2]), FadeIn(defs), run_time=beat.until("Now"))
            self.play(Write(g[3]), run_time=beat.until("last", 2))
            self.show(beat, "You", FadeIn(fortune), Indicate(g[3][5], color=A), occurrence=2, run_time=1.2)
            self.play(Write(g[4]), run_time=1.6)
            self.play(Write(g[5]), run_time=1.0)

        h = chain([
            (1, [("X^2-2Y^2", WHITE), ("=", WHITE), ("(X+Y\\sqrt{2})(X-Y\\sqrt{2})", WHITE)]),
            (0, [("=", WHITE), ("(x_1+y_1\\sqrt{2})(x_2+y_2\\sqrt{2})(x_1-y_1\\sqrt{2})(x_2-y_2\\sqrt{2})", WHITE)]),
            (0, [("=", WHITE), ("[(x_1+y_1\\sqrt{2})(x_1-y_1\\sqrt{2})]", BLUE_C), ("\\cdot", WHITE),
                 ("[(x_2+y_2\\sqrt{2})(x_2-y_2\\sqrt{2})]", YELLOW_C)]),
            (0, [("=", WHITE), ("(x_1^2-2y_1^2)", BLUE_C), ("(x_2^2-2y_2^2)", YELLOW_C)]),
        ], scale=0.62, buff=0.5).move_to(UP * 0.95)
        reorder2 = Text("same brackets, new order", font_size=20, color=NOTE).next_to(h[2], DOWN, buff=0.08)
        rule_full = MathTex("(x_1x_2+2y_1y_2)^2-2(x_1y_2+y_1x_2)^2", "=", "(x_1^2-2y_1^2)(x_2^2-2y_2^2)").scale(0.7)
        rule_full.move_to(DOWN * 2.0)
        rule_box = SurroundingRectangle(rule_full, color=GREEN_C, buff=0.18)
        rule_title = Text("Brahmagupta's rule", font_size=24, color=GREEN_C).next_to(rule_box, UP, buff=0.12)
        rule_caption = Text("the new pair's miss = first miss × second miss", font_size=22, color=NOTE).next_to(rule_box, DOWN, buff=0.15)

        with self.beat("gen2") as beat:
            self.show(beat, "The", FadeOut(VGroup(g, fortune)))
            self.play(Write(h[0]), run_time=beat.until("But"))
            self.play(Write(h[1]), run_time=beat.until("Pair"))
            self.play(Write(h[2]), FadeIn(reorder2), run_time=beat.until("first"))
            self.play(Write(VGroup(h[3][0], h[3][1])), run_time=beat.until("second"))
            self.play(Write(h[3][2]), run_time=beat.until("So"))
            self.play(Write(rule_full), Create(rule_box), run_time=beat.until("That's", 2))
            self.play(FadeIn(rule_title), FadeIn(rule_caption))

        # ---- the book's identity is this rule in disguise
        bk = chain([
            (1, [("(x_1x_2+2y_1y_2)^2-2(x_1y_2+y_1x_2)^2", WHITE), ("=", WHITE), ("(x_1^2-2y_1^2)(x_2^2-2y_2^2)", WHITE)]),
            (1, [("(bm+2an)^2-2(bn+am)^2", WHITE), ("=", WHITE), ("(b^2-2a^2)(m^2-2n^2)", WHITE)]),
            (1, [("(2an+bm)^2-2(am+bn)^2", WHITE), ("=", WHITE), ("(m^2-2n^2)(b^2-2a^2)", WHITE)]),
            (1, [("(2an+bm)^2", YELLOW_C), ("=", WHITE), ("2(am+bn)^2+(m^2-2n^2)(b^2-2a^2)", YELLOW_C)]),
        ], scale=0.7, buff=0.62).move_to(UP * 0.4)
        bk_notes = VGroup(
            MathTex("x_1, y_1, x_2, y_2 \\;\\to\\; b, a, m, n", color=NOTE).scale(0.55).next_to(bk[1], DOWN, buff=0.1),
            Text("same terms, in the book's order", font_size=20, color=NOTE).next_to(bk[2], DOWN, buff=0.1),
            Text("add 2(am + bn)² to both sides", font_size=20, color=NOTE).next_to(bk[3], DOWN, buff=0.1),
        )
        bk_box = SurroundingRectangle(bk[3], color=YELLOW_C, buff=0.15)

        with self.beat("book") as beat:
            self.show(beat, "Rename", FadeOut(VGroup(h, reorder2, defs, rule_box, rule_title, rule_caption)),
                      ReplacementTransform(rule_full, bk[0]), run_time=1.2)
            self.play(Write(bk[1]), FadeIn(bk_notes[0]), run_time=beat.until("Write"))
            self.play(Write(bk[2]), FadeIn(bk_notes[1]), run_time=beat.until("Then"))
            self.play(Write(bk[3]), FadeIn(bk_notes[2]), run_time=beat.until("That's"))
            self.play(Create(bk_box))
        book_group = VGroup(bk, bk_notes, bk_box)

        # ---- left side: the area box, every cell written as a product first
        sq_frame, sq_first, sq_then = cell_box(
            ["2an", "bm"], ["2an", "bm"],
            [["2an\\cdot 2an", "2an\\cdot bm"], ["bm\\cdot 2an", "bm\\cdot bm"]],
            [["4a^2n^2", "2abmn"], ["2abmn", "b^2m^2"]],
            [2.3, 1.7], [1.4, 1.1], [[A, B], [B, C]])
        sq = VGroup(sq_frame, sq_first, sq_then).move_to(UP * 0.9)
        left_chain = chain([
            (1, [("(2an+bm)^2", WHITE), ("=", WHITE), ("4a^2n^2", A), ("+", WHITE), ("2abmn", B), ("+", WHITE),
                 ("2abmn", B), ("+", WHITE), ("b^2m^2", C)]),
            (0, [("=", WHITE), ("4a^2n^2", A), ("+", WHITE), ("(2abmn+2abmn)", B), ("+", WHITE), ("b^2m^2", C)]),
            (0, [("=", WHITE), ("4a^2n^2", A), ("+", WHITE), ("4abmn", B), ("+", WHITE), ("b^2m^2", C)]),
        ]).move_to(DOWN * 2.15)

        with self.beat("left") as beat:
            self.show(beat, "Squaring", FadeOut(book_group))
            self.play(Create(sq_frame[0]), FadeIn(sq_frame[1]), FadeIn(sq_frame[2]), run_time=beat.until("pieces"))
            self.play(FadeIn(sq_first[0]), run_time=beat.until("is", 2))
            self.play(ReplacementTransform(sq_first[0], sq_then[0]), run_time=beat.until("Each", 2))
            self.play(FadeIn(sq_first[1]), FadeIn(sq_first[2]), run_time=beat.until("which"))
            self.play(ReplacementTransform(sq_first[1], sq_then[1]), ReplacementTransform(sq_first[2], sq_then[2]),
                      run_time=beat.until("And"))
            self.play(FadeIn(sq_first[3]), run_time=beat.until("is", 5))
            self.play(ReplacementTransform(sq_first[3], sq_then[3]), run_time=beat.until("squared", 4) + 0.4)

        with self.beat("left2") as beat:
            self.play(TransformFromCopy(VGroup(*sq_then), left_chain[0]), run_time=beat.until("same"))
            self.play(Write(left_chain[1]), run_time=beat.until("is"))
            self.play(Write(left_chain[2]), run_time=beat.until("left"))
            self.play(Indicate(left_chain[2], scale_factor=1.05), run_time=beat.until("plus", 2))
        sum_L = self.summary_line(["\\text{left: }", "4a^2n^2", "+", "4abmn", "+", "b^2m^2"], [NOTE, A, WHITE, B, WHITE, C], 0)
        self.play(FadeOut(sq), ReplacementTransform(left_chain[2].copy(), sum_L), FadeOut(left_chain), run_time=0.8)

        # ---- right side, first part
        rule = MathTex("(p+q)^2 = p^2 + 2pq + q^2", color=NOTE).scale(0.65).move_to(UP * 2.3)
        r1 = chain([
            (1, [("(am+bn)^2", WHITE), ("=", WHITE), ("(am)^2", D), ("+", WHITE), ("2\\cdot am\\cdot bn", B), ("+", WHITE), ("(bn)^2", E)]),
            (0, [("=", WHITE), ("a^2m^2", D), ("+", WHITE), ("2abmn", B), ("+", WHITE), ("b^2n^2", E)]),
            (1, [("2(am+bn)^2", WHITE), ("=", WHITE), ("2\\cdot a^2m^2", D), ("+", WHITE), ("2\\cdot 2abmn", B), ("+", WHITE), ("2\\cdot b^2n^2", E)]),
            (0, [("=", WHITE), ("2a^2m^2", D), ("+", WHITE), ("4abmn", B), ("+", WHITE), ("2b^2n^2", E)]),
        ], scale=0.78, buff=0.38).move_to(DOWN * 0.2)

        with self.beat("right1") as beat:
            self.play(FadeIn(rule), Write(r1[0]), run_time=beat.until("That's"))
            self.play(Write(r1[1]), run_time=beat.until("Then"))
            self.play(Write(r1[2]), run_time=beat.until("two", 3))
            self.play(Write(r1[3]))
        sum_R1 = self.summary_line(["\\text{right, part 1: }", "2a^2m^2", "+", "4abmn", "+", "2b^2n^2"], [NOTE, D, WHITE, B, WHITE, E], 1)
        self.play(FadeOut(rule), ReplacementTransform(r1[3].copy(), sum_R1), FadeOut(r1), run_time=0.8)

        # ---- right side, second part: every cell of the product box
        pb_frame, pb_first, pb_then = cell_box(
            ["b^2", "-2a^2"], ["m^2", "-2n^2"],
            [["m^2\\cdot b^2", "m^2\\cdot(-2a^2)"], ["(-2n^2)\\cdot b^2", "(-2n^2)(-2a^2)"]],
            [["b^2m^2", "-2a^2m^2"], ["-2b^2n^2", "+4a^2n^2"]],
            [2.8, 2.8], [0.95, 0.95], [[C, D], [E, A]], scale=0.58)
        pb = VGroup(pb_frame, pb_first, pb_then).move_to(UP * 0.7)
        sign = Text("negative × negative = positive", font_size=22, color=A).next_to(pb_frame[0][3], RIGHT, buff=0.3)
        r2 = chain([(1, [("(m^2-2n^2)(b^2-2a^2)", WHITE), ("=", WHITE), ("b^2m^2", C), ("-", WHITE), ("2a^2m^2", D),
                         ("-", WHITE), ("2b^2n^2", E), ("+", WHITE), ("4a^2n^2", A)])], scale=0.78).move_to(DOWN * 1.6)

        with self.beat("right2") as beat:
            self.play(Create(pb_frame[0]), FadeIn(pb_frame[1]), FadeIn(pb_frame[2]), run_time=beat.until("squared"))
            for k, word, occurrence in ((0, "is", 1), (1, "is", 2), (2, "is", 3)):
                self.play(FadeIn(pb_first[k]), run_time=beat.until(word, occurrence))
                self.play(ReplacementTransform(pb_first[k], pb_then[k]), run_time=0.6)
            self.play(FadeIn(pb_first[3]), run_time=beat.until("positive"))
            self.play(ReplacementTransform(pb_first[3], pb_then[3]), FadeIn(sign), run_time=beat.until("because"))
            self.play(TransformFromCopy(VGroup(*pb_then), r2[0]), run_time=beat.until("positive", 2))
        sum_R2 = self.summary_line(["\\text{right, part 2: }", "b^2m^2", "-", "2a^2m^2", "-", "2b^2n^2", "+", "4a^2n^2"],
                                   [NOTE, C, WHITE, D, WHITE, E, WHITE, A], 2)
        self.play(FadeOut(pb), FadeOut(sign), ReplacementTransform(r2[0].copy(), sum_R2), FadeOut(r2), run_time=0.8)

        # ---- add the two parts and group the cancelling pairs
        add = chain([
            (1, [("\\text{right}", WHITE), ("=", WHITE), ("(2a^2m^2", D), ("+4abmn", B), ("+2b^2n^2)", E), ("+", WHITE),
                 ("(b^2m^2", C), ("-2a^2m^2", D), ("-2b^2n^2", E), ("+4a^2n^2)", A)]),
            (0, [("=", WHITE), ("(2a^2m^2-2a^2m^2)", D), ("+", WHITE), ("(2b^2n^2-2b^2n^2)", E), ("+", WHITE),
                 ("4abmn", B), ("+", WHITE), ("b^2m^2", C), ("+", WHITE), ("4a^2n^2", A)]),
            (0, [("=", WHITE), ("0", D), ("+", WHITE), ("0", E), ("+", WHITE), ("4abmn", B), ("+", WHITE), ("b^2m^2", C),
                 ("+", WHITE), ("4a^2n^2", A)]),
            (0, [("=", WHITE), ("4a^2n^2", A), ("+", WHITE), ("4abmn", B), ("+", WHITE), ("b^2m^2", C)]),
        ], scale=0.7, buff=0.42).move_to(DOWN * 0.55)
        reorder = Text("same terms, reordered", font_size=22, color=NOTE).next_to(add[3], RIGHT, buff=0.4)

        with self.beat("cancel") as beat:
            self.play(Write(add[0]), run_time=beat.until("group"))
            self.play(Write(add[1]), run_time=beat.until("zero"))
            self.play(Indicate(add[1][1], color=D), run_time=beat.until("Two", 4))
            self.play(Indicate(add[1][3], color=E), run_time=beat.until("What's"))
            self.play(Write(add[2]), run_time=beat.until("Put"))
            self.play(Write(add[3]), FadeIn(reorder), run_time=beat.until("match"))
            self.play(Indicate(add[3], scale_factor=1.05), Indicate(sum_L, scale_factor=1.1), run_time=beat.until("So"))
            check = Text("✓ true for every a, b, m, n", font_size=28, color=GREEN_C).next_to(add, DOWN, buff=0.45)
            self.play(FadeIn(check, shift=UP * 0.2))
        self.play(FadeOut(VGroup(add, reorder, check, sum_L, sum_R1, sum_R2)), run_time=0.6)

        # ---- why the proof uses it: both facts appear, then one step at a time
        f1 = MathTex("am+bn", "=", "1")
        f2 = MathTex("b^2-2a^2", "=", "0")
        f1[0].set_color(BLUE_C)
        f2[0].set_color(YELLOW_C)
        facts = VGroup(f1, f2).arrange(RIGHT, buff=1.2).move_to(UP * 2.7)
        sub = chain([
            (1, [("(2an+bm)^2", WHITE), ("=", WHITE), ("2", WHITE), ("(am+bn)", BLUE_C), ("^2", WHITE), ("+", WHITE),
                 ("(m^2-2n^2)", WHITE), ("(b^2-2a^2)", YELLOW_C)]),
            (0, [("=", WHITE), ("2", WHITE), ("\\cdot", WHITE), ("1", BLUE_C), ("^2", WHITE), ("+", WHITE), ("(m^2-2n^2)", WHITE),
                 ("\\cdot", WHITE), ("0", YELLOW_C)]),
            (0, [("=", WHITE), ("2\\cdot 1", WHITE), ("+", WHITE), ("0", YELLOW_C)]),
            (0, [("=", WHITE), ("2", GREEN_C)]),
        ], scale=0.9, buff=0.45).move_to(DOWN * 0.2)

        with self.beat("why") as beat:
            self.play(FadeIn(sub[0]), run_time=beat.until("Because"))
            self.play(Write(f1), Indicate(sub[0][3], color=BLUE_C), run_time=beat.until("and"))
            self.play(Write(f2), Indicate(sub[0][7], color=YELLOW_C), run_time=beat.until("Substitute"))
            self.play(Write(sub[1]), run_time=beat.until("One", 2))
            self.play(Write(sub[2]), run_time=beat.until("Anything") + 1.5)
            self.play(Write(sub[3]), run_time=beat.until("two", 4))
        self.play(FadeOut(VGroup(sub, facts)), run_time=0.6)

        # ---- build near misses with the rule
        rule_top = MathTex("(x_1x_2+2y_1y_2)^2-2(x_1y_2+y_1x_2)^2", "=", "(x_1^2-2y_1^2)(x_2^2-2y_2^2)",
                           color=NOTE).scale(0.55).to_edge(UP, buff=0.35)
        rule_hint = MathTex("x = x_1x_2+2y_1y_2", "\\qquad", "y = x_1y_2+y_1x_2", color=NOTE).scale(0.55)
        rule_hint.next_to(rule_top, DOWN, buff=0.15)

        def pair_steps(rows, center):
            return chain(rows, scale=0.7, buff=0.3).move_to(center)

        c1 = pair_steps([
            (1, [("1^2-2\\cdot 1^2", WHITE), ("=", WHITE), ("1-2", WHITE), ("=", WHITE), ("-1", RED_C)]),
            (1, [("x", WHITE), ("=", WHITE), ("1\\cdot 1+2\\cdot 1\\cdot 1", WHITE), ("=", WHITE), ("1+2", WHITE), ("=", WHITE), ("3", BLUE_C)]),
            (1, [("y", WHITE), ("=", WHITE), ("1\\cdot 1+1\\cdot 1", WHITE), ("=", WHITE), ("1+1", WHITE), ("=", WHITE), ("2", BLUE_C)]),
            (1, [("\\text{miss}", WHITE), ("=", WHITE), ("(-1)\\cdot(-1)", RED_C), ("=", WHITE), ("1", GREEN_C)]),
            (1, [("3^2-2\\cdot 2^2", WHITE), ("=", WHITE), ("9-8", WHITE), ("=", WHITE), ("1", GREEN_C)]),
        ], DOWN * 0.55)
        pairs1 = MathTex("x_1, y_1 = 1, 1 \\qquad x_2, y_2 = 1, 1", color=NOTE).scale(0.6).next_to(c1, UP, buff=0.3)
        fortune2 = Text("debt × debt = fortune", font_size=24, color=A).next_to(c1[3], RIGHT, buff=0.6)

        with self.beat("chain1") as beat:
            self.show(beat, "Start", FadeOut(book_group), FadeIn(rule_top), FadeIn(rule_hint))
            self.play(Write(c1[0]), run_time=beat.until("Use", 2))
            self.show(beat, "new", FadeIn(pairs1))
            self.play(Write(c1[1]), run_time=beat.until("new", 2))
            self.play(Write(c1[2]), run_time=beat.until("new", 3))
            self.play(Write(c1[3]), run_time=beat.until("debt", 2))
            self.show(beat, "Three", FadeIn(fortune2), occurrence=2)
            self.play(Write(c1[4]), run_time=1.2)

        s2 = pair_steps([
            (1, [("x", WHITE), ("=", WHITE), ("3\\cdot 3+2\\cdot 2\\cdot 2", WHITE), ("=", WHITE), ("9+8", WHITE), ("=", WHITE), ("17", BLUE_C)]),
            (1, [("y", WHITE), ("=", WHITE), ("3\\cdot 2+2\\cdot 3", WHITE), ("=", WHITE), ("6+6", WHITE), ("=", WHITE), ("12", BLUE_C)]),
            (1, [("\\text{miss}", WHITE), ("=", WHITE), ("1\\cdot 1", WHITE), ("=", WHITE), ("1", GREEN_C)]),
            (1, [("17^2-2\\cdot 12^2", WHITE), ("=", WHITE), ("289-2\\cdot 144", WHITE), ("=", WHITE), ("289-288", WHITE), ("=", WHITE), ("1", GREEN_C)]),
        ], DOWN * 0.45)
        pairs2 = MathTex("x_1, y_1 = 3, 2 \\qquad x_2, y_2 = 3, 2", color=NOTE).scale(0.6).next_to(s2, UP, buff=0.3)

        with self.beat("chain2") as beat:
            self.show(beat, "new", FadeOut(VGroup(c1, pairs1, fortune2)), FadeIn(pairs2))
            self.play(Write(s2[0]), run_time=beat.until("new", 2))
            self.play(Write(s2[1]), run_time=beat.until("miss"))
            self.play(Write(s2[2]), run_time=beat.until("Check"))
            self.play(Write(s2[3]), run_time=beat.until("same"))
            self.play(Indicate(s2[0][6]), Indicate(s2[1][6]))

        s3 = pair_steps([
            (1, [("x", WHITE), ("=", WHITE), ("17\\cdot 3+2\\cdot 12\\cdot 2", WHITE), ("=", WHITE), ("51+48", WHITE), ("=", WHITE), ("99", YELLOW_C)]),
            (1, [("y", WHITE), ("=", WHITE), ("17\\cdot 2+12\\cdot 3", WHITE), ("=", WHITE), ("34+36", WHITE), ("=", WHITE), ("70", YELLOW_C)]),
            (1, [("99^2-2\\cdot 70^2", WHITE), ("=", WHITE), ("9801-2\\cdot 4900", WHITE), ("=", WHITE), ("9801-9800", WHITE), ("=", WHITE), ("1", GREEN_C)]),
        ], DOWN * 0.3)
        pairs3 = MathTex("x_1, y_1 = 17, 12 \\qquad x_2, y_2 = 3, 2", color=NOTE).scale(0.6).next_to(s3, UP, buff=0.3)

        with self.beat("chain3") as beat:
            self.show(beat, "new", FadeOut(VGroup(s2, pairs2)), FadeIn(pairs3))
            self.play(Write(s3[0]), run_time=beat.until("new", 2))
            self.play(Write(s3[1]), run_time=beat.until("Ninety", 2))
            self.play(Write(s3[2]), run_time=beat.until("again", 2))

        s4 = chain([
            (1, [("x", WHITE), ("=", WHITE), ("99\\cdot 3+2\\cdot 70\\cdot 2", WHITE), ("=", WHITE), ("297+280", WHITE), ("=", WHITE), ("577", GREEN_C)]),
            (1, [("y", WHITE), ("=", WHITE), ("99\\cdot 2+70\\cdot 3", WHITE), ("=", WHITE), ("198+210", WHITE), ("=", WHITE), ("408", GREEN_C)]),
            (1, [("577^2-2\\cdot 408^2", WHITE), ("=", WHITE), ("332929-2\\cdot 166464", WHITE), ("=", WHITE), ("332929-332928", WHITE),
                 ("=", WHITE), ("1", GREEN_C)]),
        ], scale=0.64, buff=0.3).move_to(DOWN * 0.3)
        pairs4 = MathTex("x_1, y_1 = 99, 70 \\qquad x_2, y_2 = 3, 2", color=NOTE).scale(0.6).next_to(s4, UP, buff=0.3)

        with self.beat("chain4") as beat:
            self.show(beat, "new", FadeOut(VGroup(s3, pairs3)), FadeIn(pairs4))
            self.play(Write(s4[0]), run_time=beat.until("new", 2))
            self.play(Write(s4[1]), run_time=beat.until("And", 2))
            self.play(Write(s4[2]), run_time=beat.until("yet"))

        # ---- the altar builders' value is the very next near miss
        big_frac = MathTex("\\frac{577}{408}", color=GREEN_C).scale(1.3)
        sb_head = Text("Śulba-sūtras: the diagonal of a square with side 1", font_size=26).to_edge(UP, buff=0.45)
        sb = chain([
            (1, [("\\text{diagonal}", WHITE), ("\\approx", WHITE), ("1+\\frac{1}{3}+\\frac{1}{3\\cdot 4}-\\frac{1}{3\\cdot 4\\cdot 34}", WHITE)]),
            (0, [("=", WHITE), ("1+\\frac{1}{3}+\\frac{1}{12}-\\frac{1}{408}", WHITE)]),
            (0, [("=", WHITE), ("\\frac{408}{408}+\\frac{136}{408}+\\frac{34}{408}-\\frac{1}{408}", WHITE)]),
            (0, [("=", WHITE), ("\\frac{408+136+34-1}{408}", WHITE)]),
            (0, [("=", WHITE), ("\\frac{577}{408}", GREEN_C)]),
        ], scale=0.72, buff=0.28).move_to(DOWN * 0.45 + LEFT * 0.8)
        denom_note = MathTex("408 = 3\\cdot 136 = 12\\cdot 34", color=NOTE).scale(0.55).next_to(sb[2], RIGHT, buff=0.5)
        nobody = Text("How they found it, no one knows.", font_size=22, color=NOTE).to_edge(DOWN, buff=0.3)

        with self.beat("sulba") as beat:
            self.show(beat, "Shulba", FadeOut(VGroup(s4, pairs4, rule_top, rule_hint)), FadeIn(big_frac))
            self.show(beat, "as", big_frac.animate.scale(0.7).to_corner(UR, buff=0.5), FadeIn(sb_head))
            self.play(Write(sb[0]), run_time=beat.until("twelfth"))
            self.play(Write(sb[1]), run_time=beat.until("Over", 3))
            self.play(Write(sb[2]), FadeIn(denom_note), run_time=beat.until("minus", 2))
            self.play(Write(sb[3]), run_time=beat.until("which"))
            self.play(Write(sb[4]), run_time=beat.until("Whether"))
            self.show(beat, "But", Indicate(big_frac), Indicate(sb[4]), FadeIn(nobody), run_time=1.2)
        self.play(FadeOut(VGroup(big_frac, sb_head, sb, denom_note, nobody)), run_time=0.6)

        # ---- why the fractions approach √2
        root = chain([
            (1, [("x^2-2y^2", WHITE), ("=", WHITE), ("1", WHITE)]),
            (1, [("\\frac{x^2}{y^2}-2", WHITE), ("=", WHITE), ("\\frac{1}{y^2}", WHITE)]),
            (1, [("\\left(\\frac{x}{y}\\right)^2", WHITE), ("=", WHITE), ("2+\\frac{1}{y^2}", GREEN_C)]),
        ], scale=0.8, buff=0.35).move_to(UP * 1.9 + LEFT * 3.4)
        divide = Text("divide both sides by y²", font_size=20, color=NOTE).next_to(root[1], RIGHT, buff=0.35)
        cases = chain([
            (1, [("\\left(\\tfrac{17}{12}\\right)^2", BLUE_C), ("=", WHITE), ("2+\\tfrac{1}{144}", WHITE)]),
            (1, [("\\left(\\tfrac{99}{70}\\right)^2", YELLOW_C), ("=", WHITE), ("2+\\tfrac{1}{4900}", WHITE)]),
            (1, [("\\left(\\tfrac{577}{408}\\right)^2", GREEN_C), ("=", WHITE), ("2+\\tfrac{1}{166464}", WHITE)]),
        ], scale=0.72, buff=0.3).move_to(UP * 1.9 + RIGHT * 3.6)
        line = NumberLine(x_range=[1.410, 1.418, 0.002], length=11, include_numbers=True,
                          decimal_number_config={"num_decimal_places": 3}, font_size=22).move_to(DOWN * 2.0)
        marks = VGroup()
        for value, tex, color, direction in ((17 / 12, "\\tfrac{17}{12}\\approx 1.4167", BLUE_C, UP),
                                             (99 / 70, "\\tfrac{99}{70}\\approx 1.4143", YELLOW_C, UP),
                                             (577 / 408, "\\tfrac{577}{408}\\approx 1.41422", GREEN_C, UP),
                                             (2 ** 0.5, "\\sqrt2\\approx 1.41421", WHITE, DOWN)):
            dot = Dot(line.n2p(value), color=color)
            label = MathTex(tex, color=color).scale(0.65).next_to(dot, direction, buff=0.3)
            marks.add(VGroup(dot, label))
        marks[1][1].shift(LEFT * 1.3)
        marks[2][1].shift(RIGHT * 1.3 + UP * 0.4)
        shrink = Text("1/y² → 0 as y grows", font_size=24, color=GREEN_C).move_to(DOWN * 0.05)

        with self.beat("sqrt2") as beat:
            self.play(Write(root[0]), run_time=beat.until("by", 1))
            self.play(Write(root[1]), FadeIn(divide), run_time=beat.until("So"))
            self.play(Write(root[2]), run_time=beat.until("For"))
            self.play(Write(cases[0]), Create(line), FadeIn(marks[0]), run_time=beat.until("For", 2))
            self.play(Write(cases[1]), FadeIn(marks[1]), run_time=beat.until("And"))
            self.play(Write(cases[2]), FadeIn(marks[2]), run_time=beat.until("As"))
            self.play(FadeIn(shrink), FadeIn(marks[3]), run_time=beat.until("closer"))

        with self.beat("outro") as beat:
            lean = Text(":= by ring", font="Noto Sans Mono", font_size=48, color=TEAL_C)
            moral = Text("an old puzzle about doubling a square,\nand a debt times a debt", font_size=28,
                         color=NOTE, line_spacing=1.2).move_to(DOWN * 1.2)
            self.play(FadeOut(VGroup(root, divide, cases, line, marks, shrink)), run_time=beat.until("ring"))
            self.play(Write(lean), run_time=beat.until("whole"))
            self.show(beat, "old", lean.animate.shift(UP * 0.8))
            self.play(FadeIn(moral))
        self.wait(0.8)
