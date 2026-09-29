import type { Metadata } from "next";
import Image from "next/image";
import { fetchGallery, fetchPageContent } from "@/lib/content";
import { SECTION_DEFAULTS } from "@/components/content/section-page";

export const metadata: Metadata = { title: "SD Art" };

export default async function SdArtPage() {
  const [content, gallery] = await Promise.all([
    fetchPageContent("sdart"),
    fetchGallery(),
  ]);

  const title = content?.title ?? SECTION_DEFAULTS.sdart.title;
  const paragraphs = content?.paragraphs?.length
    ? content.paragraphs
    : SECTION_DEFAULTS.sdart.paragraphs;

  return (
    <div className="mx-auto max-w-5xl px-4 py-12">
      <article>
        <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
          {title}
        </h1>
        <div className="mt-4 max-w-3xl space-y-3">
          {paragraphs.map((paragraph, index) => (
            <p key={index} className="text-base leading-7 text-foreground/90">
              {paragraph}
            </p>
          ))}
        </div>
      </article>

      <section aria-labelledby="gallery-title" className="mt-10">
        <h2 id="gallery-title" className="text-xl font-semibold tracking-tight">
          Gallery
        </h2>

        {gallery.length > 0 ? (
          <ul
            role="list"
            className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3"
          >
            {gallery.map((item) => (
              <li
                key={item.id}
                className="overflow-hidden rounded-lg border border-border bg-card"
              >
                <div className="relative aspect-square">
                  {/* Gallery URLs come from the backend API and can point at any
                      host, so the image optimizer's remotePatterns whitelist
                      (next.config.mjs) cannot cover them. `unoptimized` makes
                      next/image serve the backend URL directly, which keeps the
                      gallery working regardless of image host. */}
                  <Image
                    src={item.url}
                    alt={item.alt ?? item.title ?? "SD Art image"}
                    fill
                    unoptimized
                    sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
                    className="object-cover"
                  />
                </div>
                {item.title && (
                  <p className="px-3 py-2 text-sm text-muted-foreground">
                    {item.title}
                  </p>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <div
            role="status"
            className="mt-4 flex flex-col items-center rounded-lg border border-dashed border-border py-12 text-center"
          >
            <h3 className="text-sm font-medium">No images yet</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              Gallery images will appear here once uploaded via the
              ControlPanel.
            </p>
          </div>
        )}
      </section>
    </div>
  );
}
