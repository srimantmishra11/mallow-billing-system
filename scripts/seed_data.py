
"""Seed Data Script - Initialize database with sample data"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import SessionLocal, init_db
from app.models.product import Product
from app.models.denomination import ShopDenomination


def seed_products(db):
  """Seed sample products"""
  print("🌱 Seeding products...")
 
  products = [
    {
      "product_id": "P101",
      "name": "Laptop",
      "price": 50000.00,
      "tax_percentage": 18.0,
      "available_stock": 10
    },
    {
      "product_id": "P102",
      "name": "Wireless Mouse",
      "price": 500.00,
      "tax_percentage": 12.0,
      "available_stock": 50
    },
    {
      "product_id": "P103",
      "name": "Mechanical Keyboard",
      "price": 1500.00,
      "tax_percentage": 12.0,
      "available_stock": 30
    },
    {
      "product_id": "P104",
      "name": "24-inch Monitor",
      "price": 15000.00,
      "tax_percentage": 18.0,
      "available_stock": 15
    },
    {
      "product_id": "P105",
      "name": "USB-C Cable",
      "price": 200.00,
      "tax_percentage": 5.0,
      "available_stock": 100
    },
    {
      "product_id": "P106",
      "name": "Headphones",
      "price": 2500.00,
      "tax_percentage": 12.0,
      "available_stock": 25
    },
    {
      "product_id": "P107",
      "name": "Webcam HD",
      "price": 3000.00,
      "tax_percentage": 12.0,
      "available_stock": 20
    },
    {
      "product_id": "P108",
      "name": "External SSD 500GB",
      "price": 5000.00,
      "tax_percentage": 18.0,
      "available_stock": 15
    }
  ]
 
  for p_data in products:
    product = Product(**p_data)
    db.add(product)
 
  db.commit()
  print(f"Seeded {len(products)} products")


def seed_denominations(db):
  """Seed shop denominations with initial counts"""
  print("Seeding denominations...")
 
  denominations = [
    {"denomination_value": 500, "available_count": 100},
    {"denomination_value": 50, "available_count": 200},
    {"denomination_value": 20, "available_count": 300},
    {"denomination_value": 10, "available_count": 500},
    {"denomination_value": 5, "available_count": 500},
    {"denomination_value": 2, "available_count": 1000},
    {"denomination_value": 1, "available_count": 2000},
  ]
 
  for d_data in denominations:
    denom = ShopDenomination(**d_data)
    db.add(denom)
 
  db.commit()
  print(f"Seeded {len(denominations)} denominations")


def main():
  """Main seeding function"""
  print("=" * 60)
  print("Billing System - Database Seeding")
  print("=" * 60)
 
  print("\n Initializing database...")
  init_db()
  print("Database initialized\n")
 
  db = SessionLocal()
  try:
   # Check if already seeded
    existing_products = db.query(Product).count()
    if existing_products > 0:
      print("Database already contains data.")
      response = input("Do you want to continue anyway? (yes/no): ")
      if response.lower() not in ['yes', 'y']:
        print("Seeding cancelled.")
        return
   
   # Seed data
    seed_products(db)
    seed_denominations(db)
   
    print("\n" + "=" * 60)
    print("Seeding complete!")
    print("=" * 60)
    print("\n Database Summary:")
    print(f"  Products: {db.query(Product).count()}")
    print(f"  Denominations: {db.query(ShopDenomination).count()}")
    print("\n You can now start the application!")
   
  except Exception as e:
    print(f"\n Error during seeding: {str(e)}")
    db.rollback()
  finally:
    db.close()


if __name__ == "__main__":
  main()