// Course server: serves the static course site and bridges each browser Lean editor
// (lean4monaco, over a websocket) to its own `lake serve` process in the math2001 project.

import * as cp from 'node:child_process'
import * as path from 'node:path'
import express from 'express'
import { WebSocketServer } from 'ws'
import * as rpc from 'vscode-ws-jsonrpc'
import * as rpcServer from 'vscode-ws-jsonrpc/server'

const PORT = Number(process.env.PORT ?? 8080)
const PROJECT_DIR = path.resolve(process.env.LEAN_PROJECT_DIR ?? '/home/node/math2001')
const STATIC_DIR = process.env.STATIC_DIR ? path.resolve(process.env.STATIC_DIR) : null
const MAX_SESSIONS = Number(process.env.MAX_LEAN_SESSIONS ?? 4)
const LOG_RPC = process.env.LOG_RPC === '1'

const log = (...args) => console.log(`[${new Date().toISOString()}]`, ...args)

const app = express()
app.get('/healthz', (_req, res) => res.json({ ok: true, sessions: activeSessions }))
if (STATIC_DIR) app.use(express.static(STATIC_DIR, { extensions: ['html'] }))

const server = app.listen(PORT, () => {
  log(`Listening on :${PORT}; Lean project ${PROJECT_DIR}; static ${STATIC_DIR ?? '(none)'}`)
})

// Clients address files as `file:///Math2001/...`; the Lean server sees absolute paths.
function rewriteUris(obj, toServer) {
  for (const key of Object.keys(obj)) {
    const value = obj[key]
    if ((key === 'uri' || key === 'rootUri') && typeof value === 'string') {
      obj[key] = toServer
        ? value.replace('file://', `file://${PROJECT_DIR}`)
        : value.replace(`file://${PROJECT_DIR}`, 'file://')
    } else if (key === 'rootPath' && typeof value === 'string' && toServer) {
      obj[key] = path.join(PROJECT_DIR, value)
    } else if (value !== null && typeof value === 'object') {
      rewriteUris(value, toServer)
    }
  }
  return obj
}

/**
 * Lean can run arbitrary programs (`#eval IO.Process.run …`), so only pages served by this
 * server may open a Lean session: reject cross-site websocket connections from other origins
 * (any website the student visits could otherwise reach ws://localhost:8080/lean).
 */
function sameOrigin({ origin, req }) {
  if (!origin) return false
  try {
    return new URL(origin).host === req.headers.host
  } catch {
    return false
  }
}

let activeSessions = 0
const wss = new WebSocketServer({
  server,
  path: '/lean',
  verifyClient: (info, done) => {
    const ok = sameOrigin(info)
    if (!ok) log(`Rejecting Lean session from origin ${info.origin ?? '(none)'}`)
    done(ok, 403, 'Forbidden origin')
  },
})

wss.on('connection', (ws) => {
  if (activeSessions >= MAX_SESSIONS) {
    log(`Rejecting Lean session: limit of ${MAX_SESSIONS} reached`)
    ws.close(1013, 'Too many Lean sessions; close another tab and retry')
    return
  }
  activeSessions++
  const lean = cp.spawn('lake', ['serve', '--'], { cwd: PROJECT_DIR })
  log(`Lean session opened (pid ${lean.pid}, ${activeSessions} active)`)

  lean.on('error', (err) => log(`Launching Lean server failed: ${err}`))
  lean.stderr.on('data', (data) => log(`lean[${lean.pid}] ${String(data).trimEnd()}`))

  const socket = {
    onMessage: (cb) => ws.on('message', cb),
    onError: (cb) => ws.on('error', cb),
    onClose: (cb) => ws.on('close', cb),
    send: (data, cb) => ws.send(data, cb),
  }
  const socketConnection = rpcServer.createConnection(
    new rpc.WebSocketMessageReader(socket),
    new rpc.WebSocketMessageWriter(socket),
    () => ws.close(),
  )
  const leanConnection = rpcServer.createProcessStreamConnection(lean)

  socketConnection.forward(leanConnection, (message) => {
    if (LOG_RPC) log('client →', JSON.stringify(message))
    return rewriteUris(message, true)
  })
  leanConnection.forward(socketConnection, (message) => {
    if (LOG_RPC) log('lean →', JSON.stringify(message))
    return rewriteUris(message, false)
  })

  const shutdown = () => {
    if (lean.exitCode === null) lean.kill()
  }
  socketConnection.onClose(() => {
    leanConnection.dispose()
    shutdown()
  })
  leanConnection.onClose(() => socketConnection.dispose())
  lean.on('exit', (code) => {
    activeSessions--
    log(`Lean session closed (pid ${lean.pid}, exit ${code}, ${activeSessions} active)`)
  })
})
