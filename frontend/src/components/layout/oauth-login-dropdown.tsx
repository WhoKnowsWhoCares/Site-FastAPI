"use client";

import { oauthStartUrl, type OAuthProvider } from "@/lib/auth";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { ChevronDown, LogIn } from "lucide-react";

const PROVIDER_LABELS: Record<OAuthProvider, string> = {
  github: "GitHub",
  google: "Google",
  telegram: "Telegram",
};

/**
 * OAuth entry points collapsed into a single "Login" dropdown.
 * Each item redirects the browser straight to the backend route
 * that starts the provider flow (/auth/oauth/{provider}).
 */
export function OAuthLoginDropdown() {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger
        aria-label="Log in with OAuth provider"
        className="inline-flex items-center gap-1 rounded-md border border-border px-2.5 py-1.5 text-xs font-medium text-foreground transition-colors hover:bg-accent hover:text-accent-foreground focus:outline-none focus-visible:ring-2 focus-visible:ring-ring data-[state=open]:bg-accent data-[state=open]:text-accent-foreground"
      >
        <LogIn className="h-3.5 w-3.5" aria-hidden="true" />
        Login
        <ChevronDown
          className="h-3 w-3 opacity-60"
          aria-hidden="true"
        />
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="min-w-[10rem]">
        {(["github", "google", "telegram"] as const).map((provider) => (
          <DropdownMenuItem key={provider} asChild>
            <a href={oauthStartUrl(provider)}>{PROVIDER_LABELS[provider]}</a>
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
