import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Pulse 2026 — Real-time AI Intelligence",
  description:
    "Stay ahead of the AI curve. Live news feed, model leaderboard, and benchmark tracking — all in one dashboard.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-surface-0">
        {children}
      </body>
    </html>
  );
}
