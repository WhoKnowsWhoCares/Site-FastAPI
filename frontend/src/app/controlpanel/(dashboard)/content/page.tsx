"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { ContentTable } from "@/components/admin/content-table";
import { ContentForm } from "@/components/admin/content-form";
import { ConfirmDialog } from "@/components/admin/confirm-dialog";
import {
  useContentList,
  useCreateContent,
  useDeleteContent,
  useUpdateContent,
} from "@/hooks/useContent";
import type { ContentFormValues } from "@/lib/validations";
import type { ContentItem, ContentSection } from "@/types/content";
import { PlusCircle } from "lucide-react";
import { contentSections } from "@/types/content";
import { CONTENT_SECTION_LABELS } from "@/lib/auth";

function ContentPageInner() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [sectionFilter, setSectionFilter] = useState<ContentSection | "all">(
    "all"
  );
  const listQuery = useContentList(
    sectionFilter === "all" ? undefined : sectionFilter
  );

  const [formOpen, setFormOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<ContentItem | null>(null);
  const [formError, setFormError] = useState<string | null>(null);

  const [deletingItem, setDeletingItem] = useState<ContentItem | null>(null);

  const createContent = useCreateContent();
  const updateContent = useUpdateContent();
  const deleteContent = useDeleteContent();

  // "New content item" quick action opens the create dialog via ?new=1
  useEffect(() => {
    if (searchParams.get("new") === "1") {
      setEditingItem(null);
      setFormOpen(true);
      router.replace("/controlpanel/content");
    }
  }, [searchParams, router]);

  const openCreate = () => {
    setEditingItem(null);
    setFormError(null);
    setFormOpen(true);
  };

  const openEdit = (item: ContentItem) => {
    setEditingItem(item);
    setFormError(null);
    setFormOpen(true);
  };

  const handleFormSubmit = (values: ContentFormValues) => {
    setFormError(null);
    if (editingItem) {
      updateContent.mutate(
        { id: editingItem.id, ...values },
        {
          onSuccess: () => {
            setFormOpen(false);
          },
          onError: (err: Error) => setFormError(err.message),
        }
      );
    } else {
      createContent.mutate(values, {
        onSuccess: () => {
          setFormOpen(false);
        },
        onError: (err: Error) => setFormError(err.message),
      });
    }
  };

  const handleDeleteConfirm = () => {
    if (!deletingItem) return;
    deleteContent.mutate(deletingItem.id, {
      onSettled: () => setDeletingItem(null),
    });
  };

  const formPending =
    createContent.isPending || updateContent.isPending;

  return (
    <div className="space-y-6">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Content</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Create, edit and delete content for all site sections.
          </p>
        </div>
        <Button onClick={openCreate}>
          <PlusCircle aria-hidden="true" />
          New item
        </Button>
      </header>

      <div
        className="flex flex-wrap gap-2"
        role="group"
        aria-label="Filter by section"
      >
        <Button
          variant={sectionFilter === "all" ? "default" : "outline"}
          size="sm"
          onClick={() => setSectionFilter("all")}
          aria-pressed={sectionFilter === "all"}
        >
          All
        </Button>
        {contentSections.map((section) => (
          <Button
            key={section}
            variant={sectionFilter === section ? "default" : "outline"}
            size="sm"
            onClick={() => setSectionFilter(section)}
            aria-pressed={sectionFilter === section}
          >
            {CONTENT_SECTION_LABELS[section]}
          </Button>
        ))}
      </div>

      {listQuery.isError ? (
        <div className="rounded-md border border-destructive/50 p-4" role="alert">
          <p className="text-sm text-destructive">
            Failed to load content: {(listQuery.error as Error).message}
          </p>
          <Button
            variant="outline"
            size="sm"
            className="mt-3"
            onClick={() => listQuery.refetch()}
          >
            Retry
          </Button>
        </div>
      ) : (
        <ContentTable
          items={listQuery.data ?? []}
          isLoading={listQuery.isLoading}
          onEdit={openEdit}
          onDelete={setDeletingItem}
        />
      )}

      <ContentForm
        open={formOpen}
        item={editingItem}
        pending={formPending}
        serverError={formError}
        onSubmit={handleFormSubmit}
        onClose={() => setFormOpen(false)}
      />

      <ConfirmDialog
        open={deletingItem !== null}
        title="Delete content?"
        description={`"${deletingItem?.title ?? ""}" will be permanently deleted. This action cannot be undone.`}
        confirmLabel="Delete"
        destructive
        pending={deleteContent.isPending}
        onConfirm={handleDeleteConfirm}
        onCancel={() => setDeletingItem(null)}
      />
    </div>
  );
}

export default function ControlPanelContentPage() {
  return (
    <Suspense fallback={null}>
      <ContentPageInner />
    </Suspense>
  );
}
