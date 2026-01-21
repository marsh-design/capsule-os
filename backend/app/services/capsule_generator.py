"""
Capsule wardrobe generator service
"""

from loguru import logger
from app.models import CapsuleResponse, CapsuleItem, ItemOption, Quarter, Climate, StyleKeyword
from app.services.scoring import CapsuleScorer
from typing import List, Dict, Any
import json
import os


class CapsuleGenerator:
    """Generate quarterly capsule wardrobes"""
    
    def __init__(self):
        self.scorer = CapsuleScorer()
        self.templates_path = os.path.join(
            os.path.dirname(__file__), 
            "../../data/capsule_templates.json"
        )
        self._load_templates()
    
    def _load_templates(self):
        """Load capsule templates"""
        try:
            with open(self.templates_path, 'r') as f:
                self.templates = json.load(f)
        except FileNotFoundError:
            logger.warning(f"Templates file not found: {self.templates_path}")
            self.templates = self._default_templates()
    
    def _default_templates(self):
        """Default capsule templates"""
        return {
            "Q1": {
                "palette": ["black", "navy", "cream", "camel", "gray"],
                "items": ["trench_coat", "sweater", "jeans", "boots", "scarf"]
            },
            "Q2": {
                "palette": ["white", "beige", "sage", "denim", "tan"],
                "items": ["blazer", "tee", "trousers", "sneakers", "tote"]
            }
        }
    
    async def generate(
        self,
        quarter: Quarter,
        climate: Climate,
        style_keywords: List[StyleKeyword],
        budget: float,
        shopping_preferences: List[str],
        closet_items: List[Dict[str, Any]]
    ) -> CapsuleResponse:
        """
        Generate capsule wardrobe
        """
        logger.info(f"Generating {quarter} capsule for {climate} climate")
        
        # Get base template
        template_key = str(quarter.value)
        template = self.templates.get(template_key, self.templates.get("Q1"))
        
        # Generate items (for MVP, using template + mock data)
        items = await self._generate_items(
            template=template,
            climate=climate,
            style_keywords=style_keywords,
            budget=budget,
            shopping_preferences=shopping_preferences,
            closet_items=closet_items
        )
        
        # Generate outfit formulas
        outfit_formulas = self._generate_outfit_formulas(items, template["palette"])
        
        # Compute do_not_buy list
        do_not_buy = self._compute_do_not_buy(closet_items, items)
        
        return CapsuleResponse(
            quarter=quarter.value,
            palette=template["palette"],
            outfit_formulas=outfit_formulas,
            items=items,
            do_not_buy=do_not_buy
        )
    
    async def _generate_items(
        self,
        template: Dict,
        climate: Climate,
        style_keywords: List[StyleKeyword],
        budget: float,
        shopping_preferences: List[str],
        closet_items: List[Dict[str, Any]]
    ) -> List[CapsuleItem]:
        """Generate capsule items with best value/quality options"""
        # MVP: Return hardcoded items based on template
        # TODO: Replace with actual product retrieval + ranking
        
        categories = [
            "Outerwear", "Top", "Bottom", "Shoes", "Accessory",
            "Dress", "Sweater", "Tee", "Jeans", "Jacket", "Bag", "Scarf"
        ]
        
        items = []
        for i, category in enumerate(categories[:12]):  # Limit to 12 items
            items.append(CapsuleItem(
                category=category,
                item_name=f"{category} Item",
                best_value=ItemOption(
                    brand="Everlane" if "Everlane" in shopping_preferences else "Zara",
                    name=f"Best Value {category}",
                    price=budget / 12 * 0.6,  # 60% of per-item budget
                    reason="Great quality-to-price ratio"
                ),
                best_quality=ItemOption(
                    brand="Aritzia" if "Aritzia" in shopping_preferences else "Everlane",
                    name=f"Best Quality {category}",
                    price=budget / 12 * 1.4,  # 140% of per-item budget
                    reason="Premium materials and construction"
                ),
                palette_colors=template["palette"][:2]  # First 2 colors
            ))
        
        return items
    
    def _generate_outfit_formulas(self, items: List[CapsuleItem], palette: List[str]) -> List[str]:
        """Generate outfit combination formulas"""
        formulas = [
            f"{items[0].category} + {items[1].category} + {items[2].category}",
            f"{items[3].category} + {items[4].category} + {items[5].category}",
            f"{items[6].category} + {items[7].category} + {items[8].category}",
        ]
        return formulas[:3]
    
    def _compute_do_not_buy(self, closet_items: List[Dict], new_items: List[CapsuleItem]) -> List[str]:
        """Compute items to avoid (duplicates, bad value)"""
        # MVP: Simple duplicate detection
        closet_categories = {item.get("category", "").lower() for item in closet_items}
        duplicates = [
            item.category for item in new_items
            if item.category.lower() in closet_categories
        ]
        return duplicates[:3]  # Return top 3
