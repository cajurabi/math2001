// @ts-check
import { defineConfig } from 'astro/config'
import starlight from '@astrojs/starlight'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import { unified } from '@astrojs/markdown-remark'

export default defineConfig({
  // dev: forward the Lean websocket to the course server (`docker compose up`)
  vite: {
    server: { proxy: { '^/lean$': { target: 'ws://localhost:8080', ws: true } } },
  },
  markdown: {
    processor: unified({ remarkPlugins: [remarkMath], rehypePlugins: [rehypeKatex] }),
  },
  integrations: [
    starlight({
      title: 'Mechanics of Proof',
      description: 'An interactive course on The Mechanics of Proof by Heather Macbeth',
      customCss: ['katex/dist/katex.min.css', './src/styles/course.css'],
      // "On this page" also lists the book's examples, explainers and stopping points
      routeMiddleware: './src/routeData.ts',
      sidebar: [
        {
          label: 'Start here',
          items: [
            { label: 'Welcome', slug: 'index' },
            { label: 'Set up your computer', slug: 'setup' },
            { label: 'Syllabus', slug: 'syllabus' },
          ],
        },
        {
          label: 'Week 1 · Proofs by calculation',
          items: [
            { label: 'Day 1 · Proving equalities', slug: 'week-01/day-1' },
            { label: 'Day 2 · Tips and tricks', slug: 'week-01/day-2' },
            { label: 'Day 3 · Proving inequalities', slug: 'week-01/day-3' },
            { label: 'Lab · Homework 0', slug: 'week-01/lab' },
          ],
        },
      ],
    }),
  ],
})
