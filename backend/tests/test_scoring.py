"""
Comprehensive tests for scoring functions
"""

import pytest
from app.services.scoring import CapsuleScorer, ItemScorer


class TestCapsuleScorer:
    """Test capsule scoring logic"""

    def test_palette_match_score(self):
        """Test palette matching score"""
        scorer = CapsuleScorer()
        items = [
            {"colors": ["black", "white"]},
            {"colors": ["navy", "gray"]},
            {"colors": ["red", "blue"]},
        ]
        palette = ["black", "navy", "cream"]

        score = scorer._score_palette_match(items, palette)
        assert 0 <= score <= 1
        assert score > 0  # Should have some matches

    def test_palette_match_perfect(self):
        """Test perfect palette match"""
        scorer = CapsuleScorer()
        items = [
            {"colors": ["black", "navy"]},
            {"colors": ["navy", "cream"]},
            {"colors": ["black", "cream"]},
        ]
        palette = ["black", "navy", "cream"]

        score = scorer._score_palette_match(items, palette)
        assert score == 1.0  # All items match

    def test_palette_match_empty(self):
        """Test empty items returns 0"""
        scorer = CapsuleScorer()
        score = scorer._score_palette_match([], ["black", "white"])
        assert score == 0.0

    def test_versatility_score(self):
        """Test versatility scoring"""
        scorer = CapsuleScorer()
        items = [
            {"category": "tee"},
            {"category": "jeans"},
            {"category": "blazer"},
            {"category": "dress"},
        ]

        score = scorer._score_versatility(items)
        assert 0 <= score <= 1
        assert score > 0  # Should have some versatile items

    def test_versatility_all_versatile(self):
        """Test all versatile items"""
        scorer = CapsuleScorer()
        items = [
            {"category": "tee"},
            {"category": "jeans"},
            {"category": "blazer"},
            {"category": "trench"},
        ]

        score = scorer._score_versatility(items)
        assert score == 1.0  # All are versatile

    def test_closet_overlap_no_closet(self):
        """Test overlap score with no existing closet"""
        scorer = CapsuleScorer()
        items = [{"category": "tee"}, {"category": "jeans"}]
        score = scorer._score_closet_overlap(items, [])
        assert score == 1.0  # No overlap is good

    def test_closet_overlap_with_duplicates(self):
        """Test overlap penalty reduces score"""
        scorer = CapsuleScorer()
        items = [
            {"category": "tee"},
            {"category": "jeans"},
            {"category": "blazer"},
        ]
        closet = [{"category": "tee"}, {"category": "jeans"}]

        score = scorer._score_closet_overlap(items, closet)
        assert 0 <= score < 1.0  # Overlap should reduce score
        assert score < 0.5  # Significant overlap

    def test_score_capsule_complete(self):
        """Test complete capsule scoring"""
        scorer = CapsuleScorer()
        items = [
            {"colors": ["black", "white"], "category": "tee"},
            {"colors": ["navy"], "category": "jeans"},
        ]
        palette = ["black", "navy", "white"]
        closet = []

        result = scorer.score_capsule(items, palette, closet)

        assert "palette_score" in result
        assert "versatility_score" in result
        assert "overlap_score" in result
        assert "total_score" in result

        assert 0 <= result["total_score"] <= 1
        assert result["overlap_score"] == 1.0  # No closet


class TestItemScorer:
    """Test item scoring logic"""

    def test_score_price_normalized(self):
        """Test price scoring is normalized to 0-1"""
        scorer = ItemScorer()
        score = scorer._score_price(50.0)
        assert 0 <= score <= 1

    def test_score_price_none(self):
        """Test price scoring with None returns default"""
        scorer = ItemScorer()
        score = scorer._score_price(None)
        assert score == 0.5

    def test_score_price_high(self):
        """Test high price gets lower score"""
        scorer = ItemScorer()
        low_price_score = scorer._score_price(50.0)
        high_price_score = scorer._score_price(400.0)

        assert low_price_score > high_price_score

    def test_score_reviews(self):
        """Test review sentiment scoring"""
        scorer = ItemScorer()
        insights = {"review_sentiment": 0.8}
        score = scorer._score_reviews(insights)
        assert score == 0.8

    def test_score_quality_mapping(self):
        """Test quality score mapping"""
        scorer = ItemScorer()

        excellent = scorer._score_quality({"quality": "excellent"})
        good = scorer._score_quality({"quality": "good"})
        mixed = scorer._score_quality({"quality": "mixed"})
        poor = scorer._score_quality({"quality": "poor"})

        assert excellent > good > mixed > poor
        assert excellent == 1.0
        assert poor == 0.25

    def test_cost_per_wear_estimate(self):
        """Test cost-per-wear calculation"""
        scorer = ItemScorer()

        cpw = scorer._estimate_cost_per_wear(100.0, {"quality": "good"})
        assert cpw is not None
        assert cpw > 0
        assert cpw < 10  # Should be reasonable

    def test_cost_per_wear_quality_impact(self):
        """Test quality affects cost-per-wear"""
        scorer = ItemScorer()

        excellent_cpw = scorer._estimate_cost_per_wear(100.0, {"quality": "excellent"})
        poor_cpw = scorer._estimate_cost_per_wear(100.0, {"quality": "poor"})

        assert excellent_cpw < poor_cpw  # Better quality = lower CPW

    def test_cost_per_wear_none_price(self):
        """Test cost-per-wear with None price"""
        scorer = ItemScorer()
        cpw = scorer._estimate_cost_per_wear(None, {})
        assert cpw is None

    @pytest.mark.asyncio
    async def test_score_item_complete(self):
        """Test complete item scoring"""
        scorer = ItemScorer()
        product_info = {"price": 50.0}
        review_insights = {
            "review_sentiment": 0.8,
            "quality": "good",
        }

        result = await scorer.score_item(product_info, review_insights)

        assert "price_score" in result
        assert "review_score" in result
        assert "quality_score" in result
        assert "total_score" in result
        assert "cost_per_wear" in result

        assert 0 <= result["total_score"] <= 1
        assert result["review_score"] == 0.8
        assert result["cost_per_wear"] is not None
