import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/site";

/**
 * Serve /sitemap.xml with all public pages.
 *
 * lastmod: per-page dates of the last real content change. Kept manual on
 * purpose — a sitemap where every lastmod equals the build date stops being
 * trusted by crawlers.
 */
export default function sitemap(): MetadataRoute.Sitemap {
  const pages: { path: string; lastmod: string; priority: number }[] = [
    { path: "", lastmod: "2026-10-08", priority: 1 }, // hero/sections rework
    { path: "/aboutme", lastmod: "2026-10-08", priority: 0.8 }, // location line, alts
    { path: "/ihome", lastmod: "2026-10-06", priority: 0.8 }, // page published
    { path: "/trade4me", lastmod: "2026-10-08", priority: 0.8 }, // page published
    { path: "/sdart", lastmod: "2026-09-29", priority: 0.8 }, // gallery lightbox rework
  ];

  return pages.map((p) => ({
    url: `${SITE_URL}${p.path}`,
    lastModified: p.lastmod,
    changeFrequency: "monthly",
    priority: p.priority,
  }));
}
