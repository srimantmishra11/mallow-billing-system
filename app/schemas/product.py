
"""Product Schemas - Request and Response models"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
  """Base product schema with common fields"""
  product_id: str = Field(..., min_length=1, max_length=50, description="Business product ID")
  name: str = Field(..., min_length=1, max_length=200, description="Product name")
  price: float = Field(..., gt=0, description="Unit price (must be positive)")
  tax_percentage: float = Field(..., ge=0, le=100, description="Tax percentage (0-100)")
  available_stock: int = Field(..., ge=0, description="Available stock quantity")


class ProductCreate(ProductBase):
  """Schema for creating a new product"""
  pass


class ProductUpdate(BaseModel):
  """Schema for updating a product (all fields optional)"""
  name: Optional[str] = Field(None, min_length=1, max_length=200)
  price: Optional[float] = Field(None, gt=0)
  tax_percentage: Optional[float] = Field(None, ge=0, le=100)
  available_stock: Optional[int] = Field(None, ge=0)


class ProductResponse(ProductBase):
  """Schema for product response"""
  id: int
  created_at: datetime
  updated_at: datetime
 
  class Config:
    from_attributes = True # Pydantic v2 (was orm_mode in v1)