"""
Item analysis endpoints
"""

from fastapi import APIRouter, HTTPException
from loguru import logger
from app.models import AnalyzeItemRequest, AnalyzeItemResponse
from app.services.item_analyzer import ItemAnalyzer

router = APIRouter()
item_analyzer = ItemAnalyzer()


@router.post("/analyze-item", response_model=AnalyzeItemResponse)
async def analyze_item(request: AnalyzeItemRequest):
    """
    Analyze a product and provide purchase recommendation
    """
    try:
        logger.info(
            f"Analyzing item: {request.product_link or request.product_description}"
        )

        analysis = await item_analyzer.analyze(
            product_link=request.product_link,
            product_description=request.product_description,
            price=request.price,
            brand=request.brand,
            user_id=request.user_id,
        )

        return analysis
    except Exception as e:
        logger.error(f"Error analyzing item: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
