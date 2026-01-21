"""
Scoring services for capsule coherence and item evaluation
"""

from loguru import logger
from typing import Dict, Any, List, Optional
import numpy as np


class CapsuleScorer:
    """Score capsule wardrobe coherence"""
    
    def score_capsule(
        self,
        items: List[Dict[str, Any]],
        palette: List[str],
        closet_items: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Compute capsule coherence scores
        """
        palette_score = self._score_palette_match(items, palette)
        versatility_score = self._score_versatility(items)
        overlap_score = self._score_closet_overlap(items, closet_items)
        
        return {
            "palette_score": palette_score,
            "versatility_score": versatility_score,
            "overlap_score": overlap_score,
            "total_score": (palette_score + versatility_score + overlap_score) / 3
        }
    
    def _score_palette_match(self, items: List[Dict], palette: List[str]) -> float:
        """Score how well items match the palette"""
        # MVP: Simple color matching
        # TODO: Use color similarity metrics
        matches = 0
        for item in items:
            item_colors = item.get("colors", [])
            if any(color in palette for color in item_colors):
                matches += 1
        return matches / len(items) if items else 0.0
    
    def _score_versatility(self, items: List[Dict]) -> float:
        """Score how versatile items are (how many pairs)"""
        # MVP: Estimate based on categories
        # TODO: Use actual pairing logic
        versatile_categories = ["tee", "jeans", "blazer", "trench"]
        versatile_count = sum(
            1 for item in items
            if any(cat in item.get("category", "").lower() for cat in versatile_categories)
        )
        return versatile_count / len(items) if items else 0.0
    
    def _score_closet_overlap(self, items: List[Dict], closet: List[Dict]) -> float:
        """Score overlap with existing closet (lower is better for new items)"""
        if not closet:
            return 1.0  # No overlap is good
        
        closet_categories = {item.get("category", "").lower() for item in closet}
        new_categories = {item.get("category", "").lower() for item in items}
        
        overlap = len(closet_categories & new_categories)
        return 1.0 - (overlap / len(new_categories)) if new_categories else 1.0


class ItemScorer:
    """Score individual items for purchase decisions"""
    
    def __init__(self):
        pass
    
    async def score_item(
        self,
        product_info: Dict[str, Any],
        review_insights: Optional[Dict[str, Any]] = None,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Score an item across multiple dimensions
        """
        # Score components
        price_score = self._score_price(product_info.get("price"))
        review_score = self._score_reviews(review_insights) if review_insights else 0.5
        quality_score = self._score_quality(review_insights) if review_insights else 0.5
        
        # Compute cost-per-wear estimate
        cost_per_wear = self._estimate_cost_per_wear(
            product_info.get("price"),
            review_insights
        )
        
        total_score = (price_score + review_score + quality_score) / 3
        
        return {
            "price_score": price_score,
            "review_score": review_score,
            "quality_score": quality_score,
            "total_score": total_score,
            "cost_per_wear": cost_per_wear,
            "palette_score": 0.7  # TODO: Compute from user preferences
        }
    
    def _score_price(self, price: Optional[float]) -> float:
        """Score price (lower is better, normalized)"""
        if not price:
            return 0.5
        
        # Normalize to 0-1 (assuming $0-$500 range)
        normalized = 1.0 - min(price / 500.0, 1.0)
        return normalized
    
    def _score_reviews(self, review_insights: Dict[str, Any]) -> float:
        """Score based on review sentiment"""
        return review_insights.get("review_sentiment", 0.5)
    
    def _score_quality(self, review_insights: Dict[str, Any]) -> float:
        """Score quality based on review signals"""
        quality_map = {
            "excellent": 1.0,
            "good": 0.75,
            "mixed": 0.5,
            "poor": 0.25
        }
        quality_str = review_insights.get("quality", "mixed")
        return quality_map.get(quality_str, 0.5)
    
    def _estimate_cost_per_wear(
        self, 
        price: Optional[float], 
        review_insights: Optional[Dict[str, Any]]
    ) -> Optional[float]:
        """Estimate cost-per-wear"""
        if not price:
            return None
        
        # MVP: Simple heuristic
        # TODO: Use ML model based on category, quality, etc.
        base_wears = 30  # Assume 30 wears per year
        quality_multiplier = {
            "excellent": 1.5,
            "good": 1.0,
            "mixed": 0.7,
            "poor": 0.5
        }
        
        if review_insights:
            multiplier = quality_multiplier.get(review_insights.get("quality", "good"), 1.0)
            estimated_wears = base_wears * multiplier
        else:
            estimated_wears = base_wears
        
        return price / estimated_wears
