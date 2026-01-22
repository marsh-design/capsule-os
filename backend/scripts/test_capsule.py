"""
Test script for capsule generation
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import init_db, SessionLocal
from app.services.capsule_generator import CapsuleGenerator
from app.models import Quarter, Climate, StyleKeyword
import asyncio


async def test_capsule_generation():
    """Test capsule generation"""
    print("Initializing database...")
    init_db()

    # Check if database has products
    from app.database import Product

    db = SessionLocal()
    try:
        product_count = db.query(Product).count()

        if product_count == 0:
            print("Database is empty. Please run seed_db.py first:")
            print("  python scripts/seed_db.py")
            db.close()
            return

        print(f"Found {product_count} products in database")
    finally:
        db.close()

    # Create generator
    generator = CapsuleGenerator()

    # Test generation
    print("\nGenerating Q1 capsule...")
    capsule = await generator.generate(
        quarter=Quarter.Q1,
        climate=Climate.MODERATE,
        style_keywords=[StyleKeyword.EFFORTLESS, StyleKeyword.ELEVATED],
        budget=1000.0,
        shopping_preferences=["Everlane", "Aritzia", "Zara"],
        closet_items=[],
    )

    print(f"\n✅ Generated {capsule.quarter} capsule!")
    print(f"   Palette: {', '.join(capsule.palette)}")
    print(f"   Items: {len(capsule.items)}")
    print(f"   Outfit formulas: {len(capsule.outfit_formulas)}")

    if capsule.items:
        print(f"\n   First item: {capsule.items[0].item_name}")
        print(
            f"   Best Value: {capsule.items[0].best_value.brand} - ${capsule.items[0].best_value.price:.2f}"
        )
        print(
            f"   Best Quality: {capsule.items[0].best_quality.brand} - ${capsule.items[0].best_quality.price:.2f}"
        )

    print("\n✅ Capsule generation test passed!")


if __name__ == "__main__":
    asyncio.run(test_capsule_generation())
