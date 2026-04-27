"use client";

import { useState } from "react";
import { Bookmark, BookmarkCheck } from "lucide-react";

export default function BookmarkButton({
  newsId,
  title,
  url,
  source,
  category,
}: {
  newsId: string;
  title: string;
  url: string;
  source?: string;
  category?: string;
}) {
  const [bookmarked, setBookmarked] = useState(false);
  const [loading, setLoading] = useState(false);

  const toggle = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (loading) return;

    setLoading(true);
    try {
      if (!bookmarked) {
        await fetch("/api/bookmarks/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ news_id: newsId, title, url, source, category }),
        });
        setBookmarked(true);
      } else {
        await fetch(`/api/bookmarks/bm_${newsId}`, { method: "DELETE" });
        setBookmarked(false);
      }
    } catch (err) {
      console.error("Bookmark toggle failed:", err);
    }
    setLoading(false);
  };

  return (
    <button
      onClick={toggle}
      className={`p-1.5 rounded-lg transition-all ${
        bookmarked
          ? "text-yellow-400 bg-yellow-400/10"
          : "text-zinc-500 hover:text-yellow-400 hover:bg-yellow-400/5"
      }`}
      title={bookmarked ? "Remove bookmark" : "Bookmark this article"}
    >
      {bookmarked ? (
        <BookmarkCheck className="w-4 h-4" />
      ) : (
        <Bookmark className="w-4 h-4" />
      )}
    </button>
  );
}
