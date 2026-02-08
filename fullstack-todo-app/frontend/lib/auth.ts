/**
 * Token storage utilities.
 *
 * Access tokens are stored in memory only (not localStorage).
 * Refresh tokens are handled via HttpOnly cookies by the backend.
 */

// In-memory token storage (lost on page refresh)
let accessToken: string | null = null;

export function getAccessToken(): string | null {
  return accessToken;
}

export function setAccessToken(token: string | null): void {
  accessToken = token;
}

export function clearAccessToken(): void {
  accessToken = null;
}

export function isAuthenticated(): boolean {
  return accessToken !== null;
}
