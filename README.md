# CapsuleOS: Quarterly Capsule Planner + "Should I Buy This?" AI

> A wardrobe planning tool that generates a quarterly capsule (10–15 items) and acts as a purchase decision assistant by scoring items for cost-per-wear, closet overlap, and review-derived fit/value signals.

![CapsuleOS Demo](docs/demo.gif)

## 🎯 What This Demonstrates

This project showcases:

- ✅ **ML/NLP**: Review summarization, sentiment analysis, aspect extraction
- ✅ **LLM Orchestration**: Structured outputs, prompts, guardrails
- ✅ **RAG**: Store/item info retrieval, user closet retrieval
- ✅ **Ranking/Recommendation**: Top picks + tradeoffs
- ✅ **Evaluation**: Offline metrics + human eval rubric
- ✅ **Full Stack**: React + FastAPI + PostgreSQL
- ✅ **Production Engineering**: Logging, caching, tests, CI

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   React     │────▶│   FastAPI    │────▶│  PostgreSQL │
│  Frontend   │     │   Backend    │     │   + Vector  │
└─────────────┘     └──────────────┘     └─────────────┘
                            │
                            ├──▶ LLM (GPT-4o-mini)
                            ├──▶ Review ML Analyzer
                            └──▶ Capsule Coherence Scorer
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional)

### Installation

1. **Clone and setup backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Setup frontend:**
```bash
cd frontend
npm install
```

3. **Run with Docker Compose:**
```bash
docker-compose up
```

Or run separately:
```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

## 📁 Project Structure

```
capsule-os/
├── frontend/          # React + Tailwind UI
├── backend/           # FastAPI + ML pipeline
├── data/              # Sample datasets
├── notebooks/         # EDA + model experiments
├── eval/              # Evaluation harness
├── docs/              # Architecture + PRD
└── README.md
```

## 🧠 How It Works

### 1. Quarter Setup
- Input: quarter, climate, style keywords, budget, shopping preferences
- Output: Personalized capsule plan with palette + outfit formulas

### 2. Capsule Generation
- Analyzes closet overlap
- Computes palette coherence
- Ranks items by versatility
- Generates "Best Value vs Best Quality" recommendations

### 3. "Should I Buy This?" Scanner
- Extracts product details from link/description
- Analyzes reviews for fit/quality signals
- Computes closet overlap
- Generates verdict: ✅ Buy / ⚠️ Wait / ❌ Skip
- Provides alternatives via vector search

## 📊 Evaluation Results

*Evaluation metrics will be added after Week 6*

- Verdict accuracy: TBD
- Helpfulness score: TBD
- Consistency score: TBD

## 🛣️ Roadmap

- [x] Week 1: Product + Data
- [ ] Week 2: Capsule Generator v1
- [ ] Week 3: "Should I Buy This?" v1
- [ ] Week 4: Review ML Analyzer
- [ ] Week 5: Ranking + Alternatives
- [ ] Week 6: Evaluation + Polish

## ⚖️ Tradeoffs & Limitations

- **Review data**: Limited to publicly available datasets
- **Capsule templates**: Initial version uses hardcoded templates
- **LLM costs**: Using GPT-4o-mini for cost efficiency
- **Vector search**: ChromaDB for MVP, upgradeable to Pinecone/Weaviate

## 🔮 Future Improvements

- Chrome extension for one-click analysis
- Slack bot integration
- Multi-quarter planning
- Budget ladder (A/B/C tiers)
- "Do Not Buy" duplicate detection

## 📝 License

MIT

## 👤 Author

Built as a portfolio project demonstrating ML/AI engineering capabilities.
