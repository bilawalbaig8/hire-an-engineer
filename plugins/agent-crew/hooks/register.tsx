// agent-crew: a pane that shows the agents of a session as small Claude icons
// working together on your files. It only watches. It never blocks or changes
// a tool call, a turn or a spawn.

import { atom, read, update } from 'claude-code'
import type { AgentInfo, EngineInterface, Register } from 'claude-code'

import type { CrewAgent, CrewFile, CrewLog, CrewState } from '../types'
import { MODEL_THEME, effortText, modelFamily } from './models'
import { DEFAULT_FILL, MAX_FILL, MIN_FILL, agentTag, baseName, buildScene, clip } from './scene'
import type { BenchItem } from './scene'

const PANE = 'agent-crew'
const MAX_AGENTS = 24
const MAX_FILES = 6
const MAX_LOG = 40
const MAX_ROSTER = 40
// The size the pane asks for when it opens. The app may give less: it is a request.
const PANE_SIZE = { columns: 80, rows: 40 } as const
// About how many pixels one column of the pane is across. The pane reports its width
// in columns only, so this turns it into pixels; /crew bigger and /crew smaller correct a miss.
const CELL_PX = 8
// How far /crew bigger and /crew smaller move the picture's share of the pane.
const FILL_STEP = 0.15
// A finished helper stays on the floor this long, so you see it finish (the check, the
// sparkle), then it goes back to the bench.
const LINGER_MS = 8000

const MAIN: CrewAgent = {
  id: 'main',
  label: 'Claude',
  kind: 'main',
  state: 'idle',
  verb: '',
  target: '',
  file: '',
  parentId: '',
  steps: 0,
  endedAt: 0,
  model: '',
  effort: '',
}

// Change a tag when the fields of a value change: it declines what an earlier
// version stored, which outlives a reload.
const agents = atom({ plugin: 'agent-crew', key: 'agents' } as const, [MAIN], {
  shape: 'agents-3',
})
const files = atom({ plugin: 'agent-crew', key: 'files' } as const, [], {
  shape: 'files-1',
})
const log = atom({ plugin: 'agent-crew', key: 'log' } as const, [], {
  shape: 'log-1',
})
const roster = atom({ plugin: 'agent-crew', key: 'roster' } as const, [], {
  shape: 'roster-1',
})
const isBenchOpen = atom({ plugin: 'agent-crew', key: 'isBenchOpen' } as const, true, {
  shape: 'bench-1',
})
// How much of the pane's width the picture takes (1 is all of it).
const zoom = atom({ plugin: 'agent-crew', key: 'zoom' } as const, DEFAULT_FILL, {
  shape: 'zoom-3',
})

// How many state writes failed and were passed over: shown in the pane, never thrown.
let failures = 0

// The effort each Agent call asked for, by its tool_use_id, until its spawn picks it up:
// the spawn event names the model but not the effort.
const askedEffort = new Map<string, string>()

const FILE_TOOLS = new Set(['Read', 'Edit', 'MultiEdit', 'Write', 'NotebookEdit'])

const VERBS: Record<string, string> = {
  Read: 'reads',
  Edit: 'edits',
  MultiEdit: 'edits',
  Write: 'writes',
  NotebookEdit: 'edits',
  Grep: 'searches',
  Glob: 'finds',
  Bash: 'runs',
  PowerShell: 'runs',
  WebFetch: 'fetches',
  WebSearch: 'searches web',
  Agent: 'delegates',
  Task: 'delegates',
  TodoWrite: 'plans',
  Workflow: 'orchestrates',
}

const GLYPH: Record<CrewState, string> = {
  working: '✻',
  idle: '·',
  done: '✓',
  failed: '✗',
}

const COLOR: Record<CrewState, string> = {
  working: 'claude',
  idle: 'warning',
  done: 'success',
  failed: 'error',
}

const text = (value: unknown): string => (typeof value === 'string' ? value : '')

// What a tool call does and to what, in a few words.
const describeCall = (e: { tool: string }) => {
  const input = e as unknown as Record<string, unknown>
  const file = FILE_TOOLS.has(e.tool)
    ? text(input.file_path) || text(input.notebook_path)
    : ''
  const raw =
    file ||
    text(input.pattern) ||
    text(input.path) ||
    text(input.command) ||
    text(input.url) ||
    text(input.query) ||
    text(input.description)

  return {
    verb: VERBS[e.tool] ?? (e.tool.split('__').pop() ?? e.tool).toLowerCase(),
    target: file !== '' ? baseName(file) : clip(raw.replace(/\s+/g, ' '), 40),
    file,
  }
}

const blank = (id: string): CrewAgent => ({
  ...MAIN,
  id,
  label: 'agent',
  kind: 'agent',
  parentId: 'main',
})

// Drops the oldest finished helpers first, then the oldest helpers.
const trim = (list: CrewAgent[]): CrewAgent[] => {
  let out = list
  while (out.length > MAX_AGENTS) {
    const finished = out.findIndex(
      a => a.id !== 'main' && (a.state === 'done' || a.state === 'failed'),
    )
    const drop = finished !== -1 ? finished : out.findIndex(a => a.id !== 'main')
    if (drop === -1) {
      break
    }
    out = out.filter((_, i) => i !== drop)
  }

  return out
}

// Changes one agent, making it (from `seed`) when the list has none by that id.
const patchAgent = (
  list: CrewAgent[],
  id: string,
  patch: (agent: CrewAgent) => Partial<CrewAgent>,
  seed: Partial<CrewAgent> = {},
): CrewAgent[] => {
  const at = list.findIndex(a => a.id === id)
  const found = at === -1 ? undefined : list[at]
  const current = found ?? { ...blank(id), ...seed }
  const next = { ...current, ...patch(current) }

  return trim(found === undefined ? [...list, next] : list.map(a => (a.id === id ? next : a)))
}

const withMain = (list: CrewAgent[]): CrewAgent[] =>
  list.some(a => a.id === 'main') ? list : [MAIN, ...list]

const labelOf = (list: CrewAgent[], id: string): string =>
  list.find(a => a.id === id)?.label ?? (id === 'main' ? 'Claude' : 'agent')

const touchFile = (list: CrewFile[], path: string, verb: string, by: string): CrewFile[] => {
  const before = list.find(f => f.path === path)
  const entry: CrewFile = {
    path,
    name: baseName(path),
    touches: (before?.touches ?? 0) + 1,
    lastVerb: verb,
    lastBy: by,
  }

  return [entry, ...list.filter(f => f.path !== path)].slice(0, MAX_FILES)
}

const pushLog = (list: CrewLog[], who: string, line: string): CrewLog[] =>
  [...list, { who, text: line }].slice(-MAX_LOG)

// The pane is a view: a failure in it must never stop a tool call or a turn.
const safely = async (work: () => Promise<unknown>): Promise<void> => {
  try {
    await work()
  } catch {
    // Keep going, but count it so the pane can say something was missed.
    failures += 1
  }
}

const clearAll = async ($: EngineInterface): Promise<void> => {
  await update($, agents, list =>
    withMain(list)
      .filter(a => a.id === 'main')
      .map(a => ({
        ...a,
        state: 'idle' as const,
        verb: '',
        target: '',
        file: '',
        steps: 0,
        endedAt: 0,
      })),
  )
  await update($, files, () => [])
  await update($, log, () => [])
}

const STATE_OF: Record<string, CrewState> = {
  pending: 'working',
  running: 'working',
  waiting: 'idle',
  idle: 'idle',
  completed: 'done',
  failed: 'failed',
  killed: 'failed',
}

// Brings the floor in line with the engine's own list of agents. The events own
// the detail and the end of a helper's work; this fills in what they missed:
// - a helper the events never showed is added, unless the engine lists it as finished
//   (a helper cleared from the floor must not come back);
// - a helper the floor shows as finished is left alone (only an event revives it);
// - a helper in `gone` (listed before, then missing from the list twice in a row)
//   is marked done, because its end event was probably missed.
const reconcile = (
  list: CrewAgent[],
  infos: readonly AgentInfo[],
  now: number,
  gone: ReadonlySet<string>,
): CrewAgent[] =>
  infos.reduce(
    (out, info) => {
      const state = STATE_OF[info.status] ?? 'working'
      const isEnded = state === 'done' || state === 'failed'
      const onFloor = out.find(a => a.id === info.id)
      if ((onFloor === undefined && isEnded) || (onFloor !== undefined && onFloor.endedAt !== 0)) {
        return out
      }

      return patchAgent(
        out,
        info.id,
        a => ({
          label: a.label === 'agent' ? clip(info.description || info.name || info.type, 24) : a.label,
          kind: info.type,
          parentId: info.parentId ?? a.parentId,
          state,
          endedAt: isEnded ? now : 0,
        }),
        { state: 'working' },
      )
    },
    list.map(a =>
      gone.has(a.id) && a.endedAt === 0
        ? { ...a, state: 'done' as const, verb: '', target: '', file: '', endedAt: now }
        : a,
    ),
  )

// The helper ids the engine has listed at least once, and how many syncs in a row
// each has been missing since. Held in the module: a reload only starts the count again.
const listedBefore = new Set<string>()
const missingFor = new Map<string, number>()

// Notes the model and effort a loop runs on. The first one known for a helper stands
// until a model request shows what it really runs on; a write only when it changed.
const noteModel = async (
  $: EngineInterface,
  id: string,
  model: string,
  effort: string,
): Promise<void> => {
  const list = await read($, agents)
  const found = list.find(a => a.id === id)
  if (found !== undefined && found.model === model && found.effort === effort) {
    return
  }
  await update($, agents, current =>
    patchAgent(withMain(current), id, () => ({ model, effort }), { state: 'working' }),
  )
}

const syncAgents = async ($: EngineInterface): Promise<void> => {
  const infos = await $.agent.list()
  const now = await $.clock.now()
  const before = await read($, agents)

  const listed = new Set(infos.map(info => info.id))
  listed.forEach(id => listedBefore.add(id))
  const gone = new Set<string>()
  for (const a of before) {
    if (a.id === 'main' || a.endedAt !== 0 || listed.has(a.id) || !listedBefore.has(a.id)) {
      missingFor.delete(a.id)
      continue
    }
    const count = (missingFor.get(a.id) ?? 0) + 1
    missingFor.set(a.id, count)
    if (count >= 2) {
      gone.add(a.id)
    }
  }

  // Write only when something changed: a write redraws the pane.
  if (JSON.stringify(reconcile(before, infos, now, gone)) !== JSON.stringify(before)) {
    await update($, agents, current => reconcile(current, infos, now, gone))
  }
}

// A helper that finished LINGER_MS ago goes back to the bench: it leaves the floor, and
// its bench slot stops saying "out". The main agent never leaves.
const sendHome = async ($: EngineInterface): Promise<void> => {
  const now = await $.clock.now()
  const isHome = (a: CrewAgent): boolean =>
    a.id !== 'main' && a.endedAt !== 0 && now - a.endedAt >= LINGER_MS
  const list = await read($, agents)

  if (list.some(isHome)) {
    await update($, agents, current => current.filter(a => !isHome(a)))
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'crew',
      description:
        'Show the crew pane: the agents of this session working on your files. Options: bench, bigger, smaller, clear',
      argumentHint: 'bench | bigger | smaller | clear',
    })
    // Opened unasked, a pane can wait undrawn (a narrow window): say how to open it.
    // Every few seconds, check the engine's own list of agents against the floor.
    $.clock.every(3000, () => {
      void safely(() => syncAgents($))
    })
    // Once a second, send helpers that finished a while ago back to the bench.
    $.clock.every(1000, () => {
      void safely(() => sendHome($))
    })
    // The main agent shows the session's model until its first model request says more.
    await $.session
      .model()
      .then(model =>
        safely(() =>
          update($, agents, list =>
            patchAgent(withMain(list), 'main', a => ({ model: a.model === '' ? model : a.model })),
          ),
        ),
      )
      .catch(() => undefined)
    void $.ui
      .open({ id: PANE, title: 'Crew', ...PANE_SIZE })
      .then(opened => {
        if (!opened.isPlaced) {
          $.ui.toast('Crew pane is waiting: type /crew to open it')
        }
      })
      .catch(() => undefined)

    return next(e)
  })

  on('command.run', { command: 'crew' }, async ($, e) => {
    // The pane has no buttons: its settings are options of the command.
    const option = e.args.trim().toLowerCase()
    if (option === 'bench') {
      await update($, isBenchOpen, open => !open)

      return { text: `Bench ${(await read($, isBenchOpen)) ? 'shown' : 'hidden'}.` }
    }
    if (option === 'bigger' || option === 'smaller') {
      const step = option === 'bigger' ? FILL_STEP : -FILL_STEP
      await update($, zoom, z =>
        Math.min(MAX_FILL, Math.max(MIN_FILL, Math.round((z + step) * 100) / 100)),
      )

      return { text: `Picture ${option}: ${Math.round((await read($, zoom)) * 100)}% of the pane.` }
    }
    if (option === 'clear') {
      await clearAll($)

      return { text: 'Crew cleared.' }
    }

    const opened = await $.ui.open({ id: PANE, title: 'Crew', ...PANE_SIZE })

    return {
      text: opened.isPlaced
        ? 'Crew pane opened.'
        : `Crew pane is open but not drawn yet: ${opened.reason}`,
    }
  })

  // /clear starts a new conversation: the old crew has nothing left to show.
  on('session.end', async ($, e, next) => {
    if (e.reason === 'clear') {
      await safely(() => clearAll($))
    }

    return next(e)
  })

  // The engine offers every agent type the model may call. Keep the names for the bench.
  const seen = new Set<string>()
  on('agent.offer', async ($, e, next) => {
    const offer = await next(e)

    if (offer.isOffered && !seen.has(e.agent)) {
      await safely(async () => {
        await update($, roster, list =>
          list.some(r => r.name === e.agent)
            ? list
            : [...list, { name: e.agent, source: e.source, hint: clip(e.description, 160) }].slice(
                0,
                MAX_ROSTER,
              ),
        )
        // Only a name that was written is marked seen, so a failed write is tried again.
        seen.add(e.agent)
      })
    }

    return offer
  })

  on('agent.spawn', async ($, e, next) => {
    const started = await next(e)

    if (started.deny === undefined && started.agentId !== undefined) {
      const id = started.agentId
      const parent = e.parentAgentId ?? 'main'
      const label = clip(e.description || e.subagentType, 24)
      const kind = e.subagentType
      // As the Agent call asked: no model means the agent's own or the default.
      const model = e.model ?? 'inherit'
      const effort = askedEffort.get(e.tool_use_id) ?? ''
      askedEffort.delete(e.tool_use_id)

      await safely(async () => {
        const who = labelOf(await read($, agents), parent)
        // The helper may have made a tool call already: keep what it has, add who it is.
        await update($, agents, list =>
          patchAgent(
            list,
            id,
            // A model request may have shown the real model and effort already: keep them.
            a => ({
              label,
              kind,
              parentId: parent,
              model: a.model !== '' ? a.model : model,
              effort: a.effort !== '' ? a.effort : effort,
            }),
            {
              state: 'working',
              verb: 'starting',
            },
          ),
        )
        await update($, log, list => pushLog(list, who, `starts ${kind}: ${label}`))
      })
    }

    return started
  })

  on('turn.start', async ($, e, next) => {
    const id = e.agentId ?? 'main'

    await safely(() =>
      update($, agents, list =>
        patchAgent(list, id, () => ({ state: 'working', verb: 'thinking', target: '', endedAt: 0 })),
      ),
    )

    return next(e)
  })

  on('turn.complete', async ($, e, next) => {
    const id = e.agentId ?? 'main'
    const state: CrewState =
      id === 'main' ? 'idle' : e.reason === 'answer' ? 'done' : 'failed'

    await safely(async () => {
      const who = labelOf(await read($, agents), id)
      const now = await $.clock.now()
      await update($, agents, list =>
        patchAgent(list, id, () => ({
          state,
          verb: '',
          target: '',
          file: '',
          endedAt: id === 'main' ? 0 : now,
        })),
      )
      if (id !== 'main') {
        await update($, log, list => pushLog(list, who, state === 'done' ? 'finished' : 'stopped'))
      }
    })

    return next(e)
  })

  on('tool.call', async ($, e, next) => {
    const id = e.agentId ?? 'main'
    // Kept before the call runs: the spawn happens inside it.
    if (e.tool === 'Agent' && e.tool_use_id !== undefined) {
      const effort = effortText(e.effort)
      if (effort !== '') {
        askedEffort.set(e.tool_use_id, effort)
      }
    }

    // The call is recorded while the tool runs: it shows at once and costs no waiting.
    const recording = safely(async () => {
      const call = describeCall(e)
      const who = labelOf(await read($, agents), id)
      await update($, agents, list =>
        patchAgent(
          list,
          id,
          a => ({
            state: 'working',
            verb: call.verb,
            target: call.target,
            // A tool with no file (a search, a command) keeps the file it had.
            file: call.file !== '' ? call.file : a.file,
            steps: a.steps + 1,
            // A tool call is proof of life: it brings a helper back if it looked finished.
            endedAt: 0,
          }),
          { parentId: 'main' },
        ),
      )
      if (call.file !== '') {
        await update($, files, list => touchFile(list, call.file, call.verb, who))
      }
      await update($, log, list => pushLog(list, who, `${call.verb} ${call.target}`.trim()))
    })
    const ran = await next(e)
    await recording

    return ran
  })

  // Each model request names the model and effort its loop really runs on.
  on('turn.step', async function* ($, e, next) {
    await safely(() => noteModel($, e.agentId ?? 'main', e.model, effortText(e.effort)))

    return yield* next(e)
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const crew = withMain(await read($, agents))
    const shelf = await read($, files)
    const lines = await read($, log)
    const offered = await read($, roster)
    const isOpen = await read($, isBenchOpen)
    const size = await read($, zoom)
    const busy = crew.filter(a => a.state === 'working').length
    const missed = failures > 0 ? ` · ${failures} updates missed` : ''
    const summary = `${busy} working · ${crew.length - 1} helpers · ${shelf.length} files · ${offered.length} on bench${missed}`
    // Your own agents first, then the built-in ones, each group in name order.
    const bench: BenchItem[] = [...offered]
      .sort(
        (a, b) =>
          Number(a.source === 'built-in') - Number(b.source === 'built-in') ||
          a.name.localeCompare(b.name),
      )
      .map(r => ({
        ...r,
        // "Out" for as long as one of that type is on the floor, even a finished one.
        isOnDuty: crew.some(a => a.id !== 'main' && a.kind === r.name),
      }))

    if (e.surface === 'terminal') {
      const { Box, Text } = $.ui.resolve(e)

      return (
        <Box flexDirection="column">
          <Text bold color="claude">
            ✻ Crew <Text dimColor>{summary}</Text>
          </Text>
          {crew.map(a => {
            const tag = agentTag(a)
            const family = modelFamily(a.model)

            return (
              <Text color={COLOR[a.state]}>
                {GLYPH[a.state]} {a.label}{' '}
                {tag !== '' && (
                  <Text color={family === undefined ? 'subtle' : MODEL_THEME[family]}>[{tag}] </Text>
                )}
                <Text dimColor>
                  ({a.kind}) {a.verb} {a.target}
                </Text>
              </Text>
            )
          })}
          {shelf.map(f => (
            <Text dimColor>
              {f.name} {f.lastVerb} ×{f.touches} by {f.lastBy}
            </Text>
          ))}
          {bench.length > 0 && (
            <Text dimColor>bench: {bench.map(b => (b.isOnDuty ? `${b.name} (out)` : b.name)).join(', ')}</Text>
          )}
        </Box>
      )
    }

    const { Box, Svg, Text } = $.ui.resolve(e)
    const room = Math.round(e.props.bodyColumns * CELL_PX)
    const scene = buildScene(crew, shelf, bench, isOpen, Math.round(room * size))

    return (
      <Box flexDirection="column" gap={1}>
        <Text bold>
          Crew <Text dimColor>{summary}</Text>
        </Text>
        <Svg
          source={scene.svg}
          alt={scene.alt}
          width={scene.width}
          height={scene.height}
          isInteractive
        />
        <Box flexDirection="column">
          {lines.slice(-8).map(line => (
            <Text dimColor>
              {line.who}: {line.text}
            </Text>
          ))}
        </Box>
      </Box>
    )
  })
}
