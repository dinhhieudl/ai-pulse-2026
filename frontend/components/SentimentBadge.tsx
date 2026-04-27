"use client";

const sentimentConfig: Record<string, { emoji: string; label: string; class: string }> = {
  launch: { emoji: "🚀", label: "Launch", class: "bg-green-500/15 text-green-400 border-green-500/20" },
  funding: { emoji: "💰", label: "Funding", class: "bg-yellow-500/15 text-yellow-400 border-yellow-500/20" },
  update: { emoji: "⬆️", label: "Update", class: "bg-blue-500/15 text-blue-400 border-blue-500/20" },
  research: { emoji: "🔬", label: "Research", class: "bg-purple-500/15 text-purple-400 border-purple-500/20" },
  positive: { emoji: "✅", label: "Positive", class: "bg-emerald-500/15 text-emerald-400 border-emerald-500/20" },
  negative: { emoji: "⚠️", label: "Negative", class: "bg-red-500/15 text-red-400 border-red-500/20" },
  neutral: { emoji: "📌", label: "General", class: "bg-zinc-500/15 text-zinc-400 border-zinc-500/20" },
};

export default function SentimentBadge({ sentiment }: { sentiment?: string }) {
  const config = sentimentConfig[sentiment || "neutral"] || sentimentConfig.neutral;
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium border ${config.class}`}>
      <span>{config.emoji}</span>
      {config.label}
    </span>
  );
}
