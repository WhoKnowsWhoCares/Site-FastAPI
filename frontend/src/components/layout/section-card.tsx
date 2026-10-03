import Link from "next/link";
import { ArrowRight, type LucideIcon } from "lucide-react";

interface SectionCardProps {
  href: string;
  title: string;
  description: string;
  /** Lucide icon shown in a tinted square. */
  icon?: LucideIcon;
  /** Small neutral badge, e.g. section status. */
  badge?: string;
}

/** Card used on the Home page sitemap to link into each section. */
export function SectionCard({
  href,
  title,
  description,
  icon: Icon,
  badge,
}: SectionCardProps) {
  return (
    <Link
      href={href}
      className="group flex flex-col rounded-lg border border-border bg-card p-5 text-card-foreground shadow-sm transition-all hover:-translate-y-0.5 hover:border-primary/40 hover:shadow-md"
    >
      <div className="flex items-center justify-between gap-2">
        {Icon && (
          <span
            aria-hidden="true"
            className="flex h-9 w-9 items-center justify-center rounded-md bg-primary/15 text-primary"
          >
            <Icon className="h-5 w-5" />
          </span>
        )}
        {badge && (
          <span className="rounded-full border border-border px-2 py-0.5 text-xs text-muted-foreground">
            {badge}
          </span>
        )}
      </div>
      <h2 className="mt-3 text-base font-semibold">{title}</h2>
      <p className="mt-1.5 text-sm text-muted-foreground">{description}</p>
      <span
        aria-hidden="true"
        className="mt-4 inline-flex items-center gap-1 text-sm font-medium text-primary opacity-0 transition-opacity group-hover:opacity-100"
      >
        Open
        <ArrowRight className="h-4 w-4" />
      </span>
    </Link>
  );
}
