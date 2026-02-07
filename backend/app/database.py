"""
Database configuration and initialization
"""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    JSON,
    DateTime,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./capsuleos.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    preferences = Column(JSON)  # Store user preferences


class ClosetItem(Base):
    __tablename__ = "closet_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    brand = Column(String)
    category = Column(String)
    color = Column(String)
    description = Column(Text)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    name = Column(String)
    category = Column(String, index=True)
    price = Column(Float)
    description = Column(Text)
    colors = Column(JSON)  # Array of colors
    image_url = Column(String)
    link = Column(String)  # Optional shop URL (brand site, product page, etc.)
    product_metadata = Column(JSON)  # Additional product data (renamed from metadata)
    created_at = Column(DateTime, default=datetime.utcnow)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    rating = Column(Integer)  # 1-5
    text = Column(Text)
    reviewer_info = Column(JSON)  # Size, height, etc.
    created_at = Column(DateTime, default=datetime.utcnow)


class ReviewInsight(Base):
    __tablename__ = "review_insights"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    fit_signal = Column(String)  # "runs small", "runs large", "true to size"
    quality_score = Column(Float)  # 0-1
    fabric_quality = Column(String)
    common_complaints = Column(JSON)  # ["pilling", "see-through"]
    review_sentiment = Column(Float)  # 0-1
    extracted_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    # Add 'link' column to products if missing (e.g. after pulling new code)
    if DATABASE_URL.startswith("sqlite"):
        from sqlalchemy import text

        with engine.connect() as conn:
            try:
                conn.execute(text("SELECT link FROM products LIMIT 1"))
            except Exception:
                try:
                    conn.execute(text("ALTER TABLE products ADD COLUMN link VARCHAR"))
                    conn.commit()
                except Exception:
                    pass


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
