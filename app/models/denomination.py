
"""Denomination Models - Shop denominations and purchase change"""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class ShopDenomination(Base, TimestampMixin):
  """
  Shop Denomination entity representing available currency in the shop.
 
  Attributes:
    id: Auto-incrementing primary key
    denomination_value: Currency value (e.g., 500, 50, 20, 10, 5, 2, 1)
    available_count: Number of notes/coins available
  """
  __tablename__ = "shop_denominations"
 
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  denomination_value = Column(
    Integer,
    nullable=False,
    unique=True,
    index=True,
    comment="Currency denomination value"
  )
  available_count = Column(
    Integer,
    nullable=False,
    default=0,
    comment="Available count in shop"
  )
 
  def __repr__(self):
    return f"<Denomination ₹{self.denomination_value}: {self.available_count} available>"
 
  def __str__(self):
    return f"₹{self.denomination_value} x {self.available_count}"


class PurchaseDenomination(Base):
  """
  Purchase Denomination entity representing change given to customer.
 
  Attributes:
    id: Auto-incrementing primary key
    purchase_id: Foreign key to Purchase
    denomination_value: Currency value returned
    count_returned: Number of notes/coins returned
  """
  __tablename__ = "purchase_denominations"
 
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  purchase_id = Column(
    Integer,
    ForeignKey("purchases.id", ondelete="CASCADE"),
    nullable=False,
    index=True
  )
  denomination_value = Column(
    Integer,
    nullable=False,
    comment="Denomination value returned"
  )
  count_returned = Column(
    Integer,
    nullable=False,
    comment="Count of this denomination returned"
  )
 
 # Relationships
  purchase = relationship("Purchase", back_populates="denominations")
 
  def __repr__(self):
    return f"<PurchaseDenom ₹{self.denomination_value} x {self.count_returned}>"
 
  def __str__(self):
    return f"₹{self.denomination_value} x {self.count_returned}"