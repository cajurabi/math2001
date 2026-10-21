// Copies the book's Sphinx HTML build (repo `html/`) to public/book so lessons can link into it.
import fs from 'node:fs'
import path from 'node:path'

const source = path.resolve(import.meta.dirname, '../../../html')
const target = path.resolve(import.meta.dirname, '../public/book')

fs.rmSync(target, { recursive: true, force: true })
fs.cpSync(source, target, { recursive: true, filter: (src) => !src.includes(`${path.sep}_sources`) })
console.log(`sync-book: ${source} → ${target}`)
