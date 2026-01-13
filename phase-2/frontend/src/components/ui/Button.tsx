"use client";

import { ButtonHTMLAttributes, ReactNode } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: "primary" | "secondary" | "danger";
  size?: "sm" | "md";
  fullWidth?: boolean;
  isLoading?: boolean;
}

export default function Button({
  children,
  variant = "primary",
  size = "md",
  fullWidth = false,
  isLoading = false,
  disabled,
  className = "",
  ...props
}: ButtonProps) {
  const baseClasses = "btn";
  const variantClasses = {
    primary: "btn-primary",
    secondary: "btn-secondary",
    danger: "btn-danger",
  };
  const sizeClasses = size === "sm" ? "btn-sm" : "";
  const widthClasses = fullWidth ? "btn-full" : "";

  const classes = [
    baseClasses,
    variantClasses[variant],
    sizeClasses,
    widthClasses,
    className,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <button className={classes} disabled={disabled || isLoading} {...props}>
      {isLoading ? (
        <span
          style={{
            display: "inline-block",
            width: "1rem",
            height: "1rem",
            border: "2px solid currentColor",
            borderTopColor: "transparent",
            borderRadius: "50%",
            animation: "spin 0.8s linear infinite",
          }}
        />
      ) : (
        children
      )}
    </button>
  );
}
