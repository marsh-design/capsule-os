# CapsuleOS 👗✨

Quarterly capsule planner + "Should I buy this?" AI decision assistant.

![CapsuleOS Demo](docs/demo.gif)
*Demo coming soon - placeholder for app screenshots*

## What it does

CapsuleOS helps you plan a cohesive quarterly capsule wardrobe and avoid low-value purchases by scoring items for:
- closet overlap
- price-per-wear
- review-derived fit/value signals

## MVP Features

- [x] Quarter setup (style keywords, budget, climate)
- [ ] Capsule output (12-item capsule + palette + outfit formulas)
- [ ] "Should I Buy This?" scanner (Buy / Wait / Skip)
- [ ] Review insights extractor (fit/quality complaints)
- [ ] Alternatives retrieval

## Tech Stack

**Frontend:** React + Tailwind  
**Backend:** FastAPI (Python)  
**Storage:** SQLite/Postgres (TBD)  
**AI:** SentenceTransformers + (optional) OpenAI + structured outputs

## Run locally

```bash
# frontend
cd frontend
npm install
npm run dev

# backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Roadmap

- [x] Week 1: Product + Data
- [ ] Week 2: Capsule generator v1
- [ ] Week 3: Scanner v1
- [ ] Week 4: Review insights extractor
- [ ] Week 5: Ranking + alternatives
- [ ] Week 6: Evaluation + polish + deploy

## Setup

1. **Clone the repository:**
```bash
git clone https://github.com/marsh-design/capsule-os.git
cd capsule-os
```

2. **Backend setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY (optional for MVP)
```

3. **Frontend setup:**
```bash
cd frontend
npm install
```

4. **Run:**
```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

Or use Docker:
```bash
docker-compose up
```

## Project Structure

```
capsule-os/
├── frontend/          # React + Tailwind UI
├── backend/           # FastAPI + ML pipeline
├── data/              # Sample datasets
├── notebooks/         # EDA + model experiments
├── eval/              # Evaluation harness
└── docs/              # Architecture + PRD
```

## What This Demonstrates

- ✅ **ML/NLP**: Review summarization, sentiment analysis, aspect extraction
- ✅ **LLM Orchestration**: Structured outputs, prompts, guardrails
- ✅ **RAG**: Store/item info retrieval, user closet retrieval
- ✅ **Ranking/Recommendation**: Top picks + tradeoffs
- ✅ **Evaluation**: Offline metrics + human eval rubric
- ✅ **Full Stack**: React + FastAPI + PostgreSQL
- ✅ **Production Engineering**: Logging, caching, tests, CI

## License

MIT
