"use client";

import { useState, useEffect } from "react";
import { Calculator, DollarSign } from "lucide-react";

interface Model {
  model: string;
  provider: string;
  pricing_input?: string;
  pricing_output?: string;
}

function parsePrice(p: string | undefined): number {
  if (!p) return 0;
  const match = p.match(/[\d.]+/);
  return match ? parseFloat(match[0]) : 0;
}

export default function PriceCalculator() {
  const [models, setModels] = useState<Model[]>([]);
  const [selected, setSelected] = useState("");
  const [inputTokens, setInputTokens] = useState(10000);
  const [outputTokens, setOutputTokens] = useState(5000);

  useEffect(() => {
    fetch("/api/compare/all")
      .then((r) => r.json())
      .then((d) => {
        const ms = d.models || [];
        setModels(ms);
        if (ms.length > 0) setSelected(ms[0].model);
      })
      .catch(() => {});
  }, []);

  const model = models.find((m) => m.model === selected);
  const inputPrice = parsePrice(model?.pricing_input);
  const outputPrice = parsePrice(model?.pricing_output);
  const inputCost = (inputTokens / 1_000_000) * inputPrice;
  const outputCost = (outputTokens / 1_000_000) * outputPrice;
  const totalCost = inputCost + outputCost;

  return (
    <div className="glass-card p-5">
      <h3 className="text-sm font-semibold text-zinc-200 flex items-center gap-2 mb-4">
        <Calculator className="w-4 h-4 text-accent" />
        Price Calculator
      </h3>

      {/* Model selector */}
      <div className="mb-4">
        <label className="text-[10px] text-zinc-500 uppercase tracking-widest font-semibold block mb-1.5">
          Model
        </label>
        <select
          value={selected}
          onChange={(e) => setSelected(e.target.value)}
          className="w-full px-3 py-2 bg-surface-2 border border-white/[0.06] rounded-xl
                     text-sm text-zinc-100 focus:outline-none focus:border-accent/40"
        >
          {models.map((m) => (
            <option key={m.model} value={m.model}>
              {m.model} ({m.provider})
            </option>
          ))}
        </select>
      </div>

      {/* Token inputs */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div>
          <label className="text-[10px] text-zinc-500 uppercase tracking-widest font-semibold block mb-1.5">
            Input Tokens
          </label>
          <input
            type="number"
            value={inputTokens}
            onChange={(e) => setInputTokens(Number(e.target.value))}
            className="w-full px-3 py-2 bg-surface-2 border border-white/[0.06] rounded-xl
                       text-sm text-zinc-100 font-mono focus:outline-none focus:border-accent/40"
          />
        </div>
        <div>
          <label className="text-[10px] text-zinc-500 uppercase tracking-widest font-semibold block mb-1.5">
            Output Tokens
          </label>
          <input
            type="number"
            value={outputTokens}
            onChange={(e) => setOutputTokens(Number(e.target.value))}
            className="w-full px-3 py-2 bg-surface-2 border border-white/[0.06] rounded-xl
                       text-sm text-zinc-100 font-mono focus:outline-none focus:border-accent/40"
          />
        </div>
      </div>

      {/* Results */}
      <div className="space-y-2 p-3 bg-surface-3/30 rounded-xl border border-white/[0.04]">
        <div className="flex justify-between text-xs">
          <span className="text-zinc-400">Input cost</span>
          <span className="text-zinc-200 font-mono">${inputCost.toFixed(6)}</span>
        </div>
        <div className="flex justify-between text-xs">
          <span className="text-zinc-400">Output cost</span>
          <span className="text-zinc-200 font-mono">${outputCost.toFixed(6)}</span>
        </div>
        <div className="border-t border-white/[0.06] pt-2 flex justify-between">
          <span className="text-sm font-semibold text-zinc-300 flex items-center gap-1">
            <DollarSign className="w-3 h-3" />
            Total
          </span>
          <span className="text-sm font-bold text-accent font-mono">${totalCost.toFixed(6)}</span>
        </div>
        <div className="text-[10px] text-zinc-600 text-right">
          ≈ ${(totalCost * 1000).toFixed(4)} per 1K requests
        </div>
      </div>
    </div>
  );
}
