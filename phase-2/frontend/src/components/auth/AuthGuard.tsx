"use client";

import { useEffect, ReactNode, useState } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "@/lib/auth-client";
import Loading from "@/components/ui/Loading";

interface AuthGuardProps {
  children: ReactNode;
}

export default function AuthGuard({ children }: AuthGuardProps) {
  const router = useRouter();
  const { data: session, isPending } = useSession();
  const [mounted, setMounted] = useState(false);

  // Ensure component is mounted before rendering
  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (mounted && !isPending && !session) {
      router.replace("/signin");
    }
  }, [session, isPending, router, mounted]);

  if (!mounted) {
    return null;
  }

  if (isPending) {
    return (
      <div className="auth-page">
        <Loading message="Checking authentication..." />
      </div>
    );
  }

  if (!session) {
    return null;
  }

  return <>{children}</>;
}
