"use client";

import { useState } from "react";
import { Link2, Send, Check, Loader2 } from "lucide-react";

export default function SubmitLink() {
  const [url, setUrl] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [result, setResult] = useState("");

  const submit = async () => {
    if (!url.trim()) return;
    setStatus("loading");
    try {
      const res = await fetch("/api/user-links/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url.trim() }),
      });
      const data = await res.json();
      if (res.ok) {
        setStatus("success");
        setResult(data.title || "Link added to news feed!");
        setUrl("");
        setTimeout(() => setStatus("idle"), 3000);
      } else {
        setStatus("error");
        setResult(data.detail || "Failed to submit");
      }
    } catch {
      setStatus("error");
      setResult("Network error");
    }
  };

  return (
    <div className="glass-card p-4">
      <div className="flex items-center gap-2 mb-2">
        <Link2 className="w-4 h-4 text-accent" />
        <span className="text-xs font-semibold text-zinc-300">Submit a Link</span>
      </div>
      <div className="flex gap-2">
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && submit()}
          placeholder="https://example.com/article"
          className="flex-1 px-3 py-2 bg-surface-2 border border-white/[0.06] rounded-xl
                     text-sm text-zinc-100 placeholder:text-zinc-600 focus:outline-none
                     focus:border-accent/40 transition-all"
        />
        <button
          onClick={submit}
          disabled={!url.trim() || status === "loading"}
          className="px-3 py-2 rounded-xl bg-accent/15 border border-accent/30 text-accent
                     hover:bg-accent/25 transition-all disabled:opacity-30"
        >
          {status === "loading" ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : status === "success" ? (
            <Check className="w-4 h-4 text-green-400" />
          ) : (
            <Send className="w-4 h-4" />
          )}
        </button>
      </div>
      {result && (
        <p className={`text-[11px] mt-1.5 ${status === "error" ? "text-red-400" : "text-green-400"}`}>
          {result}
        </p>
      )}
    </div>
  );
}
