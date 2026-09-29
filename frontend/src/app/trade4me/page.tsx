import type { Metadata } from "next";
import { SectionPage } from "@/components/content/section-page";

export const metadata: Metadata = { title: "Trade4Me" };

export default function Trade4MePage() {
  return <SectionPage section="trade4me" />;
}
