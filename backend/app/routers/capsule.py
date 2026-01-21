"""
Capsule generation endpoints
"""

from fastapi import APIRouter, HTTPException
from loguru import logger
from app.models import CapsuleRequest, CapsuleResponse
from app.services.capsule_generator import CapsuleGenerator

router = APIRouter()
capsule_generator = CapsuleGenerator()


@router.post("/generate-capsule", response_model=CapsuleResponse)
async def generate_capsule(request: CapsuleRequest):
    """
    Generate a quarterly capsule wardrobe based on user preferences
    """
    try:
        logger.info(
            f"Generating capsule for {request.quarter}, climate: {request.climate}"
        )

        capsule = await capsule_generator.generate(
            quarter=request.quarter,
            climate=request.climate,
            style_keywords=request.style_keywords,
            budget=request.budget,
            shopping_preferences=request.shopping_preferences,
            closet_items=request.closet_items or [],
        )

        return capsule
    except Exception as e:
        logger.error(f"Error generating capsule: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
