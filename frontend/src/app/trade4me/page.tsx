import type { Metadata } from "next";
import Image from "next/image";
import {
  LEVELS,
  NEWS_PARSER,
  OVERVIEW,
  STACK,
} from "@/components/trade4me/trade4me-data";

export const metadata: Metadata = { title: "Trade4Me" };

export default function Trade4MePage() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-12">
      <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
        {OVERVIEW.headline}
      </h1>
      <p className="mt-2 max-w-3xl text-base leading-7 text-foreground/90">
        {OVERVIEW.blurb}
      </p>

      {/* Tech stack badges */}
      <ul aria-label="Tech stack" className="mt-5 flex flex-wrap gap-2">
        {STACK.map((badge) => (
          <li
            key={badge}
            className="rounded-full border border-primary/40 bg-primary/10 px-3 py-1 font-mono text-xs text-primary dark:text-foreground/90"
          >
            {badge}
          </li>
        ))}
      </ul>

      {/* Three-level approach */}
      <section aria-labelledby="levels-title" className="mt-12">
        <h2
          id="levels-title"
          className="text-xl font-semibold tracking-tight"
        >
          Three-level approach
        </h2>
        <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-3">
          {LEVELS.map((level) => (
            <div
              key={level.title}
              className="rounded-lg border border-border bg-card p-4"
            >
              <h3 className="text-sm font-semibold">{level.title}</h3>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                {level.text}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* News Parser */}
      <section aria-labelledby="newsparser-title" className="mt-12">
        <div className="flex flex-wrap items-center gap-3">
          <h2
            id="newsparser-title"
            className="text-xl font-semibold tracking-tight"
          >
            {NEWS_PARSER.title}
          </h2>
          <span className="rounded-full border border-border bg-card px-2.5 py-0.5 font-mono text-xs text-muted-foreground">
            {NEWS_PARSER.status}
          </span>
        </div>
        <p className="mt-3 max-w-3xl text-sm leading-6 text-foreground/90">
          {NEWS_PARSER.text}
        </p>

        {/* Architecture diagram (theme-aware, same pattern as iHome) */}
        <figure className="mt-4 overflow-hidden rounded-lg border border-border bg-card p-4">
          <Image
            src={NEWS_PARSER.diagram.dark.src}
            alt={NEWS_PARSER.diagram.caption}
            width={NEWS_PARSER.diagram.dark.width}
            height={NEWS_PARSER.diagram.dark.height}
            sizes="(max-width: 1024px) 100vw, 924px"
            className="hidden h-auto w-full dark:block"
          />
          <Image
            src={NEWS_PARSER.diagram.light.src}
            alt={NEWS_PARSER.diagram.caption}
            width={NEWS_PARSER.diagram.light.width}
            height={NEWS_PARSER.diagram.light.height}
            sizes="(max-width: 1024px) 100vw, 924px"
            className="h-auto w-full dark:hidden"
          />
          <figcaption className="mt-3 text-xs leading-5 text-muted-foreground">
            {NEWS_PARSER.diagram.caption}
          </figcaption>
        </figure>
      </section>
    </div>
  );
}
