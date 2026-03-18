
"""Product Repository - Data access for Product entity"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.product import Product
from app.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):
  """
  Product-specific repository extending BaseRepository.
 
  Inherits: get_by_id, get_all, create, update, delete from BaseRepository
  Adds: Product-specific query methods
  """
 
  def __init__(self, db: Session):
    """Initialize with Product model and database session"""
    super().__init__(Product, db)
 
  def get_by_product_id(self, product_id: str) -> Optional[Product]:
    """
    Get product by business product ID (not database ID).
   
    Args:
      product_id: Business product identifier (e.g., "P101")
     
    Returns:
      Product or None if not found
    """
    return self.db.query(Product).filter(
      Product.product_id == product_id
    ).first()
 
  def search_by_name(self, name: str) -> List[Product]:
    """
    Search products by name (case-insensitive partial match).
   
    Args:
      name: Product name search term
     
    Returns:
      List of matching products
    """
    return self.db.query(Product).filter(
      Product.name.ilike(f"%{name}%")
    ).all()
 
  def get_available_products(self) -> List[Product]:
    """
    Get products with available stock (stock > 0).
   
    Returns:
      List of products in stock
    """
    return self.db.query(Product).filter(
      Product.available_stock > 0
    ).all()
 
  def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
    """
    Get products with stock below threshold.
   
    Args:
      threshold: Stock level threshold
     
    Returns:
      List of low-stock products
    """
    return self.db.query(Product).filter(
      Product.available_stock < threshold,
      Product.available_stock > 0
    ).all()
 
  def get_out_of_stock_products(self) -> List[Product]:
    """
    Get products that are out of stock.
   
    Returns:
      List of out-of-stock products
    """
    return self.db.query(Product).filter(
      Product.available_stock == 0
    ).all()
 
  def decrease_stock(self, product_id: str, quantity: int) -> bool:
    """
    Decrease stock for a product (used during purchase).
   
    Args:
      product_id: Business product identifier
      quantity: Quantity to decrease
     
    Returns:
      True if successful, False if insufficient stock
    """
    product = self.get_by_product_id(product_id)
    if product and product.available_stock >= quantity:
      product.available_stock -= quantity
      self.db.commit()
      self.db.refresh(product)
      return True
    return False
 
  def increase_stock(self, product_id: str, quantity: int) -> bool:
    """
    Increase stock for a product (used for restocking/cancellations).
   
    Args:
      product_id: Business product identifier
      quantity: Quantity to increase
     
    Returns:
      True if successful, False if product not found
    """
    product = self.get_by_product_id(product_id)
    if product:
      product.available_stock += quantity
      self.db.commit()
      self.db.refresh(product)
      return True
    return False
 
  def check_stock_availability(self, product_id: str, quantity: int) -> bool:
    """
    Check if sufficient stock is available.
   
    Args:
      product_id: Business product identifier
      quantity: Required quantity
     
    Returns:
      True if sufficient stock available, False otherwise
    """
    product = self.get_by_product_id(product_id)
    return product is not None and product.available_stock >= quantity