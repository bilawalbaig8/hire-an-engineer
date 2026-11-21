// Draws the crew as one SVG picture: a Claude icon per agent, a card per file,
// and a glowing line from each working agent to the file it touches.
// The animation is SMIL inside the SVG, so the picture moves with no redraws.

import type { CrewAgent, CrewFile } from '../types'
import { icon } from './mascot'
import { MODEL_HEX, OTHER_HEX, modelFamily, modelTag } from './models'

// The canvas is narrow on purpose: the pane has a fixed width, so a narrow canvas
// is shown at a larger scale and every character and word comes out bigger.
export const SCENE_WIDTH = 260
// How much of the pane's width the picture takes: 1 is the whole width, as the
// pane's width in cells says it is. Bigger and Smaller move it in steps.
export const DEFAULT_FILL = 1
export const MIN_FILL = 0.5
export const MAX_FILL = 2

const ORANGE = '#d97757'
const PANEL = '#1c1b1a'
const CARD = '#2a2927'
const LINE = '#4a4744'
const PER_ROW = 2
const MAX_SHOWN = 8
const MAX_CARDS = 6
const MAIN_Y = 46
const SUB_TOP = 172
const ROW_GAP = 112
// From a character's centre down past its last line of words, where its lines start.
const FOOT = 79
const CARD_ROW = 56
const BENCH_COLS = 5
const BENCH_ROW = 54
const MAX_BENCH = 30

type Spot = { x: number; y: number }

// `width` and `height` are the picture's size on screen, in pixels.
export type Scene = { svg: string; alt: string; width: number; height: number }

// One agent type the session can call. `isOnDuty` when one of that type is running now.
export type BenchItem = { name: string; source: string; hint: string; isOnDuty: boolean }

export const baseName = (path: string): string => {
  const parts = path.split(/[\\/]/).filter(part => part !== '')

  return parts[parts.length - 1] ?? path
}

export const clip = (text: string, max: number): string =>
  text.length > max ? `${text.slice(0, max - 1)}…` : text

// Text goes into SVG markup, so one stray & or < would break the picture.
const esc = (text: string): string =>
  text
    .replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')

const num = (n: number): number => Math.round(n * 10) / 10

const slotX = (count: number, index: number, width: number, perRow: number = PER_ROW): number => {
  const inRow = Math.min(perRow, count - Math.floor(index / perRow) * perRow)
  // Every slot is one equal share of the width, so a short row sits in the middle.
  const cell = width / perRow

  return num((width - inRow * cell) / 2 + cell / 2 + (index % perRow) * cell)
}

const curve = (from: Spot, to: Spot): string => {
  const mid = num((from.y + to.y) / 2)

  return `M${from.x} ${from.y} C${from.x} ${mid} ${to.x} ${mid} ${to.x} ${to.y}`
}

// A line to a file: dashes that run and a bright dot that travels along it.
const beam = (from: Spot, to: Spot): string => {
  const d = curve(from, to)

  return (
    `<path d="${d}" fill="none" stroke="${ORANGE}" stroke-width="1.8" stroke-dasharray="5 4" stroke-linecap="round">` +
    '<animate attributeName="stroke-dashoffset" from="18" to="0" dur="0.9s" repeatCount="indefinite"/></path>' +
    `<circle r="3" fill="#ffd2c0"><animateMotion dur="1.4s" repeatCount="indefinite" path="${d}"/></circle>`
  )
}

const edge = (from: Spot, to: Spot, isLive: boolean): string => {
  const d = curve(from, to)

  return isLive
    ? `<path d="${d}" fill="none" stroke="#8a5f4d" stroke-width="1.3" stroke-dasharray="3 5"><animate attributeName="stroke-dashoffset" from="16" to="0" dur="2s" repeatCount="indefinite"/></path>`
    : `<path d="${d}" fill="none" stroke="${LINE}" stroke-width="1.2"/>`
}

const doing = (agent: CrewAgent): string => {
  if (agent.state === 'working') {
    const text = `${agent.verb} ${agent.target}`.trim()

    return text === '' ? 'thinking…' : text
  }
  if (agent.state === 'idle') {
    return 'waiting'
  }
  if (agent.state === 'done') {
    return `done · ${agent.steps} steps`
  }

  return 'stopped'
}

// The model and effort under a character, or '' for the main agent before its model is known.
export const agentTag = (agent: CrewAgent): string =>
  agent.id === 'main' && agent.model === '' ? '' : modelTag(agent.model, agent.effort)

const accentOf = (agent: CrewAgent): string => {
  const family = modelFamily(agent.model)

  return family === undefined ? OTHER_HEX : MODEL_HEX[family]
}

// The model's colour as a soft patch of ground under the feet, and a dot before the tag.
const drawTag = (agent: CrewAgent, x: number, y: number, scale: number): string => {
  const tag = agentTag(agent)
  if (tag === '') {
    return ''
  }
  const color = accentOf(agent)
  const shown = clip(tag, 22)
  // About how wide the words are, to sit the dot just left of them.
  const half = num(shown.length * 2.45)

  return (
    `<ellipse cx="${x}" cy="${num(y + 13.5 * scale)}" rx="${num(13 * scale)}" ry="${num(2.2 * scale)}" fill="${color}" fill-opacity="0.32"/>` +
    `<circle cx="${num(x - half - 5)}" cy="${y + 70}" r="2.6" fill="${color}"/>` +
    `<text class="m" text-anchor="middle" x="${x}" y="${y + 73}" data-model="${esc(modelFamily(agent.model) ?? 'other')}">${esc(shown)}</text>`
  )
}

const drawAgent = (agent: CrewAgent, spot: Spot, scale: number): string => {
  const isMain = agent.id === 'main'
  const name = isMain ? 'Claude' : clip(agent.label, 15)
  const kind = isMain ? 'main agent' : clip(agent.kind, 18)
  const style = agent.state === 'working' ? 'a' : 's'
  const x = spot.x
  const tag = agentTag(agent)

  return (
    `<g><title>${esc(agent.label)} (${esc(agent.kind)})${tag === '' ? '' : ` ${esc(tag)}`}: ${agent.state}, ${agent.steps} steps</title>` +
    drawTag(agent, x, spot.y, scale) +
    icon(agent, x, spot.y, scale) +
    `<text class="l" text-anchor="middle" x="${x}" y="${spot.y + 34}">${esc(name)}</text>` +
    `<text class="s" text-anchor="middle" x="${x}" y="${spot.y + 47}">${esc(kind)}</text>` +
    `<text class="${style}" text-anchor="middle" x="${x}" y="${spot.y + 60}">${esc(clip(doing(agent), 20))}</text></g>`
  )
}

const drawCard = (file: CrewFile, x: number, top: number, isHot: boolean): string => {
  const w = 102
  const left = num(x - w / 2)
  const stroke = isHot ? ORANGE : LINE
  const pulse = isHot
    ? '<animate attributeName="stroke-opacity" values="1;0.4;1" dur="1.2s" repeatCount="indefinite"/>'
    : ''

  return (
    `<g><title>${esc(file.path)}: ${file.touches} touches, last ${esc(file.lastVerb)} by ${esc(file.lastBy)}</title>` +
    `<rect x="${left}" y="${top}" width="${w}" height="46" rx="8" fill="${CARD}" stroke="${stroke}" stroke-width="${isHot ? 1.6 : 1}">${pulse}</rect>` +
    `<path d="M${left + 10} ${top + 12} h8 l5 5 v13 h-13 z" fill="none" stroke="${isHot ? ORANGE : '#8a837d'}" stroke-width="1.3" stroke-linejoin="round"/>` +
    `<text class="l" x="${left + 30}" y="${top + 20}">${esc(clip(file.name, 10))}</text>` +
    `<text class="s" x="${left + 30}" y="${top + 34}">${esc(clip(`${file.lastVerb} ×${file.touches}`, 11))}</text></g>`
  )
}

// The bench: every agent type the session can call, asleep until Claude calls it.
// One that is running now leaves an empty dashed slot ("out") and shows on the floor.
const drawBench = (items: BenchItem[], top: number, width: number): string => {
  const sleeper = (name: string): CrewAgent => ({
    id: name,
    label: name,
    kind: name,
    state: 'idle',
    verb: '',
    target: '',
    file: '',
    parentId: 'main',
    steps: 0,
    endedAt: 0,
    model: '',
    effort: '',
  })

  return items
    .map((item, i) => {
      const x = slotX(items.length, i, width, BENCH_COLS)
      const y = top + Math.floor(i / BENCH_COLS) * BENCH_ROW
      const tip = `<title>${esc(item.name)} (${esc(item.source)}): ${esc(item.hint)}</title>`
      const label = (css: string): string =>
        `<text class="${css}" text-anchor="middle" x="${x}" y="${y + 41}">${esc(clip(item.name, 9))}</text>`

      return item.isOnDuty
        ? `<g>${tip}<rect x="${num(x - 11)}" y="${y + 4}" width="22" height="26" rx="5" fill="none" stroke="${ORANGE}" stroke-opacity="0.7" stroke-dasharray="2 2"/>` +
            `<text class="a" text-anchor="middle" x="${x}" y="${y + 21}">out</text>${label('a')}</g>`
        : `<g>${tip}${icon(sleeper(item.name), x, y + 12, 0.7, false)}${label('b')}</g>`
    })
    .join('')
}

export const buildScene = (
  agents: CrewAgent[],
  files: CrewFile[],
  bench: BenchItem[] = [],
  isBenchOpen: boolean = true,
  displayWidth: number = SCENE_WIDTH,
): Scene => {
  const width = SCENE_WIDTH
  const main = agents.find(agent => agent.id === 'main')
  const helpers = agents.filter(agent => agent.id !== 'main')
  const shown = helpers.slice(-MAX_SHOWN)
  const hidden = helpers.length - shown.length
  const cards = files.slice(0, MAX_CARDS)

  const spots = new Map<string, Spot>()
  const feet = new Map<string, number>()
  if (main !== undefined) {
    spots.set('main', { x: num(width / 2), y: MAIN_Y })
    feet.set('main', MAIN_Y + FOOT)
  }
  shown.forEach((agent, i) => {
    const y = SUB_TOP + Math.floor(i / PER_ROW) * ROW_GAP
    spots.set(agent.id, { x: slotX(shown.length, i, width), y })
    feet.set(agent.id, y + FOOT)
  })

  const subRows = Math.ceil(shown.length / PER_ROW)
  const lastY = shown.length > 0 ? SUB_TOP + (subRows - 1) * ROW_GAP : MAIN_Y
  const shelfY = lastY + 97
  const cardTop = shelfY + 12
  const cardRows = Math.ceil(cards.length / PER_ROW)
  const filesBottom = cards.length > 0 ? cardTop + cardRows * CARD_ROW + 4 : shelfY + 42

  const benchItems = bench.slice(0, MAX_BENCH)
  const benchHead = filesBottom + 10
  const benchTop = benchHead + 12
  const benchRows = Math.ceil(benchItems.length / BENCH_COLS)
  const height = isBenchOpen
    ? benchTop + (benchItems.length > 0 ? benchRows * BENCH_ROW : 28) + 4
    : filesBottom

  const hot = new Set(
    agents.filter(agent => agent.state === 'working' && agent.file !== '').map(agent => agent.file),
  )
  const cardSpots = new Map<string, Spot>()
  cards.forEach((file, i) => {
    cardSpots.set(file.path, {
      x: slotX(cards.length, i, width),
      y: cardTop + Math.floor(i / PER_ROW) * CARD_ROW,
    })
  })

  const edges = shown
    .map((agent, i) => {
      const parentId = spots.has(agent.parentId) ? agent.parentId : 'main'
      const from = spots.get(parentId)
      const to = spots.get(agent.id)
      const foot = feet.get(parentId)
      // A line from the main agent to a lower row would cut through the row above.
      const isHidden = parentId === 'main' && i >= PER_ROW
      if (isHidden || from === undefined || to === undefined || foot === undefined) {
        return ''
      }

      return edge({ x: from.x, y: foot }, { x: to.x, y: to.y - 28 }, agent.state === 'working')
    })
    .join('')

  const beams = agents
    .map(agent => {
      const from = spots.get(agent.id)
      const foot = feet.get(agent.id)
      const card = cardSpots.get(agent.file)
      if (agent.state !== 'working' || from === undefined || foot === undefined || card === undefined) {
        return ''
      }

      return beam({ x: from.x, y: foot }, card)
    })
    .join('')

  const people = [
    ...(main !== undefined ? [drawAgent(main, spots.get('main') ?? { x: 0, y: 0 }, 1.8)] : []),
    ...shown.map(agent => drawAgent(agent, spots.get(agent.id) ?? { x: 0, y: 0 }, 1.5)),
  ].join('')

  const shelf =
    cards.length > 0
      ? cards
          .map(file => {
            const spot = cardSpots.get(file.path) ?? { x: 0, y: 0 }

            return drawCard(file, spot.x, spot.y, hot.has(file.path))
          })
          .join('')
      : `<text class="s" text-anchor="middle" x="${num(width / 2)}" y="${shelfY + 26}">Files show up here when agents touch them</text>`
  const more =
    hidden > 0
      ? `<text class="s" text-anchor="end" x="${width - 14}" y="22">+${hidden} earlier helpers</text>`
      : ''

  const displayHeight = Math.round((height * displayWidth) / width)

  const benchBlock = !isBenchOpen
    ? ''
    : `<text class="h" x="14" y="${benchHead + 4}">BENCH</text>` +
      (benchItems.length > 0
        ? drawBench(benchItems, benchTop, width)
        : `<text class="s" text-anchor="middle" x="${num(width / 2)}" y="${benchTop + 14}">Agents show up here after your first message</text>`)

  const svg =
    `<svg xmlns="http://www.w3.org/2000/svg" width="${displayWidth}" height="${displayHeight}" viewBox="0 0 ${width} ${height}">` +
    `<style>text{font-family:-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;paint-order:stroke;stroke:${PANEL};stroke-width:2.5px;stroke-linejoin:round}` +
    '.l{font-size:11px;font-weight:600;fill:#f3eee9}.s{font-size:9.5px;fill:#a59d97}.a{font-size:9.5px;fill:#f0a98f}.b{font-size:8.5px;fill:#a59d97}.m{font-size:9px;fill:#d8d1cb}' +
    '.h{font-size:9px;letter-spacing:.12em;fill:#7d766f;stroke:none}</style>' +
    '<defs><pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="0.8" fill="#2c2a28"/></pattern></defs>' +
    `<rect width="${width}" height="${height}" rx="14" fill="${PANEL}" stroke="#34312f"/>` +
    `<rect width="${width}" height="${height}" rx="14" fill="url(#dots)"/>` +
    `${more}${edges}${beams}` +
    `<text class="h" x="14" y="${shelfY}">FILES</text>` +
    `${shelf}${benchBlock}${people}</svg>`

  const alt = [
    ...agents.map(agent => {
      const tag = agentTag(agent)

      return `${agent.label} (${agent.kind}${tag === '' ? '' : `, ${tag}`}) ${doing(agent)}`
    }),
    cards.length > 0 ? `files: ${cards.map(file => file.name).join(', ')}` : 'no files yet',
    ...(isBenchOpen && benchItems.length > 0
      ? [`bench: ${benchItems.map(item => item.name).join(', ')}`]
      : []),
  ].join('; ')

  return { svg, alt, width: displayWidth, height: displayHeight }
}
