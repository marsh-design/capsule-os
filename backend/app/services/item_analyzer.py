"""
Item analysis service - "Should I Buy This?" functionality
"""

from loguru import logger
from app.models import AnalyzeItemRequest, AnalyzeItemResponse, Verdict
from app.services.review_analyzer import ReviewAnalyzer
from app.services.scoring import ItemScorer
from typing import Optional, Dict, Any
import httpx


class ItemAnalyzer:
    """Analyze products and provide purchase recommendations"""
    
    def __init__(self):
        self.review_analyzer = ReviewAnalyzer()
        self.scorer = ItemScorer()
    
    async def analyze(
        self,
        product_link: Optional[str] = None,
        product_description: Optional[str] = None,
        price: Optional[float] = None,
        brand: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> AnalyzeItemResponse:
        """
        Analyze a product and generate purchase recommendation
        """
        logger.info(f"Analyzing item: {product_link or product_description}")
        
        # Extract product info
        if product_link:
            product_info = await self._extract_from_link(product_link)
        else:
            product_info = {
                "description": product_description,
                "price": price,
                "brand": brand
            }
        
        # Get review insights
        review_insights = await self.review_analyzer.analyze_product(
            product_id=None,  # TODO: Lookup by brand/name
            brand=product_info.get("brand"),
            product_name=product_info.get("name")
        )
        
        # Score the item
        score_result = await self.scorer.score_item(
            product_info=product_info,
            review_insights=review_insights,
            user_id=user_id
        )
        
        # Generate verdict
        verdict = self._determine_verdict(score_result["total_score"])
        
        # Generate pros/cons
        pros, cons = self._generate_pros_cons(score_result, review_insights)
        
        # Check closet overlap
        closet_warning = await self._check_closet_overlap(
            product_info, user_id
        )
        
        # Get alternatives
        alternatives = await self._get_alternatives(product_info)
        
        return AnalyzeItemResponse(
            verdict=verdict,
            confidence=abs(score_result["total_score"]),  # Normalize to 0-1
            pros=pros,
            cons=cons,
            closet_overlap_warning=closet_warning,
            alternatives=alternatives,
            review_insights=review_insights,
            cost_per_wear_estimate=score_result.get("cost_per_wear")
        )
    
    async def _extract_from_link(self, link: str) -> Dict[str, Any]:
        """Extract product info from URL (MVP: basic parsing)"""
        # TODO: Implement actual web scraping or use product API
        return {
            "link": link,
            "brand": "Unknown",
            "name": "Product from link",
            "price": None
        }
    
    def _determine_verdict(self, score: float) -> Verdict:
        """Determine verdict from score"""
        if score > 0.7:
            return Verdict.BUY
        elif score > 0.4:
            return Verdict.WAIT
        else:
            return Verdict.SKIP
    
    def _generate_pros_cons(
        self, 
        score_result: Dict[str, Any], 
        review_insights: Optional[Dict[str, Any]]
    ) -> tuple[list[str], list[str]]:
        """Generate pros and cons list"""
        pros = []
        cons = []
        
        if score_result.get("palette_score", 0) > 0.7:
            pros.append("Matches your capsule palette")
        else:
            cons.append("May not fit your color scheme")
        
        if review_insights:
            if review_insights.get("review_sentiment", 0) > 0.7:
                pros.append("Positive reviews from customers")
            else:
                cons.append("Mixed customer reviews")
            
            if review_insights.get("fit_signal") == "runs small":
                cons.append("Runs small - consider sizing up")
        
        if score_result.get("cost_per_wear", 0) < 5:
            pros.append("Great cost-per-wear value")
        elif score_result.get("cost_per_wear", 0) > 20:
            cons.append("High cost-per-wear - may not get enough use")
        
        return pros[:5], cons[:5]  # Limit to 5 each
    
    async def _check_closet_overlap(
        self, 
        product_info: Dict[str, Any], 
        user_id: Optional[int]
    ) -> Optional[str]:
        """Check if item overlaps with existing closet"""
        # TODO: Implement actual closet comparison
        return None
    
    async def _get_alternatives(self, product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get alternative product recommendations"""
        # TODO: Implement vector search for alternatives
        return [
            {
                "brand": "Alternative Brand",
                "name": "Similar Item",
                "price": product_info.get("price", 0) * 0.8,
                "reason": "Similar style, better value"
            }
        ]
