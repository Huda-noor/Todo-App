import { forwardToNeonAuth } from "@/lib/auth";

/**
 * Auth API Route Handler
 *
 * Proxies all auth requests to Neon Auth service.
 * Neon Auth handles user registration, login, session management externally.
 */

export async function GET(request: Request) {
  return forwardToNeonAuth(request);
}

export async function POST(request: Request) {
  return forwardToNeonAuth(request);
}
