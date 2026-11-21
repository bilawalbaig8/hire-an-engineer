// The little Claude character: an orange pixel body with two dark eyes, stubby
// arms and four legs. It acts out the agent's state and wears a small prop that
// tells you what kind of agent it is.
// Everything here is plain SVG markup. The motion is SMIL, so it needs no redraws.

import type { CrewAgent, CrewState } from '../types'

const DARK = '#1c1b1a'
const GOLD = '#f2c14e'
const PAPER = '#f3eee9'

const SKIN: Record<CrewState, { body: string; shade: string }> = {
  working: { body: '#d97757', shade: '#b85f40' },
  idle: { body: '#c98e76', shade: '#a87461' },
  done: { body: '#d97757', shade: '#b85f40' },
  failed: { body: '#9b7468', shade: '#7e5b51' },
}

type Gear =
  | 'crown'
  | 'baton'
  | 'hardhat'
  | 'glasses'
  | 'magnifier'
  | 'pencil'
  | 'shield'
  | 'headphones'
  | 'clipboard'
  | 'flag'
  | 'beret'
  | 'megaphone'
  | 'lightbulb'
  | 'chart'
  | 'book'
  | 'wrench'
  | 'none'

// The prop follows the agent type: the main agent is the boss, an Explore agent
// carries a magnifier, a reviewer wears glasses, and so on. The first match wins.
const GEAR_RULES: [RegExp, Gear][] = [
  [/secur/, 'shield'],
  [/orchestrat/, 'baton'],
  [/explor|search|research/, 'magnifier'],
  [/project-manag/, 'flag'],
  [/plan|architect/, 'hardhat'],
  [/review/, 'glasses'],
  [/qa|test/, 'clipboard'],
  [/writer|doc/, 'pencil'],
  [/design|creative|art-director|ux/, 'beret'],
  [/market|growth|\bua\b/, 'megaphone'],
  [/product|business|analyst/, 'lightbulb'],
  [/data|scien/, 'chart'],
  [/guide/, 'book'],
  [/devops/, 'wrench'],
  [/engineer|backend|\bai\b/, 'headphones'],
]

const gearFor = (id: string, kind: string): Gear => {
  if (id === 'main') {
    return 'crown'
  }
  const name = kind.toLowerCase()

  return GEAR_RULES.find(([pattern]) => pattern.test(name))?.[1] ?? 'none'
}

const GEAR: Record<Exclude<Gear, 'none'>, string> = {
  crown: `<path d="M-7 -10 L-8 -16 L-3.5 -12.5 L0 -17 L3.5 -12.5 L8 -16 L7 -10 Z" fill="${GOLD}" stroke="#c9962e" stroke-width="0.8" stroke-linejoin="round"/>`,
  baton: `<path d="M-4 2.2 L0 4.2 L-4 6.2 Z M4 2.2 L0 4.2 L4 6.2 Z" fill="${PAPER}"/><path d="M15 -1 L24 -11" stroke="${PAPER}" stroke-width="1.4" stroke-linecap="round"/><circle cx="24.5" cy="-11.5" r="1.4" fill="${GOLD}"/>`,
  hardhat: `<path d="M-9 -10 a9 8 0 0 1 18 0 z" fill="${GOLD}"/><rect x="-11" y="-11" width="22" height="2.4" rx="1" fill="#e0a92f"/>`,
  glasses: `<g fill="none" stroke="${PAPER}" stroke-width="1.2"><rect x="-8.6" y="-6.8" width="7.4" height="7.6" rx="1.6"/><rect x="1.2" y="-6.8" width="7.4" height="7.6" rx="1.6"/><path d="M-1.2 -3 h2.4"/></g>`,
  magnifier: `<g stroke="${PAPER}" stroke-width="1.4"><circle cx="21" cy="-9" r="4.2" fill="${PAPER}" fill-opacity="0.18"/><path d="M18 -6 L15 -2" stroke-linecap="round"/></g>`,
  pencil: `<g transform="rotate(35 13 -14)"><rect x="11.5" y="-22" width="3" height="11" rx="0.6" fill="${GOLD}"/><rect x="11.5" y="-22" width="3" height="2" fill="#e8798a"/><path d="M11.5 -11 h3 l-1.5 3.2 z" fill="#f3d7b0"/></g>`,
  shield: `<g transform="translate(8 1.5) scale(0.62)"><path d="M0 -2 l5 1.6 v3.6 c0 2.6 -2.2 4.2 -5 5.2 c-2.8 -1 -5 -2.6 -5 -5.2 v-3.6 z" fill="#4f9d5b" stroke="#2f6b3a" stroke-width="1"/></g>`,
  headphones: `<path d="M-12 -5 a12 12 0 0 1 24 0" fill="none" stroke="#3a3836" stroke-width="2.2"/><rect x="-14.5" y="-8" width="4" height="6" rx="1.6" fill="#3a3836"/><rect x="10.5" y="-8" width="4" height="6" rx="1.6" fill="#3a3836"/>`,
  clipboard: `<g><rect x="-25" y="-8" width="9" height="12" rx="1.2" fill="${PAPER}"/><rect x="-22.5" y="-9.6" width="4" height="2.4" rx="0.8" fill="#8a837d"/><path d="M-23 -2 l1.6 1.8 l3.2 -3.6" fill="none" stroke="#4f9d5b" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></g>`,
  flag: `<path d="M-18 -2 V-17" stroke="${PAPER}" stroke-width="1.2" stroke-linecap="round"/><path d="M-18 -17 h-9 l2.2 3.2 l-2.2 3.2 h9 z" fill="#5b9bd5"/>`,
  beret: `<path d="M-9 -10 a9 4.5 0 0 1 18 0 z" fill="#6b4fa3"/><circle cx="1" cy="-14.8" r="1.2" fill="#6b4fa3"/><path d="M16 -1 L24 -12" stroke="#c9a37a" stroke-width="1.5" stroke-linecap="round"/><path d="M24 -12 l2 -3" stroke="#e8798a" stroke-width="2.6" stroke-linecap="round"/>`,
  megaphone: `<rect x="13" y="-6" width="3.5" height="6" fill="#8a6a1f"/><path d="M16 -6 l9 -5 v13 l-9 -5 z" fill="#e0a92f"/><path d="M27.5 -8 q2 3.5 0 7" fill="none" stroke="#f0a98f" stroke-width="1"/>`,
  lightbulb: `<circle cx="0" cy="-17" r="4" fill="#ffe08a"><animate attributeName="opacity" values="1;0.6;1" dur="2s" repeatCount="indefinite"/></circle><rect x="-2" y="-13.3" width="4" height="2.6" rx="0.8" fill="#9a8f88"/>`,
  chart: `<g><rect x="-26" y="-9" width="10" height="11" rx="1" fill="${PAPER}"/><path d="M-24 0 v-3 M-21 0 v-6 M-18 0 v-4.5" stroke="#d97757" stroke-width="2"/></g>`,
  book: `<g><rect x="-26" y="-8" width="10" height="12" rx="1" fill="#4a79a8"/><rect x="-24.8" y="-6.8" width="7.6" height="9.6" fill="${PAPER}" fill-opacity="0.9"/><path d="M-23.5 -4 h5 M-23.5 -1.5 h5" stroke="#4a79a8" stroke-width="0.8"/></g>`,
  wrench: `<path d="M16 -1 L24 -9" stroke="#c9d1d9" stroke-width="2" stroke-linecap="round"/><circle cx="24.5" cy="-9.5" r="3" fill="none" stroke="#c9d1d9" stroke-width="1.8"/>`,
}

// A repeating up and down (or any) shift of the shape it sits in.
const shift = (values: string, dur: string, begin = '0s'): string =>
  `<animateTransform attributeName="transform" type="translate" values="${values}" dur="${dur}" begin="${begin}" repeatCount="indefinite"/>`

const pulse = (values: string, dur: string, begin = '0s'): string =>
  `<animate attributeName="opacity" values="${values}" dur="${dur}" begin="${begin}" repeatCount="indefinite"/>`

const eyes = (state: CrewState): string => {
  if (state === 'done') {
    // Happy eyes: two little arches.
    return `<path d="M-7.5 -2 l2 -3.4 l2 3.4 M3.5 -2 l2 -3.4 l2 3.4" fill="none" stroke="${DARK}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>`
  }
  if (state === 'failed') {
    // Cross eyes.
    return `<path d="M-7 -6 l4 5 M-3 -6 l-4 5 M3 -6 l4 5 M7 -6 l-4 5" fill="none" stroke="${DARK}" stroke-width="1.5" stroke-linecap="round"/>`
  }
  if (state === 'idle') {
    // Sleepy eyes: thin slits.
    return `<rect x="-6.5" y="-2.6" width="3.4" height="1.6" fill="${DARK}"/><rect x="3.1" y="-2.6" width="3.4" height="1.6" fill="${DARK}"/>`
  }
  // A working agent blinks now and then.
  const blink = (axis: 'y' | 'height', open: number, shut: number): string =>
    `<animate attributeName="${axis}" values="${open};${open};${shut};${open}" keyTimes="0;0.9;0.95;1" dur="3.4s" repeatCount="indefinite"/>`

  return (
    `<rect x="-6.5" y="-6" width="3.4" height="5.4" fill="${DARK}">${blink('y', -6, -3.5)}${blink('height', 5.4, 0.6)}</rect>` +
    `<rect x="3.1" y="-6" width="3.4" height="5.4" fill="${DARK}">${blink('y', -6, -3.5)}${blink('height', 5.4, 0.6)}</rect>`
  )
}

// The small round mark at the top left: green dot, amber dot, check, or cross.
const badge = (state: CrewState, x: number, y: number): string => {
  if (state === 'working') {
    return `<circle cx="${x}" cy="${y}" r="3.2" fill="#5fd068"><animate attributeName="r" values="2.6;4;2.6" dur="1.2s" repeatCount="indefinite"/></circle>`
  }
  if (state === 'idle') {
    return `<circle cx="${x}" cy="${y}" r="3.2" fill="#e3b341"/>`
  }
  if (state === 'done') {
    return `<circle cx="${x}" cy="${y}" r="4.6" fill="#4f9d5b"/><path d="M${x - 2.2} ${y} l1.6 1.7 l2.9 -3.3" fill="none" stroke="#fff" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>`
  }

  return `<circle cx="${x}" cy="${y}" r="4.6" fill="#c8503f"/><path d="M${x - 1.8} ${y - 1.8} l3.6 3.6 M${x + 1.8} ${y - 1.8} l-3.6 3.6" fill="none" stroke="#fff" stroke-width="1.3" stroke-linecap="round"/>`
}

// What floats around the character: typing dots, sleep Zs, or a sparkle.
const extras = (state: CrewState): string => {
  if (state === 'working') {
    return (
      `<g fill="#f0a98f"><circle cx="14" cy="-18" r="1.3">${pulse('0.2;1;0.2', '1s')}</circle>` +
      `<circle cx="18" cy="-18" r="1.3">${pulse('0.2;1;0.2', '1s', '0.2s')}</circle>` +
      `<circle cx="22" cy="-18" r="1.3">${pulse('0.2;1;0.2', '1s', '0.4s')}</circle></g>`
    )
  }
  if (state === 'idle') {
    return (
      `<text x="15" y="-12" font-size="8" fill="#a59d97">z${pulse('0;1;0', '2.4s')}</text>` +
      `<text x="20" y="-18" font-size="10" fill="#a59d97">z${pulse('0;1;0', '2.4s', '1.2s')}</text>`
    )
  }
  if (state === 'done') {
    return `<path d="M17 -16 l1.1 3.2 l3.2 1.1 l-3.2 1.1 l-1.1 3.2 l-1.1 -3.2 l-3.2 -1.1 l3.2 -1.1 z" fill="${GOLD}">${pulse('0.3;1;0.3', '1.4s')}</path>`
  }

  return ''
}

// `hasBadge` false leaves out the status mark: the bench draws sleepers without one.
export const icon = (
  agent: CrewAgent,
  cx: number,
  cy: number,
  scale: number,
  hasBadge: boolean = true,
): string => {
  const { state } = agent
  const skin = SKIN[state]
  const isWorking = state === 'working'
  const gear = gearFor(agent.id, agent.kind)

  // A working agent bobs and walks on the spot; a waiting one breathes slowly.
  const bob = isWorking
    ? shift('0 0;0 -1.5;0 0', '0.5s')
    : state === 'idle'
      ? shift('0 0;0 1;0 0', '3s')
      : ''
  const legs = [-9, -4, 1, 6]
    .map(
      (x, i) =>
        `<rect x="${x}" y="6" width="3" height="5" fill="${skin.shade}">${
          isWorking ? shift('0 0;0 -2;0 0', '0.5s', i % 2 === 0 ? '0s' : '-0.25s') : ''
        }</rect>`,
    )
    .join('')
  // Typing hands while working, a wave when done, resting hands otherwise.
  const armY = state === 'done' ? -8 : -1
  const arm = (x: number, begin: string): string =>
    `<rect x="${x}" y="${armY}" width="4" height="5" fill="${skin.body}">${
      isWorking
        ? shift('0 0;0 -3;0 0', '0.4s', begin)
        : state === 'done'
          ? shift('0 0;0 -2;0 0', '0.8s', begin)
          : ''
    }</rect>`

  return (
    `<g transform="translate(${Math.round(cx * 10) / 10} ${Math.round((cy + 2 * scale) * 10) / 10}) scale(${scale})">` +
    `<g${state === 'failed' ? ' transform="rotate(-8)"' : ''}>` +
    `<g>${bob}${legs}${arm(-16, '0s')}${arm(12, '-0.2s')}` +
    `<rect x="-12" y="-10" width="24" height="16" rx="1.5" fill="${skin.body}"/>` +
    `<rect x="-12" y="3" width="24" height="3" fill="${skin.shade}"/>` +
    `${eyes(state)}${gear === 'none' ? '' : GEAR[gear]}${extras(state)}</g>` +
    `${hasBadge ? badge(state, -15, -15) : ''}</g></g>`
  )
}
