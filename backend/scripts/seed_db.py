"""
Seed database with sample products and reviews
"""

import sys
import os
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, Product, Review, init_db
from sqlalchemy.orm import Session


def load_json_file(filepath: str) -> dict:
    """Load JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)


def seed_products(db: Session, products_data: list):
    """Seed products table"""
    for product_data in products_data:
        product = Product(
            id=product_data['id'],
            brand=product_data['brand'],
            name=product_data['name'],
            category=product_data['category'],
            price=product_data['price'],
            description=product_data['description'],
            colors=product_data['colors'],
            image_url=product_data.get('image_url'),
            metadata=product_data.get('metadata', {})
        )
        db.add(product)
    db.commit()
    print(f"Seeded {len(products_data)} products")


def seed_reviews(db: Session, reviews_data: list):
    """Seed reviews table"""
    for review_data in reviews_data:
        review = Review(
            product_id=review_data['product_id'],
            rating=review_data['rating'],
            text=review_data['text'],
            reviewer_info=review_data.get('reviewer_info', {})
        )
        db.add(review)
    db.commit()
    print(f"Seeded {len(reviews_data)} reviews")


def main():
    """Main seeding function"""
    print("Initializing database...")
    init_db()
    
    db = SessionLocal()
    try:
        # Get data directory
        data_dir = Path(__file__).parent.parent.parent / "data"
        
        # Load sample data
        products_data = load_json_file(data_dir / "sample_products.json")
        reviews_data = load_json_file(data_dir / "sample_reviews.json")
        
        # Seed database
        print("Seeding products...")
        seed_products(db, products_data)
        
        print("Seeding reviews...")
        seed_reviews(db, reviews_data)
        
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
