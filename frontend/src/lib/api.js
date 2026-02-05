/**
 * API base URL: use relative path so Vite proxy works in dev.
 * In production, set VITE_API_URL or use same origin.
 */
export const API_BASE =
  typeof import.meta !== "undefined" && import.meta.env?.VITE_API_URL
    ? import.meta.env.VITE_API_URL
    : ""
