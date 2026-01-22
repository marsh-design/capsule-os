"""
Capsule wardrobe generator service
"""

from loguru import logger
from app.models import (
    CapsuleResponse,
    CapsuleItem,
    ItemOption,
    Quarter,
    Climate,
    StyleKeyword,
)
from app.services.scoring import CapsuleScorer
from app.database import SessionLocal, Product
from typing import List, Dict, Any, Optional
import json
import os


class CapsuleGenerator:
    """Generate quarterly capsule wardrobes"""

    def __init__(self):
        self.scorer = CapsuleScorer()
        self.templates_path = os.path.join(
            os.path.dirname(__file__), "../../data/capsule_templates.json"
        )
        self._load_templates()
        self._load_category_mapping()

    def _load_templates(self):
        """Load capsule templates"""
        try:
            with open(self.templates_path, "r") as f:
                self.templates = json.load(f)
        except FileNotFoundError:
            logger.warning(f"Templates file not found: {self.templates_path}")
            self.templates = self._default_templates()

    def _load_category_mapping(self):
        """Map template item names to database categories"""
        self.category_mapping = {
            "trench_coat": ["Outerwear"],
            "wool_coat": ["Outerwear"],
            "sweater": ["Top", "Sweater"],
            "jeans": ["Bottom", "Jeans"],
            "boots": ["Shoes"],
            "scarf": ["Accessory"],
            "turtleneck": ["Top"],
            "blazer": ["Outerwear"],
            "trousers": ["Bottom"],
            "loafers": ["Shoes"],
            "bag": ["Accessory"],
            "belt": ["Accessory"],
            "tee": ["Top", "Tee"],
            "trousers": ["Bottom"],
            "sneakers": ["Shoes"],
            "tote": ["Accessory"],
            "cardigan": ["Top", "Sweater"],
            "midi_dress": ["Dress"],
            "sandals": ["Shoes"],
            "linen_shirt": ["Top"],
            "wide_leg_pants": ["Bottom"],
            "crossbody": ["Accessory"],
            "sunglasses": ["Accessory"],
            "sundress": ["Dress"],
            "shorts": ["Bottom"],
            "tank": ["Top"],
            "hat": ["Accessory"],
            "linen_pants": ["Bottom"],
            "kimono": ["Outerwear"],
            "bikini": ["Top"],
            "coverup": ["Outerwear"],
            "gloves": ["Accessory"],
        }

    def _default_templates(self):
        """Default capsule templates"""
        return {
            "Q1": {
                "palette": ["black", "navy", "cream", "camel", "gray"],
                "items": ["trench_coat", "sweater", "jeans", "boots", "scarf"],
            },
            "Q2": {
                "palette": ["white", "beige", "sage", "denim", "tan"],
                "items": ["blazer", "tee", "trousers", "sneakers", "tote"],
            },
        }

    async def generate(
        self,
        quarter: Quarter,
        climate: Climate,
        style_keywords: List[StyleKeyword],
        budget: float,
        shopping_preferences: List[str],
        closet_items: List[Dict[str, Any]],
    ) -> CapsuleResponse:
        """
        Generate capsule wardrobe
        """
        logger.info(f"Generating {quarter} capsule for {climate} climate")

        # Get base template
        template_key = str(quarter.value)
        template = self.templates.get(template_key, self.templates.get("Q1"))

        # Generate items from database
        items = await self._generate_items(
            template=template,
            climate=climate,
            style_keywords=style_keywords,
            budget=budget,
            shopping_preferences=shopping_preferences,
            closet_items=closet_items,
        )

        # Extract palette from selected items
        palette = self._extract_palette(items, template["palette"])

        # Generate outfit formulas
        outfit_formulas = self._generate_outfit_formulas(items, palette)

        # Compute do_not_buy list
        do_not_buy = self._compute_do_not_buy(closet_items, items)

        return CapsuleResponse(
            quarter=quarter.value,
            palette=palette,
            outfit_formulas=outfit_formulas,
            items=items,
            do_not_buy=do_not_buy,
        )

    async def _generate_items(
        self,
        template: Dict,
        climate: Climate,
        style_keywords: List[StyleKeyword],
        budget: float,
        shopping_preferences: List[str],
        closet_items: List[Dict[str, Any]],
    ) -> List[CapsuleItem]:
        """Generate capsule items with best value/quality options from database"""
        db = SessionLocal()
        try:
            template_items = template.get("items", [])[:12]  # Limit to 12 items
            capsule_items = []

            for template_item in template_items:
                # Map template item to database categories
                categories = self.category_mapping.get(
                    template_item, [template_item.capitalize()]
                )

                # Query products matching categories
                products = (
                    db.query(Product).filter(Product.category.in_(categories)).all()
                )

                if not products:
                    # Fallback: create placeholder item
                    capsule_items.append(
                        self._create_placeholder_item(
                            template_item, budget, shopping_preferences
                        )
                    )
                    continue

                # Filter by shopping preferences if provided
                if shopping_preferences:
                    preferred_products = [
                        p for p in products if p.brand in shopping_preferences
                    ]
                    if preferred_products:
                        products = preferred_products

                # Select best value and best quality
                best_value = self._select_best_value(products, budget / 12)
                best_quality = self._select_best_quality(products, budget / 12)

                # Get colors from selected items
                item_colors = []
                if best_value and best_value.colors:
                    item_colors.extend(best_value.colors)
                if best_quality and best_quality.colors:
                    item_colors.extend(best_quality.colors)

                capsule_items.append(
                    CapsuleItem(
                        category=self._format_category_name(template_item),
                        item_name=template_item.replace("_", " ").title(),
                        best_value=ItemOption(
                            brand=best_value.brand if best_value else "Generic",
                            name=(
                                best_value.name
                                if best_value
                                else f"{template_item} (Value)"
                            ),
                            price=best_value.price if best_value else budget / 12 * 0.6,
                            reason="Great quality-to-price ratio",
                        ),
                        best_quality=ItemOption(
                            brand=best_quality.brand if best_quality else "Generic",
                            name=(
                                best_quality.name
                                if best_quality
                                else f"{template_item} (Quality)"
                            ),
                            price=(
                                best_quality.price
                                if best_quality
                                else budget / 12 * 1.4
                            ),
                            reason="Premium materials and construction",
                        ),
                        palette_colors=(
                            list(set(item_colors))[:3]
                            if item_colors
                            else template["palette"][:2]
                        ),
                    )
                )

            return capsule_items[:12]  # Ensure max 12 items

        finally:
            db.close()

    def _select_best_value(
        self, products: List[Product], target_price: float
    ) -> Optional[Product]:
        """Select product with best value (price closest to target, lower preferred)"""
        if not products:
            return None

        # Score by price proximity to target (prefer lower)
        best_product = None
        best_score = float("inf")

        for product in products:
            if product.price <= target_price * 1.2:  # Within 20% of target
                score = abs(product.price - target_price * 0.7)  # Prefer 70% of target
                if score < best_score:
                    best_score = score
                    best_product = product

        # Fallback to cheapest if no good match
        if not best_product:
            best_product = min(products, key=lambda p: p.price)

        return best_product

    def _select_best_quality(
        self, products: List[Product], target_price: float
    ) -> Optional[Product]:
        """Select product with best quality (higher price, premium brands)"""
        if not products:
            return None

        # Prefer higher-priced items (proxy for quality)
        # Also prefer premium brands
        premium_brands = ["Aritzia", "Everlane", "Reformation"]
        premium_products = [p for p in products if p.brand in premium_brands]

        if premium_products:
            # Select highest priced premium product
            return max(premium_products, key=lambda p: p.price)

        # Fallback to highest priced overall
        return max(products, key=lambda p: p.price)

    def _create_placeholder_item(
        self, template_item: str, budget: float, shopping_preferences: List[str]
    ) -> CapsuleItem:
        """Create placeholder item when no products found"""
        category = self._format_category_name(template_item)
        return CapsuleItem(
            category=category,
            item_name=template_item.replace("_", " ").title(),
            best_value=ItemOption(
                brand=shopping_preferences[0] if shopping_preferences else "Generic",
                name=f"Best Value {category}",
                price=budget / 12 * 0.6,
                reason="Great quality-to-price ratio",
            ),
            best_quality=ItemOption(
                brand=(
                    shopping_preferences[1]
                    if len(shopping_preferences) > 1
                    else "Premium"
                ),
                name=f"Best Quality {category}",
                price=budget / 12 * 1.4,
                reason="Premium materials and construction",
            ),
            palette_colors=["black", "white"],
        )

    def _format_category_name(self, template_item: str) -> str:
        """Format template item name to readable category"""
        return template_item.replace("_", " ").title()

    def _extract_palette(
        self, items: List[CapsuleItem], default_palette: List[str]
    ) -> List[str]:
        """Extract color palette from selected items"""
        all_colors = []
        for item in items:
            if item.palette_colors:
                all_colors.extend(item.palette_colors)

        # Get unique colors, prioritize common ones
        color_counts = {}
        for color in all_colors:
            color_lower = color.lower()
            color_counts[color_lower] = color_counts.get(color_lower, 0) + 1

        # Sort by frequency and take top colors
        sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
        extracted = [color for color, _ in sorted_colors[:6]]

        # Fallback to default if not enough colors
        if len(extracted) < 4:
            extracted.extend(default_palette[: 6 - len(extracted)])

        return extracted[:6]  # Max 6 colors

    def _generate_outfit_formulas(
        self, items: List[CapsuleItem], palette: List[str]
    ) -> List[str]:
        """Generate outfit combination formulas"""
        if len(items) < 3:
            return []

        formulas = []
        # Create 3-4 outfit combinations
        combinations = [
            (0, 1, 2),  # First 3 items
            (3, 4, 5),  # Next 3 items
            (6, 7, 8),  # Next 3 items
            (9, 10, 11) if len(items) > 9 else None,  # Last 3 if available
        ]

        for combo in combinations:
            if combo and all(i < len(items) for i in combo):
                formula = " + ".join(
                    [items[i].category for i in combo if i < len(items)]
                )
                formulas.append(formula)

        # Fallback formulas if not enough items
        if not formulas and items:
            formulas.append(
                f"{items[0].category} + {items[1].category if len(items) > 1 else 'Accessories'}"
            )

        return formulas[:4]  # Max 4 formulas

    def _compute_do_not_buy(
        self, closet_items: List[Dict], new_items: List[CapsuleItem]
    ) -> List[str]:
        """Compute items to avoid (duplicates, bad value)"""
        if not closet_items:
            return []

        # Check for duplicate categories
        closet_categories = {item.get("category", "").lower() for item in closet_items}
        duplicates = [
            item.category
            for item in new_items
            if item.category.lower() in closet_categories
        ]

        return duplicates[:3]  # Return top 3
