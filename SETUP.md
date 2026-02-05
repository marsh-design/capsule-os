# CapsuleOS Setup Guide

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Copy environment file
cp backend/.env.example backend/.env
# Edit backend/.env and add your OPENAI_API_KEY

# Start services
docker-compose up
```

Frontend: http://localhost:3000
Backend: http://localhost:8000

### Option 2: Local Development

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env and add OPENAI_API_KEY if using LLM features

# Seed database (creates tables + 10 products, 20 reviews with real image URLs)
python scripts/seed_db.py

# Run server (DB initializes automatically on startup if needed)
uvicorn main:app --reload
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Database Seeding

Run from the `backend` directory (with venv activated):

```bash
python scripts/seed_db.py
```

This will:
- Create database tables (if not already present)
- Clear existing products and reviews (safe to re-run)
- Load 10 sample products (with Unsplash image URLs)
- Load 20 sample reviews

## Testing the API

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Generate Capsule
```bash
curl -X POST http://localhost:8000/api/generate-capsule \
  -H "Content-Type: application/json" \
  -d '{
    "quarter": "Q1",
    "climate": "moderate",
    "style_keywords": ["effortless", "elevated"],
    "budget": 1000,
    "shopping_preferences": ["Everlane", "Aritzia"]
  }'
```

### Analyze Item
```bash
curl -X POST http://localhost:8000/api/analyze-item \
  -H "Content-Type: application/json" \
  -d '{
    "product_description": "Classic white t-shirt",
    "price": 28.0,
    "brand": "Everlane"
  }'
```

## Project Structure

```
<project-root>/
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── routers/  # capsule, analyze, closet
│   │   ├── services/ # capsule_generator, item_analyzer, scoring, cache
│   │   ├── database.py
│   │   └── models.py
│   ├── scripts/      # seed_db.py, test_capsule.py
│   └── main.py
├── frontend/         # React + Vite + Tailwind
│   └── src/
│       ├── pages/    # QuarterSetup, CapsuleOutput, ItemScanner
│       └── components/
├── data/             # sample_products.json, sample_reviews.json, capsule_templates
├── docs/             # STATUS, PRD, ARCHITECTURE, checklists
└── docker-compose.yml
```

## Environment Variables

Required:
- `OPENAI_API_KEY`: For LLM features (get from https://platform.openai.com)

Optional:
- `DATABASE_URL`: Database connection string (default: SQLite)
- `LOG_LEVEL`: Logging level (default: INFO)

## Troubleshooting

### Backend won't start
- Check Python version (3.10+)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check database file permissions

### Frontend won't connect to backend
- Verify backend is running on port 8000
- Check CORS in `backend/main.py` (localhost:3000, localhost:5173)
- Frontend proxy: `frontend/vite.config.js` forwards `/api` to http://localhost:8000

### Database errors
- Delete the SQLite DB file in `backend/` (e.g. `capsuleos.db` or as in `database.py`) and restart the server or re-run `python scripts/seed_db.py`
- Check file permissions for the DB file

## Next Steps

1. **Done:** Capsule generation with DB products and product images
2. **Done:** Scanner UI + API (heuristic verdict, pros/cons, alternatives from DB)
3. **Planned:** LLM integration for richer pros/cons; real review insights ML
4. **Planned:** Vector search for similar-item alternatives; evaluation and polish
