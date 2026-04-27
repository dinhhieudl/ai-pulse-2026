# AI Pulse 2026

> Real-time AI intelligence dashboard — multi-source news feed + multi-source model leaderboard.

## 🚀 Deploy

### Option 1: Docker (Recommended)

```bash
git clone https://github.com/dinhhieudl/ai-pulse-2026.git
cd ai-pulse-2026
docker compose up -d
```

Open: **http://localhost:3000**

### Option 2: Manual

```bash
# Backend
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Frontend
cd frontend
npm install
npm run build
npm start
```

### Option 3: VPS / Cloud (Production)

**Backend (FastAPI + Gunicorn):**
```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Frontend (Next.js standalone):**
```bash
cd frontend
npm install
npm run build
# Output in .next/standalone — serve with:
node .next/standalone/server.js
```

**With Nginx reverse proxy:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Option 4: Vercel + Railway

**Frontend → Vercel:**
1. Fork this repo
2. Go to [vercel.com](https://vercel.com) → Import Project
3. Set Root Directory: `frontend`
4. Add env var: `NEXT_PUBLIC_API_URL=https://your-backend.railway.app`
5. Deploy

**Backend → Railway:**
1. Go to [railway.app](https://railway.app) → New Project → From GitHub
2. Set Root Directory: `backend`
3. Add start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Deploy

### Option 5: Fly.io

```bash
# Backend
cd backend
fly launch --dockerfile Dockerfile.backend
fly deploy

# Frontend
cd frontend
fly launch --dockerfile Dockerfile.frontend
fly deploy
```

---

## 📡 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `""` (same origin) | Backend API URL for frontend |
| `PORT` | `8000` / `3000` | Server port |

## 🔄 Scraper Schedule

- Runs automatically every **30 minutes**
- Trigger manually: `POST /api/scrape/run`
- Each scraper has **fallback data** if live scraping fails

## 📊 Data Sources

### News
| Source | Type |
|--------|------|
| The Rundown AI | Daily AI newsletter |
| MIT Technology Review | In-depth analysis |
| Wired (AI Section) | Tech journalism |
| VentureBeat | Enterprise AI |
| ArXiv (cs.AI) | Research papers |

### Leaderboard
| Source | Focus |
|--------|-------|
| LMSYS Chatbot Arena | ELO from user battles |
| Vellum LLM Leaderboard | Cost / speed / perf |
| HuggingFace Open LLM | Open-source benchmarks |

## 🏗 Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js 15, React 19, Tailwind CSS 3.4 |
| Backend | FastAPI, httpx, BeautifulSoup4, APScheduler |
| Scraping | Async HTTP + CSS selectors + JSON APIs |
| Icons | Lucide React |

## 📁 Project Structure

```
ai-pulse-2026/
├── backend/
│   ├── main.py                 # FastAPI app + scheduler
│   ├── models.py               # Data models + in-memory store
│   ├── api/                    # API routes
│   │   ├── news.py
│   │   ├── leaderboard.py
│   │   └── scrape.py
│   └── scrapers/               # 8 scrapers
│       ├── rundown.py, mit_tech.py, wired.py, venturebeat.py, arxiv.py
│       ├── lmsys.py, vellum.py, huggingface.py
│       └── orchestrator.py
├── frontend/
│   ├── app/                    # Next.js App Router
│   ├── components/             # React components
│   └── lib/api.ts              # API client
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── start.sh
└── README.md
```
