import { expect, mock, test } from 'claude-code/testing'

import { modelName, modelTag } from '../hooks/models'

// The session's MCP tools make tool.call's input a union too deep for tsc to check
// against a literal, so the tests call it through a plain signature.
const callTool = ($: { tool: { call: unknown } }, input: { tool: string } & Record<string, unknown>) =>
  ($.tool.call as unknown as (i: typeof input) => Promise<unknown>)(input)

const PANE = {
  plugin: 'agent-crew',
  component: 'Pane',
  requestId: 'agent-crew',
  props: {
    title: 'Crew',
    isFocused: false,
    bodyColumns: 40,
    placement: 'dock',
    scroll: { offset: 0, bodyRows: 20 },
    view: {},
  },
} as const

test('the pane shows a helper and the file being edited, on every surface', async ($, on) => {
  // Nothing sits beneath the plugin: each hook here stands for the engine.
  on('command.register', () => ({ value: { command: 'crew' } }))
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))
  on('agent.spawn', () => ({ model: 'sonnet', agentId: 'helper-1' }))
  on('turn.start', (_, e) => ({ turnId: e.turnId }))
  on('tool.call', () => ({ result: {} }))

  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
  await $.agent.spawn({
    tool_use_id: 'spawn-1',
    prompt: 'Fix the parser',
    description: 'Fix the parser',
    subagentType: 'Explore',
    provider: { plugin: 'engine', tier: 'core' },
    parentModel: 'sonnet',
    background: false,
    fork: false,
  })
  await $.turn.start({ text: 'Fix the parser', turnId: 't1', agentId: 'helper-1' })
  await callTool($, {
    tool: 'Edit',
    file_path: 'D:\\work\\src\\parser.ts',
    old_string: 'a',
    new_string: 'b',
  })

  for (const surface of ['terminal', 'desktop', 'vscode', 'mobile'] as const) {
    const ui = await $.ui.mount({ ...PANE, surface })

    // The helper and the file each show in words, whatever the surface draws.
    expect(await ui.find({ type: 'Text', text: /Explore/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /parser\.ts/ })).toBeDefined()
    if (surface !== 'terminal') {
      expect(await ui.find({ type: 'Svg' })).toBeDefined()
    }
    await ui.unmount()
  }
})

test('a helper that just finished stays on the floor when the next turn starts', async ($, on) => {
  on('command.register', () => ({ value: { command: 'crew' } }))
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))
  on('agent.spawn', () => ({ model: 'sonnet', agentId: 'helper-1' }))
  on('turn.start', (_, e) => ({ turnId: e.turnId }))
  on('turn.complete', () => ({ text: '' }))

  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
  await $.agent.spawn({
    tool_use_id: 'spawn-1',
    prompt: 'Look around',
    description: 'Look around',
    subagentType: 'Explore',
    provider: { plugin: 'engine', tier: 'core' },
    parentModel: 'sonnet',
    background: true,
    fork: false,
  })
  await $.turn.start({ text: 'Look around', turnId: 't1', agentId: 'helper-1' })
  await $.turn.complete({
    answer: 'Done',
    durationMs: 5,
    isAborted: false,
    turnId: 't1',
    agentId: 'helper-1',
    reason: 'answer',
  })
  // A background helper's report starts a turn of the main agent.
  await $.turn.start({ text: 'The helper reported', turnId: 't2' })

  const ui = await $.ui.mount({ ...PANE, surface: 'terminal' })

  expect(await ui.find({ type: 'Text', text: /Look around/ })).toBeDefined()
  await ui.unmount()
})

test('a helper goes back to the bench a few seconds after it finishes', async ($, on) => {
  // A start time past zero: the mod reads an end time of 0 as "not finished yet".
  const clock = mock.clock(on, { now: 1_000_000 })
  on('command.register', () => ({ value: { command: 'crew' } }))
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))
  on('agent.list', () => ({ value: [] }))
  on('agent.offer', () => ({ isOffered: true }))
  on('agent.spawn', () => ({ model: 'sonnet', agentId: 'helper-1' }))
  on('turn.start', (_, e) => ({ turnId: e.turnId }))
  on('turn.complete', () => ({ text: '' }))

  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
  await $.agent.offer({
    agent: 'Explore',
    description: 'Searches many files',
    source: 'built-in',
    provider: { plugin: 'engine', tier: 'core' },
  })
  await $.agent.spawn({
    tool_use_id: 'spawn-1',
    prompt: 'Look around',
    description: 'Look around',
    subagentType: 'Explore',
    provider: { plugin: 'engine', tier: 'core' },
    parentModel: 'sonnet',
    background: true,
    fork: false,
  })
  await $.turn.start({ text: 'Look around', turnId: 't1', agentId: 'helper-1' })
  await $.turn.complete({
    answer: 'Done',
    durationMs: 5,
    isAborted: false,
    turnId: 't1',
    agentId: 'helper-1',
    reason: 'answer',
  })

  // Just finished: it is on the floor and its bench slot says out.
  const before = await $.ui.mount({ ...PANE, surface: 'terminal' })
  expect(await before.find({ type: 'Text', text: /Look around/ })).toBeDefined()
  expect(await before.find({ type: 'Text', text: /Explore \(out\)/ })).toBeDefined()
  await before.unmount()

  await clock.advance(9000)

  // Eight seconds on: it is back on the bench.
  const after = await $.ui.mount({ ...PANE, surface: 'terminal' })
  expect(await after.find({ type: 'Text', text: /Look around/ })).toBeUndefined()
  expect(await after.find({ type: 'Text', text: /bench: Explore$/ })).toBeDefined()
  await after.unmount()
})

test('the bench lists the agents the engine offers, your own first', async ($, on) => {
  on('command.register', () => ({ value: { command: 'crew' } }))
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))
  on('agent.offer', () => ({ isOffered: true }))

  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
  await $.agent.offer({
    agent: 'Explore',
    description: 'Searches many files',
    source: 'built-in',
    provider: { plugin: 'engine', tier: 'core' },
  })
  await $.agent.offer({
    agent: 'architect',
    description: 'Designs systems',
    source: 'plugin',
    provider: { plugin: 'team', tier: 'user' },
  })

  const ui = await $.ui.mount({ ...PANE, surface: 'terminal' })

  expect(await ui.find({ type: 'Text', text: /bench: architect, Explore/ })).toBeDefined()
  await ui.unmount()
})

test('a value an earlier version stored is declined', async ($, on) => {
  // What the code before this edit wrote stays through the reload.
  on('state.get', () => ({
    value: { value: [{ bogus: 1 }], version: 1 },
  }))

  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })

  expect(await ui.find({ type: 'Text', text: /0 working · 0 helpers · 0 files/ })).toBeDefined()
  await ui.unmount()
})

const SPAWN = {
  prompt: 'Look around',
  subagentType: 'Explore',
  provider: { plugin: 'engine', tier: 'core' },
  parentModel: 'claude-opus-5-5',
  background: true,
  fork: false,
} as const

test('each helper shows the model and effort it was spawned with', async ($, on) => {
  on('command.register', () => ({ value: { command: 'crew' } }))
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))
  on('session.model', () => ({ value: 'claude-opus-5-5' }))
  on('agent.spawn', (_, e) => ({
    model: e.model ?? 'claude-opus-5-5',
    agentId: e.tool_use_id === 'spawn-1' ? 'helper-1' : 'helper-2',
  }))
  on('tool.call', () => ({ result: {} }))

  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
  // The Agent call asks for the effort; the spawn inside it names the model.
  await callTool($, {
    tool: 'Agent',
    tool_use_id: 'spawn-1',
    description: 'Quick look',
    prompt: 'Look around',
    subagent_type: 'Explore',
    model: 'haiku',
    effort: 'low',
  })
  await $.agent.spawn({ ...SPAWN, tool_use_id: 'spawn-1', description: 'Quick look', model: 'haiku' })
  // No model and no effort asked: it inherits.
  await $.agent.spawn({ ...SPAWN, tool_use_id: 'spawn-2', description: 'Deep look' })

  const text = await $.ui.mount({ ...PANE, surface: 'terminal' })
  expect((await text.find({ type: 'Text', text: /^\[Haiku · low\]/ }))?.text).toMatch(/^\[Haiku · low\] $/)
  expect((await text.find({ type: 'Text', text: /^\[inherit\]/ }))?.text).toMatch(/^\[inherit\] $/)
  // The main agent shows the session's model, pretty-printed.
  expect(await text.find({ type: 'Text', text: /^\[Opus 5\.5\]/ })).toBeDefined()
  await text.unmount()

  const picture = await $.ui.mount({ ...PANE, surface: 'desktop' })
  const svg = await picture.find({ type: 'Svg' })
  expect(String(svg?.props.source)).toContain('Haiku · low')
  expect(String(svg?.props.source)).toContain('>inherit<')
  // Haiku's green accent, and the alt text says the same tag.
  expect(String(svg?.props.source)).toContain('#5cc87a')
  expect(String(svg?.props.alt)).toContain('Quick look (Explore, Haiku · low)')
  await picture.unmount()
})

test('the main agent shows the model and effort of its model requests', async ($, on) => {
  on('command.register', () => ({ value: { command: 'crew' } }))
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))
  on('session.model', () => ({ value: 'sonnet' }))
  on('turn.step', async function* (_, e) {
    return {
      turnId: e.turnId,
      index: e.index,
      answer: '',
      toolUses: [],
      stopReason: 'end_turn' as const,
      usage: null,
    }
  })

  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
  const before = await $.ui.mount({ ...PANE, surface: 'terminal' })
  expect(await before.find({ type: 'Text', text: /^\[Sonnet\]/ })).toBeDefined()
  await before.unmount()

  for await (const _ of $.turn.step({
    turnId: 't1',
    index: 0,
    model: 'claude-fable-5',
    effort: 'high',
    messageCount: 1,
  })) {
    // Nothing streams from the stand-in beneath.
  }

  const after = await $.ui.mount({ ...PANE, surface: 'terminal' })
  expect(await after.find({ type: 'Text', text: /^\[Fable 5 · high\]/ })).toBeDefined()
  await after.unmount()
})

test('model names are pretty-printed from aliases and full ids', async () => {
  expect(modelTag('haiku', 'low')).toBe('Haiku · low')
  expect(modelTag('', '')).toBe('inherit')
  expect(modelTag('inherit', 'max')).toBe('inherit · max')
  expect(modelName('claude-opus-5-5')).toBe('Opus 5.5')
  expect(modelName('claude-sonnet-4-5-20250929[1m]')).toBe('Sonnet 4.5')
  expect(modelName('claude-3-5-sonnet-20241022')).toBe('Sonnet 3.5')
  expect(modelName('us.anthropic.claude-haiku-4-5-20251001-v1:0')).toBe('Haiku 4.5')
  expect(modelName('claude-sonnet-4-20250514')).toBe('Sonnet 4')
  expect(modelName('fable')).toBe('Fable')
})
