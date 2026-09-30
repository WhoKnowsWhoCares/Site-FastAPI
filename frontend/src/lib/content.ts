import { apiUrl } from "@/lib/api";
import {
  isSection,
  type GalleryItem,
  type PageContent,
  type ContentSection,
} from "@/types/content";

/**
 * Fetch a section's page content from the backend.
 *
 * Used by public pages at request time (SSR). Returns null when the
 * backend is unreachable or has no content yet, so pages can fall back
 * to sensible defaults instead of erroring.
 */
export async function fetchPageContent(
  section: ContentSection
): Promise<PageContent | null> {
  if (!isSection(section)) return null;
  try {
    const res = await fetch(apiUrl(`/api/v1/content/${section}`), {
      cache: "no-store",
      headers: { Accept: "application/json" },
    });
    if (!res.ok) return null;
    const data: unknown = await res.json();
    if (!isPageContent(data)) return null;
    return data;
  } catch {
    return null;
  }
}

/** Fetch SD Art gallery items. Returns [] when unavailable. */
export async function fetchGallery(): Promise<GalleryItem[]> {
  try {
    const res = await fetch(apiUrl("/api/v1/content/sdart/gallery"), {
      cache: "no-store",
      headers: { Accept: "application/json" },
    });
    if (!res.ok) return [];
    const data: unknown = await res.json();
    return Array.isArray(data) ? data.filter(isGalleryItem) : [];
  } catch {
    return [];
  }
}

function isPageContent(value: unknown): value is PageContent {
  if (typeof value !== "object" || value === null) return false;
  const v = value as Record<string, unknown>;
  return (
    typeof v.section === "string" &&
    typeof v.title === "string" &&
    Array.isArray(v.paragraphs) &&
    v.paragraphs.every((p) => typeof p === "string")
  );
}

function isGalleryItem(value: unknown): value is GalleryItem {
  if (typeof value !== "object" || value === null) return false;
  const v = value as Record<string, unknown>;
  return typeof v.id === "string" && typeof v.url === "string";
}
