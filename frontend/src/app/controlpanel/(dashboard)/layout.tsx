"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { AdminSidebar } from "@/components/admin/admin-sidebar";

/**
 * Protected layout for the ControlPanel. The middleware already gates on the
 * session cookie; this re-checks the session via the backend and guards the
 * role, so a stale/expired cookie never renders admin UI.
 */
export default function ControlPanelLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !user) {
      const next = encodeURIComponent(
        window.location.pathname + window.location.search
      );
      router.replace(`/controlpanel/login?next=${next}`);
    }
  }, [isLoading, user, router]);

  if (isLoading || !user) {
    return (
      <div
        className="flex min-h-screen items-center justify-center"
        role="status"
        aria-live="polite"
      >
        <p className="text-sm text-muted-foreground">Loading&hellip;</p>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen">
      <AdminSidebar user={user} />
      <div className="flex-1 overflow-x-hidden">
        <main className="mx-auto w-full max-w-6xl p-6 lg:p-8">{children}</main>
      </div>
    </div>
  );
}
