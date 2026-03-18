
"""Purchase API Endpoints - Purchase history and details"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas.purchase import PurchaseResponse, PurchaseListItem
from app.services.purchase_service import PurchaseService
from app.api.dependencies import get_purchase_service

router = APIRouter()


@router.get("/", response_model=List[PurchaseResponse])
async def list_purchases(
	skip: int = Query(0, ge=0),
	limit: int = Query(50, ge=1, le=100),
	service: PurchaseService = Depends(get_purchase_service)
):
	"""Get all purchases with pagination"""
	purchases = service.get_all_purchases(skip, limit)
	return purchases


@router.get("/customer/{email}", response_model=List[PurchaseResponse])
async def get_customer_purchases(
	email: str,
	skip: int = Query(0, ge=0),
	limit: int = Query(50, ge=1, le=100),
	service: PurchaseService = Depends(get_purchase_service)
):
	"""Get all purchases by customer email"""
	purchases = service.get_customer_purchases(email, skip, limit)
	return purchases


@router.get("/{purchase_id}", response_model=PurchaseResponse)
async def get_purchase_details(
	purchase_id: int,
	service: PurchaseService = Depends(get_purchase_service)
):
	"""Get detailed purchase information"""
	purchase = service.get_purchase_details(purchase_id)

	if not purchase:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"Purchase {purchase_id} not found"
		)

	return purchase


@router.get("/recent/", response_model=List[PurchaseResponse])
async def get_recent_purchases(
  days: int = Query(30, ge=1, le=365),
  service: PurchaseService = Depends(get_purchase_service)
):
  """Get purchases from the last N days"""
  purchases = service.get_recent_purchases(days)
  return purchases