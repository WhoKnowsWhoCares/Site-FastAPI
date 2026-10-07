import type { Metadata } from "next";
import Image from "next/image";
import {
  ARCHITECTURE,
  MEDIA_ITEMS,
  MORNING_ROUTINE,
  OVERVIEW,
  STACK,
} from "@/components/ihome/ihome-data";
import { MediaGrid } from "@/components/ihome/media-grid";

export const metadata: Metadata = { title: "iHome" };

export default function IHomePage() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-12">
      <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">iHome</h1>
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

      {/* Key facts */}
      {/* <dl className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {OVERVIEW.stats.map((s) => (
          <div
            key={s.label}
            className="rounded-lg border border-border bg-card p-3"
          >
            <dt className="text-xs text-muted-foreground">{s.label}</dt>
            <dd className="mt-0.5 text-sm font-semibold">{s.value}</dd>
          </div>
        ))}
      </dl> */}

      {/* Architecture diagram (theme-aware) */}
      <section aria-labelledby="architecture-title" className="mt-12">
        <h2
          id="architecture-title"
          className="text-xl font-semibold tracking-tight"
        >
          Architecture
        </h2>
        <figure className="mt-4 overflow-hidden rounded-lg border border-border bg-card p-4">
          {/* Theme-aware: the site toggles dark mode via a class (next-themes), so both
              variants are rendered and switched with Tailwind's dark: variant. */}
          <Image
            src={ARCHITECTURE.dark.src}
            alt={ARCHITECTURE.caption}
            width={ARCHITECTURE.dark.width}
            height={ARCHITECTURE.dark.height}
            sizes="(max-width: 1024px) 100vw, 924px"
            className="hidden h-auto w-full dark:block"
          />
          <Image
            src={ARCHITECTURE.light.src}
            alt={ARCHITECTURE.caption}
            width={ARCHITECTURE.light.width}
            height={ARCHITECTURE.light.height}
            sizes="(max-width: 1024px) 100vw, 924px"
            className="h-auto w-full dark:hidden"
          />
          <figcaption className="mt-3 text-xs leading-5 text-muted-foreground">
            {ARCHITECTURE.caption}
          </figcaption>
        </figure>
      </section>

      {/* Morning automation chain */}
      <section aria-labelledby="automation-title" className="mt-12">
        <h2
          id="automation-title"
          className="text-xl font-semibold tracking-tight"
        >
          Morning automation
        </h2>
        <p className="mt-2 text-sm text-muted-foreground">
          The phone alarm starts a chain of scripts that gets the day going.
        </p>
        <ol className="mt-4 border-l-2 border-border pl-6">
          {MORNING_ROUTINE.map((step, i) => (
            <li key={i} className="relative pb-4 last:pb-0">
              <span
                aria-hidden="true"
                className="absolute -left-[31px] top-1 h-2.5 w-2.5 rounded-full bg-accent"
              />
              <span className="mr-2 font-mono text-xs text-muted-foreground">
                {step.time}
              </span>
              <span className="text-sm">{step.text}</span>
            </li>
          ))}
        </ol>
      </section>

      {/* Interfaces & infrastructure gallery */}
      <section aria-labelledby="media-title" className="mt-12">
        <h2 id="media-title" className="text-xl font-semibold tracking-tight">
          Dashboards &amp; hardware
        </h2>
        <MediaGrid items={MEDIA_ITEMS} />
      </section>
    </div>
  );
}
