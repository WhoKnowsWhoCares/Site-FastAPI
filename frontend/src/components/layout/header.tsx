"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { ChevronDown, FolderGit2 } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { TOP_NAV_ITEMS, PROJECT_NAV_ITEMS, isProjectPath } from "./nav-items";
import { ThemeToggle } from "./theme-toggle";

const linkClasses = (active: boolean, block = false) =>
  `${block ? "block" : ""} rounded-md px-3 py-1.5 text-sm transition-colors ${
    active
      ? "bg-accent font-medium text-accent-foreground"
      : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
  }`;

export function Header() {
  const pathname = usePathname();
  const [menuOpen, setMenuOpen] = useState(false);
  const projectsActive = isProjectPath(pathname);

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-background/95 backdrop-blur">
      <div className="mx-auto flex h-14 max-w-5xl items-center justify-between px-4">
        <Link
          href="/"
          className="text-base font-semibold tracking-tight"
          onClick={() => setMenuOpen(false)}
        >
          Frants
          <span className="font-mono text-muted-foreground">Tech</span>
        </Link>

        {/* Desktop nav */}
        <nav aria-label="Main" className="hidden md:flex md:items-center md:gap-1">
          <ul className="flex items-center gap-1">
            {TOP_NAV_ITEMS.map((item) => {
              const active =
                item.href === "/"
                  ? pathname === "/"
                  : pathname.startsWith(item.href);
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    aria-current={active ? "page" : undefined}
                    className={linkClasses(active)}
                  >
                    {item.label}
                  </Link>
                </li>
              );
            })}

            {/* Projects dropdown */}
            <li>
              <DropdownMenu>
                <DropdownMenuTrigger
                  aria-current={projectsActive ? "true" : undefined}
                  className={linkClasses(projectsActive, false) +
                    " inline-flex items-center gap-1 data-[state=open]:bg-accent data-[state=open]:text-accent-foreground"}
                >
                  <FolderGit2 className="h-3.5 w-3.5" aria-hidden="true" />
                  Projects
                  <ChevronDown className="h-3 w-3 opacity-60" aria-hidden="true" />
                </DropdownMenuTrigger>
                <DropdownMenuContent align="start" className="min-w-[10rem]">
                  {PROJECT_NAV_ITEMS.map((item) => (
                    <DropdownMenuItem key={item.href} asChild>
                      <Link href={item.href}>{item.label}</Link>
                    </DropdownMenuItem>
                  ))}
                </DropdownMenuContent>
              </DropdownMenu>
            </li>
          </ul>
          <div className="ml-2 border-l border-border pl-2">
            <ThemeToggle />
          </div>
        </nav>

        {/* Mobile: theme toggle + burger */}
        <div className="flex items-center gap-2 md:hidden">
          <ThemeToggle />
          <button
            type="button"
            aria-expanded={menuOpen}
            aria-controls="mobile-nav"
            aria-label={menuOpen ? "Close menu" : "Open menu"}
            className="rounded-md p-2 text-muted-foreground hover:bg-accent hover:text-accent-foreground"
            onClick={() => setMenuOpen((open) => !open)}
          >
            <svg
              aria-hidden="true"
              viewBox="0 0 24 24"
              width="20"
              height="20"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
            >
              {menuOpen ? (
                <path d="M18 6 6 18M6 6l12 12" />
              ) : (
                <path d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile nav panel: flat list, project links included inline */}
      {menuOpen && (
        <nav
          id="mobile-nav"
          aria-label="Main mobile"
          className="border-t border-border md:hidden"
        >
          <ul className="mx-auto max-w-5xl px-4 py-2">
            {TOP_NAV_ITEMS.map((item) => {
              const active =
                item.href === "/"
                  ? pathname === "/"
                  : pathname.startsWith(item.href);
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    aria-current={active ? "page" : undefined}
                    className={linkClasses(active, true)}
                    onClick={() => setMenuOpen(false)}
                  >
                    {item.label}
                  </Link>
                </li>
              );
            })}
            <li aria-hidden="true" className="my-1 h-px bg-border" />
            {PROJECT_NAV_ITEMS.map((item) => {
              const active = pathname.startsWith(item.href);
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    aria-current={active ? "page" : undefined}
                    className={linkClasses(active, true)}
                    onClick={() => setMenuOpen(false)}
                  >
                    {item.label}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
      )}
    </header>
  );
}
