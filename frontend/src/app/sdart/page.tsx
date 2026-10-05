import type { Metadata } from "next";
import { GalleryGrid } from "@/components/gallery/gallery-grid";

export const metadata: Metadata = { title: "AI Art" };

export default function SdArtPage() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-12">
      <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">AI Art</h1>
      <GalleryGrid />
    </div>
  );
}
