"use client";

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import { api } from "@/lib/api";
import type {
  ContentItem,
  ContentSection,
  ContentStats,
} from "@/types/content";
import type { ContentFormValues } from "@/lib/validations";

export type CreateContentInput = ContentFormValues;
export type UpdateContentInput = Partial<ContentFormValues>;

export function useContentList(section?: ContentSection) {
  const params = section ? `?section=${encodeURIComponent(section)}` : "";
  return useQuery({
    queryKey: ["admin", "content", section ?? "all"],
    queryFn: () => api<ContentItem[]>(`/api/v1/admin/content${params}`),
  });
}

export function useContentStats() {
  return useQuery({
    queryKey: ["admin", "stats"],
    queryFn: () => api<ContentStats>("/api/v1/admin/content/stats"),
  });
}

export function useCreateContent() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (input: CreateContentInput) =>
      api<ContentItem>("/api/v1/admin/content", {
        method: "POST",
        body: input,
      }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin"] });
    },
  });
}

export function useUpdateContent() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...input }: UpdateContentInput & { id: number }) =>
      api<ContentItem>(`/api/v1/admin/content/${id}`, {
        method: "PATCH",
        body: input,
      }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin"] });
    },
  });
}

export function useDeleteContent() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) =>
      api<void>(`/api/v1/admin/content/${id}`, { method: "DELETE" }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin"] });
    },
  });
}
