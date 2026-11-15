import { expect, test } from 'claude-code/testing'

const PANE = {
  plugin: 'hire-an-engineer-board',
  component: 'Pane',
  requestId: 'hire-an-engineer-board',
  props: {
    title: 'Project board',
    isFocused: false,
    bodyColumns: 48,
    placement: 'dock',
    scroll: { offset: 0, bodyRows: 40 },
    view: {},
  },
} as const

const TASKS = [
  '# Tasks',
  '',
  '| # | title | size | stage | status | round | branch | slot | needs | cost | note |',
  '|---|---|---|---|---|---|---|---|---|---|---|',
  '| 1 | Order form | Small | verify | done | 1 | task/1 | A | none | 2 tasks | |',
  '| 2 | Orders list | Small | build | progress | 2 | task/2 | B | — | | |',
  '| 3 | WhatsApp alert | Medium | review | review | 1 | task/3 | C | test | | |',
  '| 4 | Daily report | Small |  | queued | 0 |  |  |  | | waits #2 |',
].join('\n')

const STATE = [
  '# Project state',
  '## Current focus',
  '- Building the orders list',
  '## Authorization (never trimmed)',
  '- scope: bakery orders · cap: 6 tasks, 3 rounds each · integration branch: develop',
  '- mode: autopilot · status: active · date: 2026-11-15',
  '## Known issues',
].join('\n')

function engine(on: any, files: Record<string, string>) {
  on('command.register', () => ({ value: { command: 'board' } }))
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('clock.every', () => ({ value: { id: 't' } }))
  on('session.start', (_: any, e: any) => ({ cwd: e.cwd }))
  on('session.cwd', () => ({ value: '/proj' }))
  on('fs.read', (_: any, e: any) => {
    const name = Object.keys(files).find(n => e.path.replace(/\\/g, '/').endsWith('/' + n))
    if (!name) throw new Error('ENOENT')
    return { value: files[name] }
  })
}

test('the pane shows tasks by stage and what waits for the person', async ($, on) => {
  engine(on, { 'TASKS.md': TASKS, 'PROJECT_STATE.md': STATE })
  await $.session.start({ cwd: '/proj', surface: 'desktop', isInteractive: true })

  for (const surface of ['terminal', 'desktop', 'vscode', 'mobile'] as const) {
    const ui = await $.ui.mount({ ...PANE, surface })
    expect((await ui.find({ type: 'Text', text: /^proj$/ }))?.text).toBe('proj')
    expect((await ui.find({ type: 'Text', text: /Mode:/ }))?.text).toBe(
      'Mode: autopilot · Approval: active',
    )
    expect((await ui.find({ type: 'Text', text: /Waiting for you/ }))?.text).toBe(
      'Waiting for you (1)',
    )
    expect((await ui.find({ type: 'Text', text: /#3 WhatsApp alert:/ }))?.text).toBe(
      '#3 WhatsApp alert: test it',
    )
    expect((await ui.find({ type: 'Text', text: /^build \d/ }))?.text).toBe('build 1')
    expect((await ui.find({ type: 'Text', text: /^done \d/ }))?.text).toBe('done 1')
    expect((await ui.find({ type: 'Text', text: /round 2/ }))?.text).toBe(
      'build · size Small · round 2 · lane B',
    )
    expect((await ui.find({ type: 'Text', text: /Next up/ }))?.text).toBe('Next up (1)')
    expect((await ui.find({ type: 'Text', text: /Now:/ }))?.text).toBe(
      'Now: Building the orders list',
    )
    await ui.unmount()
  }
})

test('a folder with no project shows a plain explanation', async ($, on) => {
  engine(on, {})
  await $.session.start({ cwd: '/proj', surface: 'desktop', isInteractive: true })
  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  expect((await ui.find({ type: 'Text', text: /No project board/ }))?.text).toBe(
    'No project board here yet',
  )
  await ui.unmount()
})
