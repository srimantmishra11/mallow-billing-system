
"""Purchase Item Model - Represents individual items in a purchase"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class PurchaseItem(Base):
  """
  Purchase Item entity representing a single product in a purchase.
 
  Attributes:
    id: Auto-incrementing primary key
    purchase_id: Foreign key to Purchase
    product_id: Foreign key to Product (business ID)
    quantity: Quantity purchased
    unit_price: Price per unit (captured at purchase time)
    tax_percentage: Tax percentage (captured at purchase time)
    purchase_price: unit_price * quantity
    tax_amount: Tax calculated on purchase_price
    total_price: purchase_price + tax_amount
  """
  __tablename__ = "purchase_items"
 
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  purchase_id = Column(
    Integer,
    ForeignKey("purchases.id", ondelete="CASCADE"),
    nullable=False,
    index=True
  )
  product_id = Column(
    String(50),
    ForeignKey("products.product_id", ondelete="RESTRICT"),
    nullable=False,
    index=True
  )
  quantity = Column(
    Integer,
    nullable=False,
    comment="Quantity purchased"
  )
  unit_price = Column(
    Float,
    nullable=False,
    comment="Unit price at time of purchase"
  )
  tax_percentage = Column(
    Float,
    nullable=False,
    comment="Tax percentage at time of purchase"
  )
  purchase_price = Column(
    Float,
    nullable=False,
    comment="unit_price * quantity"
  )
  tax_amount = Column(
    Float,
    nullable=False,
    comment="Tax calculated on purchase_price"
  )
  total_price = Column(
    Float,
    nullable=False,
    comment="purchase_price + tax_amount"
  )
 
 # Relationships
  purchase = relationship("Purchase", back_populates="items")
  product = relationship("Product", back_populates="purchase_items")
 
  def __repr__(self):
    return f"<PurchaseItem {self.product_id} x {self.quantity} = ₹{self.total_price}>"
 
  def __str__(self):
    return f"{self.product_id} (Qty: {self.quantity})"