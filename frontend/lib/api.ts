const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

export async function fetchNews(params: {
  category?: string;
  source?: string;
  q?: string;
  limit?: number;
}) {
  const searchParams = new URLSearchParams();
  if (params.category) searchParams.set("category", params.category);
  if (params.source) searchParams.set("source", params.source);
  if (params.q) searchParams.set("q", params.q);
  if (params.limit) searchParams.set("limit", String(params.limit));

  const qs = searchParams.toString();
  const url = `${API_BASE}/api/news${qs ? `?${qs}` : ""}`;

  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new Error(`News API error: ${res.status}`);
  return res.json();
}

export async function fetchLeaderboard(params: {
  provider?: string;
  q?: string;
  sort_by?: string;
  order?: string;
}) {
  const searchParams = new URLSearchParams();
  if (params.provider) searchParams.set("provider", params.provider);
  if (params.q) searchParams.set("q", params.q);
  if (params.sort_by) searchParams.set("sort_by", params.sort_by);
  if (params.order) searchParams.set("order", params.order);

  const qs = searchParams.toString();
  const url = `${API_BASE}/api/leaderboard${qs ? `?${qs}` : ""}`;

  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new Error(`Leaderboard API error: ${res.status}`);
  return res.json();
}

export async function triggerScrape() {
  const res = await fetch(`${API_BASE}/api/scrape/run`, { method: "POST" });
  if (!res.ok) throw new Error(`Scrape trigger error: ${res.status}`);
  return res.json();
}
