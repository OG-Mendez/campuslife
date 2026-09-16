// Single source of truth for the backend base URL.
// Docker build sets VITE_API_BASE_URL=/api (relative, proxied by nginx).
// Falls back to the live Render backend for the Vercel production build,
// where no such env var is set.
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || `${API_BASE_URL}`;
