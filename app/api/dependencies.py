
"""Dependencies for API endpoints - Dependency Injection"""
from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.product_service import ProductService
from app.services.billing_service import BillingService
from app.services.purchase_service import PurchaseService
from app.services.denomination_service import DenominationService


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
  """Dependency for ProductService"""
  return ProductService(db)


def get_billing_service(db: Session = Depends(get_db)) -> BillingService:
  """Dependency for BillingService"""
  return BillingService(db)


def get_purchase_service(db: Session = Depends(get_db)) -> PurchaseService:
  """Dependency for PurchaseService"""
  return PurchaseService(db)


def get_denomination_service(db: Session = Depends(get_db)) -> DenominationService:
  """Dependency for DenominationService"""
  return DenominationService(db)