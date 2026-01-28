"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "@/lib/auth-client";
import Loading from "@/components/ui/Loading";

export default function Home() {
  const router = useRouter();
  const { data: session, isPending } = useSession();

  useEffect(() => {
    if (!isPending) {
      if (session) {
        router.replace("/todos");
      } else {
        router.replace("/signin");
      }
    }
  }, [session, isPending, router]);

  return (
    <div className="auth-page">
      <Loading />
    </div>
  );
}
