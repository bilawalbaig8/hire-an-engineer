export type BoardTask = {
  id: string
  title: string
  size: string
  stage: string
  status: string
  round: string
  slot: string
  needs: string
  note: string
}

export type Board = {
  /** A TASKS.md or PROJECT_STATE.md was found in the session's folder. */
  isFound: boolean
  project: string
  tasks: BoardTask[]
  /** Key/value pairs of the PROJECT_STATE.md "Authorization" block. */
  auth: Record<string, string>
  /** One line from PROJECT_STATE.md about what is happening now, if any. */
  focus: string
  /** Where the board came from, e.g. "TASKS.md". */
  source: string
}

declare module 'claude-code' {
  interface PluginState {
    'hire-an-engineer-board': { board: Shaped<Board> }
  }
}
