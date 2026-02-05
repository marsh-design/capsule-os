# CapsuleOS Architecture

## System Overview

CapsuleOS is a full-stack application with three main components:

1. **Frontend**: React + Tailwind CSS
2. **Backend**: FastAPI (Python)
3. **Database**: SQLite (MVP) / PostgreSQL (production)

## Component Architecture

### Backend Services

```
app/
├── routers/          # API endpoints
│   ├── capsule.py    # Capsule generation
│   ├── analyze.py    # Item analysis
│   └── closet.py     # Closet management
├── services/         # Business logic
│   ├── capsule_generator.py
│   ├── item_analyzer.py
│   ├── review_analyzer.py
│   └── scoring.py
├── database.py       # SQLAlchemy models
└── models.py         # Pydantic schemas
```

### Data Flow

1. **Capsule Generation**:
   - User inputs → FastAPI → CapsuleGenerator → Template + Scoring → Response

2. **Item Analysis**:
   - Product link/description → ItemAnalyzer → ReviewAnalyzer (rule-based) → ItemScorer → Response (optional LLM for pros/cons)

3. **Review Analysis**:
   - Reviews → Keyword extraction → Sentiment analysis → Structured insights

## ML Pipeline

### Review Analysis (Week 4)
- Input: Product reviews (text + rating)
- Processing: Keyword extraction → Aspect extraction → Sentiment
- Output: Structured insights (fit, quality, complaints)

### Scoring System
- Palette match: Color similarity
- Versatility: Pairing potential
- Closet overlap: Duplicate detection
- Cost-per-wear: Price / estimated wears

## Current Behavior

- **Capsule API** returns `image_url` on each item’s best_value / best_quality options (from Product table). Frontend shows one product image per capsule item in the lookbook grid.
- **Alternatives** are fetched from the same DB (same price range); no vector search yet.

## Future Enhancements

- Vector search for similar-item alternatives (e.g. ChromaDB)
- LLM integration for richer pros/cons generation
- Real review-insights ML pipeline
- Real-time product link parsing
