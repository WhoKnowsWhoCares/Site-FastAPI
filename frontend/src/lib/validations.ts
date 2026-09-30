import { z } from "zod";
import { contentSections } from "@/types/content";

export const emailSchema = z.string().email("Enter a valid email address");

export const passwordSchema = z
  .string()
  .min(8, "Password must be at least 8 characters");

export const contentFormSchema = z.object({
  section: z.enum(contentSections, {
    errorMap: () => ({ message: "Select a section" }),
  }),
  title: z
    .string()
    .min(1, "Title is required")
    .max(200, "Title must be 200 characters or fewer"),
  slug: z
    .string()
    .min(1, "Slug is required")
    .max(200, "Slug must be 200 characters or fewer")
    .regex(
      /^[a-z0-9]+(?:-[a-z0-9]+)*$/,
      "Slug must be lowercase letters, numbers and hyphens"
    ),
  body: z.string().max(50000, "Body must be 50,000 characters or fewer"),
  isPublished: z.boolean(),
  sortOrder: z
    .number({ invalid_type_error: "Sort order must be a number" })
    .int("Sort order must be an integer")
    .min(0, "Sort order must be 0 or greater")
    .max(9999, "Sort order must be 9999 or less"),
});

export type ContentFormValues = z.infer<typeof contentFormSchema>;
