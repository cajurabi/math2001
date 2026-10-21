// Builds the <lean-editor> web component as a standalone bundle, kept separate from the
// Astro site because lean4monaco's setup (node polyfills, esbuild import.meta.url plugin)
// is documented and tested against Vite 6, while Astro 7 ships Vite 8.
import path from 'node:path'
import { defineConfig, normalizePath } from 'vite'
import { nodePolyfills } from 'vite-plugin-node-polyfills'
import { viteStaticCopy } from 'vite-plugin-static-copy'
import importMetaUrlPlugin from '@codingame/esbuild-import-meta-url-plugin'

const infoviewDist = path.resolve(__dirname, 'node_modules/@leanprover/infoview/dist')

export default defineConfig(({ command }) => ({
  // the bundle is served from the course site under /lean-editor/; dev serves from the root
  base: command === 'build' ? '/lean-editor/' : '/',
  optimizeDeps: {
    esbuildOptions: { plugins: [importMetaUrlPlugin] },
  },
  plugins: [
    nodePolyfills({ overrides: { fs: 'memfs' } }),
    viteStaticCopy({
      targets: [
        {
          src: [
            normalizePath(`${infoviewDist}/*`),
            normalizePath(path.resolve(__dirname, 'node_modules/lean4monaco/dist/webview/webview.js')),
          ],
          // lean4monaco's infoview iframe loads these from the absolute path /infoview/
          dest: command === 'build' ? '../infoview' : 'infoview',
        },
        { src: normalizePath(`${infoviewDist}/codicon.ttf`), dest: 'assets' },
      ],
    }),
  ],
  build: {
    outDir: path.resolve(__dirname, '../site/public/lean-editor'),
    emptyOutDir: true,
    // the site reads .vite/manifest.json to link the extracted CSS alongside the entry script
    manifest: true,
    rollupOptions: {
      input: path.resolve(__dirname, 'src/lean-editor.ts'),
      output: { entryFileNames: 'lean-editor.js' },
    },
  },
  server: {
    // dev: `npm run dev` serves spike.html and proxies /lean to the course server
    proxy: { '^/lean$': { target: 'ws://localhost:8080', ws: true } },
  },
}))
