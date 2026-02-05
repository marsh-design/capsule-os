# GitHub Issues (Reference)

Status as of current codebase. Use these as templates for new issues or to track remaining work.

## ✅ Done (no issue needed)

- **Capsule generator:** `/api/generate-capsule` with dynamic generation, product retrieval, palette, best value/quality, product images.
- **Scanner UI:** "Should I Buy This?" page with verdict, pros/cons, alternatives.
- **Scoring:** Palette match, versatility, closet overlap, cost-per-wear in `backend/app/services/scoring.py`.
- **Review insights baseline:** Rule-based/mock in `review_analyzer`; not full ML yet.

## Issue 1: Real review insights extractor (ML)
**Labels:** `enhancement`, `ml`

Replace mock review insights with keyword/sentiment extraction to identify fit signals, quality issues, and common complaints. See `docs/PRD.md` and `docs/ARCHITECTURE.md`.

## Issue 2: Evaluation harness skeleton
**Labels:** `enhancement`, `testing`

Create evaluation harness with verdict accuracy, helpfulness score, consistency score, and a small test dataset.

## Issue 3: Product link parsing (scanner)
**Labels:** `enhancement`, `backend`

When user submits a product URL, fetch and parse the page to prefill description/brand/price (or integrate with a product API).

## Issue 4: Vector search for alternatives
**Labels:** `enhancement`, `backend`, `ml`

Add embedding-based or vector search for “similar items” alternatives instead of (or in addition to) same price-range DB lookup.
