import type { Metadata } from "next";
import { GalleryGrid } from "@/components/gallery/gallery-grid";

export const metadata: Metadata = {
  title: "AI Art",
  description:
    "AI-generated art gallery: images created and edited with neural networks, prompts and model metadata included.",
  openGraph: {
    title: "AI Art — neural network gallery",
    description:
      "Images generated and edited with neural networks. Prompts and model metadata for every piece.",
    images: [{ url: "/sdart/home_1.webp", width: 1920, height: 1280, alt: "AI-generated artwork from the gallery" }],
  },
};

export default function SdArtPage() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-12">
      <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">AI Art</h1>
      <GalleryGrid />
    </div>
  );
}
