# CapsuleOS: Product Requirements Document

## Vision

A wardrobe planning tool that generates quarterly capsule wardrobes (10-15 items) and acts as an AI purchase decision assistant, scoring items for cost-per-wear, closet overlap, and review-derived fit/value signals.

## Target User

- Fashion-conscious consumers who want to build intentional wardrobes
- People who struggle with decision fatigue when shopping
- Users who want to reduce returns and impulse purchases

## Core Features

### 1. Quarter Setup Page

**Inputs:**
- Quarter selection (Q1-Q4)
- Climate (Cold / Moderate / Warm / Hot)
- Style keywords (Effortless / Elevated / Sexy / Minimal / Classic)
- Budget range ($500-$5000)
- Shopping preferences (checkboxes: Everlane, Aritzia, Zara, etc.)
- Optional: Closet upload (JSON or manual entry)

**Output:**
- Confirmation with summary

### 2. Capsule Output Page

**Displays:**
- Color palette (5-7 colors)
- Outfit formulas (e.g., "Trench + White Tee + Jeans + Loafers")
- 12-item capsule list with:
  - Product image (when available from API)
  - Item name
  - Category
  - "Best Value" option (brand, name, price)
  - "Best Quality" option (brand, name, price)
- "Do Not Buy" list (duplicates or bad value items)

### 3. "Should I Buy This?" Scanner

**Input:**
- Product link (URL) OR
- Manual entry: description + price + brand

**Output:**
- Verdict: ✅ Buy / ⚠️ Wait / ❌ Skip
- Pros & Cons (structured list)
- Closet overlap warning (if closet exists)
- Alternatives (2-3 similar items)

## Technical Requirements

### ML Components

1. **Review Insights Model**
   - Extract: sizing (runs small/large), fabric quality, durability, comfort, see-through, pilling, return reasons
   - Output: Structured JSON with confidence scores

2. **Capsule Coherence Score**
   - Palette match (0-1)
   - Versatility (pairs with # items)
   - Closet overlap (0-1)
   - Price-per-wear estimate

3. **LLM Layer**
   - Structured output generation (JSON)
   - Pros/cons writing
   - Explanation generation

### API Endpoints

- `POST /api/generate-capsule` - Generate quarterly capsule
- `POST /api/analyze-item` - Analyze single item
- `POST /api/closet/upload` - Upload closet data
- `GET /api/closet` - Retrieve user closet
- `GET /api/alternatives/{item_id}` - Get alternatives

### Data Requirements

- 50-100 sample products (structured JSON)
- 500-2000 reviews (scraped or public dataset)
- Product metadata: brand, category, price, description, images

## Success Metrics

- Verdict accuracy: >80% (human-labeled test set)
- Helpfulness score: >4.0/5.0 (user feedback)
- Consistency score: >0.85 (inter-rater agreement)

## MVP Scope

**In Scope:**
- 3-page flow (Setup → Capsule → Scanner)
- Basic review analysis
- Hardcoded capsule templates
- SQLite database
- React frontend + FastAPI backend

**Out of Scope (v1):**
- User authentication
- Multi-user support
- Chrome extension
- Mobile app
- Real-time product scraping

## Timeline

- Week 1: Product + Data ✅
- Week 2: Capsule Generator v1 ✅
- Week 3: "Should I Buy This?" v1 ✅
- Week 4: Review ML Analyzer (planned)
- Week 5: Ranking + Alternatives ✅ (DB-backed alternatives; vector search planned)
- Week 6: Evaluation + Polish (planned)
