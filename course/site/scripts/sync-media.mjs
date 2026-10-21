// Copies the media listed in course/assets.lock.json from the asset cache (outside the repo)
// into public/media. Missing files are reported, not fatal: the lesson shows a placeholder.
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'

const cacheDir = process.env.COURSE_ASSET_CACHE ?? path.join(os.homedir(), '.cache', 'math2001-course')
const lockPath = path.resolve(import.meta.dirname, '../../assets.lock.json')
const target = path.resolve(import.meta.dirname, '../public/media')

const lock = fs.existsSync(lockPath) ? JSON.parse(fs.readFileSync(lockPath, 'utf8')) : {}
fs.mkdirSync(target, { recursive: true })

let copied = 0
const missing = []
for (const [id, asset] of Object.entries(lock)) {
  for (const file of Object.values(asset.files ?? {})) {
    const source = path.join(cacheDir, 'files', file)
    const dest = path.join(target, file)
    if (fs.existsSync(dest)) continue
    if (fs.existsSync(source)) {
      fs.copyFileSync(source, dest)
      copied++
    } else {
      missing.push(`${id}: ${file}`)
    }
  }
}
// drop superseded renders so they don't ship in the site or the image
const wanted = new Set(Object.values(lock).flatMap((asset) => Object.values(asset.files ?? {})))
let pruned = 0
for (const file of fs.readdirSync(target)) {
  if (!wanted.has(file)) {
    fs.rmSync(path.join(target, file))
    pruned++
  }
}

console.log(`sync-media: ${copied} copied from ${cacheDir}, ${pruned} superseded removed`)
if (missing.length) console.log(`sync-media: not in cache (explainer placeholders will show):\n  ${missing.join('\n  ')}`)
