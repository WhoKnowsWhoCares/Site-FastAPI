import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/site";

/** Serve /sitemap.xml with all public pages. */
export default function sitemap(): MetadataRoute.Sitemap {
  const pages = ["", "/aboutme", "/ihome", "/trade4me", "/sdart"];

  return pages.map((path) => ({
    url: `${SITE_URL}${path}`,
    lastModified: new Date(),
    changeFrequency: "monthly",
    priority: path === "" ? 1 : 0.8,
  }));
}
