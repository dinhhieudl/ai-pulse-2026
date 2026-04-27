"use client";

import { useState, useEffect } from "react";
import { GitCompareArrows, X, Plus, Search } from "lucide-react";
import { fetchAllModels, compareModels } from "@/lib/api";

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

const DEMO_MODELS: Model[] = [
  { model: "GPT-5.5", provider: "OpenAI", elo_score: 1352, mmlu_score: 93.2, pricing_input: "$15.00", pricing_output: "$45.00", speed_tps: 85, notes: "Multimodal, native tool use, best overall" },
  { model: "Claude 4.7 Opus", provider: "Anthropic", elo_score: 1348, mmlu_score: 92.8, pricing_input: "$20.00", pricing_output: "$60.00", speed_tps: 62, notes: "200K context, safety-first, best reasoning" },
  { model: "Gemini 2.5 Ultra", provider: "Google", elo_score: 1341, mmlu_score: 92.5, pricing_input: "$12.00", pricing_output: "$36.00", speed_tps: 92, notes: "Native multimodal, fast inference" },
  { model: "MiMo-V2-Pro", provider: "Xiaomi", elo_score: 1332, mmlu_score: 91.8, pricing_input: "$8.00", pricing_output: "$24.00", speed_tps: 78, notes: "Efficient reasoning, edge-ready, great value" },
  { model: "Grok-3", provider: "xAI", elo_score: 1325, mmlu_score: 90.1, pricing_input: "$10.00", pricing_output: "$30.00", speed_tps: 88, notes: "Real-time web knowledge, X integrated" },
  { model: "Llama 4 405B", provider: "Meta", elo_score: 1318, mmlu_score: 91.0, pricing_input: "Free (open)", pricing_output: "Free (open)", speed_tps: 45, notes: "Best open-weight, MoE architecture" },
  { model: "DeepSeek-V3", provider: "DeepSeek", elo_score: 1310, mmlu_score: 89.7, pricing_input: "$2.00", pricing_output: "$6.00", speed_tps: 95, notes: "Ultra-low cost, strong coding" },
  { model: "Mistral Large 3", provider: "Mistral AI", elo_score: 1305, mmlu_score: 90.5, pricing_input: "$6.00", pricing_output: "$18.00", speed_tps: 72, notes: "European sovereignty focus" },
  { model: "Qwen-3 72B", provider: "Alibaba", elo_score: 1298, mmlu_score: 88.8, pricing_input: "$4.00", pricing_output: "$12.00", speed_tps: 68, notes: "Multilingual, open-weight" },
  { model: "Command R++", provider: "Cohere", elo_score: 1290, mmlu_score: 89.2, pricing_input: "$5.00", pricing_output: "$15.00", speed_tps: 75, notes: "RAG-native, enterprise optimized" },
];

export default function ModelCompare() {
  const [allModels, setAllModels] = useState<Model[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [compared, setCompared] = useState<Model[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    fetchAllModels()
      .then((d) => setAllModels(d.models || []))
      .catch(() => setAllModels(DEMO_MODELS));
  }, []);

  const doCompare = async () => {
    if (selected.length < 2) return;
    setLoading(true);
    try {
      const data = await compareModels(selected);
      setCompared(data.items || []);
    } catch {
      // Fallback: filter from local data
      setCompared(allModels.filter((m) => selected.includes(m.model)));
    }
    setLoading(false);
  };

  const toggle = (model: string) => {
    setSelected((prev) =>
      prev.includes(model) ? prev.filter((m) => m !== model) : [...prev, model].slice(0, 4)
    );
  };

  // Filter models by search query
  const filteredModels = searchQuery
    ? allModels.filter(
        (m) =>
          m.model.toLowerCase().includes(searchQuery.toLowerCase()) ||
          m.provider.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : allModels;

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

      {/* Search input */}
      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted" />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search models by name or provider..."
          className="w-full pl-10 pr-10 py-2.5 bg-surface-2 border border-white/[0.06] rounded-xl
                     text-sm text-zinc-100 placeholder:text-zinc-500 focus:outline-none
                     focus:border-accent/40 focus:ring-1 focus:ring-accent/20 transition-all"
        />
        {searchQuery && (
          <button
            onClick={() => setSearchQuery("")}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted hover:text-white"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Model picker */}
      <div className="flex flex-wrap gap-2 mb-4">
        {filteredModels.length === 0 && (
          <p className="text-xs text-zinc-500 py-2">
            {searchQuery ? `No models matching "${searchQuery}"` : "No models available"}
          </p>
        )}
        {filteredModels.map((m) => (
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
            <span className="ml-1.5 text-[10px] text-zinc-600">{m.provider}</span>
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

      {/* Hint when less than 2 selected */}
      {selected.length < 2 && selected.length > 0 && (
        <p className="text-xs text-zinc-500 mt-2">Select at least {2 - selected.length} more model to compare</p>
      )}
    </div>
  );
}
