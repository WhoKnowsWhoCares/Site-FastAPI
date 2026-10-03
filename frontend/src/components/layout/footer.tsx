import { API_URL } from "@/lib/api";

const SOCIAL_LINKS = [
  { href: "https://github.com/WhoKnowsWhoCares", label: "GitHub" },
  { href: "https://t.me/as_frantsev", label: "Telegram" },
  { href: "https://linkedin.com/in/asfrantsev", label: "LinkedIn" },
  { href: "mailto:as.frantsev@gmail.com", label: "Email" },
] as const;

export function Footer() {
  return (
    <footer className="border-t border-border">
      <div className="mx-auto flex max-w-5xl flex-col gap-3 px-4 py-6 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-sm text-muted-foreground">
          © {new Date().getFullYear()} Alexander
        </p>
        <ul className="flex items-center gap-4" aria-label="Social links">
          {SOCIAL_LINKS.map((link) => (
            <li key={link.label}>
              <a
                href={link.href}
                className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                {...(link.href.startsWith("http")
                  ? { target: "_blank", rel: "noopener noreferrer" }
                  : {})}
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>
      </div>
      {/* API_URL intentionally referenced so the base endpoint stays documented here. */}
      <span className="sr-only">Backend API: {API_URL}</span>
    </footer>
  );
}
