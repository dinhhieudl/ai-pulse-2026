"use client";

import { Activity, Zap } from "lucide-react";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-white/[0.06] bg-surface-0/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-glow">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <div className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-success rounded-full border-2 border-surface-0 animate-pulse-slow" />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-white">
                AI Pulse
                <span className="text-accent ml-1 font-mono text-sm font-medium">
                  2026
                </span>
              </h1>
              <p className="text-[10px] text-muted font-medium tracking-widest uppercase -mt-0.5">
                Real-time Intelligence
              </p>
            </div>
          </div>

          {/* Status */}
          <div className="flex items-center gap-2 text-xs text-muted">
            <Activity className="w-3.5 h-3.5 text-success" />
            <span className="hidden sm:inline">Live</span>
          </div>
        </div>
      </div>
    </header>
  );
}
