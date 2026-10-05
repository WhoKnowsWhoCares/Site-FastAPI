import type { Metadata, Viewport } from "next";
import { Sora, JetBrains_Mono } from "next/font/google";
import { ThemeProvider } from "next-themes";
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
  title: {
    default: "Alexander Frantsev — Senior Data Scientist",
    template: "%s — Alexander Frantsev",
  },
  description:
    "Senior Data Scientist: ML products end-to-end, fintech & big tech. Smart home, trading bots and generated art as side projects.",
  openGraph: {
    title: "Alexander Frantsev — Senior Data Scientist",
    description:
      "ML products end-to-end: fintech, big tech, retail. Smart home, trading and AI art on the side.",
    type: "website",
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
