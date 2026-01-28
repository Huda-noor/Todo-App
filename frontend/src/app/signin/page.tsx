"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "@/lib/auth-client";
import SignInForm from "@/components/auth/SignInForm";
import Loading from "@/components/ui/Loading";

export default function SignInPage() {
  const router = useRouter();
  const { data: session, isPending } = useSession();

  useEffect(() => {
    if (!isPending && session) {
      router.replace("/todos");
    }
  }, [session, isPending, router]);

  if (isPending) {
    return (
      <div className="auth-page">
        <Loading />
      </div>
    );
  }

  if (session) {
    return null;
  }

  return (
    <div className="auth-page">
      <SignInForm />
    </div>
  );
}
