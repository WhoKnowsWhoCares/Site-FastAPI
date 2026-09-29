"use client";

import { Suspense, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth, type OAuthProvider } from "@/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { GitBranch, Globe, Send } from "lucide-react";

const PROVIDERS: { id: OAuthProvider; label: string; icon: typeof GitBranch }[] = [
  { id: "github", label: "Continue with GitHub", icon: GitBranch },
  { id: "google", label: "Continue with Google", icon: Globe },
  { id: "telegram", label: "Continue with Telegram", icon: Send },
];

function LoginForm() {
  const { user, isLoading } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const next = searchParams.get("next") ?? "/controlpanel";

  useEffect(() => {
    if (!isLoading && user) {
      router.replace(next.startsWith("/controlpanel") ? next : "/controlpanel");
    }
  }, [isLoading, user, next, router]);

  if (isLoading || user) {
    return (
      <p className="text-sm text-muted-foreground" role="status" aria-live="polite">
        Loading&hellip;
      </p>
    );
  }

  return (
    <div className="space-y-3">
      {PROVIDERS.map(({ id, label, icon: Icon }) => (
        <Button
          key={id}
          variant="outline"
          className="w-full justify-start"
          onClick={() => {
            const url = `/api/v1/auth/oauth/${id}?next=${encodeURIComponent(next)}`;
            window.location.href = url;
          }}
        >
          <Icon aria-hidden="true" />
          {label}
        </Button>
      ))}
    </div>
  );
}

export default function ControlPanelLoginPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4">
      <div className="w-full max-w-sm rounded-lg border bg-card p-8 shadow-sm">
        <h1 className="text-xl font-semibold tracking-tight">Control Panel</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Sign in with an administrator account to manage site content.
        </p>
        <div className="mt-6">
          <Suspense fallback={null}>
            <LoginForm />
          </Suspense>
        </div>
      </div>
    </main>
  );
}
