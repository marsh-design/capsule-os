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
# Edit .env and add your OPENAI_API_KEY

# Initialize database
python -m app.database init_db

# Seed sample data (optional)
python scripts/seed_db.py

# Run server
uvicorn main:app --reload
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Database Seeding

To populate the database with sample products and reviews:

```bash
cd backend
python scripts/seed_db.py
```

This will:
- Create database tables
- Load 10 sample products
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
capsule-os/
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── routers/  # API endpoints
│   │   ├── services/ # Business logic
│   │   ├── database.py
│   │   └── models.py
│   ├── scripts/      # Utility scripts
│   └── main.py
├── frontend/         # React application
│   └── src/
│       ├── pages/    # Page components
│       └── components/
├── data/             # Sample datasets
├── docs/             # Documentation
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
- Check CORS settings in `backend/main.py`
- Verify proxy settings in `frontend/vite.config.js`

### Database errors
- Delete `capsuleos.db` and re-run `init_db()`
- Check database file permissions
- Verify SQLite is installed

## Next Steps

1. **Week 2**: Implement actual capsule generation logic
2. **Week 3**: Add LLM integration for pros/cons
3. **Week 4**: Build review analysis ML pipeline
4. **Week 5**: Add vector search for alternatives
5. **Week 6**: Evaluation and polish
