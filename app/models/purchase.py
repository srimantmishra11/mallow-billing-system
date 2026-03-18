
"""Purchase Model - Represents a customer purchase transaction"""
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, TimestampMixin


class Purchase(Base, TimestampMixin):
  """
  Purchase entity representing a complete billing transaction.
 
  Attributes:
    id: Auto-incrementing primary key
    customer_email: Customer's email address
    total_amount: Sum of all purchase prices before tax
    tax_amount: Total tax amount
    net_amount: Total amount including tax (total_amount + tax_amount)
    rounded_amount: Floor of net_amount (rounded down)
    cash_paid: Amount paid by customer
    balance_returned: Change returned to customer
    purchase_date: Transaction timestamp
    items: List of purchased items
    denominations: Denominations used for change
  """
  __tablename__ = "purchases"
 
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  customer_email = Column(
    String(255),
    nullable=False,
    index=True,
    comment="Customer email address"
  )
  total_amount = Column(
    Float,
    nullable=False,
    comment="Total before tax"
  )
  tax_amount = Column(
    Float,
    nullable=False,
    comment="Total tax amount"
  )
  net_amount = Column(
    Float,
    nullable=False,
    comment="Total including tax"
  )
  rounded_amount = Column(
    Integer,
    nullable=False,
    comment="Floor of net_amount"
  )
  cash_paid = Column(
    Float,
    nullable=False,
    comment="Cash paid by customer"
  )
  balance_returned = Column(
    Float,
    nullable=False,
    comment="Change returned to customer"
  )
  purchase_date = Column(
    DateTime,
    default=datetime.utcnow,
    nullable=False,
    index=True,
    comment="Purchase timestamp"
  )
 
 # Relationships
  items = relationship(
    "PurchaseItem",
    back_populates="purchase",
    cascade="all, delete-orphan",
    lazy="joined" # Eager load items
  )
  denominations = relationship(
    "PurchaseDenomination",
    back_populates="purchase",
    cascade="all, delete-orphan",
    lazy="joined" # Eager load denominations
  )
 
  def __repr__(self):
    return f"<Purchase {self.id}: {self.customer_email} - ₹{self.rounded_amount}>"
 
  def __str__(self):
    return f"Purchase #{self.id} - {self.customer_email}"