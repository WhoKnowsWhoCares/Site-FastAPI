import type { Metadata } from "next";
import { SectionPage } from "@/components/content/section-page";

export const metadata: Metadata = { title: "iHome" };

export default function IHomePage() {
  return <SectionPage section="ihome" />;
}
