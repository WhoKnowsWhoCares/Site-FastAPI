"use client";

import { useState } from "react";
import Image from "next/image";
import { X } from "lucide-react";
import * as DialogPrimitive from "@radix-ui/react-dialog";
import type { MediaItem } from "./ihome-data";

function MediaCard({ item }: { item: MediaItem }) {
  const [open, setOpen] = useState(false);

  return (
    <DialogPrimitive.Root open={open} onOpenChange={setOpen}>
      <DialogPrimitive.Trigger asChild>
        <figure
          aria-label={`Open ${item.caption} fullscreen`}
          className="group relative cursor-zoom-in overflow-hidden rounded-lg border border-border bg-card shadow-sm"
        >
          <Image
            src={item.src}
            alt={item.alt}
            width={item.width}
            height={item.height}
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 640px"
            className="h-auto w-full object-cover transition-transform duration-200 group-hover:scale-[1.02]"
          />
          {/* Caption bar: fades in on hover/focus */}
          <figcaption className="pointer-events-none absolute inset-0 flex flex-col justify-end bg-gradient-to-t from-black/80 via-black/40 to-transparent p-4 opacity-0 transition-opacity duration-200 group-hover:opacity-100 group-focus-within:opacity-100">
            <p className="text-sm font-semibold text-white">{item.caption}</p>
          </figcaption>
        </figure>
      </DialogPrimitive.Trigger>

      {/* Fullscreen lightbox: click anywhere (image included) closes it */}
      <DialogPrimitive.Portal>
        <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/90 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
        <DialogPrimitive.Content
          aria-label={item.caption}
          className="fixed inset-0 z-50 flex cursor-zoom-out items-center justify-center p-4 focus:outline-none sm:p-8"
          onClick={() => setOpen(false)}
        >
          <DialogPrimitive.Close asChild>
            <button
              type="button"
              aria-label="Close fullscreen view"
              className="absolute right-4 top-4 z-10 rounded-md border border-white/20 bg-white/10 p-2 text-white backdrop-blur transition-colors hover:bg-white/20"
            >
              <X className="h-5 w-5" aria-hidden="true" />
            </button>
          </DialogPrimitive.Close>
          <DialogPrimitive.Title className="sr-only">
            {item.caption}
          </DialogPrimitive.Title>
          <Image
            src={item.src}
            alt={item.alt}
            width={item.width}
            height={item.height}
            sizes="100vw"
            className="max-h-full max-w-full rounded-lg object-contain shadow-2xl"
            quality={90}
          />
        </DialogPrimitive.Content>
      </DialogPrimitive.Portal>
    </DialogPrimitive.Root>
  );
}

export function MediaGrid({ items }: { items: MediaItem[] }) {
  return (
    <ul role="list" className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
      {items.map((item) => (
        <li key={item.src}>
          <MediaCard item={item} />
        </li>
      ))}
    </ul>
  );
}
