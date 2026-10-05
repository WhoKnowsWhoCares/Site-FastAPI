import { API_URL } from "@/lib/api";

export type OAuthProvider = "github" | "google" | "telegram";

export const OAUTH_PROVIDERS: readonly OAuthProvider[] = [
  "github",
  "google",
  "telegram",
];

/**
 * URL that starts the OAuth flow for a provider on the backend.
 * The backend handles the provider round-trip and redirects back.
 */
export function oauthStartUrl(provider: OAuthProvider): string {
  return `${API_URL}/auth/oauth/${provider}`;
}

/** Name of the httpOnly cookie the backend sets after a successful OAuth login. */
export const SESSION_COOKIE = "cp_session";

/** Human-readable labels for the content sections (used by the admin UI). */
export const CONTENT_SECTION_LABELS: Record<string, string> = {
  home: "Home",
  aboutme: "About Me",
  ihome: "iHome",
  trade4me: "Trade4Me",
  sdart: "AI Art",
};
