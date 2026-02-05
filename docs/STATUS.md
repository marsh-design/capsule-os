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
- Shows 12 items with Best Value / Best Quality per item (brand, name, price, reason).
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
- No product images, no links to buy. “Do Not Buy” still usually blank (no closet in flow).

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

**Works:** Quarter Setup → Generate Capsule → see a real capsule (palette, formulas, 12 items from DB or placeholders). Scanner returns a structured verdict + pros/cons/cost-per-wear, but all backend logic is mock/fake.

**Doesn’t / bare:** Real link parsing, real review insights, real alternatives, closet in the flow, product images/links, and most “smart” behavior. Scanner and many capsule slots are placeholder-level.
