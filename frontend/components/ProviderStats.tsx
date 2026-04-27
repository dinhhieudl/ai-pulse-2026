"use client";

import { useState, useEffect } from "react";
import { BarChart3 } from "lucide-react";

interface StatItem {
  source?: string;
  category?: string;
  sentiment?: string;
  count: number;
}

const SENTIMENT_COLORS: Record<string, string> = {
  launch: "bg-green-400",
  funding: "bg-yellow-400",
  update: "bg-blue-400",
  research: "bg-purple-400",
  positive: "bg-emerald-400",
  negative: "bg-red-400",
  neutral: "bg-zinc-400",
};

const CATEGORY_COLORS: Record<string, string> = {
  llm: "bg-cyan-400",
  image_gen: "bg-pink-400",
  robotics: "bg-orange-400",
  other: "bg-zinc-400",
};

export default function ProviderStats() {
  const [stats, setStats] = useState<{
    by_source: StatItem[];
    by_category: StatItem[];
    by_sentiment: StatItem[];
  } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/trends/providers?days=30")
      .then((r) => r.json())
      .then(setStats)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="glass-card p-5">
        <div className="h-32 bg-surface-3 rounded-lg animate-pulse" />
      </div>
    );
  }

  if (!stats) return null;

  const maxSource = Math.max(...stats.by_source.map((s) => s.count), 1);
  const maxSentiment = Math.max(...stats.by_sentiment.map((s) => s.count), 1);

  return (
    <div className="glass-card p-5">
      <h3 className="text-sm font-semibold text-zinc-200 flex items-center gap-2 mb-4">
        <BarChart3 className="w-4 h-4 text-accent" />
        Coverage Stats (30d)
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* By Source */}
        <div>
          <h4 className="text-[10px] text-zinc-500 uppercase tracking-widest font-semibold mb-3">
            By Source
          </h4>
          <div className="space-y-2">
            {stats.by_source.slice(0, 8).map((s) => (
              <div key={s.source}>
                <div className="flex justify-between text-[11px] mb-0.5">
                  <span className="text-zinc-400">{s.source}</span>
                  <span className="text-zinc-300 font-mono">{s.count}</span>
                </div>
                <div className="h-1.5 bg-surface-4 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-accent to-purple-400"
                    style={{ width: `${(s.count / maxSource) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* By Category */}
        <div>
          <h4 className="text-[10px] text-zinc-500 uppercase tracking-widest font-semibold mb-3">
            By Category
          </h4>
          <div className="space-y-2">
            {stats.by_category.map((s) => (
              <div key={s.category} className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${CATEGORY_COLORS[s.category || ""] || "bg-zinc-400"}`} />
                <span className="text-xs text-zinc-400 flex-1">{s.category}</span>
                <span className="text-xs text-zinc-300 font-mono">{s.count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* By Sentiment */}
        <div>
          <h4 className="text-[10px] text-zinc-500 uppercase tracking-widest font-semibold mb-3">
            By Sentiment
          </h4>
          <div className="space-y-2">
            {stats.by_sentiment.map((s) => (
              <div key={s.sentiment}>
                <div className="flex justify-between text-[11px] mb-0.5">
                  <span className="text-zinc-400 capitalize">{s.sentiment}</span>
                  <span className="text-zinc-300 font-mono">{s.count}</span>
                </div>
                <div className="h-1.5 bg-surface-4 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full ${SENTIMENT_COLORS[s.sentiment || ""] || "bg-zinc-400"}`}
                    style={{ width: `${(s.count / maxSentiment) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
