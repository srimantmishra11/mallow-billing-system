
"""Product API Endpoints -CRUD operations for products"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import ProductService
from app.api.dependencies import get_product_service

router = APIRouter()


@router.get("/", response_model=List[ProductResponse])
async def list_products(
	skip: int = 0,
	limit: int = 100,
	service: ProductService = Depends(get_product_service)
):
	"""Get all products"""
	products = service.get_all_products(skip, limit)
	return products


@router.get("/available", response_model=List[ProductResponse])
async def list_available_products(
	service: ProductService = Depends(get_product_service)
):
	"""Get products with stock > 0"""
	products = service.get_available_products()
	return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
	product_id: str,
	service: ProductService = Depends(get_product_service)
):
	"""Get product by business ID"""
	product = service.get_product(product_id)
	if not product:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"Product {product_id} not found"
		)
	return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
	product_data: ProductCreate,
	service: ProductService = Depends(get_product_service)
):
  """Create a new product"""
 # Check if product ID already exists
  existing = service.get_product(product_data.product_id)
  if existing:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"Product {product_data.product_id} already exists"
    )
 
  product = service.create_product(
    product_id=product_data.product_id,
    name=product_data.name,
    price=product_data.price,
    tax_percentage=product_data.tax_percentage,
    available_stock=product_data.available_stock
  )
  return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
  product_id: str,
  product_data: ProductUpdate,
  service: ProductService = Depends(get_product_service)
):
  """Update a product"""
 # Convert to dict, excluding None values
  updates = product_data.model_dump(exclude_none=True)
 
  product = service.update_product(product_id, **updates)
  if not product:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Product {product_id} not found"
    )
  return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
  product_id: str,
  service: ProductService = Depends(get_product_service)
):
  """Delete a product"""
  success = service.delete_product(product_id)
  if not success:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Product {product_id} not found"
    )
  return None