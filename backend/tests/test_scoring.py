"""
Tests for scoring functions
"""

import pytest
from app.services.scoring import CapsuleScorer, ItemScorer


def test_capsule_scorer_palette_match():
    """Test palette matching score"""
    scorer = CapsuleScorer()
    items = [
        {"colors": ["black", "white"]},
        {"colors": ["navy", "gray"]},
    ]
    palette = ["black", "navy", "cream"]
    
    score = scorer._score_palette_match(items, palette)
    assert 0 <= score <= 1


def test_capsule_scorer_versatility():
    """Test versatility scoring"""
    scorer = CapsuleScorer()
    items = [
        {"category": "tee"},
        {"category": "jeans"},
        {"category": "blazer"},
    ]
    
    score = scorer._score_versatility(items)
    assert 0 <= score <= 1


def test_item_scorer_price():
    """Test price scoring"""
    scorer = ItemScorer()
    score = scorer._score_price(50.0)
    assert 0 <= score <= 1


def test_item_scorer_cost_per_wear():
    """Test cost-per-wear estimation"""
    scorer = ItemScorer()
    cpw = scorer._estimate_cost_per_wear(100.0, {"quality": "good"})
    assert cpw is not None
    assert cpw > 0
