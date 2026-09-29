"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2 } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  contentFormSchema,
  type ContentFormValues,
} from "@/lib/validations";
import { CONTENT_SECTION_LABELS } from "@/lib/auth";
import { contentSections, type ContentItem } from "@/types/content";

interface ContentFormProps {
  open: boolean;
  /** Existing item when editing, null when creating. */
  item: ContentItem | null;
  pending?: boolean;
  serverError?: string | null;
  onSubmit: (values: ContentFormValues) => void;
  onClose: () => void;
}

const EMPTY_VALUES: ContentFormValues = {
  section: "home",
  title: "",
  slug: "",
  body: "",
  isPublished: false,
  sortOrder: 0,
};

export function ContentForm({
  open,
  item,
  pending = false,
  serverError,
  onSubmit,
  onClose,
}: ContentFormProps) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ContentFormValues>({
    resolver: zodResolver(contentFormSchema),
    defaultValues: EMPTY_VALUES,
  });

  useEffect(() => {
    if (open) {
      reset(
        item
          ? {
              section: item.section,
              title: item.title,
              slug: item.slug,
              body: item.body,
              isPublished: item.isPublished,
              sortOrder: item.sortOrder,
            }
          : EMPTY_VALUES
      );
    }
  }, [open, item, reset]);

  return (
    <Dialog open={open} onOpenChange={(next) => !next && onClose()}>
      <DialogContent className="max-h-[90vh] overflow-y-auto sm:max-w-xl">
        <DialogHeader>
          <DialogTitle>
            {item ? "Edit content" : "New content"}
          </DialogTitle>
          <DialogDescription>
            {item
              ? "Update the content item and save your changes."
              : "Create a new content item for a site section."}
          </DialogDescription>
        </DialogHeader>

        <form
          noValidate
          onSubmit={handleSubmit(onSubmit)}
          className="space-y-4"
          aria-busy={pending}
        >
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div className="space-y-1.5">
              <label htmlFor="content-section" className="text-sm font-medium">
                Section
              </label>
              <select
                id="content-section"
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                aria-invalid={Boolean(errors.section)}
                {...register("section")}
              >
                {contentSections.map((section) => (
                  <option key={section} value={section}>
                    {CONTENT_SECTION_LABELS[section]}
                  </option>
                ))}
              </select>
              {errors.section && (
                <p className="text-sm text-destructive" role="alert">
                  {errors.section.message}
                </p>
              )}
            </div>

            <div className="space-y-1.5">
              <label htmlFor="content-sort-order" className="text-sm font-medium">
                Sort order
              </label>
              <Input
                id="content-sort-order"
                type="number"
                min={0}
                step={1}
                aria-invalid={Boolean(errors.sortOrder)}
                {...register("sortOrder", { valueAsNumber: true })}
              />
              {errors.sortOrder && (
                <p className="text-sm text-destructive" role="alert">
                  {errors.sortOrder.message}
                </p>
              )}
            </div>
          </div>

          <div className="space-y-1.5">
            <label htmlFor="content-title" className="text-sm font-medium">
              Title
            </label>
            <Input
              id="content-title"
              aria-invalid={Boolean(errors.title)}
              {...register("title")}
            />
            {errors.title && (
              <p className="text-sm text-destructive" role="alert">
                {errors.title.message}
              </p>
            )}
          </div>

          <div className="space-y-1.5">
            <label htmlFor="content-slug" className="text-sm font-medium">
              Slug
            </label>
            <Input
              id="content-slug"
              aria-invalid={Boolean(errors.slug)}
              aria-describedby="content-slug-hint"
              {...register("slug")}
            />
            <p id="content-slug-hint" className="text-xs text-muted-foreground">
              URL-friendly identifier, e.g. &quot;my-post&quot;
            </p>
            {errors.slug && (
              <p className="text-sm text-destructive" role="alert">
                {errors.slug.message}
              </p>
            )}
          </div>

          <div className="space-y-1.5">
            <label htmlFor="content-body" className="text-sm font-medium">
              Body
            </label>
            <textarea
              id="content-body"
              rows={8}
              className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              aria-invalid={Boolean(errors.body)}
              {...register("body")}
            />
            {errors.body && (
              <p className="text-sm text-destructive" role="alert">
                {errors.body.message}
              </p>
            )}
          </div>

          <div className="flex items-center gap-2">
            <input
              id="content-published"
              type="checkbox"
              className="h-4 w-4 rounded border-input"
              {...register("isPublished")}
            />
            <label htmlFor="content-published" className="text-sm font-medium">
              Published
            </label>
          </div>

          {serverError && (
            <p className="text-sm text-destructive" role="alert">
              {serverError}
            </p>
          )}

          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose} disabled={pending}>
              Cancel
            </Button>
            <Button type="submit" disabled={pending} aria-busy={pending}>
              {pending && <Loader2 className="animate-spin" aria-hidden="true" />}
              {item ? "Save changes" : "Create"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
