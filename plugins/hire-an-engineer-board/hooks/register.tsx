import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Board, BoardTask } from '../types'

const PANE = 'hire-an-engineer-board'
const TITLE = 'Project board'
const REFRESH_MS = 4000

const EMPTY: Board = {
  isFound: false,
  project: '',
  tasks: [],
  auth: {},
  focus: '',
  source: '',
}

// Change the tag when Board's fields change: it declines what an earlier
// version stored, which outlives a reload.
const board = atom({ plugin: 'hire-an-engineer-board', key: 'board' } as const, EMPTY, {
  shape: 'board-1',
})

const STAGES = ['plan', 'build', 'review', 'verify'] as const

const NEEDS_LABEL: Record<string, string> = {
  plan: 'approve the plan',
  approve: 'approve',
  test: 'test it',
  merge: 'OK to merge',
  help: 'needs your help',
  question: 'answer a question',
  answer: 'answer a question',
  approval: 'approval needed',
}

// ---------- parsing (pure) ----------

function cells(line: string): string[] {
  const t = line.trim().replace(/^\|/, '').replace(/\|$/, '')
  return t.split('|').map(c => c.trim())
}

function clean(s: string | undefined): string {
  return (s ?? '').replace(/`/g, '').replace(/\*\*/g, '').trim()
}

function isNone(s: string): boolean {
  return s === '' || s === '-' || s === '—' || /^(none|no|n\/a)$/i.test(s)
}

export function parseTasks(md: string): BoardTask[] {
  const lines = md.split(/\r?\n/)
  for (let i = 0; i < lines.length - 1; i++) {
    if (!lines[i].trim().startsWith('|')) continue
    const head = cells(lines[i]).map(h => clean(h).toLowerCase())
    const hasId = head.includes('#') || head.includes('id')
    const hasFlow = head.includes('stage') || head.includes('status')
    if (!hasId || !hasFlow) continue
    if (!/^\s*\|?\s*:?-{2,}/.test(lines[i + 1])) continue
    const col = (name: string) => head.indexOf(name)
    const idCol = col('#') >= 0 ? col('#') : col('id')
    const titleCol = ['title', 'task', 'name', 'what'].map(col).find(c => c >= 0) ?? -1
    const tasks: BoardTask[] = []
    for (let j = i + 2; j < lines.length && lines[j].trim().startsWith('|'); j++) {
      const row = cells(lines[j])
      const at = (c: number) => (c >= 0 ? clean(row[c]) : '')
      const id = at(idCol).replace(/^#/, '')
      if (!id) continue
      tasks.push({
        id,
        title: at(titleCol),
        size: at(col('size')),
        stage: at(col('stage')).toLowerCase(),
        status: at(col('status')).toLowerCase(),
        round: at(col('round')),
        slot: at(col('slot')),
        needs: at(col('needs')).toLowerCase(),
        note: at(col('note')),
      })
    }
    return tasks
  }
  return []
}

export function parseAuth(md: string): Record<string, string> {
  const lines = md.split(/\r?\n/)
  const out: Record<string, string> = {}
  const start = lines.findIndex(l => /^#{1,6}\s*authori[sz]ation/i.test(l.trim()))
  if (start < 0) return out
  for (let i = start + 1; i < lines.length; i++) {
    const l = lines[i].trim()
    if (/^#{1,6}\s/.test(l)) break
    for (const part of l.replace(/^[-*]\s*/, '').split('·')) {
      const m = part.match(/^\s*([A-Za-z][\w -]{0,30}?)\s*:\s*(.+?)\s*$/)
      if (m) out[m[1].toLowerCase()] = clean(m[2])
    }
  }
  return out
}

export function parseFocus(md: string): string {
  const lines = md.split(/\r?\n/)
  const start = lines.findIndex(l =>
    /^#{1,6}\s*(current|now|focus|next step|where we are)/i.test(l.trim()),
  )
  if (start < 0) return ''
  for (let i = start + 1; i < lines.length; i++) {
    const l = lines[i].trim()
    if (/^#{1,6}\s/.test(l)) break
    const text = clean(l.replace(/^[-*]\s*/, ''))
    if (text) return text.length > 140 ? text.slice(0, 137) + '…' : text
  }
  return ''
}

function isDone(t: BoardTask): boolean {
  return t.status === 'done' || t.status === 'dropped'
}

function needsLabel(n: string): string {
  const key = n.split(/[\s:(]/)[0]
  return NEEDS_LABEL[key] ?? n
}

// ---------- reading files ----------

let lastJson = ''

function join(dir: string, name: string): string {
  const sep = dir.includes('\\') && !dir.includes('/') ? '\\' : '/'
  return dir.replace(/[\\/]+$/, '') + sep + name
}

function baseName(dir: string): string {
  const parts = dir.split(/[\\/]+/).filter(Boolean)
  return parts[parts.length - 1] ?? dir
}

async function readText($: any, path: string): Promise<string | undefined> {
  try {
    return await $.fs.read(path)
  } catch {
    return undefined
  }
}

async function load($: any): Promise<Board> {
  const cwd: string = await $.session.cwd()
  let tasksMd: string | undefined
  let source = ''
  for (const name of ['TASKS.md', 'docs/TASKS.md']) {
    tasksMd = await readText($, join(cwd, name))
    if (tasksMd !== undefined) {
      source = name
      break
    }
  }
  const stateMd = await readText($, join(cwd, 'PROJECT_STATE.md'))
  if (tasksMd === undefined && stateMd === undefined) return EMPTY
  return {
    isFound: true,
    project: baseName(cwd),
    tasks: tasksMd ? parseTasks(tasksMd) : [],
    auth: stateMd ? parseAuth(stateMd) : {},
    focus: stateMd ? parseFocus(stateMd) : '',
    source: source || 'PROJECT_STATE.md',
  }
}

async function refresh($: any): Promise<Board> {
  const next = await load($)
  const json = JSON.stringify(next)
  if (json !== lastJson) {
    lastJson = json
    await update($, board, () => next)
  }
  return next
}

// ---------- hooks ----------

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'board',
      description: 'Show the hire-an-engineer project board beside the chat',
    })
    try {
      const b = await refresh($)
      if (b.isFound) void $.ui.open({ id: PANE, title: TITLE })
    } catch {
      // A board that cannot be read never blocks the session.
    }
    $.clock.every(REFRESH_MS, async () => {
      try {
        await refresh($)
      } catch {
        // Try again on the next tick.
      }
    })
    return next(e)
  })

  on('command.run', { command: 'board' }, async $ => {
    const b = await refresh($)
    await $.ui.open({ id: PANE, title: TITLE })
    return {
      text: b.isFound
        ? 'Project board opened.'
        : 'Project board opened. No TASKS.md or PROJECT_STATE.md in this folder yet.',
    }
  })

  on('tool.call', async ($, e, next) => {
    const ran = await next(e)
    const input = (e as any).input ?? {}
    const path = String(input.file_path ?? input.path ?? '')
    if (/(TASKS|PROJECT_STATE)\.md$/i.test(path)) {
      try {
        await refresh($)
      } catch {
        // The timer will pick it up.
      }
    }
    return ran
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const b = await read($, board)

    if (!b.isFound) {
      return (
        <Box flexDirection="column" padding={1} gap={1}>
          <Text weight="semibold">No project board here yet</Text>
          <Text dimColor>
            This pane shows TASKS.md and PROJECT_STATE.md from the session's folder. They appear
            once the hire-an-engineer skill starts a project here.
          </Text>
        </Box>
      )
    }

    const open = b.tasks.filter(t => !isDone(t))
    const done = b.tasks.filter(t => t.status === 'done')
    const waiting = open.filter(t => !isNone(t.needs))
    const live = open.filter(t => (STAGES as readonly string[]).includes(t.stage))
    const queued = open.filter(t => !(STAGES as readonly string[]).includes(t.stage))
    const a = b.auth
    const mode = a['mode'] ?? ''
    const status = a['status'] ?? ''
    const cap = a['cap'] ?? ''
    const isUntrusted = /untrusted/i.test(status)

    return (
      <Box flexDirection="column" padding={1} gap={1}>
        <Box flexDirection="column">
          <Text size="heading" weight="bold">
            {b.project}
          </Text>
          {(mode || status) && (
            <Text color={isUntrusted ? 'error' : status === 'active' ? 'success' : 'subtle'}>
              {[mode && `Mode: ${mode}`, status && `Approval: ${status}`].filter(Boolean).join(' · ')}
            </Text>
          )}
          {cap && <Text dimColor>Cap: {cap}</Text>}
          {b.focus && <Text dimColor>Now: {b.focus}</Text>}
        </Box>

        {waiting.length > 0 && (
          <Box flexDirection="column" borderStyle="round" borderColor="warning" padding={1}>
            <Text weight="semibold" color="warning">
              Waiting for you ({waiting.length})
            </Text>
            {waiting.map(t => (
              <Text>
                #{t.id} {t.title || '(untitled)'}: {needsLabel(t.needs)}
              </Text>
            ))}
          </Box>
        )}

        <Box flexDirection="row" flexWrap="wrap" gap={1}>
          {STAGES.map(s => {
            const n = live.filter(t => t.stage === s).length
            return (
              <Box borderStyle="round" borderColor={n > 0 ? 'claude' : 'inactive'} paddingX={1}>
                <Text dimColor={n === 0}>
                  {s} {n}
                </Text>
              </Box>
            )
          })}
          <Box borderStyle="round" borderColor={done.length > 0 ? 'success' : 'inactive'} paddingX={1}>
            <Text dimColor={done.length === 0}>done {done.length}</Text>
          </Box>
        </Box>

        <Box flexDirection="column">
          <Text weight="semibold">In the loop ({live.length})</Text>
          {live.length === 0 && <Text dimColor>Nothing is being built right now.</Text>}
          {live.map(t => (
            <Box flexDirection="column" marginTop={1}>
              <Text>
                #{t.id} {t.title || '(untitled)'}
              </Text>
              <Text dimColor>
                {[
                  t.stage,
                  t.size && `size ${t.size}`,
                  t.round && t.round !== '0' && `round ${t.round}`,
                  t.slot && !isNone(t.slot) && `lane ${t.slot}`,
                ]
                  .filter(Boolean)
                  .join(' · ')}
              </Text>
            </Box>
          ))}
        </Box>

        {queued.length > 0 && (
          <Box flexDirection="column">
            <Text weight="semibold">Next up ({queued.length})</Text>
            {queued.slice(0, 8).map(t => (
              <Text dimColor>
                #{t.id} {t.title || '(untitled)'}
                {t.status ? ` · ${t.status}` : ''}
              </Text>
            ))}
            {queued.length > 8 && <Text dimColor>…and {queued.length - 8} more</Text>}
          </Box>
        )}

        <Text dimColor size="caption">
          From {b.source}
          {b.tasks.length === 0 && b.source !== 'PROJECT_STATE.md' ? ' (no task table found)' : ''}
        </Text>
      </Box>
    )
  })
}
