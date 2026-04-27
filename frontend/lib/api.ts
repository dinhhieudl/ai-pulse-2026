const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

// ── News ──
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

// ── Leaderboard ──
export async function fetchLeaderboard(params: {
  provider?: string;
  source?: string;
  q?: string;
  sort_by?: string;
  order?: string;
}) {
  const searchParams = new URLSearchParams();
  if (params.provider) searchParams.set("provider", params.provider);
  if (params.source) searchParams.set("source", params.source);
  if (params.q) searchParams.set("q", params.q);
  if (params.sort_by) searchParams.set("sort_by", params.sort_by);
  if (params.order) searchParams.set("order", params.order);

  const qs = searchParams.toString();
  const url = `${API_BASE}/api/leaderboard${qs ? `?${qs}` : ""}`;

  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new Error(`Leaderboard API error: ${res.status}`);
  return res.json();
}

// ── Scrape ──
export async function triggerScrape() {
  const res = await fetch(`${API_BASE}/api/scrape/run`, { method: "POST" });
  if (!res.ok) throw new Error(`Scrape trigger error: ${res.status}`);
  return res.json();
}

// ── Bookmarks ──
export async function fetchBookmarks() {
  const res = await fetch(`${API_BASE}/api/bookmarks/`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Bookmarks API error: ${res.status}`);
  return res.json();
}

export async function addBookmark(data: {
  news_id: string;
  title: string;
  url: string;
  source?: string;
  category?: string;
}) {
  const res = await fetch(`${API_BASE}/api/bookmarks/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(`Add bookmark error: ${res.status}`);
  return res.json();
}

export async function removeBookmark(id: string) {
  const res = await fetch(`${API_BASE}/api/bookmarks/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error(`Remove bookmark error: ${res.status}`);
  return res.json();
}

// ── Compare ──
export async function compareModels(models: string[]) {
  const res = await fetch(`${API_BASE}/api/compare/?models=${models.join(",")}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Compare API error: ${res.status}`);
  return res.json();
}

export async function fetchAllModels() {
  const res = await fetch(`${API_BASE}/api/compare/all`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Models API error: ${res.status}`);
  return res.json();
}

// ── Trends ──
export async function fetchModelTrends(model?: string, days?: number) {
  const params = new URLSearchParams();
  if (model) params.set("model", model);
  if (days) params.set("days", String(days));
  const qs = params.toString();
  const res = await fetch(`${API_BASE}/api/trends/models${qs ? `?${qs}` : ""}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Trends API error: ${res.status}`);
  return res.json();
}

export async function fetchProviderStats(days?: number) {
  const qs = days ? `?days=${days}` : "";
  const res = await fetch(`${API_BASE}/api/trends/providers${qs}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Provider stats error: ${res.status}`);
  return res.json();
}

// ── User Links ──
export async function submitUserLink(url: string, title?: string) {
  const res = await fetch(`${API_BASE}/api/user-links/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, title }),
  });
  if (!res.ok) throw new Error(`Submit link error: ${res.status}`);
  return res.json();
}

// ── Digest ──
export async function fetchDigest(type: "daily" | "weekly" | "telegram" = "daily") {
  const res = await fetch(`${API_BASE}/api/digest/${type}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Digest API error: ${res.status}`);
  return res.json();
}
