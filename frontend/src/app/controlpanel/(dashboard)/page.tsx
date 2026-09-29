"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useAuth } from "@/hooks/useAuth";
import { CONTENT_SECTION_LABELS } from "@/lib/auth";
import { contentSections, type ContentStats } from "@/types/content";
import { FileText, PlusCircle, Eye } from "lucide-react";

function useContentStats() {
  return useQuery({
    queryKey: ["admin", "stats"],
    queryFn: () => api<ContentStats>("/api/v1/admin/content/stats"),
  });
}

export default function ControlPanelDashboardPage() {
  const { user } = useAuth();
  const statsQuery = useContentStats();
  const stats = statsQuery.data;

  const statCards = [
    {
      label: "Total content",
      value: stats?.total,
      icon: FileText,
    },
    {
      label: "Published",
      value: stats?.published,
      icon: Eye,
    },
    {
      label: "Drafts",
      value: stats?.drafts,
      icon: PlusCircle,
    },
  ];

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Welcome back{user?.name ? `, ${user.name}` : ""}. Here is an overview
          of your content.
        </p>
      </header>

      {statsQuery.isError ? (
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-destructive" role="alert">
              Failed to load stats: {(statsQuery.error as Error).message}
            </p>
            <Button
              variant="outline"
              size="sm"
              className="mt-3"
              onClick={() => statsQuery.refetch()}
            >
              Retry
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div
          className="grid grid-cols-1 gap-4 sm:grid-cols-3"
          aria-busy={statsQuery.isLoading}
        >
          {statCards.map(({ label, value, icon: Icon }) => (
            <Card key={label}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardDescription>{label}</CardDescription>
                <Icon className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
              </CardHeader>
              <CardContent>
                {statsQuery.isLoading ? (
                  <div className="h-8 w-12 animate-pulse rounded bg-muted" />
                ) : (
                  <p className="text-2xl font-semibold tabular-nums">{value}</p>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Content by section</CardTitle>
          <CardDescription>Items in each site section</CardDescription>
        </CardHeader>
        <CardContent>
          {statsQuery.isLoading ? (
            <div className="space-y-2" aria-hidden="true">
              {contentSections.map((s) => (
                <div key={s} className="h-5 w-full animate-pulse rounded bg-muted" />
              ))}
            </div>
          ) : (
            <dl className="space-y-2">
              {contentSections.map((section) => (
                <div
                  key={section}
                  className="flex items-center justify-between border-b pb-2 last:border-b-0 last:pb-0"
                >
                  <dt className="text-sm text-muted-foreground">
                    {CONTENT_SECTION_LABELS[section]}
                  </dt>
                  <dd className="text-sm font-medium tabular-nums">
                    {stats?.bySection?.[section] ?? 0}
                  </dd>
                </div>
              ))}
            </dl>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Quick actions</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-3">
          <Button asChild>
            <Link href="/controlpanel/content?new=1">
              <PlusCircle aria-hidden="true" />
              New content item
            </Link>
          </Button>
          <Button asChild variant="outline">
            <Link href="/controlpanel/content">
              <FileText aria-hidden="true" />
              Manage content
            </Link>
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
