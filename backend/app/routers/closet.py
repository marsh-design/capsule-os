"""
Closet management endpoints
"""

from fastapi import APIRouter, HTTPException
from loguru import logger
from typing import List, Dict, Any
from app.database import get_db, ClosetItem
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter()


@router.post("/upload")
async def upload_closet(
    items: List[Dict[str, Any]],
    user_id: int = 1,  # TODO: Get from auth
    db: Session = Depends(get_db)
):
    """
    Upload closet items
    """
    try:
        logger.info(f"Uploading {len(items)} closet items for user {user_id}")
        
        # Clear existing items (for MVP, single user)
        db.query(ClosetItem).filter(ClosetItem.user_id == user_id).delete()
        
        # Add new items
        for item in items:
            closet_item = ClosetItem(
                user_id=user_id,
                brand=item.get("brand"),
                category=item.get("category"),
                color=item.get("color"),
                description=item.get("description"),
                price=item.get("price", 0.0)
            )
            db.add(closet_item)
        
        db.commit()
        return {"status": "success", "items_uploaded": len(items)}
    except Exception as e:
        logger.error(f"Error uploading closet: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def get_closet(
    user_id: int = 1,  # TODO: Get from auth
    db: Session = Depends(get_db)
):
    """
    Get user's closet items
    """
    try:
        items = db.query(ClosetItem).filter(ClosetItem.user_id == user_id).all()
        return {
            "items": [
                {
                    "id": item.id,
                    "brand": item.brand,
                    "category": item.category,
                    "color": item.color,
                    "description": item.description,
                    "price": item.price
                }
                for item in items
            ]
        }
    except Exception as e:
        logger.error(f"Error getting closet: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
