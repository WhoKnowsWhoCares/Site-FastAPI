import type { Metadata } from "next";
import { SectionPage } from "@/components/content/section-page";

export const metadata: Metadata = { title: "About Me" };

export default function AboutMePage() {
  return <SectionPage section="aboutme" />;
}
