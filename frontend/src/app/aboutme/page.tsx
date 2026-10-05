import type { Metadata } from "next";
import { Download, Mail, GraduationCap, Sparkles } from "lucide-react";
import {
  SUMMARY,
  EDUCATION,
  SKILLS,
  INTERESTS,
  EXPERIENCE,
  ACHIEVEMENTS,
  CONTACTS,
  CV_DOWNLOAD_URL,
} from "@/components/about/about-data";
import { PortraitCarousel } from "@/components/about/portrait-carousel";

export const metadata: Metadata = { title: "About Me" };

export default function AboutMePage() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-12">
      {/* ============ Summary ============ */}
      <section aria-labelledby="about-summary" id="summary">
        <div className="flex flex-col-reverse gap-8 sm:flex-row sm:items-start sm:justify-between">
          <div className="max-w-2xl">
            <h1
              id="about-summary"
              className="text-2xl font-bold tracking-tight sm:text-3xl"
            >
              Alexander Frantsev
            </h1>
            <p className="mt-1 font-mono text-sm text-muted-foreground">
              {SUMMARY.headline}
            </p>
            <p className="mt-4 text-base leading-7 text-foreground/90">
              {SUMMARY.blurb}
            </p>

            <dl className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-3">
              {SUMMARY.stats.map((s) => (
                <div
                  key={s.label}
                  className="rounded-lg border border-border bg-card p-4"
                >
                  <dt className="text-xs text-muted-foreground">{s.label}</dt>
                  <dd className="mt-1 text-lg font-semibold">{s.years}</dd>
                </div>
              ))}
            </dl>

            <a
              href={CV_DOWNLOAD_URL}
              download="Alexander_Frantsev_CV.pdf"
              className="mt-6 inline-flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-opacity hover:opacity-90"
            >
              <Download className="h-4 w-4" aria-hidden="true" />
              Download CV
            </a>
          </div>

          <PortraitCarousel className="w-full max-w-[320px] shrink-0 self-center sm:self-start" />
        </div>
      </section>

      {/* ============ Skills ============ */}
      <section aria-labelledby="about-skills" className="mt-14">
        <h2
          id="about-skills"
          className="text-xl font-semibold tracking-tight"
        >
          Skills
        </h2>
        <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-3">
          {SKILLS.map((group) => (
            <div
              key={group.group}
              className="rounded-lg border border-border bg-card p-5"
            >
              <h3 className="text-sm font-semibold">{group.group}</h3>
              <ul className="mt-3 space-y-1.5">
                {group.items.map((item) => (
                  <li
                    key={item}
                    className="text-sm leading-6 text-muted-foreground"
                  >
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      {/* ============ Education & Interests ============ */}
      <section
        aria-labelledby="about-education"
        className="mt-14 grid grid-cols-1 gap-8 lg:grid-cols-2"
      >
        <div>
          <h2
            id="about-education"
            className="flex items-center gap-2 text-xl font-semibold tracking-tight"
          >
            <GraduationCap className="h-5 w-5 text-primary" aria-hidden="true" />
            Education
          </h2>
          <ul className="mt-4 space-y-4">
            {EDUCATION.map((e) => (
              <li
                key={e.degree}
                className="rounded-lg border border-border bg-card p-4"
              >
                <div className="flex items-baseline justify-between gap-3">
                  <h3 className="text-sm font-semibold">{e.degree}</h3>
                  <span className="shrink-0 font-mono text-xs text-muted-foreground">
                    {e.period}
                  </span>
                </div>
                <p className="mt-1 text-sm text-muted-foreground">{e.place}</p>
                {e.note && (
                  <p className="mt-1 text-xs text-primary">{e.note}</p>
                )}
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h2 className="flex items-center gap-2 text-xl font-semibold tracking-tight">
            <Sparkles className="h-5 w-5 text-primary" aria-hidden="true" />
            Interests
          </h2>
          <ul className="mt-4 flex flex-wrap gap-2">
            {INTERESTS.map((i) => (
              <li
                key={i}
                className="rounded-full border border-primary/40 bg-primary/10 px-3 py-1.5 text-xs text-primary dark:text-foreground/90"
              >
                {i}
              </li>
            ))}
          </ul>

          <h2 className="mt-8 text-xl font-semibold tracking-tight">
            Honors & Awards
          </h2>
          <ul className="mt-4 space-y-2">
            {ACHIEVEMENTS.map((a) => (
              <li key={a.year} className="flex gap-3 text-sm">
                <span className="shrink-0 font-mono text-xs text-muted-foreground">
                  {a.year}
                </span>
                <span className="text-muted-foreground">{a.text}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* ============ Detailed experience ============ */}
      <section aria-labelledby="about-experience" className="mt-14">
        <h2 id="about-experience" className="text-xl font-semibold tracking-tight">
          Experience
        </h2>
        <ol className="mt-6 space-y-8 border-l border-border pl-6">
          {EXPERIENCE.map((job) => (
            <li key={job.period} className="relative">
              <span
                aria-hidden="true"
                className="absolute -left-[31px] top-1.5 h-2.5 w-2.5 rounded-full border-2 border-background bg-primary"
              />
              <div className="flex flex-wrap items-baseline justify-between gap-2">
                <h3 className="text-base font-semibold">{job.org}</h3>
                <span className="font-mono text-xs text-muted-foreground">
                  {job.period}
                </span>
              </div>
              <p className="mt-0.5 text-sm text-muted-foreground">{job.role}</p>
              <ul className="mt-3 space-y-1.5">
                {job.points.map((p) => (
                  <li
                    key={p.slice(0, 40)}
                    className="flex gap-2 text-sm leading-6 text-foreground/85"
                  >
                    <span aria-hidden="true" className="mt-2 h-1 w-1 shrink-0 rounded-full bg-muted-foreground" />
                    {p}
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ol>
      </section>

      {/* ============ Contacts ============ */}
      <section aria-labelledby="about-contacts" className="mt-14">
        <h2 id="about-contacts" className="flex items-center gap-2 text-xl font-semibold tracking-tight">
          <Mail className="h-5 w-5 text-primary" aria-hidden="true" />
          Contact
        </h2>
        <ul className="mt-4 flex flex-wrap gap-3">
          <li>
            <a
              href={`mailto:${CONTACTS.email}`}
              className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-4 py-2 text-sm transition-colors hover:bg-accent hover:text-accent-foreground"
            >
              {CONTACTS.email}
            </a>
          </li>
          <li>
            <a
              href={CONTACTS.linkedin}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-4 py-2 text-sm transition-colors hover:bg-accent hover:text-accent-foreground"
            >
              LinkedIn
            </a>
          </li>
          <li>
            <a
              href={CONTACTS.telegram}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-4 py-2 text-sm transition-colors hover:bg-accent hover:text-accent-foreground"
            >
              Telegram
            </a>
          </li>
          <li>
            <a
              href={CONTACTS.github}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-4 py-2 text-sm transition-colors hover:bg-accent hover:text-accent-foreground"
            >
              GitHub
            </a>
          </li>
        </ul>
      </section>
    </div>
  );
}
