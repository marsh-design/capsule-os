# CapsuleOS — What Works / What Doesn’t (Bare Bones)

## What it can do now (full capacity)

**Quarter Setup (`/`)**
- Submit quarter (Q1–Q4), climate, style keywords, budget, and preferred brands.
- Form calls `POST /api/generate-capsule`; response is saved to `localStorage` and user is redirected to the capsule page.
- In-page validation: “Select at least one style keyword” if none selected. API uses relative `/api` (Vite proxy in dev).
- From capsule page, “Edit setup” link returns to Quarter Setup to change inputs and regenerate.

**Capsule Output (`/capsule`)**
- Reads capsule from `localStorage`.
- Renders **palette** (color swatches + labels via color-name → hex map: sage, camel, navy, etc.).
- Renders **outfit formulas** (3–4 text combinations).
- Renders **12 capsule items** with product image (when `image_url` exists in API response), item name, palette dots, and **Best Value** / **Best Quality** per slot (brand, name, price). Images come from seed data (Unsplash URLs) and are passed through the capsule API.
- Shows **“Do Not Buy”** when closet items were provided (closet not wired in flow, so often empty).
- Empty state: if no capsule in `localStorage`, shows “No capsule yet” and “Create capsule” (no auto-redirect).
- Loading: spinner on capsule page and on “Generating...” button. Errors: in-page red banner (no `alert()`).

**“Should I Buy This?” Scanner (`/scanner`)**
- **Link input**: UI accepts a URL; backend does **not** fetch or parse it—returns a generic “Product from link” style response.
- **Manual input**: User enters description, brand, price. Backend uses these for scoring heuristics only (no LLM, no review lookup).
- Calls `POST /api/analyze-item`; UI shows **verdict** (Buy / Wait / Skip), **pros**, **cons**, **cost-per-wear**, and **alternatives**.
- Pros/cons use price and brand (e.g. “Budget-friendly”, “From Everlane”). Alternatives are **real products from DB** (same price range, different brand, up to 3) when available; fallback message if none.
- Loading: “Analyzing...” on submit. Errors: in-page message.

**Browse / Catalog (`/browse`)**
- Lists all products from DB via `GET /api/products` with optional **category** filter (All, Top, Bottom, Outerwear, Shoes, Dress, Accessory).
- Shows product image, name, brand, price, colors; pagination via `limit`/`offset` (UI shows total count and grid).
- Empty state: message to run `python scripts/seed_db.py` in backend.

**Backend APIs**
- **Capsule:** `POST /api/generate-capsule` — returns real capsule from DB (products from seed data); **caching** (1h TTL) for repeat inputs.
- **Analyze:** `POST /api/analyze-item` — verdict + pros/cons/cost-per-wear + alternatives from DB (heuristic-based, no LLM).
- **Products:** `GET /api/products` — list with optional `category`, `limit`, `offset`.
- **Closet:** Closet API exists under `/api/closet` but is **not** used in the current UI flow.
- **Health:** `GET /`, `GET /api/health` — ok/healthy + version + DB status.
- **DB:** SQLite; init on startup; seed with `python scripts/seed_db.py` in `backend/`.
- **Scoring:** Palette match, versatility, overlap run in capsule pipeline; not exposed in UI.

**Tech / quality**
- Frontend: React + Vite + Tailwind; 4 routes (Quarter Setup, Capsule, Browse, Scanner).
- Backend: FastAPI, Pydantic models, structured JSON responses.
- CI: lint (flake8), format (black), tests (pytest). Docker Compose available.
- Evaluation harness: `python eval/run_eval.py` (from repo root) runs capsule + scanner test cases and reports pass/fail.

---

## What works (reference)

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
