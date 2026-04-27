"use client";

import { useState, useEffect } from "react";
import { Newspaper, Calendar, Send } from "lucide-react";

interface DigestNews {
  title: string;
  url: string;
  source: string;
  category: string;
  sentiment: string;
}

interface DigestData {
  date?: string;
  period?: string;
  news: DigestNews[];
  top_models?: { rank: number; model: string; provider: string; elo_score?: number }[];
  total_articles?: number;
  by_category?: Record<string, number>;
}

export default function DigestView() {
  const [type, setType] = useState<"daily" | "weekly">("daily");
  const [data, setData] = useState<DigestData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/digest/${type}`)
      .then((r) => r.json())
      .then(setData)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [type]);

  const sentimentEmoji: Record<string, string> = {
    launch: "🚀", funding: "💰", update: "⬆️", research: "🔬",
    positive: "✅", negative: "⚠️", neutral: "📌",
  };

  return (
    <div className="glass-card p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-zinc-200 flex items-center gap-2">
          <Newspaper className="w-4 h-4 text-accent" />
          AI Digest
        </h3>
        <div className="flex gap-1 p-0.5 bg-surface-3 rounded-lg">
          {(["daily", "weekly"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setType(t)}
              className={`px-3 py-1 rounded-md text-xs font-medium transition-all ${
                type === t ? "bg-accent/15 text-accent" : "text-zinc-500 hover:text-white"
              }`}
            >
              {t === "daily" ? "Today" : "This Week"}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="space-y-2">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-12 bg-surface-3 rounded-lg animate-pulse" />
          ))}
        </div>
      ) : !data || data.news.length === 0 ? (
        <div className="text-center py-8 text-sm text-zinc-500">
          No digest data yet. Will populate after scraping.
        </div>
      ) : (
        <div className="space-y-4">
          {data.total_articles && (
            <div className="text-[10px] text-zinc-500 uppercase tracking-widest">
              {data.total_articles} articles · {data.period || data.date}
            </div>
          )}

          {/* Category breakdown */}
          {data.by_category && (
            <div className="flex flex-wrap gap-2">
              {Object.entries(data.by_category).map(([cat, count]) => (
                <span
                  key={cat}
                  className="px-2 py-0.5 rounded-full text-[10px] font-medium bg-surface-3/60 border border-white/[0.06] text-zinc-400"
                >
                  {cat}: {count}
                </span>
              ))}
            </div>
          )}

          {/* News list */}
          <div className="space-y-2">
            {data.news.map((n, i) => (
              <a
                key={i}
                href={n.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-start gap-2 p-2.5 rounded-lg hover:bg-white/[0.02] transition-colors group"
              >
                <span className="text-sm mt-0.5">{sentimentEmoji[n.sentiment] || "📌"}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-medium text-zinc-200 group-hover:text-accent transition-colors line-clamp-2">
                    {n.title}
                  </p>
                  <p className="text-[10px] text-zinc-500 mt-0.5">{n.source}</p>
                </div>
              </a>
            ))}
          </div>

          {/* Top models */}
          {data.top_models && data.top_models.length > 0 && (
            <div className="pt-3 border-t border-white/[0.04]">
              <h4 className="text-[10px] text-zinc-500 uppercase tracking-widest font-semibold mb-2">
                🏆 Top Models
              </h4>
              <div className="space-y-1">
                {data.top_models.map((m) => (
                  <div key={m.model} className="flex items-center justify-between text-xs">
                    <span className="text-zinc-300">
                      <span className="text-zinc-500 font-mono mr-1.5">#{m.rank}</span>
                      {m.model}
                      <span className="text-zinc-500 ml-1">({m.provider})</span>
                    </span>
                    {m.elo_score && (
                      <span className="text-zinc-400 font-mono text-[11px]">ELO {m.elo_score}</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
