import Link from "next/link";

interface SectionCardProps {
  href: string;
  title: string;
  description: string;
  /** Small neutral badge, e.g. section status. */
  badge?: string;
}

/** Card used on the Home page sitemap to link into each section. */
export function SectionCard({
  href,
  title,
  description,
  badge,
}: SectionCardProps) {
  return (
    <Link
      href={href}
      className="group flex flex-col rounded-lg border border-border bg-card p-5 text-card-foreground transition-colors hover:border-foreground/20 hover:bg-accent"
    >
      <div className="flex items-center justify-between gap-2">
        <h2 className="text-base font-semibold">{title}</h2>
        {badge && (
          <span className="rounded-full border border-border px-2 py-0.5 text-xs text-muted-foreground">
            {badge}
          </span>
        )}
      </div>
      <p className="mt-2 text-sm text-muted-foreground">{description}</p>
      <span
        aria-hidden="true"
        className="mt-4 text-sm font-medium text-foreground opacity-0 transition-opacity group-hover:opacity-100"
      >
        Open →
      </span>
    </Link>
  );
}
