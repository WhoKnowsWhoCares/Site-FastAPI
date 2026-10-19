import type { Metadata, Viewport } from "next";
import { Sora, JetBrains_Mono } from "next/font/google";
import { ThemeProvider } from "next-themes";
import { SITE_URL, SITE_NAME } from "@/lib/site";
import "./globals.css";
import { Providers } from "@/components/providers";
import { Header } from "@/components/layout/header";
import { Footer } from "@/components/layout/footer";

const sora = Sora({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
});

/** Schema.org Person — ties the name to this site and its profiles in search engines. */
const personJsonLd = {
  "@context": "https://schema.org",
  "@type": "Person",
  name: "Alexander Frantsev",
  alternateName: ["Александр Францев"],
  url: SITE_URL,
  image: `${SITE_URL}/og.png`,
  jobTitle: "Senior Data Scientist",
  // No current employer listed; Yandex stays in the Experience section as past work.
  alumniOf: { "@type": "Organization", name: "Yandex" },
  description:
    "Senior Data Scientist: ML products end-to-end, fintech & big tech. Smart home, trading bots and generated art as side projects.",
  address: {
    "@type": "PostalAddress",
    addressLocality: "Moscow",
    addressCountry: "RU",
  },
  sameAs: [
    "https://linkedin.com/in/asfrantsev",
    "https://github.com/WhoKnowsWhoCares",
    "https://t.me/as_frantsev",
  ],
  email: "mailto:as.frantsev@gmail.com",
  knowsAbout: [
    "Machine Learning",
    "Data Science",
    "LLM",
    "Python",
    "Home Assistant",
    "Algorithmic Trading",
  ],
};

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: "Alexander Frantsev — Senior Data Scientist",
    // Pages are found by name: put the person's name in every <title>.
    template: `%s — Alexander Frantsev`,
  },
  description:
    "Alexander Frantsev — Senior Data Scientist in Moscow: ML products end-to-end, fintech & big tech. Smart home, trading bots and generated art as side projects.",
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "Alexander Frantsev — Senior Data Scientist",
    description:
      "ML products end-to-end: fintech, big tech, retail. Smart home, trading and AI art on the side.",
    type: "website",
    siteName: SITE_NAME,
    url: SITE_URL,
    locale: "en_US",
    images: [{ url: "/og.png", width: 1200, height: 630, alt: "Alexander Frantsev — Senior Data Scientist (FrantsTech)" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Alexander Frantsev — Senior Data Scientist",
    description:
      "ML products end-to-end: fintech, big tech, retail. Smart home, trading and AI art on the side.",
    images: ["/og.png"],
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: dark)", color: "#171f38" },
    { media: "(prefers-color-scheme: light)", color: "#f9fafb" },
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script
          type="application/ld+json"
          // Static, trusted JSON defined above — safe to inline.
          dangerouslySetInnerHTML={{ __html: JSON.stringify(personJsonLd) }}
        />
      </head>
      <body
        className={`${sora.variable} ${jetbrainsMono.variable} flex min-h-screen flex-col font-sans antialiased`}
      >
        <ThemeProvider attribute="class" defaultTheme="dark" enableSystem={false}>
          <Providers>
            <Header />
            <main className="flex-1">{children}</main>
            <Footer />
          </Providers>
        </ThemeProvider>
      </body>
    </html>
  );
}
