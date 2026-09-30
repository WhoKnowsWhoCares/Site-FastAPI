/**
 * API base URL for the backend.
 * Set in .env.local (see .env.example).
 */
export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

/** Build an API endpoint URL from a path. */
export function apiUrl(path: string): string {
  return `${API_URL}${path}`;
}

export class ApiRequestError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiRequestError";
    this.status = status;
  }
}

interface RequestOptions extends Omit<RequestInit, "body"> {
  body?: unknown;
}

/**
 * Fetch wrapper for the backend API.
 * Sends cookies (session JWT is stored in an httpOnly cookie)
 * and parses JSON error bodies into ApiRequestError.
 */
export async function api<T>(
  path: string,
  options: RequestOptions = {}
): Promise<T> {
  const { body, headers, ...rest } = options;

  const res = await fetch(apiUrl(path), {
    ...rest,
    credentials: "include",
    headers: {
      ...(body !== undefined ? { "Content-Type": "application/json" } : {}),
      ...headers,
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) {
    let message = `Request failed with status ${res.status}`;
    try {
      const data = await res.json();
      if (typeof data?.detail === "string") {
        message = data.detail;
      }
    } catch {
      // non-JSON error body — keep the default message
    }
    throw new ApiRequestError(res.status, message);
  }

  if (res.status === 204) {
    return undefined as T;
  }

  return (await res.json()) as T;
}
