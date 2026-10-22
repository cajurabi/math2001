// Fails the build when a lesson leaves out book text.
//
// The course must contain all of the book's text, not links to it. For every book file the built
// site quotes (found from the excerpts' source lines), this walks the book's text blocks in order,
// finds the furthest block that appears on some course page, and requires every block before it
// to appear somewhere too. Chapters the syllabus hasn't reached yet don't count as missing, but a
// skipped introduction or subsection does. Math is compared by its TeX source (the book's \( \)
// and \[ \], the course's KaTeX annotation), so a dropped or altered equation fails too. Headings
// are left out (lessons title sections in their own words).
//
//   node scripts/check-book-coverage.mjs        (runs after `astro build`; see package.json)

import fs from 'node:fs'
import path from 'node:path'
import { parse } from 'parse5'

const SITE = path.resolve(import.meta.dirname, '..')
const DIST = path.join(SITE, 'dist')
const BOOK_DIR = path.resolve(SITE, '../../html')

const BLOCK_TAGS = new Set(['p', 'li', 'pre', 'td', 'th', 'dt', 'dd', 'figcaption', 'caption'])
const SKIP_CLASSES = ['headerlink', 'section-number']
// short or repeated blocks ("Solution", "Problem") can't tell one place in the book from another
const MIN_DISTINCTIVE = 30

const classesOf = (node) => (node.attrs?.find((a) => a.name === 'class')?.value ?? '').split(/\s+/)
const skipped = (node) => ['script', 'style'].includes(node.nodeName) || classesOf(node).some((c) => SKIP_CLASSES.includes(c))
const normalize = (text) => text.replace(/’/g, "'").replace(/\s+/g, ' ').trim()
// display math is its own block: the book's <div class="math">, the course's <div class="book-math">
const isBlock = (node) => BLOCK_TAGS.has(node.nodeName) ||
  (node.nodeName === 'div' && classesOf(node).some((c) => c === 'math' || c === 'book-math'))

const rawText = (node) => (node.nodeName === '#text' ? node.value : (node.childNodes ?? []).map(rawText).join(''))
const tex = (source) => `⟨${normalize(source)}⟩`

function textOf(node) {
  if (node.nodeName === '#text') return node.value
  if (skipped(node)) return ''
  const classes = classesOf(node)
  // the book: \(…\) or \[…\] inside a "math notranslate" span or div
  if (classes.includes('math') && classes.includes('notranslate')) {
    return tex(rawText(node).trim().replace(/^\\[([]/, '').replace(/\\[)\]]$/, ''))
  }
  // the course: KaTeX keeps the source in an annotation, and an error keeps it in its title
  if (classes.includes('katex')) {
    const annotation = find(node, (n) => n.nodeName === 'annotation')
    return tex(annotation ? rawText(annotation) : '')
  }
  if (classes.includes('katex-error')) return tex(node.attrs.find((a) => a.name === 'title')?.value ?? '')
  return (node.childNodes ?? []).map(textOf).join('')
}

/** Text of each outermost block element under `node`, in document order. */
function blocks(node, out = []) {
  if (skipped(node)) return out
  if (isBlock(node)) {
    const text = normalize(textOf(node))
    if (text) out.push(text)
    return out
  }
  for (const child of node.childNodes ?? []) blocks(child, out)
  if (node.content) blocks(node.content, out) // <template>
  return out
}

function find(node, test) {
  if (test(node)) return node
  for (const child of node.childNodes ?? []) {
    const hit = find(child, test)
    if (hit) return hit
  }
  return null
}

function pages(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) return ['book', '_astro', 'pagefind', 'media', 'lean-editor', 'infoview'].includes(entry.name) ? [] : pages(full)
    return entry.name.endsWith('.html') ? [full] : []
  })
}

const sitePages = pages(DIST)
const html = sitePages.map((file) => fs.readFileSync(file, 'utf8'))
const siteText = html.map((page) => blocks(parse(page)).join(' ')).join(' ')
const bookFiles = [...new Set(html.flatMap((page) =>
  [...page.matchAll(/<p class="book-source">[\s\S]*?href="\/book\/([^".#]+)\.html/g)].map((m) => m[1])))].sort()

let failed = false
for (const file of bookFiles) {
  const tree = parse(fs.readFileSync(path.join(BOOK_DIR, `${file}.html`), 'utf8'))
  const body = find(tree, (n) => n.attrs?.some((a) => a.name === 'itemprop' && a.value === 'articleBody'))
  const all = blocks(body)
  const count = new Map()
  for (const b of all) count.set(b, (count.get(b) ?? 0) + 1)
  const distinctive = all.filter((b) => b.length >= MIN_DISTINCTIVE && count.get(b) === 1)
  const present = distinctive.map((b) => siteText.includes(b))
  const reach = present.lastIndexOf(true)
  const missing = distinctive.slice(0, reach + 1).filter((_, i) => !present[i])
  const covered = present.slice(0, reach + 1).filter(Boolean).length
  console.log(`book coverage: ${file}: ${covered}/${reach + 1} blocks up to the furthest one quoted` +
    (reach + 1 < distinctive.length ? ` (${distinctive.length - reach - 1} later blocks not reached yet)` : ''))
  for (const text of missing) {
    console.log(`  MISSING: ${text.slice(0, 140)}${text.length > 140 ? '…' : ''}`)
    failed = true
  }
}

if (failed) {
  console.error('\nbook coverage: some book text is missing from the course. Add the <Book> excerpt that contains it.')
  process.exit(1)
}
