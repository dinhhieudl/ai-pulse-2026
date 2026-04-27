#!/usr/bin/env bash
set -euo pipefail

# ── AI Pulse 2026 — One-command launcher ──────────────────────────
# Usage: ./start.sh

ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "🚀 Starting AI Pulse 2026..."
echo ""

# ── Backend ──────────────────────────────────────────────────────
echo "📦 Setting up Python backend..."
cd "$ROOT/backend"

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

echo "✅ Backend dependencies installed"
echo "🐍 Starting FastAPI on :8000..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# ── Frontend ─────────────────────────────────────────────────────
echo ""
echo "📦 Setting up Next.js frontend..."
cd "$ROOT/frontend"

if [ ! -d "node_modules" ]; then
  npm install
fi

echo "✅ Frontend dependencies installed"
echo "⚡ Starting Next.js on :3000..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🌐 AI Pulse 2026 is live!"
echo ""
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/docs"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Trap Ctrl+C
trap "echo ''; echo 'Shutting down...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM

wait
