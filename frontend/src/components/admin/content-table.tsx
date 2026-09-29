"use client";

import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { CONTENT_SECTION_LABELS } from "@/lib/auth";
import type { ContentItem } from "@/types/content";
import { Pencil, Trash2, CheckCircle2, Circle } from "lucide-react";

interface ContentTableProps {
  items: ContentItem[];
  isLoading?: boolean;
  onEdit: (item: ContentItem) => void;
  onDelete: (item: ContentItem) => void;
}

export function ContentTable({
  items,
  isLoading = false,
  onEdit,
  onDelete,
}: ContentTableProps) {
  if (isLoading) {
    return (
      <div className="space-y-2" aria-busy="true" aria-label="Loading content">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="h-12 w-full animate-pulse rounded bg-muted" />
        ))}
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div role="status" className="rounded-md border py-12 text-center">
        <h3 className="text-sm font-medium">No content yet</h3>
        <p className="mt-1 text-sm text-muted-foreground">
          Create your first content item to get started.
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-16">Status</TableHead>
            <TableHead>Title</TableHead>
            <TableHead className="hidden md:table-cell">Section</TableHead>
            <TableHead className="hidden md:table-cell">Slug</TableHead>
            <TableHead className="hidden lg:table-cell">Order</TableHead>
            <TableHead className="w-24 text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {items.map((item) => (
            <TableRow key={item.id}>
              <TableCell>
                {item.isPublished ? (
                  <span className="inline-flex items-center gap-1.5 text-sm text-muted-foreground">
                    <CheckCircle2 className="h-4 w-4" aria-hidden="true" />
                    <span className="sr-only">Published</span>
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1.5 text-sm text-muted-foreground">
                    <Circle className="h-4 w-4" aria-hidden="true" />
                    <span className="sr-only">Draft</span>
                  </span>
                )}
              </TableCell>
              <TableCell className="font-medium">{item.title}</TableCell>
              <TableCell className="hidden md:table-cell">
                {CONTENT_SECTION_LABELS[item.section] ?? item.section}
              </TableCell>
              <TableCell className="hidden font-mono text-xs md:table-cell">
                {item.slug}
              </TableCell>
              <TableCell className="hidden lg:table-cell tabular-nums">
                {item.sortOrder}
              </TableCell>
              <TableCell className="text-right">
                <div className="flex justify-end gap-1">
                  <Button
                    variant="ghost"
                    size="icon"
                    aria-label={`Edit ${item.title}`}
                    onClick={() => onEdit(item)}
                  >
                    <Pencil aria-hidden="true" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    aria-label={`Delete ${item.title}`}
                    onClick={() => onDelete(item)}
                  >
                    <Trash2 aria-hidden="true" />
                  </Button>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
