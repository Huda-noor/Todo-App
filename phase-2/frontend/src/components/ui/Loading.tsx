"use client";

interface LoadingProps {
  message?: string;
}

export default function Loading({ message }: LoadingProps) {
  return (
    <div className="loading">
      <div className="loading-spinner" />
      {message && (
        <p style={{ marginLeft: "0.75rem", color: "var(--muted)" }}>
          {message}
        </p>
      )}
    </div>
  );
}
