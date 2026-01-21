"""
LLM prompt templates for structured outputs
"""

# Capsule generation prompt
CAPSULE_GENERATION_PROMPT = """
You are a fashion stylist helping create a quarterly capsule wardrobe.

User preferences:
- Quarter: {quarter}
- Climate: {climate}
- Style: {style_keywords}
- Budget: ${budget}
- Shopping preferences: {shopping_preferences}

Generate a capsule wardrobe with 12 items that:
1. Fit the color palette: {palette}
2. Work for the climate
3. Match the style keywords
4. Stay within budget
5. Are versatile and mix-and-match

Return a JSON object with:
{{
  "items": [
    {{
      "category": "string",
      "item_name": "string",
      "best_value": {{
        "brand": "string",
        "name": "string",
        "price": number,
        "reason": "string"
      }},
      "best_quality": {{
        "brand": "string",
        "name": "string",
        "price": number,
        "reason": "string"
      }},
      "palette_colors": ["string"]
    }}
  ],
  "outfit_formulas": ["string"]
}}
"""

# Item analysis prompt
ITEM_ANALYSIS_PROMPT = """
Analyze this product and provide a purchase recommendation.

Product: {product_description}
Price: ${price}
Brand: {brand}

Review insights:
{review_insights}

User's existing closet: {closet_summary}

Provide a structured analysis with:
1. Verdict: "buy", "wait", or "skip"
2. Confidence: 0-1
3. Pros: list of 3-5 reasons to buy
4. Cons: list of 3-5 reasons to avoid
5. Closet overlap warning: if item duplicates existing items

Return JSON:
{{
  "verdict": "buy|wait|skip",
  "confidence": 0.0-1.0,
  "pros": ["string"],
  "cons": ["string"],
  "closet_overlap_warning": "string or null",
  "reasoning": "string"
}}
"""

# Pros/cons generation prompt
PROS_CONS_PROMPT = """
Generate pros and cons for this product purchase decision.

Product: {product_name}
Price: ${price}
Review insights: {review_insights}
Score breakdown: {score_breakdown}

Generate:
- 3-5 pros (reasons to buy)
- 3-5 cons (reasons to avoid)

Be specific and actionable. Return JSON:
{{
  "pros": ["string"],
  "cons": ["string"]
}}
"""
