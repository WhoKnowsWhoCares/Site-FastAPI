/**
 * Content types matching the backend API schemas
 * (see SPEC.md: backend/models/content.py — PageContent, Project, Media).
 */

export const contentSections = [
  "home",
  "aboutme",
  "ihome",
  "trade4me",
  "sdart",
] as const;

export type ContentSection = (typeof contentSections)[number];

export function isSection(value: string): value is ContentSection {
  return (contentSections as readonly string[]).includes(value);
}

/** Generic page content returned by GET /api/v1/content/{section}. */
export interface PageContent {
  section: ContentSection;
  title: string;
  /** Plain-text or markdown body blocks (one paragraph per entry). */
  paragraphs: string[];
  updatedAt?: string;
}

/** Gallery item for the SD Art section. */
export interface GalleryItem {
  id: string;
  url: string;
  title?: string;
  alt?: string;
}

/** Admin-side content row (admin content list endpoints). */
export interface ContentItem {
  id: number;
  section: ContentSection;
  title: string;
  slug: string;
  body: string;
  isPublished: boolean;
  sortOrder: number;
  createdAt: string;
  updatedAt: string;
}

/** Aggregated content counts for the admin dashboard. */
export interface ContentStats {
  total: number;
  published: number;
  drafts: number;
  bySection: Record<ContentSection, number>;
}
