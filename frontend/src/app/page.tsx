import Image from "next/image";
import Link from "next/link";
import {
  HomeIcon,
  LineChart,
  Palette,
  UserRound,
  ArrowRight,
} from "lucide-react";
import { SectionCard } from "@/components/layout/section-card";
import { SUMMARY } from "@/components/about/about-data";

const SKILL_BADGES = [
  "Python",
  "PyTorch",
  "SQL",
  "LLM",
  "FastAPI",
  "Docker",
  "Home Assistant",
  "AI Art",
  // from About Me → Skills
  "scikit-learn",
  "pandas",
  "LightGBM",
  "Optuna",
  "Forecasting",
  "NLP",
  "A/B testing",
  "ClickHouse",
  "YTsaurus",
  "Git",
  "Linux",
] as const;

const SECTIONS = [
  {
    href: "/aboutme",
    title: "About Me",
    description:
      "Senior Data Scientist. ML products end-to-end — from architecture to production and business impact.",
    icon: UserRound,
  },
  {
    href: "/ihome",
    title: "iHome",
    description:
      "Smart home on Home Assistant: Raspberry Pi 4 server, Zigbee/WiFi/ESPHome sensors, automations and dashboards.",
    icon: HomeIcon,
  },
  {
    href: "/trade4me",
    title: "Trade4Me",
    description: "Trading bot: strategy, statistics and current status.",
    icon: LineChart,
  },
  {
    href: "/sdart",
    title: "AI Art",
    description: "Image gallery generated and edited with neural networks.",
    icon: Palette,
  },
] as const;

export default function HomePage() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-12 sm:py-16">
      {/* Hero */}
      <section
        aria-labelledby="hero-title"
        className="flex flex-col-reverse items-start gap-8 sm:flex-row sm:items-center sm:justify-between"
      >
        <div className="max-w-2xl">
          <p className="font-mono text-sm text-muted-foreground">
            Hi, I&apos;m
          </p>
          <h1
            id="hero-title"
            className="mt-1 text-3xl font-bold tracking-tight sm:text-4xl"
          >
            Alexander Frantsev
          </h1>
          <p className="mt-3 text-base text-foreground/90 sm:text-lg">
            Senior Data Scientist. I own ML products end-to-end — from
            architecture and modeling to production, monitoring and business
            impact.
          </p>
          <p className="mt-2 max-w-xl text-sm leading-6 text-muted-foreground sm:text-base">
            On the side I automate my home, build trading tools and create art
            with neural networks.
          </p>

          <ul aria-label="Tech stack" className="mt-5 flex flex-wrap gap-2">
            {SKILL_BADGES.map((badge) => (
              <li
                key={badge}
                className="rounded-full border border-primary/40 bg-primary/10 px-3 py-1 font-mono text-xs text-primary dark:text-foreground/90"
              >
                {badge}
              </li>
            ))}
          </ul>

          {/* Experience stats */}
          <dl className="mt-6 grid max-w-md grid-cols-2 gap-3">
            {SUMMARY.stats.map((s) => (
              <div
                key={s.label}
                className="rounded-lg border border-border bg-card p-3"
              >
                <dt className="text-xs text-muted-foreground">{s.label}</dt>
                <dd className="mt-0.5 text-base font-semibold">{s.years}</dd>
              </div>
            ))}
          </dl>

          <div className="mt-6 flex flex-wrap items-center gap-3">
            <Link
              href="/aboutme"
              className="inline-flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-opacity hover:opacity-90"
            >
              About me
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
            <a
              href="https://github.com/WhoKnowsWhoCares"
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-md border border-border px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground"
            >
              GitHub
            </a>
          </div>
        </div>

        <div className="shrink-0">
          <div className="rounded-full bg-gradient-to-br from-primary via-accent to-accent-foreground p-[3px]">
            <Image
              src="/alexander.jpg"
              alt="Portrait of Alexander Frantsev"
              width={160}
              height={160}
              priority
              className="h-32 w-32 rounded-full object-cover sm:h-40 sm:w-40"
            />
          </div>
        </div>
      </section>

      {/* Site map */}
      <section aria-labelledby="sitemap-title" className="mt-14">
        <h2 id="sitemap-title" className="text-xl font-semibold tracking-tight">
          Sections
        </h2>
        <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {SECTIONS.map((section) => (
            <SectionCard key={section.href} {...section} />
          ))}
        </div>
      </section>
    </div>
  );
}
