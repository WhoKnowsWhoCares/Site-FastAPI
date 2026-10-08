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

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: "Alexander Frantsev — Senior Data Scientist",
    template: `%s — ${SITE_NAME}`,
  },
  description:
    "Senior Data Scientist: ML products end-to-end, fintech & big tech. Smart home, trading bots and generated art as side projects.",
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
  },
  twitter: {
    card: "summary_large_image",
    title: "Alexander Frantsev — Senior Data Scientist",
    description:
      "ML products end-to-end: fintech, big tech, retail. Smart home, trading and AI art on the side.",
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
