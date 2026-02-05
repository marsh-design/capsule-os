# CapsuleOS — What Works / What Doesn’t (Bare Bones)

## What works

**Quarter Setup**
- Form submits quarter, climate, style keywords, budget, brands.
- Calls `/api/generate-capsule` and gets a response.
- Saves result to `localStorage` and redirects to capsule page.

**Capsule Output**
- Reads capsule from `localStorage`.
- Shows palette (color swatches + labels).
- Shows outfit formulas (text list).
- Shows 12 items with **product images** (when available from API), item name, palette dots, and Best Value / Best Quality per item (brand, name, price). Images come from seed data (Unsplash URLs) and are passed through the capsule API (`image_url` on each option).
- Shows “Do Not Buy” if you had closet items (we don’t have closet upload wired yet, so this is usually empty).

**Backend**
- `/api/generate-capsule` returns real data from DB (products from sample_products.json).
- Caching works (repeat same inputs → cached response).
- Scoring (palette, versatility, overlap) runs; not shown in UI.
- `/api/health` works.
- DB is SQLite; seed with `python scripts/seed_db.py` in `backend/`.

**“Should I Buy This?” (Scanner)**
- UI: link vs manual entry, form, submit.
- Calls `/api/analyze-item` and gets JSON.
- Displays verdict (Buy/Wait/Skip), pros, cons, cost-per-wear, alternatives.
- Pros/cons now use price and brand (e.g. “Budget-friendly”, “From Everlane”). Alternatives are **real products from DB** (same price range, different brand) when available.

---

## What doesn’t work / is bare or fake

**Quarter Setup**
- In-page validation: “Select at least one style keyword” if none selected. API calls use relative `/api` (Vite proxy in dev).
- No “back” from capsule to edit setup (you start over from “Quarter Setup”).

**Capsule Output**
- Palette uses a **color-name → hex map** (sage, camel, navy, etc.) so swatches render correctly.
- **Empty state**: if no capsule in localStorage, shows “No capsule yet” and a “Create capsule” button instead of redirecting.
- Product images: shown when the capsule was generated after seeding DB with `image_url` (re-seed and regenerate capsule to see them). No product links to buy yet. “Do Not Buy” still usually blank (no closet in flow).

**Scanner**
- **Link input**: backend does not fetch or parse the URL. It returns a generic “Product from link” style response. No real data from the link.
- **Manual input**: description/brand/price are used only for scoring heuristics. No LLM, no review lookup, no real “insight”.
- Pros/cons are from simple rules (e.g. “runs small” only if a mock review_insights says so). Not personalized or rich.
- Alternatives: real products from DB in same price range (up to 3). Fallback message if DB lookup fails.

**Data / logic**
- Only ~10 seed products. Many capsule slots (e.g. “Scarf”, “Belt”) have no matching product, so you get generic “Best Value / Best Quality” placeholders.
- No user accounts, no real “closet”. Closet API exists but isn’t used in the UI flow.
- No real review insights: review_analyzer returns fixed mock data.
- No vector/embedding search, no real “alternatives” or “similar items”.

**UX / polish**
- Loading: spinner on capsule page and on buttons (“Generating...”, “Analyzing...”).
- Errors: **in-page message** (red banner), no `alert()`.
- No demo GIF/screenshot in README (placeholder only). No mobile-specific layout.

---

## One-line summary

**Works:** Quarter Setup → Generate Capsule → see a real capsule (palette, formulas, 12 items from DB with product images when seeded, or placeholders). Scanner returns a structured verdict + pros/cons/cost-per-wear + alternatives from DB; backend uses heuristics and DB lookups (no LLM required).

**Doesn’t / bare:** Real product-link parsing, real review-insights ML, closet in the flow, product buy links. Some capsule slots still get generic placeholders when no DB product matches the category.
