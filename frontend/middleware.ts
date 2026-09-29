import { NextRequest, NextResponse } from "next/server";

const SESSION_COOKIE = "cp_session";
const CONTROL_PANEL_PATH = "/controlpanel";
const LOGIN_PATH = "/controlpanel/login";

/**
 * Protects the ControlPanel:
 * - no session cookie  -> redirect to /controlpanel/login
 * - session cookie present on the login page -> redirect to the dashboard
 *
 * Token verification (signature, role check) happens in the backend API;
 * the cookie's presence is the cheap gate here.
 */
export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const hasSession = Boolean(request.cookies.get(SESSION_COOKIE)?.value);

  if (pathname.startsWith(CONTROL_PANEL_PATH) && !pathname.startsWith(LOGIN_PATH)) {
    if (!hasSession) {
      const loginUrl = new URL(LOGIN_PATH, request.url);
      loginUrl.searchParams.set("next", pathname);
      return NextResponse.redirect(loginUrl);
    }
  }

  if (pathname.startsWith(LOGIN_PATH) && hasSession) {
    return NextResponse.redirect(new URL(CONTROL_PANEL_PATH, request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/controlpanel/:path*"],
};
