"""
Refine a user's "three words" (Alison Bornstein–style vibe) into more specific
style descriptors for capsule generation. Makes suggestions more precise.
"""

import re
from typing import List

# Map common vibe words to more specific wardrobe-relevant descriptors.
# Expands vague terms into actionable style language for matching products/palette.
STYLE_EXPANSION = {
    "relaxed": ["relaxed", "comfortable", "easy", "unfussy", "lived-in"],
    "minimal": ["minimal", "clean", "simple", "understated", "quiet luxury"],
    "french": ["effortless", "classic", "neutral", "timeless", "understated", "quality basics"],
    "elevated": ["elevated", "polished", "refined", "intentional", "put-together"],
    "sexy": ["sexy", "fitted", "confident", "bold", "statement"],
    "classic": ["classic", "timeless", "traditional", "wardrobe staples", "versatile"],
    "effortless": ["effortless", "easy", "relaxed", "unfussy", "natural"],
    "cozy": ["cozy", "soft", "comfortable", "layered", "warm"],
    "edgy": ["edgy", "bold", "black", "leather", "contrast", "statement"],
    "romantic": ["romantic", "soft", "feminine", "flowing", "delicate"],
    "sporty": ["sporty", "active", "clean lines", "comfortable", "functional"],
    "bohemian": ["bohemian", "flowing", "natural", "layered", "relaxed", "earthy"],
    "professional": ["professional", "polished", "tailored", "classic", "refined"],
    "casual": ["casual", "relaxed", "everyday", "comfortable", "easy"],
    "neutral": ["neutral", "earth tones", "beige", "cream", "black", "versatile"],
    "bold": ["bold", "statement", "color", "confident", "eye-catching"],
    "quiet": ["quiet luxury", "understated", "minimal", "quality", "refined"],
    "coastal": ["relaxed", "light", "linen", "neutral", "easy", "breathable"],
    "streetwear": ["streetwear", "casual", "sneakers", "oversized", "urban"],
    "preppy": ["preppy", "classic", "tailored", "polished", "traditional"],
}


def refine_style_words(three_words: str) -> List[str]:
    """
    Take 3 (or fewer/more) user words and return a list of more specific
    style descriptors for capsule generation (Alison Bornstein–style refinement).

    - Normalizes and splits input (comma or space).
    - Expands known terms via STYLE_EXPANSION.
    - Unknown words are kept as-is (user's own descriptors).
    - Deduplicates and limits to a reasonable length for prompts.
    """
    if not three_words or not three_words.strip():
        return ["versatile", "classic", "easy"]  # safe default

    # Split on commas and/or spaces, normalize
    raw = re.sub(r"[,;]+", " ", three_words.strip().lower())
    words = [w.strip() for w in raw.split() if w.strip()][:5]  # cap input words

    seen = set()
    result: List[str] = []

    for word in words:
        key = word.lower()
        if key in seen:
            continue
        if key in STYLE_EXPANSION:
            for descriptor in STYLE_EXPANSION[key]:
                d = descriptor.lower()
                if d not in seen:
                    seen.add(d)
                    result.append(descriptor)
        else:
            if key not in seen:
                seen.add(key)
                result.append(word)

    # Cap total descriptors so the prompt stays focused
    return result[:10] if result else ["versatile", "classic", "easy"]
