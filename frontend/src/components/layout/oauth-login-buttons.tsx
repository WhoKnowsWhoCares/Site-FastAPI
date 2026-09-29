"use client";

import { oauthStartUrl, type OAuthProvider } from "@/lib/auth";

const PROVIDER_LABELS: Record<OAuthProvider, string> = {
  github: "GitHub",
  google: "Google",
  telegram: "Telegram",
};

/**
 * OAuth entry points. Each button redirects the browser straight to the
 * backend route that starts the provider flow (/auth/oauth/{provider}),
 * so no client-side OAuth logic is needed here.
 */
export function OAuthLoginButtons() {
  return (
    <div
      role="group"
      aria-label="Log in with OAuth provider"
      className="flex items-center gap-1.5"
    >
      {(["github", "google", "telegram"] as const).map((provider) => (
        <a
          key={provider}
          href={oauthStartUrl(provider)}
          className="rounded-md border border-border px-2.5 py-1.5 text-xs font-medium text-foreground transition-colors hover:bg-accent hover:text-accent-foreground"
        >
          {PROVIDER_LABELS[provider]}
        </a>
      ))}
    </div>
  );
}
