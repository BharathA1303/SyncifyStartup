/**
 * auth.js — Syncify Auth Module
 * Handles JWT storage, auth state, and page protection.
 * Import this on every page that needs auth.
 */

const AUTH_KEY  = 'syncify_jwt';
const USER_KEY  = 'syncify_user';
const API_BASE  = 'http://localhost:5000';

// ── Token management ──────────────────────────────
export function getToken()    { return localStorage.getItem(AUTH_KEY); }
export function getUser()     {
  try { return JSON.parse(localStorage.getItem(USER_KEY)); }
  catch { return null; }
}
export function isLoggedIn()  { return !!getToken(); }

export function saveAuth(jwt, user) {
  localStorage.setItem(AUTH_KEY, jwt);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function clearAuth() {
  localStorage.removeItem(AUTH_KEY);
  localStorage.removeItem(USER_KEY);
}

// ── Page guards ───────────────────────────────────
/** Call on protected pages. Redirects to /login if not authenticated. */
export function requireAuth(redirectTo = '/login') {
  if (!isLoggedIn()) {
    window.location.href = redirectTo;
    return false;
  }
  return true;
}

/** Call on auth pages (login/signup). Redirects to dashboard if already logged in. */
export function redirectIfLoggedIn(redirectTo = '/dashboard') {
  if (isLoggedIn()) {
    window.location.href = redirectTo;
    return true;
  }
  return false;
}

// ── API call with auth header ─────────────────────
export async function authFetch(path, options = {}) {
  const token = getToken();
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  });

  // Auto-logout on 401
  if (res.status === 401) {
    clearAuth();
    window.location.href = '/login';
    return null;
  }

  return res;
}

// ── Logout ────────────────────────────────────────
export async function logout() {
  clearAuth();
  window.location.href = '/login';
}

// ── Get fresh /api/auth/me ─────────────────────────
export async function fetchCurrentUser() {
  const res = await authFetch('/api/auth/me');
  if (!res || !res.ok) return null;
  const data = await res.json();
  return data.data || null;
}