# Week 1 Checklist: Product + Data

## ✅ Completed

- [x] Project structure created
- [x] PRD written (`docs/PRD.md`)
- [x] UI wireframe (3 pages implemented)
- [x] Data schema defined (`data/schema.json`)
- [x] Sample products dataset (10 items in `data/sample_products.json`)
- [x] Sample reviews dataset (20 reviews in `data/sample_reviews.json`)
- [x] Baseline scoring logic (`backend/app/services/scoring.py`)
- [x] Database models (`backend/app/database.py`)
- [x] API endpoints structure (`backend/app/routers/`)
- [x] Frontend pages (Quarter Setup, Capsule Output, Item Scanner)
- [x] Docker setup
- [x] README with architecture

## 📋 Deliverables

### Documentation
- ✅ PRD (`docs/PRD.md`)
- ✅ Architecture doc (`docs/ARCHITECTURE.md`)
- ✅ README (`README.md`)
- ✅ Setup guide (`SETUP.md`)

### Data
- ✅ Schema definition (`data/schema.json`)
- ✅ 10 sample products (`data/sample_products.json`)
- ✅ 20 sample reviews (`data/sample_reviews.json`)
- ✅ Capsule templates (`data/capsule_templates.json`)

### Code
- ✅ Backend API structure
- ✅ Frontend React app
- ✅ Database models
- ✅ Baseline services (scoring, generators, analyzers)
- ✅ Seed script (`backend/scripts/seed_db.py`)

## 🎯 Progress Since Week 1 (Weeks 2–3)

1. **Capsule Generator v1** ✅
   - Dynamic generation from templates + DB product retrieval
   - Palette extraction, outfit formulas, best value / best quality per item
   - Product images in API and capsule lookbook (seed data has Unsplash URLs)
   - Caching and scoring in place

2. **Scanner v1** ✅
   - “Should I Buy This?” UI and `/api/analyze-item` endpoint
   - Verdict (Buy/Wait/Skip), pros/cons, cost-per-wear, alternatives from DB

3. **Frontend**
   - Loading states and in-page error messages
   - SSENSE-style editorial UI (typography, layout, lookbook grid with images)

4. **Testing**
   - Unit tests for scoring and cache
   - See `docs/STATUS.md` for current “what works / what’s bare”

## 📊 Data Quality

Current dataset:
- **Products**: 10 items across 5 categories
- **Reviews**: 20 reviews (2 per product average)
- **Brands**: Everlane, Aritzia, Zara
- **Categories**: Top, Bottom, Outerwear, Shoes, Dress, Accessory

**Note**: Sample products include `image_url` (Unsplash) for capsule lookbook. For production, expand to 50-100 products and 500-2000 reviews.

## 🔧 Technical Debt

- [ ] Add proper error handling
- [ ] Add input validation
- [ ] Add logging throughout
- [ ] Add unit tests
- [ ] Add API documentation (Swagger)
- [ ] Improve type hints
- [ ] Add database migrations (Alembic)
