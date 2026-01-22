#!/usr/bin/env python3
"""Quick test of capsule generation"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.services.capsule_generator import CapsuleGenerator
from app.models import Quarter, Climate, StyleKeyword


async def test():
    print("🧪 Testing Capsule Generator...\n")

    gen = CapsuleGenerator()
    result = await gen.generate(
        quarter=Quarter.Q1,
        climate=Climate.MODERATE,
        style_keywords=[StyleKeyword.EFFORTLESS, StyleKeyword.ELEVATED],
        budget=1000.0,
        shopping_preferences=["Everlane", "Aritzia", "Zara"],
        closet_items=[],
    )

    print(f"✅ Generated {result.quarter} Capsule!")
    print(f"\n🎨 Color Palette: {', '.join(result.palette)}")
    print(f"\n📦 Items ({len(result.items)}):")

    for i, item in enumerate(result.items[:5], 1):
        print(f"\n  {i}. {item.item_name} ({item.category})")
        print(f"     💰 Best Value: {item.best_value.brand} - {item.best_value.name}")
        print(f"        Price: ${item.best_value.price:.2f}")
        print(
            f"     ✨ Best Quality: {item.best_quality.brand} - {item.best_quality.name}"
        )
        print(f"        Price: ${item.best_quality.price:.2f}")

    print(f"\n👗 Outfit Formulas ({len(result.outfit_formulas)}):")
    for formula in result.outfit_formulas:
        print(f"   • {formula}")

    if result.do_not_buy:
        print(f"\n❌ Do Not Buy: {', '.join(result.do_not_buy)}")

    print("\n✅ Test completed successfully!")


if __name__ == "__main__":
    asyncio.run(test())
