# Interactive course on *The Mechanics of Proof*

This branch (`interactive-course`) turns the book into a self-paced web course for an 11th grader with Algebra 1/2 and Trig, but no Calculus II. Read `course/PLAN.md` first: it holds the syllabus, the homework mapping, the tooling decisions and the current status.

## Explainers: never hide steps

**Every explainer shows every intermediate step of any algebra or arithmetic it performs.** Nothing is skipped as "obvious" or "assumed". This rule applies to all explainers, existing and new.

What it means in practice:
- **Expansions.** Write each product before simplifying it (e.g. `2an·bm → 2abmn`). Show like terms being combined (`2abmn + 2abmn = 4abmn`). Show squares of sums term by term (`(am+bn)² = (am)² + 2·am·bn + (bn)²`) before distributing a factor.
- **Signs.** Call out sign rules where they act (`(−2n²)(−2a²) = +4a²n²`: negative × negative), and in subtractions (`−z² − (−2z²) = +z²`).
- **Cancellation.** Group the cancelling terms explicitly (`(2a²m² − 2a²m²) = 0`) before showing what is left. Show a reordering step when the result matches the other side only up to order.
- **Substitution and arithmetic.** Go one step at a time: `2·1² + (m²−2n²)·0 → 2·1 + 0 → 2`, and `17² − 2·12² → 289 − 2·144 → 289 − 288 → 1`.
- **Claims.** Any claim like "these get closer to √2" needs its reason on screen, not only the numbers.
- **Narration and screen.** The narration may summarize, but the screen must carry every line, so a student can pause on any frame and check it.
- **Lean first.** Verify every equation that appears in an explainer with Lean (`ring` / `numbers`) in the course image before rendering.
- **Cue words.** Each `beat.until(word, n)` / `self.show(beat, word, occurrence=n)` must name the n-th time that word is spoken in the beat, in order. Check them statically before rendering: a wrong occurrence fails the render or rushes an animation.

## Explainers: engaging, not only correct

Don't show only the pure math. Where a result has a history, give the person and the context briefly. Then show the intuition: what someone in their day could have noticed, and how a student could have discovered it themselves with tools they know (Algebra 2, pictures, small cases). The Brahmagupta explainer is the model: bio, the Śulba-sūtra altar puzzle, tile "near misses", conjugates, then the book's identity.

- **History is sourced.** State only what sources support (MacTutor, Bhāvanā magazine, the book itself). When the record is silent on how something was found, say so on screen and frame the discovery path as "one way you could have found it", never as what the mathematician did.
- **Length.** A story and a full check together can run long (Brahmagupta is ~13 min). Offer to split one into two explainers when that helps.

## Course content rules

- **The book's text is the lesson.** It is pulled unedited from `html/` (`Book.astro`), and exercises come from `Math2001/` (`LeanExercise.astro`). Nothing is retyped. The author authorized educational use.
- **All of it, not links to it.** Every paragraph of the book up to where the syllabus has reached must be on a course page, including chapter and section introductions, the Preface and homework text. `scripts/check-book-coverage.mjs` runs after `astro build` and fails the build when a block is missing.
- **On this page.** `src/routeData.ts` rebuilds Starlight's "On this page" from each page's MDX: its headings, every book subsection a `<Book>` includes, each `<Explainer>` and the stopping point. A new component that should appear there needs an `h2`/`h3` with an id, plus a case in that file.
- **Additions are marked.** Everything written for the course (guide notes, refreshers, hints, explainers) goes in a `CourseNote` box labelled "Added for this course". Book excerpts carry a source line.
- **Homework duplicates.** Some end-of-section exercises are homework problems word for word (e.g. §1.3 exercises 6 and 12 are HW1 #1 and #2). Flag them, and never use them as practice.
- **Lesson split points.** Split lessons at subsection boundaries, where the tools the next homework needs are complete (e.g. §1.4 splits after 1.4.7 because HW0 needs `extra`).
- **Hint ladders.** Hints go from a nudge to a worked first step. They never give a full homework solution.
- **Solutions.** Reference solutions must compile in the course image. They stay out of this public repo: they go to the private solutions repo, and are in `~/.cache/math2001-course/review/` for now.

## Generated media

- **Content-addressed cache.** Narration audio, alignments and videos live in `~/.cache/math2001-course` (`COURSE_ASSET_CACHE`), keyed by content hash. Only `course/assets.lock.json` is committed.
- **Dry run first.** Always run `course/media/build.sh --dry-run`, which reports what is missing and its cost, before a real build. Render with `--quality draft` and review a frame contact sheet before `--quality high`.
- **Narration.** It goes through OpenRouter (`elevenlabs/eleven-v4`, voice `george`), with the key in `.env.local`. Never print or commit that key.

## Hosting (linux-dev, `ssh linux-dev`, 192.168.50.205)

- **Location.** The repo is at `~/source/github/math2001`, served on port 28080 with `docker compose -f compose.yaml -f compose.hosted.yaml up -d --build`. The password is in its `.env`.
- **Deploying.** Push the branch to linux-dev as `incoming` (the checked-out branch can't be pushed directly), then `git merge --ff-only incoming` there. Copy `course/site/public/media/` with `rsync --delete`, since media isn't in git. Rebuild, then verify pages, media and a Lean round-trip over the network. The round-trip must authenticate the way a browser does: sign in on a page with Basic auth, then open the `/lean` socket with **only** the `course_session` cookie and no Authorization header. Browsers don't resend Basic credentials on websockets, so a check that sends them hides failures.
- **Security.** Lean `#eval` can run programs, so the hosted server keeps its password and origin check. Never expose it beyond the LAN without TLS.
