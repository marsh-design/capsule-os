"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class Quarter(str, Enum):
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"


class Climate(str, Enum):
    COLD = "cold"
    MODERATE = "moderate"
    WARM = "warm"
    HOT = "hot"


class StyleKeyword(str, Enum):
    EFFORTLESS = "effortless"
    ELEVATED = "elevated"
    SEXY = "sexy"
    MINIMAL = "minimal"
    CLASSIC = "classic"


class CapsuleRequest(BaseModel):
    quarter: Quarter
    climate: Climate
    style_keywords: List[StyleKeyword] = Field(..., min_items=1, max_items=3)
    budget: float = Field(..., gt=0, le=10000)
    shopping_preferences: List[str] = []  # Brand names
    closet_items: Optional[List[Dict[str, Any]]] = None


class ItemOption(BaseModel):
    brand: str
    name: str
    price: float
    link: Optional[str] = None
    image_url: Optional[str] = None
    reason: str  # Why this is the best value/quality option


class CapsuleItem(BaseModel):
    category: str
    item_name: str
    best_value: ItemOption
    best_quality: ItemOption
    palette_colors: List[str]


class CapsuleResponse(BaseModel):
    quarter: str
    palette: List[str]  # 5-7 colors
    outfit_formulas: List[str]
    items: List[CapsuleItem]
    do_not_buy: List[str]  # Items to avoid


class AnalyzeItemRequest(BaseModel):
    product_link: Optional[str] = None
    product_description: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None
    user_id: Optional[int] = None


class Verdict(str, Enum):
    BUY = "buy"
    WAIT = "wait"
    SKIP = "skip"


class AnalyzeItemResponse(BaseModel):
    verdict: Verdict
    confidence: float  # 0-1
    pros: List[str]
    cons: List[str]
    closet_overlap_warning: Optional[str] = None
    alternatives: List[Dict[str, Any]]
    review_insights: Optional[Dict[str, Any]] = None
    cost_per_wear_estimate: Optional[float] = None
