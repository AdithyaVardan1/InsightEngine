# InsightEngine 🔍

**AI SEO Analyzer** - Analyze your website's readiness for AI-powered search engines.

## Overview

InsightEngine helps you optimize your website for the new era of AI search - ChatGPT, Perplexity, Google AI Overviews, and more. Get actionable recommendations based on 5 key analysis categories.

## Tech Stack

- **Frontend**: Next.js 15 (React, TypeScript)
- **Backend**: Python (FastAPI)
- **AI**: Google Gemini API

## Project Structure

```
insight-engine/
├── src/                    # Next.js Frontend
│   └── app/
│       ├── page.tsx        # Landing page
│       ├── layout.tsx      # Root layout
│       ├── globals.css     # Premium dark theme
│       └── analyze/        # Results page (TBD)
├── backend/                # Python Backend
│   ├── main.py             # FastAPI app
│   ├── requirements.txt    # Python deps
│   └── app/
│       ├── api/
│       │   └── routes.py   # API endpoints
│       └── analyzers/      # Analysis modules
│           ├── robots_analyzer.py
│           ├── schema_analyzer.py
│           ├── content_analyzer.py
│           ├── technical_analyzer.py
│           └── llms_txt_analyzer.py
├── package.json
└── README.md
```

## Analysis Categories

| Category | Weight | What We Check |
|----------|--------|---------------|
| **AI Crawler Access** | 25% | robots.txt for GPTBot, ClaudeBot, PerplexityBot |
| **Structured Data** | 25% | JSON-LD schema markup |
| **Content Structure** | 25% | Headings, FAQs, answer-first patterns |
| **Technical SEO** | 15% | Meta tags, SSR, semantic HTML |
| **llms.txt** | 10% | Emerging AI instruction standard |

## Getting Started

### Backend (Python)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend (Next.js)

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the app.

## API Endpoints

- `POST /api/analyze` - Analyze a URL
- `GET /api/health` - Health check

## Environment Variables

Create a `.env` file in `backend/`:

```
GEMINI_API_KEY=your_gemini_api_key
```

## License

MIT

---

Built for the AI-first web 🚀
