"use client";

import { useState, useEffect, useCallback } from "react";
import { Newspaper, Trophy, Search, Filter, RefreshCw, X, Database } from "lucide-react";
import NewsFeed from "./NewsFeed";
import Leaderboard from "./Leaderboard";
import { fetchNews, fetchLeaderboard, triggerScrape } from "@/lib/api";

type Tab = "news" | "leaderboard";

const NEWS_SOURCES = [
  "All", "The Rundown AI", "MIT Technology Review", "Wired",
  "VentureBeat", "ArXiv",
];
const CATEGORIES = ["All", "LLM", "Image Gen", "Robotics"];
const LB_SOURCES = ["All", "LMSYS Chatbot Arena", "Vellum LLM Leaderboard", "HuggingFace Open LLM Leaderboard"];
const PROVIDERS = [
  "All", "OpenAI", "Anthropic", "Google", "Xiaomi", "Meta",
  "Mistral AI", "xAI", "DeepSeek", "Alibaba", "Cohere",
];

export default function Dashboard() {
  const [tab, setTab] = useState<Tab>("news");
  const [newsItems, setNewsItems] = useState<any[]>([]);
  const [leaderboardItems, setLeaderboardItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [scraping, setScraping] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [selectedNewsSource, setSelectedNewsSource] = useState("All");
  const [selectedProvider, setSelectedProvider] = useState("All");
  const [selectedLbSource, setSelectedLbSource] = useState("All");
  const [showFilters, setShowFilters] = useState(false);

  const loadNews = useCallback(async () => {
    setLoading(true);
    try {
      const catMap: Record<string, string> = {
        "All": "", "LLM": "llm", "Image Gen": "image_gen", "Robotics": "robotics",
      };
      const data = await fetchNews({
        category: catMap[selectedCategory] || undefined,
        source: selectedNewsSource !== "All" ? selectedNewsSource : undefined,
        q: searchQuery || undefined,
        limit: 50,
      });
      setNewsItems(data.items || []);
    } catch (e) {
      console.error("Failed to load news:", e);
      setNewsItems(DEMO_NEWS);
    }
    setLoading(false);
  }, [searchQuery, selectedCategory, selectedNewsSource]);

  const loadLeaderboard = useCallback(async () => {
    setLoading(true);
    try {
      const data = await fetchLeaderboard({
        provider: selectedProvider !== "All" ? selectedProvider : undefined,
        source: selectedLbSource !== "All" ? selectedLbSource : undefined,
        q: searchQuery || undefined,
      });
      setLeaderboardItems(data.items || []);
    } catch (e) {
      console.error("Failed to load leaderboard:", e);
      setLeaderboardItems([]);
    }
    setLoading(false);
  }, [searchQuery, selectedProvider, selectedLbSource]);

  useEffect(() => {
    if (tab === "news") loadNews();
    else loadLeaderboard();
  }, [tab, loadNews, loadLeaderboard]);

  const handleScrape = async () => {
    setScraping(true);
    try {
      await triggerScrape();
      if (tab === "news") await loadNews();
      else await loadLeaderboard();
    } catch (e) {
      console.error("Scrape failed:", e);
    }
    setScraping(false);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {/* Tab Bar + Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
        <div className="flex items-center gap-2 p-1 bg-surface-1 rounded-xl border border-white/[0.06]">
          <button
            onClick={() => setTab("news")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 border ${
              tab === "news" ? "tab-active" : "tab-inactive"
            }`}
          >
            <Newspaper className="w-4 h-4" />
            <span>News Feed</span>
          </button>
          <button
            onClick={() => setTab("leaderboard")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 border ${
              tab === "leaderboard" ? "tab-active" : "tab-inactive"
            }`}
          >
            <Trophy className="w-4 h-4" />
            <span>Leaderboard</span>
          </button>
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <button
            onClick={handleScrape}
            disabled={scraping}
            className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-muted
                       bg-surface-2 rounded-lg border border-white/[0.06] hover:text-white
                       hover:bg-surface-3 transition-all disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${scraping ? "animate-spin" : ""}`} />
            <span className="hidden sm:inline">Refresh</span>
          </button>
        </div>
      </div>

      {/* Search + Filter Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 mb-6">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={tab === "news" ? "Search news..." : "Search models..."}
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

        <button
          onClick={() => setShowFilters(!showFilters)}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium
                     border transition-all ${
                       showFilters
                         ? "bg-accent/10 border-accent/30 text-accent"
                         : "bg-surface-2 border-white/[0.06] text-muted hover:text-white"
                     }`}
        >
          <Filter className="w-4 h-4" />
          Filters
        </button>
      </div>

      {/* Filter Chips */}
      {showFilters && (
        <div className="space-y-3 mb-6 animate-fade-in">
          {tab === "news" ? (
            <>
              {/* Category filters */}
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-[10px] text-zinc-500 uppercase tracking-widest font-semibold mr-1">Category</span>
                {CATEGORIES.map((cat) => (
                  <button
                    key={cat}
                    onClick={() => setSelectedCategory(cat)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
                      selectedCategory === cat
                        ? "bg-accent/15 border-accent/30 text-accent"
                        : "bg-surface-3/50 border-white/5 text-zinc-400 hover:text-white hover:bg-surface-3"
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
              {/* Source filters */}
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-[10px] text-zinc-500 uppercase tracking-widest font-semibold mr-1">Source</span>
                {NEWS_SOURCES.map((src) => (
                  <button
                    key={src}
                    onClick={() => setSelectedNewsSource(src)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
                      selectedNewsSource === src
                        ? "bg-accent/15 border-accent/30 text-accent"
                        : "bg-surface-3/50 border-white/5 text-zinc-400 hover:text-white hover:bg-surface-3"
                    }`}
                  >
                    {src}
                  </button>
                ))}
              </div>
            </>
          ) : (
            <>
              {/* Provider filters */}
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-[10px] text-zinc-500 uppercase tracking-widest font-semibold mr-1">Provider</span>
                {PROVIDERS.map((prov) => (
                  <button
                    key={prov}
                    onClick={() => setSelectedProvider(prov)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
                      selectedProvider === prov
                        ? "bg-accent/15 border-accent/30 text-accent"
                        : "bg-surface-3/50 border-white/5 text-zinc-400 hover:text-white hover:bg-surface-3"
                    }`}
                  >
                    {prov}
                  </button>
                ))}
              </div>
              {/* Leaderboard source filters */}
              <div className="flex flex-wrap items-center gap-2">
                <Database className="w-3 h-3 text-zinc-500 mr-1" />
                <span className="text-[10px] text-zinc-500 uppercase tracking-widest font-semibold mr-1">Source</span>
                {LB_SOURCES.map((src) => (
                  <button
                    key={src}
                    onClick={() => setSelectedLbSource(src)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
                      selectedLbSource === src
                        ? "bg-accent/15 border-accent/30 text-accent"
                        : "bg-surface-3/50 border-white/5 text-zinc-400 hover:text-white hover:bg-surface-3"
                    }`}
                  >
                    {src === "All" ? "All" : src.replace(" Chatbot Arena", "").replace(" LLM Leaderboard", "").replace(" Open LLM Leaderboard", "")}
                  </button>
                ))}
              </div>
            </>
          )}
        </div>
      )}

      {/* Content */}
      {tab === "news" ? (
        <NewsFeed items={newsItems} loading={loading} />
      ) : (
        <Leaderboard items={leaderboardItems} loading={loading} />
      )}
    </div>
  );
}

// Demo data when backend is unreachable
const DEMO_NEWS = [
  {
    id: "demo1",
    title: "OpenAI Announces GPT-5.5 with Native Tool Use",
    summary: "OpenAI's latest model introduces seamless function calling, multimodal reasoning across text, image, and audio — with a 93.2 MMLU benchmark score.",
    url: "https://openai.com",
    source: "The Rundown AI",
    category: "llm",
    published: "2026-04-25",
  },
  {
    id: "demo2",
    title: "Xiaomi MiMo-V2-Pro: Efficient Reasoning at the Edge",
    summary: "Xiaomi's new model achieves 91.8 MMLU while running efficiently on edge devices, marking a new era for on-device AI inference.",
    url: "https://xiaomi.com",
    source: "VentureBeat",
    category: "llm",
    published: "2026-04-24",
  },
  {
    id: "demo3",
    title: "Google Veo 3 Generates Photorealistic 4K Video",
    summary: "Google DeepMind unveils Veo 3, capable of generating cinema-quality 4K video from text prompts with unprecedented temporal consistency.",
    url: "https://deepmind.google",
    source: "MIT Technology Review",
    category: "image_gen",
    published: "2026-04-23",
  },
  {
    id: "demo4",
    title: "Figure 03 Humanoid Robot Learns Kitchen Tasks",
    summary: "Figure's third-generation humanoid demonstrates autonomous kitchen task learning, from slicing vegetables to loading dishwashers.",
    url: "https://figure.ai",
    source: "Wired",
    category: "robotics",
    published: "2026-04-22",
  },
  {
    id: "demo5",
    title: "Claude 4.7 Opus: 200K Context with Safety-First Design",
    summary: "Anthropic's Claude 4.7 Opus pushes context to 200K tokens while maintaining industry-leading safety benchmarks and interpretability tools.",
    url: "https://anthropic.com",
    source: "ArXiv",
    category: "llm",
    published: "2026-04-21",
  },
  {
    id: "demo6",
    title: "Stable Diffusion 5 Open-Source Release",
    summary: "Stability AI releases SD5 as fully open-weight, rivaling proprietary image generators in quality while maintaining complete community freedom.",
    url: "https://stability.ai",
    source: "The Rundown AI",
    category: "image_gen",
    published: "2026-04-20",
  },
];
