
"""Product Model - Represents products available in the shop"""
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Product(Base, TimestampMixin):
  """
  Product entity representing items available for purchase.
 
  Attributes:
    id: Auto-incrementing primary key
    product_id: Business identifier (e.g., P101, P102)
    name: Product name
    price: Unit price (float)
    tax_percentage: Tax percentage applicable (float, e.g., 12.0 for 12%)
    available_stock: Current available quantity
  """
  __tablename__ = "products"
 
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  product_id = Column(
    String(50),
    unique=True,
    nullable=False,
    index=True,
    comment="Business product identifier"
  )
  name = Column(String(200), nullable=False, comment="Product name")
  price = Column(Float, nullable=False, comment="Unit price")
  tax_percentage = Column(Float, nullable=False, comment="Tax percentage (e.g., 12.0)")
  available_stock = Column(
    Integer,
    nullable=False,
    default=0,
    comment="Available quantity in stock"
  )
 
 # Relationships
  purchase_items = relationship(
    "PurchaseItem",
    back_populates="product",
    cascade="all, delete-orphan"
  )
 
  def __repr__(self):
    return f"<Product {self.product_id}: {self.name} (₹{self.price})>"
 
  def __str__(self):
    return f"{self.product_id} - {self.name}"