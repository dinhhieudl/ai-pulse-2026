"use client";

import { useState, useEffect } from "react";
import { GitCompareArrows, X, Plus } from "lucide-react";

interface Model {
  model: string;
  provider: string;
  elo_score?: number;
  mmlu_score?: number;
  pricing_input?: string;
  pricing_output?: string;
  speed_tps?: number;
  notes?: string;
}

export default function ModelCompare() {
  const [allModels, setAllModels] = useState<Model[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [compared, setCompared] = useState<Model[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch("/api/compare/all")
      .then((r) => r.json())
      .then((d) => setAllModels(d.models || []))
      .catch(() => {});
  }, []);

  const doCompare = async () => {
    if (selected.length < 2) return;
    setLoading(true);
    try {
      const res = await fetch(`/api/compare/?models=${selected.join(",")}`);
      const data = await res.json();
      setCompared(data.items || []);
    } catch {}
    setLoading(false);
  };

  const toggle = (model: string) => {
    setSelected((prev) =>
      prev.includes(model) ? prev.filter((m) => m !== model) : [...prev, model].slice(0, 4)
    );
  };

  const metrics = [
    { key: "elo_score", label: "ELO Score", format: (v: any) => v ?? "—" },
    { key: "mmlu_score", label: "MMLU", format: (v: any) => v ?? "—" },
    { key: "pricing_input", label: "Input Price", format: (v: any) => v ?? "—" },
    { key: "pricing_output", label: "Output Price", format: (v: any) => v ?? "—" },
    { key: "speed_tps", label: "Speed", format: (v: any) => v ? `${v} tok/s` : "—" },
    { key: "notes", label: "Notes", format: (v: any) => v ?? "—" },
  ];

  return (
    <div className="glass-card p-5">
      <h3 className="text-sm font-semibold text-zinc-200 flex items-center gap-2 mb-4">
        <GitCompareArrows className="w-4 h-4 text-accent" />
        Compare Models (pick 2–4)
      </h3>

      {/* Model picker */}
      <div className="flex flex-wrap gap-2 mb-4">
        {allModels.map((m) => (
          <button
            key={m.model}
            onClick={() => toggle(m.model)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
              selected.includes(m.model)
                ? "bg-accent/15 border-accent/30 text-accent"
                : "bg-surface-3/50 border-white/5 text-zinc-400 hover:text-white hover:bg-surface-3"
            }`}
          >
            {selected.includes(m.model) && <span className="mr-1">✓</span>}
            {m.model}
          </button>
        ))}
      </div>

      {/* Compare button */}
      <button
        onClick={doCompare}
        disabled={selected.length < 2 || loading}
        className="px-4 py-2 rounded-lg text-sm font-medium bg-accent/15 border border-accent/30
                   text-accent hover:bg-accent/25 transition-all disabled:opacity-30 disabled:cursor-not-allowed mb-4"
      >
        {loading ? "Comparing..." : `Compare ${selected.length} Models`}
      </button>

      {/* Comparison table */}
      {compared.length >= 2 && (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-white/[0.06]">
                <th className="px-3 py-2 text-left text-[11px] text-zinc-500 uppercase">Metric</th>
                {compared.map((m) => (
                  <th key={m.model} className="px-3 py-2 text-center text-[11px] text-zinc-300 font-semibold">
                    {m.model}
                    <div className="text-[10px] text-zinc-500 font-normal">{m.provider}</div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {metrics.map((metric) => (
                <tr key={metric.key} className="border-b border-white/[0.03]">
                  <td className="px-3 py-2.5 text-xs text-zinc-400">{metric.label}</td>
                  {compared.map((m) => (
                    <td key={m.model} className="px-3 py-2.5 text-center text-xs text-zinc-200 font-mono">
                      {metric.format((m as any)[metric.key])}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
