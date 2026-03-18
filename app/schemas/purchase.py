
"""Purchase Schemas - Response models for purchase history"""
from pydantic import BaseModel, EmailStr, Field
from typing import List
from datetime import datetime


class PurchaseItemResponse(BaseModel):
  """Schema for purchase item"""
  id: int
  product_id: str
  quantity: int
  unit_price: float
  tax_percentage: float
  purchase_price: float
  tax_amount: float
  total_price: float
 
  class Config:
    from_attributes = True


class PurchaseDenominationResponse(BaseModel):
  """Schema for purchase denomination"""
  id: int
  denomination_value: int
  count_returned: int
 
  class Config:
    from_attributes = True


class PurchaseResponse(BaseModel):
  """Schema for purchase response"""
  id: int
  customer_email: str
  total_amount: float
  tax_amount: float
  net_amount: float
  rounded_amount: int
  cash_paid: float
  balance_returned: float
  purchase_date: datetime
  items: List[PurchaseItemResponse]
  denominations: List[PurchaseDenominationResponse]
 
  class Config:
    from_attributes = True


class PurchaseListItem(BaseModel):
  """Schema for purchase list item (summary)"""
  id: int
  customer_email: str
  rounded_amount: int
  purchase_date: datetime
  item_count: int = Field(default=0, description="Number of items in purchase")
 
  class Config:
    from_attributes = True