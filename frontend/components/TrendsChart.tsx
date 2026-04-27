"use client";

import { useState, useEffect } from "react";
import { TrendingUp } from "lucide-react";

interface TrendPoint {
  date: string;
  mmlu_score?: number;
  elo_score?: number;
  speed_tps?: number;
}

interface TrendData {
  model: string;
  provider: string;
  data_points: TrendPoint[];
}

const COLORS = [
  "#22d3ee", "#f472b6", "#a78bfa", "#34d399", "#fbbf24",
  "#fb923c", "#60a5fa", "#e879f9", "#4ade80", "#f87171",
];

export default function TrendsChart() {
  const [data, setData] = useState<TrendData[]>([]);
  const [metric, setMetric] = useState<"elo_score" | "mmlu_score" | "speed_tps">("elo_score");
  const [days, setDays] = useState(30);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/trends/models?days=${days}`)
      .then((r) => r.json())
      .then((d) => setData(d.items || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [days]);

  if (loading) {
    return (
      <div className="glass-card p-5">
        <div className="h-64 bg-surface-3 rounded-lg animate-pulse" />
      </div>
    );
  }

  // Simple SVG chart
  const allDates = [...new Set(data.flatMap((d) => d.data_points.map((p) => p.date)))].sort();
  const maxVal = Math.max(
    ...data.flatMap((d) => d.data_points.map((p) => (p as any)[metric] || 0)),
    1
  );
  const minVal = Math.min(
    ...data.flatMap((d) => d.data_points.map((p) => (p as any)[metric] || Infinity)),
    0
  );
  const range = maxVal - minVal || 1;

  const w = 600;
  const h = 200;
  const pad = { top: 10, right: 10, bottom: 30, left: 50 };
  const chartW = w - pad.left - pad.right;
  const chartH = h - pad.top - pad.bottom;

  const xScale = (i: number) => pad.left + (i / Math.max(allDates.length - 1, 1)) * chartW;
  const yScale = (v: number) => pad.top + chartH - ((v - minVal) / range) * chartH;

  const metricLabels: Record<string, string> = {
    elo_score: "ELO Score",
    mmlu_score: "MMLU Score",
    speed_tps: "Speed (tok/s)",
  };

  return (
    <div className="glass-card p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-zinc-200 flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-accent" />
          Model Trends
        </h3>
        <div className="flex items-center gap-2">
          {(["elo_score", "mmlu_score", "speed_tps"] as const).map((m) => (
            <button
              key={m}
              onClick={() => setMetric(m)}
              className={`px-2 py-1 rounded text-[10px] font-medium border transition-all ${
                metric === m
                  ? "bg-accent/15 border-accent/30 text-accent"
                  : "bg-surface-3/50 border-white/5 text-zinc-500 hover:text-white"
              }`}
            >
              {metricLabels[m]}
            </button>
          ))}
          <select
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
            className="px-2 py-1 bg-surface-2 border border-white/[0.06] rounded text-[10px] text-zinc-300"
          >
            <option value={7}>7d</option>
            <option value={30}>30d</option>
            <option value={90}>90d</option>
          </select>
        </div>
      </div>

      {data.length === 0 ? (
        <div className="h-48 flex items-center justify-center text-sm text-zinc-500">
          No trend data yet. Trends will appear after the first scrape cycle.
        </div>
      ) : (
        <div className="overflow-x-auto">
          <svg viewBox={`0 0 ${w} ${h}`} className="w-full h-auto">
            {/* Grid lines */}
            {[0, 0.25, 0.5, 0.75, 1].map((pct) => {
              const y = pad.top + chartH * (1 - pct);
              const val = minVal + range * pct;
              return (
                <g key={pct}>
                  <line x1={pad.left} y1={y} x2={w - pad.right} y2={y} stroke="rgba(255,255,255,0.04)" />
                  <text x={pad.left - 5} y={y + 3} textAnchor="end" fill="#71717a" fontSize="9">
                    {val.toFixed(metric === "speed_tps" ? 0 : 1)}
                  </text>
                </g>
              );
            })}

            {/* X-axis labels */}
            {allDates.filter((_, i) => i % Math.max(1, Math.floor(allDates.length / 6)) === 0).map((date) => {
              const idx = allDates.indexOf(date);
              return (
                <text key={date} x={xScale(idx)} y={h - 5} textAnchor="middle" fill="#71717a" fontSize="9">
                  {date.slice(5)}
                </text>
              );
            })}

            {/* Lines */}
            {data.map((series, si) => {
              const points = allDates.map((date) => {
                const dp = series.data_points.find((p) => p.date === date);
                return dp ? (dp as any)[metric] : null;
              });

              const pathD = points
                .map((v, i) => {
                  if (v === null) return null;
                  const cmd = i === 0 || points.slice(0, i).every((p) => p === null) ? "M" : "L";
                  return `${cmd}${xScale(i)},${yScale(v)}`;
                })
                .filter(Boolean)
                .join(" ");

              return (
                <g key={series.model}>
                  <path d={pathD} fill="none" stroke={COLORS[si % COLORS.length]} strokeWidth="2" />
                  {/* Dots */}
                  {points.map((v, i) =>
                    v !== null ? (
                      <circle
                        key={i}
                        cx={xScale(i)}
                        cy={yScale(v)}
                        r="3"
                        fill={COLORS[si % COLORS.length]}
                      />
                    ) : null
                  )}
                </g>
              );
            })}
          </svg>

          {/* Legend */}
          <div className="flex flex-wrap gap-3 mt-3">
            {data.map((series, si) => (
              <div key={series.model} className="flex items-center gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: COLORS[si % COLORS.length] }} />
                <span className="text-[10px] text-zinc-400">{series.model}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
