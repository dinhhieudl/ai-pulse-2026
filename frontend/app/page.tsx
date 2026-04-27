import { Suspense } from "react";
import Header from "@/components/Header";
import Dashboard from "@/components/Dashboard";

export default function Home() {
  return (
    <main className="min-h-screen">
      <Header />
      <Suspense fallback={<LoadingSkeleton />}>
        <Dashboard />
      </Suspense>
    </main>
  );
}

function LoadingSkeleton() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="animate-pulse space-y-6">
        <div className="h-10 bg-surface-3 rounded-lg w-64" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-48 bg-surface-2 rounded-xl" />
          ))}
        </div>
      </div>
    </div>
  );
}
