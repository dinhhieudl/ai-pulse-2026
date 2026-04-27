"use client";

import { Trophy, ArrowUpDown, Crown, Medal, Award, Zap, DollarSign, Gauge } from "lucide-react";

interface ModelEntry {
  rank: number;
  model: string;
  provider: string;
  mmlu_score?: number;
  elo_score?: number;
  arena_elo?: number;
  pricing_input?: string;
  pricing_output?: string;
  speed_tps?: number;
  source?: string;
  released?: string;
  notes?: string;
}

const providerColors: Record<string, string> = {
  OpenAI: "bg-green-500/15 text-green-400 border-green-500/20",
  Anthropic: "bg-orange-500/15 text-orange-400 border-orange-500/20",
  Google: "bg-blue-500/15 text-blue-400 border-blue-500/20",
  Xiaomi: "bg-red-500/15 text-red-400 border-red-500/20",
  Meta: "bg-sky-500/15 text-sky-400 border-sky-500/20",
  "Mistral AI": "bg-yellow-500/15 text-yellow-400 border-yellow-500/20",
  xAI: "bg-purple-500/15 text-purple-400 border-purple-500/20",
  DeepSeek: "bg-teal-500/15 text-teal-400 border-teal-500/20",
  Alibaba: "bg-amber-500/15 text-amber-400 border-amber-500/20",
  Cohere: "bg-indigo-500/15 text-indigo-400 border-indigo-500/20",
  "01.AI": "bg-rose-500/15 text-rose-400 border-rose-500/20",
  Microsoft: "bg-cyan-500/15 text-cyan-400 border-cyan-500/20",
};

const sourceIcons: Record<string, string> = {
  "LMSYS Chatbot Arena": "⚔️",
  "Vellum LLM Leaderboard": "💰",
  "HuggingFace Open LLM Leaderboard": "🤗",
  "Combined": "📊",
};

function RankIcon({ rank }: { rank: number }) {
  if (rank === 1) return <Crown className="w-4 h-4 text-yellow-400" />;
  if (rank === 2) return <Medal className="w-4 h-4 text-zinc-300" />;
  if (rank === 3) return <Award className="w-4 h-4 text-amber-600" />;
  return <span className="text-xs text-muted font-mono w-4 text-center">{rank}</span>;
}

function ScoreBar({ score, max = 100, color = "from-accent to-purple-400" }: { score: number; max?: number; color?: string }) {
  const pct = Math.min(100, Math.max(0, (score / max) * 100));
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 bg-surface-4 rounded-full overflow-hidden max-w-[80px]">
        <div
          className={`h-full rounded-full bg-gradient-to-r ${color} transition-all duration-700`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-sm font-mono font-semibold text-zinc-200">{score}</span>
    </div>
  );
}

function ELOBar({ elo }: { elo: number }) {
  // ELO range ~1200-1400, scale to percentage
  const pct = Math.min(100, Math.max(0, ((elo - 1200) / 200) * 100));
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 bg-surface-4 rounded-full overflow-hidden max-w-[80px]">
        <div
          className="h-full rounded-full bg-gradient-to-r from-amber-400 to-orange-500 transition-all duration-700"
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-sm font-mono font-semibold text-zinc-200">{elo}</span>
    </div>
  );
}

export default function Leaderboard({
  items,
  loading,
}: {
  items: ModelEntry[];
  loading: boolean;
}) {
  if (loading) {
    return (
      <div className="glass-card overflow-hidden">
        <div className="p-4 space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-16 bg-surface-3 rounded-lg animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  // Group by source for summary
  const sourceCounts: Record<string, number> = {};
  items.forEach((item) => {
    const s = item.source || "Unknown";
    sourceCounts[s] = (sourceCounts[s] || 0) + 1;
  });

  return (
    <div className="space-y-4">
      {/* Source summary chips */}
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-[10px] text-zinc-500 uppercase tracking-widest font-semibold">
          {items.length} models from
        </span>
        {Object.entries(sourceCounts).map(([source, count]) => (
          <span
            key={source}
            className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px]
                       font-medium bg-surface-3/60 border border-white/[0.06] text-zinc-400"
          >
            <span>{sourceIcons[source] || "📋"}</span>
            {source} ({count})
          </span>
        ))}
      </div>

      {/* Table */}
      <div className="glass-card overflow-hidden">
        {/* Desktop Table */}
        <div className="hidden md:block overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/[0.06]">
                <th className="px-5 py-3.5 text-left text-[11px] font-semibold text-zinc-500 uppercase tracking-widest w-16">
                  Rank
                </th>
                <th className="px-5 py-3.5 text-left text-[11px] font-semibold text-zinc-500 uppercase tracking-widest">
                  Model
                </th>
                <th className="px-5 py-3.5 text-left text-[11px] font-semibold text-zinc-500 uppercase tracking-widest">
                  Provider
                </th>
                <th className="px-5 py-3.5 text-left text-[11px] font-semibold text-zinc-500 uppercase tracking-widest">
                  <div className="flex items-center gap-1">
                    <Zap className="w-3 h-3" />
                    ELO
                  </div>
                </th>
                <th className="px-5 py-3.5 text-left text-[11px] font-semibold text-zinc-500 uppercase tracking-widest">
                  <div className="flex items-center gap-1">
                    MMLU
                    <ArrowUpDown className="w-3 h-3" />
                  </div>
                </th>
                <th className="px-5 py-3.5 text-left text-[11px] font-semibold text-zinc-500 uppercase tracking-widest">
                  <div className="flex items-center gap-1">
                    <DollarSign className="w-3 h-3" />
                    Pricing
                  </div>
                </th>
                <th className="px-5 py-3.5 text-left text-[11px] font-semibold text-zinc-500 uppercase tracking-widest hidden lg:table-cell">
                  <div className="flex items-center gap-1">
                    <Gauge className="w-3 h-3" />
                    Speed
                  </div>
                </th>
                <th className="px-5 py-3.5 text-left text-[11px] font-semibold text-zinc-500 uppercase tracking-widest hidden xl:table-cell">
                  Source
                </th>
              </tr>
            </thead>
            <tbody>
              {items.map((item, idx) => {
                const pColor = providerColors[item.provider] || "bg-zinc-500/15 text-zinc-400 border-zinc-500/20";
                return (
                  <tr
                    key={`${item.model}-${item.source}-${idx}`}
                    className="border-b border-white/[0.03] hover:bg-white/[0.02] transition-colors animate-slide-up"
                    style={{ animationDelay: `${idx * 25}ms` }}
                  >
                    <td className="px-5 py-4">
                      <RankIcon rank={item.rank} />
                    </td>
                    <td className="px-5 py-4">
                      <div>
                        <span className="text-sm font-semibold text-zinc-100">{item.model}</span>
                        {item.notes && (
                          <p className="text-[10px] text-zinc-600 mt-0.5 max-w-[200px] truncate">{item.notes}</p>
                        )}
                      </div>
                    </td>
                    <td className="px-5 py-4">
                      <span className={`badge border ${pColor}`}>{item.provider}</span>
                    </td>
                    <td className="px-5 py-4">
                      {(item.elo_score || item.arena_elo) ? (
                        <ELOBar elo={item.elo_score || item.arena_elo || 0} />
                      ) : (
                        <span className="text-xs text-zinc-600">—</span>
                      )}
                    </td>
                    <td className="px-5 py-4">
                      {item.mmlu_score ? (
                        <ScoreBar score={item.mmlu_score} />
                      ) : (
                        <span className="text-xs text-zinc-600">—</span>
                      )}
                    </td>
                    <td className="px-5 py-4">
                      <div className="text-xs">
                        <div className="text-zinc-300 font-mono">In: {item.pricing_input || "—"}</div>
                        <div className="text-zinc-500 font-mono">Out: {item.pricing_output || "—"}</div>
                      </div>
                    </td>
                    <td className="px-5 py-4 hidden lg:table-cell">
                      {item.speed_tps ? (
                        <span className="text-xs font-mono text-zinc-300">{item.speed_tps} tok/s</span>
                      ) : (
                        <span className="text-xs text-zinc-600">—</span>
                      )}
                    </td>
                    <td className="px-5 py-4 hidden xl:table-cell">
                      <span className="text-[10px] text-zinc-500">
                        {sourceIcons[item.source || ""] || ""} {item.source || "—"}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Mobile Cards */}
        <div className="md:hidden divide-y divide-white/[0.04]">
          {items.map((item, idx) => {
            const pColor = providerColors[item.provider] || "bg-zinc-500/15 text-zinc-400 border-zinc-500/20";
            return (
              <div
                key={`${item.model}-${item.source}-${idx}`}
                className="p-4 animate-slide-up"
                style={{ animationDelay: `${idx * 25}ms` }}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <RankIcon rank={item.rank} />
                    <span className="text-sm font-semibold text-zinc-100">{item.model}</span>
                  </div>
                  <span className={`badge border text-[10px] ${pColor}`}>{item.provider}</span>
                </div>

                {/* Scores */}
                <div className="grid grid-cols-2 gap-2 mb-2">
                  {(item.elo_score || item.arena_elo) && (
                    <div>
                      <span className="text-[10px] text-zinc-500 uppercase">ELO</span>
                      <ELOBar elo={item.elo_score || item.arena_elo || 0} />
                    </div>
                  )}
                  {item.mmlu_score && (
                    <div>
                      <span className="text-[10px] text-zinc-500 uppercase">MMLU</span>
                      <ScoreBar score={item.mmlu_score} />
                    </div>
                  )}
                </div>

                {/* Pricing + Speed */}
                <div className="flex items-center justify-between text-xs text-zinc-500">
                  <span className="font-mono">
                    {item.pricing_input || "—"} / {item.pricing_output || "—"}
                  </span>
                  {item.speed_tps && (
                    <span className="font-mono">{item.speed_tps} tok/s</span>
                  )}
                </div>

                {/* Source + Notes */}
                <div className="flex items-center justify-between mt-1.5">
                  <span className="text-[10px] text-zinc-600">
                    {sourceIcons[item.source || ""] || ""} {item.source || ""}
                  </span>
                  {item.notes && (
                    <span className="text-[10px] text-zinc-600 max-w-[150px] truncate">{item.notes}</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
