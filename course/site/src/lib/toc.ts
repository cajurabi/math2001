// Anchor ids for course components that appear in the "On this page" sidebar
// (see src/routeData.ts, which builds the sidebar from each page's MDX source).

export function explainerSlug(id: string): string {
  return `explainer-${id.replace(/[^A-Za-z0-9]+/g, '-')}`
}

export const STOP_SLUG = 'stopping-point'
