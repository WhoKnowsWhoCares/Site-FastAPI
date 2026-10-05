"use client";

import { useState } from "react";
import Image from "next/image";
import { Check, Copy, X } from "lucide-react";
import * as DialogPrimitive from "@radix-ui/react-dialog";
import { GALLERY_ITEMS, type GalleryItem } from "./gallery-data";

function GalleryCard({ item }: { item: GalleryItem }) {
  const [copied, setCopied] = useState(false);
  const [open, setOpen] = useState(false);

  const copyPrompt = async () => {
    try {
      await navigator.clipboard.writeText(item.prompt);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // Clipboard API unavailable (e.g. insecure context) — silently ignore.
    }
  };

  return (
    <DialogPrimitive.Root open={open} onOpenChange={setOpen}>
      <DialogPrimitive.Trigger asChild>
        <figure
          aria-label={`Open ${item.title} fullscreen`}
          className="group relative cursor-zoom-in overflow-hidden rounded-lg border border-border bg-card shadow-sm"
        >
          <Image
            src={item.src}
            alt={item.title}
            width={item.width}
            height={item.height}
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 640px"
            className="h-auto w-full object-cover"
          />

          {/* Overlay: hidden by default, fades in on hover/focus */}
          <figcaption className="pointer-events-none absolute inset-0 flex flex-col justify-end bg-gradient-to-t from-black/80 via-black/40 to-transparent p-4 opacity-0 transition-opacity duration-200 group-hover:opacity-100 group-focus-within:opacity-100">
            <p className="text-sm font-semibold text-white">{item.title}</p>
            <p className="mt-0.5 font-mono text-[11px] text-white/70">
              Model: {item.model} · Sampler: {item.sampler}
            </p>
            <p className="mt-1 line-clamp-4 text-xs leading-5 text-white/80">
              {item.prompt}
            </p>
            <button
              type="button"
              aria-label={`Copy prompt for ${item.title}`}
              className="pointer-events-auto mt-3 inline-flex w-fit items-center gap-1.5 rounded-md border border-white/20 bg-white/10 px-2.5 py-1.5 text-xs font-medium text-white backdrop-blur transition-colors hover:bg-white/20"
              onClick={(e) => {
                // Don't open the lightbox when the user just copies the prompt.
                e.stopPropagation();
                copyPrompt();
              }}
            >
              {copied ? (
                <>
                  <Check className="h-3.5 w-3.5" aria-hidden="true" />
                  Copied
                </>
              ) : (
                <>
                  <Copy className="h-3.5 w-3.5" aria-hidden="true" />
                  Copy prompt
                </>
              )}
            </button>
          </figcaption>
        </figure>
      </DialogPrimitive.Trigger>

      {/* Fullscreen lightbox: click anywhere (image included) closes it */}
      <DialogPrimitive.Portal>
        <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/90 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
        <DialogPrimitive.Content
          aria-label={item.title}
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
            {item.title}
          </DialogPrimitive.Title>
          <Image
            src={item.src}
            alt={item.title}
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

export function GalleryGrid() {
  return (
    <ul role="list" className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
      {GALLERY_ITEMS.map((item) => (
        <li key={item.src}>
          <GalleryCard item={item} />
        </li>
      ))}
    </ul>
  );
}
