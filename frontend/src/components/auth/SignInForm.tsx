"use client";

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { signIn } from "@/lib/auth-client";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";

interface FormErrors {
  email?: string;
  password?: string;
  general?: string;
}

export default function SignInForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({});

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    if (!email) {
      newErrors.email = "Email is required";
    }

    if (!password) {
      newErrors.password = "Password is required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setErrors({});

    try {
      const result = await signIn.email({
        email,
        password,
      });

      if (result.error) {
        setErrors({ general: "Invalid email or password" });
      } else if (result.data) {
        // Token is automatically stored by auth-client
        router.push("/todos");
      } else {
        setErrors({ general: "Sign in failed. Please try again." });
      }
    } catch (error) {
      setErrors({ general: "An unexpected error occurred. Please try again." });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="card auth-card">
      <h1 className="auth-title">Sign In</h1>

      {errors.general && (
        <div className="alert alert-error">{errors.general}</div>
      )}

      <form onSubmit={handleSubmit}>
        <Input
          label="Email"
          type="email"
          name="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          error={errors.email}
          placeholder="you@example.com"
          autoComplete="email"
          disabled={isLoading}
        />

        <Input
          label="Password"
          type="password"
          name="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          error={errors.password}
          placeholder="Your password"
          autoComplete="current-password"
          disabled={isLoading}
        />

        <Button type="submit" fullWidth isLoading={isLoading}>
          Sign In
        </Button>
      </form>

      <p className="auth-footer">
        Don&apos;t have an account? <Link href="/signup">Sign up</Link>
      </p>
    </div>
  );
}
