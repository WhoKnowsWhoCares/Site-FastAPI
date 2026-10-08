import type { MetadataRoute } from "next";

/** Serve /manifest.webmanifest — makes the site installable and gives it a proper name on share sheets. */
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "FrantsTech — Alexander Frantsev",
    short_name: "FrantsTech",
    description:
      "Senior Data Scientist: ML products, smart home, trading automation and AI art.",
    start_url: "/",
    display: "standalone",
    background_color: "#171f38",
    theme_color: "#171f38",
    icons: [
      {
        src: "/icon.svg",
        type: "image/svg+xml",
        sizes: "any",
      },
    ],
  };
}
