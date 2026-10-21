// <lean-editor> and <lean-infoview> custom elements.
//
// A page holds one LeanMonaco instance (one websocket → one `lake serve`) and one shared
// infoview; every <lean-editor> on the page is a separate Lean file in the math2001 project.
//
//   <lean-infoview></lean-infoview>
//   <lean-editor file="Math2001/Course/W01D1/Example1.lean" prelude-lines="3">
//     <template>import Library.Basic …</template>
//   </lean-editor>
//
// Each editor reports a status when Lean finishes checking it:
//   "checking" | "error" | "incomplete" (contains sorry) | "solved"
// via a `lean-status` event and its `status` attribute.

import { LeanMonaco, LeanMonacoEditor, type LeanClient } from 'lean4monaco'
import './lean-editor.css'

export type LeanStatus = 'connecting' | 'checking' | 'error' | 'incomplete' | 'solved'

type Diagnostic = { severity?: number; message: string }
type PublishDiagnostics = { uri: string; diagnostics: Diagnostic[] }
type FileProgress = [uri: string, processing: unknown[]]

/** Starlight sets data-theme on <html>; fall back to the OS preference elsewhere. */
function prefersDark(): boolean {
  const theme = document.documentElement.dataset.theme
  if (theme === 'dark' || theme === 'light') return theme === 'dark'
  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

let leanMonaco: LeanMonaco | null = null

function websocketUrl(): string {
  const configured = document.documentElement.dataset.leanWebsocket
  if (configured) return configured
  const scheme = location.protocol === 'https:' ? 'wss' : 'ws'
  return `${scheme}://${location.host}/lean`
}

function infoviewHost(): HTMLElement {
  let host = document.querySelector<HTMLElement>('lean-infoview')
  if (!host) {
    host = document.createElement('lean-infoview')
    host.setAttribute('floating', '')
    document.body.append(host)
  }
  return host
}

/** Start the page's single LeanMonaco on first use. */
function ensureLeanMonaco(): LeanMonaco {
  if (leanMonaco) return leanMonaco
  leanMonaco = new LeanMonaco()
  leanMonaco.setInfoviewElement(infoviewHost())
  void leanMonaco.start({
    websocket: { url: websocketUrl() },
    vscode: {
      'workbench.colorTheme': prefersDark() ? 'Visual Studio Dark' : 'Visual Studio Light',
      'editor.wordWrap': true,
      'editor.minimap.enabled': false,
      'editor.lineNumbers': 'on',
      'editor.fontSize': 15,
      'lean4.input.leader': '\\',
      'lean4.infoview.showExpectedType': false,
      'lean4.infoview.emphasizeFirstGoal': true,
      'lean4.infoview.showGoalNames': false,
    },
  })
  return leanMonaco
}

/** Resolve once the language client exists (it is created when the first file opens). */
async function whenClient(lm: LeanMonaco): Promise<LeanClient> {
  await lm.whenReady
  const provider = lm.clientProvider!
  const existing = provider.getClients()[0]
  if (existing) return existing
  return new Promise((resolve) => {
    const sub = provider.clientAdded((client: LeanClient) => {
      sub.dispose()
      resolve(client)
    })
  })
}

/**
 * Monaco tracks focus per editor from focus/blur events. LeanMonacoEditor.start() calls focus()
 * on each editor it creates, and when that happens while the page itself is unfocused (e.g. still
 * loading) the matching blur events never arrive, so an editor can keep believing it has focus.
 * That editor then grabs real focus on its next cursor update and steals the student's
 * keystrokes. Tell every editor that doesn't actually have focus that it lost it.
 */
function syncEditorFocusState() {
  for (const textArea of document.querySelectorAll<HTMLTextAreaElement>('lean-editor textarea.inputarea')) {
    if (document.activeElement !== textArea) textArea.dispatchEvent(new FocusEvent('blur'))
  }
}
window.addEventListener('focus', syncEditorFocusState)

function storageKey(file: string) {
  return `lean-editor:${location.pathname}:${file}`
}

function loadSaved(file: string): string | null {
  try {
    return localStorage.getItem(storageKey(file))
  } catch {
    return null
  }
}

function save(file: string, code: string | null) {
  try {
    if (code === null) localStorage.removeItem(storageKey(file))
    else localStorage.setItem(storageKey(file), code)
  } catch {
    // storage unavailable (private window, blocked site data): work without persistence
  }
}

function statusFrom(diagnostics: Diagnostic[]): LeanStatus {
  if (diagnostics.some((d) => d.severity === 1)) return 'error'
  if (diagnostics.some((d) => d.message.includes("declaration uses 'sorry'"))) return 'incomplete'
  return 'solved'
}

const STATUS_LABEL: Record<LeanStatus, string> = {
  connecting: 'Starting Lean…',
  checking: 'Lean is checking…',
  error: 'Lean found an error',
  incomplete: 'Not finished yet (sorry)',
  solved: 'Proof complete ✓',
}

class LeanEditorElement extends HTMLElement {
  private editor: LeanMonacoEditor | null = null
  private original = ''
  private diagnostics: Diagnostic[] = []
  private badge!: HTMLElement
  private disposers: { dispose(): void }[] = []

  get file(): string {
    return this.getAttribute('file') ?? 'Math2001/Course/Scratch.lean'
  }

  async connectedCallback() {
    if (this.editor) return
    const template = this.querySelector('template')
    this.original = (template?.content.textContent ?? this.textContent ?? '').replace(/^\n/, '').trimEnd() + '\n'
    this.replaceChildren()

    const toolbar = document.createElement('div')
    toolbar.className = 'lean-editor-toolbar'
    this.badge = document.createElement('span')
    this.badge.className = 'lean-editor-status'
    const reset = document.createElement('button')
    reset.type = 'button'
    reset.textContent = 'Reset'
    reset.title = 'Restore the original exercise'
    reset.addEventListener('click', () => this.reset())
    toolbar.append(this.badge, reset)

    const codeview = document.createElement('div')
    codeview.className = 'lean-editor-code'
    // initial guess; replaced by the real content height once Monaco has laid out the code
    const visible = this.original.split('\n').length - Number(this.getAttribute('prelude-lines') ?? 0)
    codeview.style.height = `${Math.max(4, visible + 1) * 1.5}em`
    this.append(codeview, toolbar)
    this.setStatus('connecting')

    const lm = ensureLeanMonaco()
    await lm.whenReady
    const editor = new LeanMonacoEditor()
    this.editor = editor
    // LeanMonacoEditor.start() focuses the new editor; don't let that steal focus or scroll the page
    const previousFocus = document.activeElement
    const scroll = [window.scrollX, window.scrollY] as const
    await editor.start(codeview, this.file, loadSaved(this.file) ?? this.original)
    if (previousFocus instanceof HTMLElement && previousFocus !== document.body) previousFocus.focus({ preventScroll: true })
    else if (this.contains(document.activeElement)) (document.activeElement as HTMLElement).blur()
    window.scrollTo(...scroll)
    syncEditorFocusState()
    this.hidePrelude()
    this.fitToContent(codeview)
    this.repairClickFocus(codeview)

    const model = editor.editor.getModel()!
    const uri = model.uri.toString()
    this.disposers.push(model.onDidChangeContent(() => {
      const code = model.getValue()
      save(this.file, code === this.original ? null : code)
      this.setStatus('checking')
    }))

    const client = await whenClient(lm)
    this.setStatus('checking')
    this.disposers.push(client.diagnostics((params: PublishDiagnostics) => {
      if (params.uri === uri) this.diagnostics = params.diagnostics
    }))
    this.disposers.push(client.progressChanged(([progressUri, processing]: FileProgress) => {
      if (progressUri === uri && processing.length === 0) this.setStatus(statusFrom(this.diagnostics))
    }))
  }

  disconnectedCallback() {
    this.disposers.forEach((d) => d.dispose())
    this.disposers = []
    this.editor?.dispose()
    this.editor = null
  }

  /**
   * LeanMonacoEditor.start() calls focus() on every editor it creates, which leaves Monaco's
   * internal focus state stale: the first click into another editor then places no text focus,
   * and keystrokes land in whichever editor Monaco still thinks is focused. After a click,
   * make sure the clicked editor's own text area really has focus.
   */
  private repairClickFocus(codeview: HTMLElement) {
    const onMouseUp = () => {
      setTimeout(() => {
        const textArea = codeview.querySelector<HTMLTextAreaElement>('textarea.inputarea')
        if (textArea && document.activeElement !== textArea) textArea.focus({ preventScroll: true })
      })
    }
    codeview.addEventListener('mouseup', onMouseUp)
    this.disposers.push({ dispose: () => codeview.removeEventListener('mouseup', onMouseUp) })
  }

  /** Grow the editor with its content (no inner vertical scrolling), and let the page scroll over it. */
  private fitToContent(codeview: HTMLElement) {
    const ed = this.editor!.editor
    ed.updateOptions({
      scrollBeyondLastLine: false,
      scrollbar: { alwaysConsumeMouseWheel: false, vertical: 'hidden' },
    })
    const fit = () => {
      const height = Math.min(Math.max(ed.getContentHeight() + 8, 96), 900)
      codeview.style.height = `${height}px`
      ed.layout()
    }
    this.disposers.push(ed.onDidContentSizeChange(fit))
    fit()
  }

  /** Fold away the import/`math2001_init` header so students see only the exercise. */
  private hidePrelude() {
    const count = Number(this.getAttribute('prelude-lines') ?? 0)
    if (!count || !this.editor) return
    const ed = this.editor.editor as unknown as { setHiddenAreas?: (ranges: object[]) => void }
    ed.setHiddenAreas?.([{ startLineNumber: 1, startColumn: 1, endLineNumber: count, endColumn: 1 }])
    // number the visible lines from 1, as the student sees them
    this.editor.editor.updateOptions({ lineNumbers: (n: number) => String(n - count) })
  }

  private reset() {
    this.editor?.editor.getModel()?.setValue(this.original)
    save(this.file, null)
  }

  private setStatus(status: LeanStatus) {
    this.setAttribute('status', status)
    this.badge.textContent = STATUS_LABEL[status]
    this.badge.dataset.status = status
    this.dispatchEvent(new CustomEvent('lean-status', { detail: { status, file: this.file }, bubbles: true }))
  }
}

class LeanInfoviewElement extends HTMLElement {}

customElements.define('lean-editor', LeanEditorElement)
customElements.define('lean-infoview', LeanInfoviewElement)
