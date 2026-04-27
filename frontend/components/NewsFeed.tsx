"use client";

import { ExternalLink, Clock, Tag } from "lucide-react";

interface NewsItem {
  id: string;
  title: string;
  summary: string;
  url: string;
  source: string;
  category: string;
  published?: string;
}

const categoryConfig: Record<string, { label: string; class: string }> = {
  llm: { label: "LLM", class: "badge-llm" },
  image_gen: { label: "Image Gen", class: "badge-image_gen" },
  robotics: { label: "Robotics", class: "badge-robotics" },
  other: { label: "Other", class: "badge-other" },
};

const sourceColors: Record<string, string> = {
  TechCrunch: "text-green-400",
  VentureBeat: "text-blue-400",
  ArXiv: "text-red-400",
  "The Verge": "text-purple-400",
};

function timeAgo(dateStr: string): string {
  if (!dateStr) return "";
  const now = new Date();
  const date = new Date(dateStr);
  const diffMs = now.getTime() - date.getTime();
  const diffH = Math.floor(diffMs / 3600000);
  if (diffH < 1) return "Just now";
  if (diffH < 24) return `${diffH}h ago`;
  const diffD = Math.floor(diffH / 24);
  if (diffD < 7) return `${diffD}d ago`;
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

export default function NewsFeed({
  items,
  loading,
}: {
  items: NewsItem[];
  loading: boolean;
}) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="glass-card p-5 animate-pulse">
            <div className="flex items-center gap-2 mb-3">
              <div className="h-5 w-16 bg-surface-4 rounded-full" />
              <div className="h-4 w-20 bg-surface-4 rounded" />
            </div>
            <div className="h-5 w-3/4 bg-surface-4 rounded mb-2" />
            <div className="h-4 w-full bg-surface-4 rounded mb-1" />
            <div className="h-4 w-2/3 bg-surface-4 rounded" />
          </div>
        ))}
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-center">
        <div className="w-16 h-16 rounded-2xl bg-surface-2 flex items-center justify-center mb-4">
          <Tag className="w-8 h-8 text-muted" />
        </div>
        <h3 className="text-lg font-semibold text-zinc-300 mb-1">No articles found</h3>
        <p className="text-sm text-muted">Try adjusting your search or filters</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {items.map((item, idx) => {
        const cat = categoryConfig[item.category] || categoryConfig.other;
        return (
          <a
            key={item.id}
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            className="glass-card p-5 group animate-slide-up flex flex-col"
            style={{ animationDelay: `${idx * 40}ms` }}
          >
            {/* Meta row */}
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <span className={cat.class}>{cat.label}</span>
                <span className={`text-xs font-medium ${sourceColors[item.source] || "text-zinc-400"}`}>
                  {item.source}
                </span>
              </div>
              {item.published && (
                <div className="flex items-center gap-1 text-xs text-zinc-500">
                  <Clock className="w-3 h-3" />
                  {timeAgo(item.published)}
                </div>
              )}
            </div>

            {/* Title */}
            <h3 className="text-sm font-semibold text-zinc-100 leading-snug mb-2 group-hover:text-accent transition-colors line-clamp-2">
              {item.title}
            </h3>

            {/* Summary */}
            <p className="text-xs text-zinc-400 leading-relaxed line-clamp-3 flex-1">
              {item.summary}
            </p>

            {/* Footer */}
            <div className="flex items-center justify-between mt-4 pt-3 border-t border-white/[0.04]">
              <span className="text-[10px] text-zinc-600 font-mono uppercase tracking-wider">
                {item.source}
              </span>
              <ExternalLink className="w-3.5 h-3.5 text-zinc-600 group-hover:text-accent transition-colors" />
            </div>
          </a>
        );
      })}
    </div>
  );
}
