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

/**
 * Extract one example from a chapter's Lean file, delimited by its `-- Example x.y.z` comment
 * and the next `-- Example` comment (or the end of the file).
 * @param file  path under Math2001/, e.g. "01_Proofs_by_Calculation/02_Proving_Equalities_in_Lean.lean"
 * @param label the example number, e.g. "1.2.2"
 */
export function leanExample(file: string, label: string): LeanExample {
  const lines = fs.readFileSync(path.join(LEAN_ROOT, file), 'utf8').split('\n')

  const firstImport = lines.findIndex((l) => l.startsWith('import '))
  const init = lines.findIndex((l) => l.trim() === 'math2001_init')
  if (firstImport < 0 || init < 0) throw new Error(`lean: ${file} has no import/math2001_init header`)
  const header = lines.slice(firstImport, init + 1)

  const marker = new RegExp(`^-- Example ${label.replaceAll('.', '\\.')}\\.?\\s*$`)
  const start = lines.findIndex((l) => marker.test(l))
  if (start < 0) throw new Error(`lean: ${file} has no "-- Example ${label}"`)
  let end = lines.findIndex((l, i) => i > start && /^-- Example \d/.test(l))
  if (end < 0) end = lines.length
  // the lesson already titles the exercise, so drop the `-- Example x.y.z` marker itself
  const body = lines.slice(start + 1, end)
  while (body.length && body[body.length - 1].trim() === '') body.pop()

  return { code: [...header, ...body].join('\n') + '\n', preludeLines: header.length }
}
