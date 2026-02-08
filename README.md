# CapsuleOS 👗✨

[![CI](https://github.com/marsh-design/capsule-os/actions/workflows/ci.yml/badge.svg)](https://github.com/marsh-design/capsule-os/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Quarterly capsule planner + "Should I buy this?" AI decision assistant.

![CapsuleOS Demo](docs/demo.gif)
*Demo coming soon - placeholder for app screenshots*

## What it does

CapsuleOS helps you plan a cohesive quarterly capsule wardrobe and avoid low-value purchases by scoring items for:
- closet overlap
- price-per-wear
- review-derived fit/value signals

## System Status (Honest Snapshot)

CapsuleOS is intentionally built in stages. Below is a clear view of what is production-ready today vs. what is currently mocked or heuristic-based.

### ✅ Fully Implemented
- End-to-end capsule generation using real product data (SQLite)
- Palette extraction, versatility scoring, overlap penalties
- Capsule caching (1h TTL)
- "Should I Buy This?" decision flow (heuristic-based)
- Alternatives retrieval from DB (price-range + category)
- Structured APIs, validation, health checks
- CI (lint, format, tests)

### ⚠️ Heuristic / Mocked (by design)
- Review insights (rule-based placeholder; ML planned)
- Product link parsing (URL accepted but not fetched yet)
- Closet overlap (API exists, UI not wired)

### 🚧 In Progress / Planned
- Review insights ML pipeline (aspect-based sentiment)
- Vector search for similar-item alternatives
- Real product-link parsing
- Evaluation harness + metrics

## MVP Features

- [x] Quarter setup (style keywords, budget, climate)
- [x] Capsule output (12-item capsule + palette + outfit formulas + product images)
- [x] "Should I Buy This?" scanner (Buy / Wait / Skip + pros/cons + alternatives)
- [ ] Review insights extractor (real fit/quality from reviews; currently rule-based)
- [x] Alternatives retrieval (same price range from DB)
- [x] Product images in capsule lookbook (Unsplash placeholders in seed data)

## Tech Stack

**Frontend:** React + Vite + Tailwind  
**Backend:** FastAPI (Python)  
**Storage:** SQLite (DB initializes on server startup)  
**AI:** Heuristics + (optional) OpenAI; structured outputs for capsule/scanner

## Run locally

```bash
# backend (from backend/ with venv activated)
pip install -r requirements.txt
python scripts/seed_db.py   # optional: seed products + reviews
uvicorn main:app --reload

# frontend (from frontend/)
npm install
npm run dev
```

## Roadmap

- [x] Week 1: Product + Data
- [x] Week 2: Capsule generator v1
- [x] Week 3: Scanner v1 (UI + API, heuristic-based)
- [ ] Week 4: Review insights extractor (real ML/NLP)
- [x] Week 5: Ranking + alternatives (DB-backed alternatives)
- [ ] Week 6: Evaluation + polish + deploy

## Setup

1. **Clone the repository** and go to the project directory.

2. **Backend setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Add OPENAI_API_KEY if using LLM features
```

3. **Seed the database** (creates tables and sample products + reviews):
```bash
python scripts/seed_db.py
```

4. **Frontend setup:**
```bash
cd frontend
npm install
```

5. **Run:**
```bash
# Terminal 1: Backend (initializes DB on startup)
cd backend && source venv/bin/activate && uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev
```

Frontend: http://localhost:5173 (Vite) or http://localhost:3000 — proxy forwards `/api` to backend:8000.

**Docker:** `cp backend/.env.example backend/.env` then `docker-compose up`. Frontend: http://localhost:3000, Backend: http://localhost:8000.

**Troubleshooting:** Backend won’t start — check Python 3.10+, `pip install -r requirements.txt`. Frontend can’t reach backend — ensure backend on 8000 and CORS allows localhost:3000/5173. DB issues — delete the SQLite file in `backend/` and re-run `python scripts/seed_db.py`.

## Project Structure

```
ai_stylist/
├── frontend/            # React + Vite + Tailwind
├── backend/             # FastAPI, routers, services, DB
├── data/                # Sample products, reviews, capsule templates, schema
├── docs/                # STATUS (what works / what doesn’t)
├── eval/                # Evaluation harness (placeholder)
└── docker-compose.yml
```

## How It Works

### Capsule Generation Logic (v1)

CapsuleOS generates personalized quarterly capsules through a multi-step process:

1. **Template Selection**: Based on quarter (Q1-Q4), selects a base template with recommended item categories and color palette
2. **Product Retrieval**: Queries database for products matching template categories, filtered by user's shopping preferences (brands)
3. **Item Selection**: For each category, selects:
   - **Best Value**: Product closest to 70% of per-item budget, prioritizing lower prices
   - **Best Quality**: Highest-priced product from premium brands (Aritzia, Everlane, etc.)
4. **Palette Extraction**: Extracts color palette from selected items, prioritizing most common colors
5. **Scoring & Ranking**: Computes capsule coherence scores:
   - **Palette Match**: How well items match the target color palette (0-1)
   - **Versatility**: Percentage of versatile items (tees, jeans, blazers) (0-1)
   - **Closet Overlap**: Penalty for duplicate categories in existing closet (0-1)
6. **Outfit Formulas**: Generates 3-4 outfit combinations from selected items
7. **Caching**: Results are cached for 1 hour to improve performance for similar requests

### Future Enhancements

- **Personalization**: ML-based item recommendations based on user style history
- **Closet Integration**: Real-time overlap detection with user's existing wardrobe
- **Dynamic Pricing**: Cost-per-wear optimization across the entire capsule
- **Style Matching**: Semantic similarity for style keyword matching

## What This Demonstrates

- ✅ **Full Stack**: React + Vite + FastAPI + SQLite
- ✅ **Ranking/Recommendation**: Best value / best quality picks, alternatives from DB
- ✅ **Caching**: TTL-based capsule response cache
- ✅ **Structured APIs**: Pydantic models, health check, capsule + analyze endpoints
- 🚧 **ML/NLP**: Review insights (baseline/rule-based; full pipeline planned)
- 🚧 **LLM**: Optional for pros/cons; prompts in place
- 📋 **Planned**: RAG, vector search, evaluation harness, production deploy

## Development Progress

### ✅ Completed
- [x] Project structure & setup
- [x] Database models & seeding
- [x] Capsule generator with real product data
- [x] Scoring logic (palette, versatility, overlap)
- [x] Caching layer (TTL-based)
- [x] Unit tests for scoring & caching
- [x] CI/CD pipeline (lint, format, tests)
- [x] API health check endpoint

### 🚧 In Progress
- [ ] Review insights extractor (real ML; currently rule-based)
- [ ] LLM integration for richer pros/cons

### 📋 Planned
- [ ] Vector search for similar-item alternatives
- [ ] Evaluation harness
- [ ] Production deployment
- [ ] Real product-link parsing (scanner)

## License

MIT
