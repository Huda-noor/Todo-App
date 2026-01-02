"use client";

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { signUp } from "@/lib/auth-client";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";

interface FormErrors {
  email?: string;
  password?: string;
  general?: string;
}

export default function SignUpForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({});

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    if (!email) {
      newErrors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = "Please enter a valid email address";
    }

    if (!password) {
      newErrors.password = "Password is required";
    } else if (password.length < 8) {
      newErrors.password = "Password must be at least 8 characters";
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
      const result = await signUp.email({
        email,
        password,
        name: email.split("@")[0], // Use email prefix as name
      });

      if (result.error) {
        if (result.error.message?.includes("already exists") || result.error.code === "USER_ALREADY_EXISTS") {
          setErrors({ email: "An account with this email already exists" });
        } else {
          setErrors({ general: result.error.message || "Sign up failed" });
        }
      } else if (result.data) {
        // Token is automatically stored by auth-client
        router.push("/todos");
      } else {
        setErrors({ general: "Sign up failed. Please try again." });
      }
    } catch (error) {
      setErrors({ general: "An unexpected error occurred. Please try again." });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="card auth-card">
      <h1 className="auth-title">Create Account</h1>

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
          placeholder="At least 8 characters"
          autoComplete="new-password"
          disabled={isLoading}
        />

        <Button type="submit" fullWidth isLoading={isLoading}>
          Sign Up
        </Button>
      </form>

      <p className="auth-footer">
        Already have an account? <Link href="/signin">Sign in</Link>
      </p>
    </div>
  );
}
