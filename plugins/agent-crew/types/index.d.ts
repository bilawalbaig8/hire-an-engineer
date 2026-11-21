// The values the agent-crew mod keeps in $.state.

export type CrewState = 'working' | 'idle' | 'done' | 'failed'

// One Claude icon on the floor: the main agent or a helper.
export type CrewAgent = {
  id: string // 'main' for the main loop, else the id the engine gives the helper
  label: string // the short name shown under the icon
  kind: string // the agent type, for example Explore or general-purpose
  state: CrewState
  verb: string // what it does now, for example "edits"
  target: string // what it does it to, for example a file name
  file: string // full path of the file it works on, or '' for none
  parentId: string // the agent that started it, '' for the main agent
  steps: number // how many tool calls it made
  endedAt: number // when it finished (ms since 1970), 0 while it has not finished
  model: string // the model as given: an alias (haiku), a full id, 'inherit', or '' while unknown
  effort: string // the effort level (low ... max) or a budget, '' while unknown
}

// One file card on the shelf.
export type CrewFile = {
  path: string
  name: string
  touches: number
  lastVerb: string
  lastBy: string
}

// One line of the activity list.
export type CrewLog = { who: string; text: string }

// One agent type the session can call, as the engine offered it to the model.
export type CrewRoster = {
  name: string // the agent type, for example architect
  source: string // where its definition came from, for example built-in
  hint: string // its short "when to use" line
}

declare module 'claude-code' {
  interface PluginState {
    'agent-crew': {
      agents: Shaped<CrewAgent[]>
      files: Shaped<CrewFile[]>
      log: Shaped<CrewLog[]>
      roster: Shaped<CrewRoster[]>
      isBenchOpen: Shaped<boolean>
      zoom: Shaped<number>
    }
  }
}
