
"""Purchase Repository - Data access for Purchase entity"""
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from app.models.purchase import Purchase
from app.repositories.base_repository import BaseRepository


class PurchaseRepository(BaseRepository[Purchase]):
  """
  Purchase-specific repository extending BaseRepository.
 
  Handles purchase history queries with eager loading of related entities.
  """
 
  def __init__(self, db: Session):
    """Initialize with Purchase model and database session"""
    super().__init__(Purchase, db)
 
  def get_by_customer_email(
    self,
    email: str,
    skip: int = 0,
    limit: int = 50
  ) -> List[Purchase]:
    """
    Get all purchases by customer email, ordered by date (newest first).
   
    Args:
      email: Customer email address
      skip: Offset for pagination
      limit: Maximum records to return
     
    Returns:
      List of purchases with items and denominations eager-loaded
    """
    return self.db.query(Purchase).filter(
      Purchase.customer_email == email
    ).options(
      joinedload(Purchase.items),
      joinedload(Purchase.denominations)
    ).order_by(
      desc(Purchase.purchase_date)
    ).offset(skip).limit(limit).all()
 
  def get_with_details(self, purchase_id: int) -> Optional[Purchase]:
    """
    Get purchase with all related items and denominations loaded.
   
    Args:
      purchase_id: Purchase ID
     
    Returns:
      Purchase with items and denominations, or None
    """
    return self.db.query(Purchase).filter(
      Purchase.id == purchase_id
    ).options(
      joinedload(Purchase.items),
      joinedload(Purchase.denominations)
    ).first()
 
  def get_recent_purchases(self, days: int = 30, limit: int = 100) -> List[Purchase]:
    """
    Get purchases from the last N days.
   
    Args:
      days: Number of days to look back
      limit: Maximum records to return
     
    Returns:
      List of recent purchases
    """
    since = datetime.utcnow() - timedelta(days=days)
    return self.db.query(Purchase).filter(
      Purchase.purchase_date >= since
    ).order_by(
      desc(Purchase.purchase_date)
    ).limit(limit).all()
 
  def get_purchases_by_date_range(
    self,
    start_date: datetime,
    end_date: datetime
  ) -> List[Purchase]:
    """
    Get purchases within a date range.
   
    Args:
      start_date: Start of date range
      end_date: End of date range
     
    Returns:
      List of purchases in date range
    """
    return self.db.query(Purchase).filter(
      Purchase.purchase_date.between(start_date, end_date)
    ).order_by(desc(Purchase.purchase_date)).all()
 
  def get_total_sales(self, start_date: datetime, end_date: datetime) -> float:
    """
    Calculate total sales amount in a date range.
   
    Args:
      start_date: Start of date range
      end_date: End of date range
     
    Returns:
      Total sales amount
    """
    result = self.db.query(
      func.sum(Purchase.net_amount)
    ).filter(
      Purchase.purchase_date.between(start_date, end_date)
    ).scalar()
    return float(result) if result else 0.0
 
  def get_purchase_count(self, customer_email: str) -> int:
    """
    Get total number of purchases by a customer.
   
    Args:
      customer_email: Customer email
     
    Returns:
      Number of purchases
    """
    return self.db.query(Purchase).filter(
      Purchase.customer_email == customer_email
    ).count()
 
  def get_all_with_details(self, skip: int = 0, limit: int = 50) -> List[Purchase]:
    """
    Get all purchases with items and denominations eager-loaded.
   
    Args:
      skip: Offset for pagination
      limit: Maximum records to return
     
    Returns:
      List of purchases with details
    """
    return self.db.query(Purchase).options(
      joinedload(Purchase.items),
      joinedload(Purchase.denominations)
    ).order_by(
      desc(Purchase.purchase_date)
    ).offset(skip).limit(limit).all()