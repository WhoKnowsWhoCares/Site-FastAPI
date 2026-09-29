import type { ContentSection } from "@/types/content";
import { fetchPageContent } from "@/lib/content";

/** Fallback copy shown when the backend has no content for a section yet. */
export const SECTION_DEFAULTS: Record<
  ContentSection,
  { title: string; paragraphs: string[] }
> = {
  home: {
    title: "Home",
    paragraphs: [
      "Personal site home. Use the navigation above to explore the sections.",
    ],
  },
  aboutme: {
    title: "About Me",
    paragraphs: [
      "I'm Alexander, an analyst-developer. I work with data, build APIs and automate everyday tasks.",
      "This section is managed from the ControlPanel — content will appear here once published.",
    ],
  },
  ihome: {
    title: "iHome",
    paragraphs: [
      "Smart home dashboard preview: sensor readings, automations and device status.",
      "This section is managed from the ControlPanel — content will appear here once published.",
    ],
  },
  trade4me: {
    title: "Trade4Me",
    paragraphs: [
      "Trading bot project: strategy overview, statistics and current status.",
      "This section is managed from the ControlPanel — content will appear here once published.",
    ],
  },
  sdart: {
    title: "SD Art",
    paragraphs: [
      "Gallery of images generated with Stable Diffusion.",
      "This section is managed from the ControlPanel — content will appear here once published.",
    ],
  },
};

/**
 * Server component that renders a section page from backend content,
 * falling back to defaults when the API is unreachable or empty.
 */
export async function SectionPage({
  section,
}: {
  section: ContentSection;
}) {
  const content = await fetchPageContent(section);
  const title = content?.title ?? SECTION_DEFAULTS[section].title;
  const paragraphs = content?.paragraphs?.length
    ? content.paragraphs
    : SECTION_DEFAULTS[section].paragraphs;

  return (
    <div className="mx-auto max-w-3xl px-4 py-12">
      <article>
        <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
          {title}
        </h1>
        <div className="mt-6 space-y-4">
          {paragraphs.map((paragraph, index) => (
            <p key={index} className="text-base leading-7 text-foreground/90">
              {paragraph}
            </p>
          ))}
        </div>
        {!content && (
          <p className="mt-8 rounded-md border border-border bg-muted px-4 py-3 text-sm text-muted-foreground">
            Showing placeholder content — the backend is unreachable or this
            section has no published content yet.
          </p>
        )}
      </article>
    </div>
  );
}
