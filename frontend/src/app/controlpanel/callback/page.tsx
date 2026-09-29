"use client";

import { Suspense } from "react";
import OAuthCallbackInner from "./oauth-callback-inner";

export default function OAuthCallbackPage() {
  return (
    <Suspense
      fallback={
        <main
          className="flex min-h-screen items-center justify-center p-8"
          role="status"
          aria-live="polite"
        >
          <p className="text-sm text-muted-foreground">Completing sign-in&hellip;</p>
        </main>
      }
    >
      <OAuthCallbackInner />
    </Suspense>
  );
}
