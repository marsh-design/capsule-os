"""
Capsule generation endpoints
"""

from fastapi import APIRouter, HTTPException
from loguru import logger
from app.models import CapsuleRequest, CapsuleResponse
from app.services.capsule_generator import CapsuleGenerator
from app.services.style_refiner import refine_style_words

router = APIRouter()
capsule_generator = CapsuleGenerator()


def _get_style_descriptors(request: CapsuleRequest) -> list:
    """Resolve style descriptors from three words (refined) or legacy style_keywords."""
    if request.style_three_words and request.style_three_words.strip():
        return refine_style_words(request.style_three_words)
    if request.style_keywords:
        return [kw.value for kw in request.style_keywords]
    return ["versatile", "classic", "easy"]


@router.post("/generate-capsule", response_model=CapsuleResponse)
async def generate_capsule(request: CapsuleRequest):
    """
    Generate a quarterly capsule wardrobe based on user preferences.
    Style: use style_three_words (e.g. "relaxed, minimal, French") or legacy style_keywords.
    """
    try:
        style_descriptors = _get_style_descriptors(request)
        logger.info(
            f"Generating capsule for {request.quarter}, climate: {request.climate}, style: {style_descriptors}"
        )

        capsule = await capsule_generator.generate(
            quarter=request.quarter,
            climate=request.climate,
            style_descriptors=style_descriptors,
            budget=request.budget,
            shopping_preferences=request.shopping_preferences,
            closet_items=request.closet_items or [],
        )

        return capsule
    except Exception as e:
        logger.error(f"Error generating capsule: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
