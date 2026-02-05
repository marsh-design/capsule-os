/**
 * Map color names to hex for consistent palette swatches.
 * Covers common capsule palette names.
 */
export const COLOR_HEX = {
  black: "#1a1a1a",
  white: "#fafafa",
  navy: "#1e3a5f",
  gray: "#6b7280",
  cream: "#fff8e7",
  camel: "#c19a6b",
  burgundy: "#800020",
  beige: "#d4b896",
  tan: "#d2b48c",
  khaki: "#c3b091",
  sage: "#9caa7c",
  denim: "#6f8faf",
  red: "#b91c1c",
  nude: "#e8d5c4",
  brown: "#78350f",
  coral: "#e07850",
  yellow: "#facc15",
}

export function getColorHex(name) {
  if (!name || typeof name !== "string") return "#9ca3af"
  const key = name.toLowerCase().trim()
  return COLOR_HEX[key] || `var(--tw-gray-400, #9ca3af)`
}
