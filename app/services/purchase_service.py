
"""Purchase Service - Business logic for purchase history"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.purchase_repository import PurchaseRepository
from app.models.purchase import Purchase


class PurchaseService:
  """
  Service for purchase history operations.
 
  Handles querying and retrieving purchase records.
  """
 
  def __init__(self, db: Session):
    """Initialize purchase service with database session"""
    self.db = db
    self.repo = PurchaseRepository(db)
 
  def get_customer_purchases(
    self,
    email: str,
    skip: int = 0,
    limit: int = 50
  ) -> List[Purchase]:
    """Get all purchases by customer email"""
    return self.repo.get_by_customer_email(email, skip, limit)
 
  def get_purchase_details(self, purchase_id: int) -> Optional[Purchase]:
    """Get purchase with all details"""
    return self.repo.get_with_details(purchase_id)
 
  def get_recent_purchases(self, days: int = 30) -> List[Purchase]:
    """Get recent purchases"""
    return self.repo.get_recent_purchases(days)
 
  def get_all_purchases(self, skip: int = 0, limit: int = 50) -> List[Purchase]:
    """Get all purchases with pagination"""
    return self.repo.get_all_with_details(skip, limit)