// Starlight builds "On this page" from Markdown headings only, so the book's examples (pulled in
// by <Book>) and the explainers never appeared there. This middleware reads the page's MDX source
// and rebuilds the list in document order: the page's own headings, every book subsection a
// <Book> includes, every <Explainer>, and the stopping point.

import { defineRouteMiddleware } from '@astrojs/starlight/route-data'
import { bookHeadings } from './lib/book'
import { explainerSlug, STOP_SLUG } from './lib/toc'

type Entry = { depth: number; slug: string; text: string }
type TocItem = Entry & { children: TocItem[] }

/** `name="value"`, `name='value'`, `name={CONST}` or `name={["a", "b"]}` attributes of a JSX tag. */
function attributes(tag: string, consts: Map<string, string>): Map<string, string | string[]> {
  const attrs = new Map<string, string | string[]>()
  for (const m of tag.matchAll(/(\w+)=(?:"([^"]*)"|'([^']*)'|\{([^}]*)\})/g)) {
    const [, name, dq, sq, expr] = m
    if (expr === undefined) attrs.set(name, dq ?? sq)
    else if (expr.trim().startsWith('[')) attrs.set(name, [...expr.matchAll(/["']([^"']+)["']/g)].map((p) => p[1]))
    else if (consts.has(expr.trim())) attrs.set(name, consts.get(expr.trim())!)
    else if (/^["'].*["']$/.test(expr.trim())) attrs.set(name, expr.trim().slice(1, -1))
  }
  return attrs
}

function pageEntries(body: string, headings: Entry[]): Entry[] {
  const source = body.replace(/^(```|~~~)[\s\S]*?^\1/gm, '')
  const consts = new Map([...source.matchAll(/^export const (\w+) = ['"]([^'"]+)['"]/gm)].map((m) => [m[1], m[2]]))
  const ownHeadings = headings.filter((h) => h.depth === 2 || h.depth === 3)
  const entries: Entry[] = []
  const pattern = /^(#{2,3})\s+.+$|<Book\b[^>]*?\/>|<Explainer\b[^>]*?\/>|<CourseNote\b[^>]*?kind="stop"[^>]*>/gm
  for (const [match, hashes] of source.matchAll(pattern)) {
    if (hashes) {
      const heading = ownHeadings.shift()
      if (heading) entries.push(heading)
    } else if (match.startsWith('<Book')) {
      const attrs = attributes(match, consts)
      const parts = attrs.get('parts')
      for (const h of bookHeadings(attrs.get('file') as string, attrs.get('section') as string,
        Array.isArray(parts) ? parts : undefined)) {
        entries.push({ depth: 3, ...h })
      }
    } else if (match.startsWith('<Explainer')) {
      const attrs = attributes(match, consts)
      entries.push({ depth: 3, slug: explainerSlug(attrs.get('id') as string), text: `Explainer: ${attrs.get('title')}` })
    } else {
      const title = attributes(match, consts).get('title') as string | undefined
      entries.push({ depth: 3, slug: STOP_SLUG, text: title ?? 'Stopping point' })
    }
  }
  return entries
}

export const onRequest = defineRouteMiddleware((context) => {
  const route = context.locals.starlightRoute
  const body = route.entry.body
  if (!route.toc || !body) return
  const [overview] = route.toc.items
  const items: TocItem[] = overview ? [overview] : []
  let section: TocItem | undefined
  for (const entry of pageEntries(body, route.headings)) {
    const item: TocItem = { ...entry, children: [] }
    if (entry.depth === 2) {
      items.push(item)
      section = item
    } else if (section) {
      section.children.push(item)
    } else {
      items.push(item)
    }
  }
  route.toc.items = items
})
