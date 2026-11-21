// Turns a model (an alias, a full id, or 'inherit') and an effort into the short tag
// shown under each character: "Haiku · low", "Opus 5.5 · high", "inherit".

export type ModelFamily = 'haiku' | 'sonnet' | 'opus' | 'fable'

const FAMILIES: readonly ModelFamily[] = ['haiku', 'sonnet', 'opus', 'fable']

const title = (word: string): string => word.charAt(0).toUpperCase() + word.slice(1)

// The model's family, from an alias or a full id, or undefined for any other model.
export const modelFamily = (model: string): ModelFamily | undefined => {
  const lower = model.toLowerCase()

  return FAMILIES.find(family => lower.includes(family))
}

// "claude-opus-5-5" → "Opus 5.5", "haiku" → "Haiku", "claude-3-5-sonnet-20241022" →
// "Sonnet 3.5", '' or "inherit" → "inherit". Any other model is shown as given, cut short.
export const modelName = (model: string): string => {
  const raw = model.trim()
  if (raw === '' || raw.toLowerCase() === 'inherit') {
    return 'inherit'
  }
  const lower = raw
    .toLowerCase()
    .replace(/\[[^\]]*\]/g, '') // a context tag such as [1m]
    .replace(/^.*anthropic[./]/, '') // a provider prefix such as us.anthropic.
    .replace(/[@:].*$/, '') // a version suffix such as @20250805 or -v1:0
    .replace(/-v\d+$/, '')
    .replace(/-\d{8}$/, '') // a date suffix
  if (lower === 'opusplan') {
    return 'Opus plan'
  }
  const family = modelFamily(lower)
  if (family === undefined) {
    return raw.length > 16 ? `${raw.slice(0, 15)}…` : raw
  }
  // A version after the family (claude-opus-5-5), else before it (claude-3-5-sonnet).
  const after = new RegExp(`${family}-(\\d+)(?:-(\\d{1,2}))?(?!\\d)`).exec(lower)
  const before = new RegExp(`(\\d+)(?:-(\\d{1,2}))?-${family}`).exec(lower)
  const found = after ?? before
  const version =
    found === null ? '' : found[2] !== undefined ? ` ${found[1]}.${found[2]}` : ` ${found[1]}`

  return `${title(family)}${version}`
}

// An effort level as given, or an integer budget as a number; '' for none.
export const effortText = (effort: unknown): string =>
  typeof effort === 'string' ? effort.trim() : typeof effort === 'number' ? String(effort) : ''

// The tag: the model's name, then the effort when there is one.
export const modelTag = (model: string, effort: string): string =>
  effort === '' ? modelName(model) : `${modelName(model)} · ${effort}`

// The accent drawn in the picture, which sits on a dark panel on every theme.
export const MODEL_HEX: Record<ModelFamily, string> = {
  haiku: '#5cc87a',
  sonnet: '#5aa2f2',
  opus: '#b48af5',
  fable: '#e5b84a',
}
export const OTHER_HEX = '#8a837d'

// The accent in the terminal: theme keys, so it follows a light or a dark theme.
export const MODEL_THEME: Record<ModelFamily, string> = {
  haiku: 'success',
  sonnet: 'suggestion',
  opus: 'merged',
  fable: 'warning',
}
