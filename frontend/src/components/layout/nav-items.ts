/**
 * Top-level navigation model.
 * - Flat items render as direct links in the header.
 * - The `projects` group renders as a "Projects" dropdown.
 * - OAuth login renders as a "Login" dropdown (see oauth-login-dropdown.tsx).
 */
type NavItem = { href: string; label: string };

const TOP_NAV_ITEMS: readonly NavItem[] = [
  { href: "/", label: "Home" },
  { href: "/aboutme", label: "About Me" },
  { href: "/sdart", label: "AI Art" },
] as const;

const PROJECT_NAV_ITEMS: readonly NavItem[] = [
  { href: "/ihome", label: "iHome" },
  { href: "/trade4me", label: "Trade4Me" },
] as const;

/** True when the header should highlight the Projects dropdown for this path. */
function isProjectPath(pathname: string): boolean {
  return PROJECT_NAV_ITEMS.some((item) => pathname.startsWith(item.href));
}

export { TOP_NAV_ITEMS, PROJECT_NAV_ITEMS, isProjectPath };
export type { NavItem };
