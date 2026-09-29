export type OAuthProvider = "github" | "google" | "telegram";

export interface User {
  id: number;
  email: string;
  name: string;
  isActive: boolean;
  isSuperuser?: boolean;
  createdAt: string;
}

export interface AuthSession {
  user: User;
  expiresAt: string;
}
