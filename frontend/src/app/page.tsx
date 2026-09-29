import { SectionCard } from "@/components/layout/section-card";

const SECTIONS = [
  {
    href: "/aboutme",
    title: "About Me",
    description: "Who I am, my stack and experience as an analyst-developer.",
  },
  {
    href: "/ihome",
    title: "iHome",
    description: "Smart home dashboard: sensors, automations and previews.",
  },
  {
    href: "/trade4me",
    title: "Trade4Me",
    description: "Trading bot: strategy, statistics and current status.",
  },
  {
    href: "/sdart",
    title: "SD Art",
    description: "Image gallery generated with Stable Diffusion.",
  },
] as const;

export default function HomePage() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-12 sm:py-16">
      {/* Hero */}
      <section aria-labelledby="hero-title">
        <h1
          id="hero-title"
          className="text-3xl font-bold tracking-tight sm:text-4xl"
        >
          Hi, I&apos;m Alexander
        </h1>
        <p className="mt-3 max-w-2xl text-base text-muted-foreground sm:text-lg">
          Analyst-developer. I build tools for myself and share what I learn —
          from smart home automations to trading bots and generated art.
        </p>
      </section>

      {/* Site map */}
      <section aria-labelledby="sitemap-title" className="mt-12">
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
