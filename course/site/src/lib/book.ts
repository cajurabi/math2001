// Build-time access to the book's own text: extracts sections from the Sphinx HTML build in
// the repo's `html/` folder and re-renders their math with KaTeX, so lessons show the author's
// text unedited. The full book is also served at /book/ (see scripts/sync-book.mjs), and links
// that point outside the excerpt are rewritten to go there.

import fs from 'node:fs'
import path from 'node:path'
import katex from 'katex'

const REPO_ROOT = path.resolve(process.cwd(), '../..')
const BOOK_DIR = path.join(REPO_ROOT, 'html')

const fileCache = new Map<string, string>()

function readChapter(file: string): string {
  let html = fileCache.get(file)
  if (html === undefined) {
    html = fs.readFileSync(path.join(BOOK_DIR, `${file}.html`), 'utf8')
    fileCache.set(file, html)
  }
  return html
}

/** Inner HTML of `<section id="…">`, matching nested section tags. */
function sectionInner(html: string, id: string): string {
  const open = `<section id="${id}">`
  const start = html.indexOf(open)
  if (start < 0) throw new Error(`book: no <section id="${id}">`)
  const tag = /<section\b|<\/section>/g
  tag.lastIndex = start + open.length
  let depth = 1
  for (let m = tag.exec(html); m; m = tag.exec(html)) {
    depth += m[0] === '</section>' ? -1 : 1
    if (depth === 0) return html.slice(start + open.length, m.index)
  }
  throw new Error(`book: unterminated <section id="${id}">`)
}

/** Split a section into the text before its first subsection and its direct subsections. */
function splitSubsections(inner: string): { intro: string; parts: Map<string, string> } {
  const parts = new Map<string, string>()
  const first = inner.search(/<section id="/)
  const intro = first < 0 ? inner : inner.slice(0, first)
  let rest = first < 0 ? '' : inner.slice(first)
  while (rest.startsWith('<section id="') || rest.trimStart().startsWith('<section id="')) {
    rest = rest.trimStart()
    const id = rest.slice('<section id="'.length, rest.indexOf('"', '<section id="'.length))
    const body = sectionInner(rest, id)
    parts.set(id, `<section id="${id}">${body}</section>`)
    rest = rest.slice(rest.indexOf(body) + body.length + '</section>'.length)
  }
  return { intro, parts }
}

const NAMED_ENTITIES: Record<string, string> = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ' }

function decodeEntities(s: string): string {
  return s.replace(/&(#x[0-9a-f]+|#\d+|\w+);/gi, (whole, body: string) => {
    if (body[0] === '#') {
      const code = body[1].toLowerCase() === 'x' ? parseInt(body.slice(2), 16) : parseInt(body.slice(1), 10)
      return String.fromCodePoint(code)
    }
    return NAMED_ENTITIES[body] ?? whole
  })
}

function renderMath(tex: string, displayMode: boolean): string {
  return katex.renderToString(decodeEntities(tex).trim(), { displayMode, throwOnError: false })
}

function transform(html: string, file: string, ownIds: Set<string>): string {
  return html
    // Starlight renders its own heading anchors
    .replace(/<a class="headerlink"[^>]*>.*?<\/a>/g, '')
    // a subsection's id moves onto its heading, so "On this page" can link to and track it
    .replace(/<section id="([^"]+)">(\s*(?:<span id="[^"]*"><\/span>)?\s*)<h([23])>/g, '<section>$2<h$3 id="$1">')
    .replace(/<div class="math notranslate nohighlight">\s*\\\[([\s\S]*?)\\\]\s*<\/div>/g,
      (_m, tex: string) => `<div class="book-math">${renderMath(tex, true)}</div>`)
    .replace(/<span class="math notranslate nohighlight">\\\(([\s\S]*?)\\\)<\/span>/g,
      (_m, tex: string) => renderMath(tex, false))
    .replace(/href="#([^"]+)"/g, (_m, id: string) =>
      ownIds.has(id) ? `href="#${id}"` : `href="/book/${file}.html#${id}"`)
    .replace(/href="(?!https?:|\/|#|mailto:)([^"]+\.html(?:#[^"]*)?)"/g, 'href="/book/$1"')
    .replace(/<a class="reference external" href="/g, '<a class="reference external" target="_blank" rel="noopener" href="')
    .replace(/src="_images\//g, 'src="/book/_images/')
    // the book's figures are small at their print widths; show them 1.5× (relative sizes kept)
    .replace(/(<img [^>]*style=")width: (\d+)px;/g, (_m, head: string, width: string) =>
      `${head}width: ${Math.round(Number(width) * 1.5)}px; max-width: 100%;`)
}

/** The chosen parts of a section, as [id, html] pairs in the order asked for. */
function selectParts(inner: string, section: string, parts?: string[]): [string, string][] {
  const { intro, parts: subsections } = splitSubsections(inner)
  const wanted = parts ?? ['intro', ...subsections.keys()]
  return wanted.map((id) => {
    if (id === 'intro') return [id, intro.replace(/(<span id="[^"]*"><\/span>)?<h[12]>[\s\S]*?<\/h[12]>/, '')]
    const chunk = subsections.get(id)
    if (!chunk) throw new Error(`book: section "${section}" has no subsection "${id}"`)
    return [id, chunk]
  })
}

/**
 * The subsection headings an excerpt shows (e.g. "Example 1.3.1"), with the ids `bookExcerpt`
 * puts on them, for the "On this page" sidebar.
 */
export function bookHeadings(file: string, section: string, parts?: string[]): { slug: string; text: string }[] {
  const inner = sectionInner(readChapter(file), section)
  return selectParts(inner, section, parts).flatMap(([id, chunk]) => {
    if (id === 'intro') return []
    const heading = chunk.match(/<h[23]>(?:<span class="section-number">([\d.]+)\.\s*<\/span>)?([\s\S]*?)<a class="headerlink"/)
    if (!heading) return []
    const text = decodeEntities(heading[2]).trim()
    return [{ slug: id, text: heading[1] ? `${text} ${heading[1]}` : text }]
  })
}

export type BookExcerpt = {
  html: string
  /** "1.2" — the section number shown in the source line */
  number: string
  title: string
  url: string
}

/**
 * Extract part of a book section.
 * @param file    chapter file without extension, e.g. "01_Proofs_by_Calculation"
 * @param section the section's id, e.g. "proving-equalities-in-lean"
 * @param parts   subsection ids to include (default: all); "intro" is the text before the first one
 */
export function bookExcerpt(file: string, section: string, parts?: string[]): BookExcerpt {
  const chapter = readChapter(file)
  const inner = sectionInner(chapter, section)
  const heading = inner.match(/<h[12]>(?:<span class="section-number">([\d.]+)\.\s*<\/span>)?([\s\S]*?)<a class="headerlink"/)
  const number = heading?.[1] ?? ''
  const title = decodeEntities(heading?.[2] ?? section).trim()

  const chunks = selectParts(inner, section, parts).map(([, chunk]) => chunk)
  const selected = chunks.join('\n')
  const ownIds = new Set([...selected.matchAll(/\bid="([^"]+)"/g)].map((m) => m[1]))
  return { html: transform(selected, file, ownIds), number, title, url: `/book/${file}.html#${section}` }
}
