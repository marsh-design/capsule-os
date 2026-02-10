#!/usr/bin/env python3
"""
CapsuleOS evaluation harness (skeleton).

Runs capsule and scanner APIs against fixed test cases and reports
response shape, basic assertions, and placeholder metrics.
Run from repo root: python eval/run_eval.py
Or from backend with DB: cd backend && python ../eval/run_eval.py
"""

import json
import os
import sys
from pathlib import Path

# Run from repo root; ensure backend is on path for main:app
REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND = REPO_ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))
os.chdir(BACKEND)

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# --- Test cases ---
CAPSULE_PAYLOAD = {
    "quarter": "Q1",
    "climate": "moderate",
    "style_three_words": "relaxed, minimal, classic",
    "budget": 800,
    "shopping_preferences": ["Everlane", "Aritzia"],
}

ANALYZE_PAYLOAD = {
    "product_description": "Classic white crewneck tee",
    "price": 28.0,
    "brand": "Everlane",
}


def eval_capsule():
    """Call generate-capsule and check response shape and coherence score."""
    r = client.post("/api/generate-capsule", json=CAPSULE_PAYLOAD)
    assert r.status_code == 200, f"Capsule API returned {r.status_code}: {r.text}"
    data = r.json()
    assert "quarter" in data and data["quarter"] == "Q1"
    assert "palette" in data and isinstance(data["palette"], list)
    assert "outfit_formulas" in data and isinstance(data["outfit_formulas"], list)
    assert "items" in data and len(data["items"]) <= 12
    assert "do_not_buy" in data
    scores = data.get("coherence_scores")
    if scores:
        total = scores.get("total_score")
        assert total is not None and 0 <= total <= 1, f"total_score out of range: {total}"
    return {"ok": True, "items_count": len(data["items"]), "has_scores": scores is not None}


def eval_analyze():
    """Call analyze-item and check verdict and structure."""
    r = client.post("/api/analyze-item", json=ANALYZE_PAYLOAD)
    assert r.status_code == 200, f"Analyze API returned {r.status_code}: {r.text}"
    data = r.json()
    assert "verdict" in data and data["verdict"] in ("buy", "wait", "skip")
    assert "pros" in data and isinstance(data["pros"], list)
    assert "cons" in data and isinstance(data["cons"], list)
    assert "alternatives" in data and isinstance(data["alternatives"], list)
    return {"ok": True, "verdict": data["verdict"]}


def main():
    print("CapsuleOS evaluation harness (skeleton)\n")
    results = {}

    try:
        results["capsule"] = eval_capsule()
        print("  [PASS] Capsule: response shape and coherence score OK")
    except Exception as e:
        results["capsule"] = {"ok": False, "error": str(e)}
        print(f"  [FAIL] Capsule: {e}")

    try:
        results["analyze"] = eval_analyze()
        print("  [PASS] Scanner: verdict and structure OK")
    except Exception as e:
        results["analyze"] = {"ok": False, "error": str(e)}
        print(f"  [FAIL] Scanner: {e}")

    passed = sum(1 for v in results.values() if isinstance(v, dict) and v.get("ok"))
    total = len(results)
    print(f"\nResult: {passed}/{total} checks passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
