
"""Billing Schemas - Request and Response models for billing"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Dict, Any
from datetime import datetime


class BillingItemRequest(BaseModel):
  """Schema for a single item in billing request"""
  product_id: str = Field(..., min_length=1, description="Product ID")
  quantity: int = Field(..., gt=0, description="Quantity (must be positive)")


class BillingRequest(BaseModel):
  """Schema for creating a bill"""
  customer_email: EmailStr = Field(..., description="Customer email address")
  items: List[BillingItemRequest] = Field(..., min_items=1, description="List of products to purchase")
  cash_paid: float = Field(..., gt=0, description="Amount paid by customer")
 
  @field_validator('items')
  @classmethod
  def validate_items_not_empty(cls, v):
    if not v or len(v) == 0:
      raise ValueError("At least one item is required")
    return v


class BillItemResponse(BaseModel):
  """Schema for bill item in response"""
  product_id: str
  product_name: str
  quantity: int
  unit_price: float
  tax_percentage: float
  purchase_price: float
  tax_amount: float
  total_price: float


class DenominationResponse(BaseModel):
  """Schema for denomination breakdown"""
  value: int
  count: int
  amount: int


class BillSummaryResponse(BaseModel):
  """Schema for complete bill summary response"""
  purchase_id: int
  customer_email: str
  purchase_date: datetime
  items: List[BillItemResponse]
  total_amount: float
  tax_amount: float
  net_amount: float
  rounded_amount: int
  cash_paid: float
  balance_returned: float
  denominations: List[DenominationResponse]
 
  class Config:
    from_attributes = True