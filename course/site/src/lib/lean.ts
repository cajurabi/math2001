// Build-time access to the book's Lean files in the repo's `Math2001/` folder.

import fs from 'node:fs'
import path from 'node:path'

const LEAN_ROOT = path.resolve(process.cwd(), '../../Math2001')

export type LeanExample = {
  /** full file contents for the editor: the file's imports + `math2001_init`, then the example */
  code: string
  /** number of header lines, hidden in the editor */
  preludeLines: number
}

function readLines(file: string): string[] {
  return fs.readFileSync(path.join(LEAN_ROOT, file), 'utf8').split('\n')
}

/** The file's `import …` lines through `math2001_init`. */
function header(file: string, lines: string[]): string[] {
  const firstImport = lines.findIndex((l) => l.startsWith('import '))
  const init = lines.findIndex((l) => l.trim() === 'math2001_init')
  if (firstImport < 0 || init < 0) throw new Error(`lean: ${file} has no import/math2001_init header`)
  return lines.slice(firstImport, init + 1)
}

function trimTrailingBlank(body: string[]): string[] {
  const out = [...body]
  while (out.length && out[out.length - 1].trim() === '') out.pop()
  return out
}

function withHeader(file: string, lines: string[], body: string[]): LeanExample {
  const head = header(file, lines)
  return { code: [...head, ...trimTrailingBlank(body)].join('\n') + '\n', preludeLines: head.length }
}

/** A block ends at the next example marker, a `/-!` section heading, or the end of the file. */
function blockEnd(lines: string[], start: number, isBoundary: (line: string) => boolean): number {
  const end = lines.findIndex((l, i) => i > start && (isBoundary(l) || l.startsWith('/-!')))
  return end < 0 ? lines.length : end
}

/**
 * One worked example from a chapter's Lean file, delimited by its `-- Example x.y.z` comment.
 * @param file  path under Math2001/, e.g. "01_Proofs_by_Calculation/02_Proving_Equalities_in_Lean.lean"
 * @param label the example number, e.g. "1.2.2"
 */
export function leanExample(file: string, label: string): LeanExample {
  const lines = readLines(file)
  const marker = new RegExp(`^-- Example ${label.replaceAll('.', '\\.')}\\.?\\s*$`)
  const start = lines.findIndex((l) => marker.test(l))
  if (start < 0) throw new Error(`lean: ${file} has no "-- Example ${label}"`)
  const end = blockEnd(lines, start, (l) => /^-- Example \d/.test(l))
  // the lesson already titles the exercise, so drop the `-- Example x.y.z` marker itself
  return withHeader(file, lines, lines.slice(start + 1, end))
}

/**
 * The n-th exercise (1-based) after a file's `/-! # Exercises` heading. Exercises are unlabelled
 * `example`s separated by blank lines.
 */
export function leanExercise(file: string, n: number): LeanExample {
  const lines = readLines(file)
  const heading = lines.findIndex((l) => l.startsWith('/-! # Exercises'))
  if (heading < 0) throw new Error(`lean: ${file} has no "/-! # Exercises" heading`)
  const starts = lines.flatMap((l, i) => (i > heading && /^(example|theorem)\b/.test(l) ? [i] : []))
  if (n < 1 || n > starts.length) throw new Error(`lean: ${file} has ${starts.length} exercises, not #${n}`)
  const end = n < starts.length ? starts[n] : lines.length
  return withHeader(file, lines, lines.slice(starts[n - 1], end))
}

/**
 * Homework problem `k` from Math2001/Homework/hw<N>.lean. Its `@[autograded]` tag (for the
 * original course's Gradescope grader) is left out: here Lean checks the proof directly.
 */
export function leanHomework(hw: number, problem: number): LeanExample {
  const file = `Homework/hw${hw}.lean`
  const lines = readLines(file)
  const start = lines.findIndex((l) => new RegExp(`^theorem problem${problem}\\b`).test(l))
  if (start < 0) throw new Error(`lean: ${file} has no problem${problem}`)
  const end = blockEnd(lines, start, (l) => /^(@\[|theorem |example )/.test(l))
  return withHeader(file, lines, lines.slice(start, end))
}
