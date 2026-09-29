"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

const CONTROL_PANEL_PATH = "/controlpanel";

/**
 * OAuth callback landing page. The backend handles the provider handshake and
 * sets the httpOnly session cookie, then redirects here. We just revalidate
 * the session and forward the user to their intended destination.
 */
export default function OAuthCallbackInner() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [error, setError] = useState<string | null>(null);
  const attemptedRef = useRef(false);

  useEffect(() => {
    if (attemptedRef.current) return;
    attemptedRef.current = true;

    const oauthError =
      searchParams.get("error") ?? searchParams.get("error_description");
    const next = searchParams.get("next") ?? CONTROL_PANEL_PATH;

    if (oauthError) {
      setError(oauthError);
      return;
    }

    // Session cookie was set by the backend callback; verify it took effect,
    // then revalidate server state and forward the user to their destination.
    fetch("/api/v1/auth/me", { credentials: "include" })
      .then((res) => {
        if (!res.ok) throw new Error("Session was not established");
        return res.json();
      })
      .then(() => router.replace(next))
      .catch((err: Error) => {
        setError(err.message);
      });
  }, [router, searchParams]);

  if (error) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center gap-2 p-8">
        <h1 className="text-lg font-semibold">Sign-in failed</h1>
        <p className="text-sm text-muted-foreground">{error}</p>
        <a
          href="/controlpanel/login"
          className="text-sm font-medium underline underline-offset-4"
        >
          Back to sign in
        </a>
      </main>
    );
  }

  return (
    <main
      className="flex min-h-screen flex-col items-center justify-center gap-2 p-8"
      role="status"
      aria-live="polite"
    >
      <p className="text-sm text-muted-foreground">Completing sign-in&hellip;</p>
    </main>
  );
}
