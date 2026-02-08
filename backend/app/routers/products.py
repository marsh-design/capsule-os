"""
Product catalog endpoints — list products for Browse / Shop
"""

from typing import Optional

from fastapi import APIRouter, Query
from app.database import SessionLocal, Product

router = APIRouter()


@router.get("/products")
def list_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """List products for Browse page. Optional category filter (Top, Bottom, Outerwear, Shoes, Dress, Accessory)."""
    db = SessionLocal()
    try:
        q = db.query(Product)
        if category:
            q = q.filter(Product.category == category)
        total = q.count()
        products = q.order_by(Product.id).offset(offset).limit(limit).all()
        return {
            "products": [
                {
                    "id": p.id,
                    "brand": p.brand,
                    "name": p.name,
                    "category": p.category,
                    "price": p.price,
                    "description": p.description,
                    "colors": p.colors or [],
                    "image_url": p.image_url,
                    "link": p.link,
                }
                for p in products
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }
    finally:
        db.close()
