
"""Product Service - Business logic for product management"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository
from app.models.product import Product
from app.core.exceptions import ProductNotFoundError


class ProductService:
  """
  Service for product management operations.
 
  Handles CRUD operations and business logic for products.
  """
 
  def __init__(self, db: Session):
    """Initialize product service with database session"""
    self.db = db
    self.repo = ProductRepository(db)
 
  def get_all_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
    """Get all products with pagination"""
    return self.repo.get_all(skip, limit)
 
  def get_product(self, product_id: str) -> Optional[Product]:
    """Get product by business ID"""
    return self.repo.get_by_product_id(product_id)
 
  def get_product_by_db_id(self, id: int) -> Optional[Product]:
    """Get product by database ID"""
    return self.repo.get_by_id(id)
 
  def create_product(
    self,
    product_id: str,
    name: str,
    price: float,
    tax_percentage: float,
    available_stock: int
  ) -> Product:
    """Create a new product"""
    return self.repo.create(
      product_id=product_id,
      name=name,
      price=price,
      tax_percentage=tax_percentage,
      available_stock=available_stock
    )
 
  def update_product(
    self,
    product_id: str,
    **updates
  ) -> Optional[Product]:
    """Update product by business ID"""
    product = self.repo.get_by_product_id(product_id)
    if not product:
      return None
    return self.repo.update(product.id, **updates)
 
  def delete_product(self, product_id: str) -> bool:
    """Delete product by business ID"""
    product = self.repo.get_by_product_id(product_id)
    if not product:
      return False
    return self.repo.delete(product.id)
 
  def get_available_products(self) -> List[Product]:
    """Get products with stock > 0"""
    return self.repo.get_available_products()
 
  def search_products(self, name: str) -> List[Product]:
    """Search products by name"""
    return self.repo.search_by_name(name)