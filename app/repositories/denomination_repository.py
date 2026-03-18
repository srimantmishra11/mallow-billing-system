
"""Denomination Repository - Data access for ShopDenomination entity"""
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.denomination import ShopDenomination
from app.repositories.base_repository import BaseRepository


class DenominationRepository(BaseRepository[ShopDenomination]):
  """
  Denomination-specific repository extending BaseRepository.
 
  Manages shop currency denominations and their availability.
  """
 
  def __init__(self, db: Session):
    """Initialize with ShopDenomination model and database session"""
    super().__init__(ShopDenomination, db)
 
  def get_all_as_dict(self) -> Dict[int, int]:
    """
    Get all denominations as a dictionary.
   
    Returns:
      Dictionary mapping {denomination_value: available_count}
      Example: {500: 100, 50: 200, 20: 300, ...}
    """
    denoms = self.get_all(limit=1000) # Get all denominations
    return {d.denomination_value: d.available_count for d in denoms}
 
  def get_all_sorted(self, descending: bool = True) -> List[ShopDenomination]:
    """
    Get all denominations sorted by value.
   
    Args:
      descending: If True, sort from largest to smallest
     
    Returns:
      List of denominations sorted by value
    """
    query = self.db.query(ShopDenomination)
    if descending:
      query = query.order_by(desc(ShopDenomination.denomination_value))
    else:
      query = query.order_by(ShopDenomination.denomination_value)
    return query.all()
 
  def get_by_value(self, value: int) -> Optional[ShopDenomination]:
    """
    Get denomination by its value.
   
    Args:
      value: Denomination value (e.g., 500, 50, 20)
     
    Returns:
      ShopDenomination or None if not found
    """
    return self.db.query(ShopDenomination).filter(
      ShopDenomination.denomination_value == value
    ).first()
 
  def decrease_count(self, value: int, count: int) -> bool:
    """
    Decrease the count of a specific denomination.
   
    Args:
      value: Denomination value
      count: Number to decrease
     
    Returns:
      True if successful, False if insufficient count or not found
    """
    denom = self.get_by_value(value)
    if denom and denom.available_count >= count:
      denom.available_count -= count
      self.db.commit()
      self.db.refresh(denom)
      return True
    return False
 
  def increase_count(self, value: int, count: int) -> bool:
    """
    Increase the count of a specific denomination.
   
    Args:
      value: Denomination value
      count: Number to increase
     
    Returns:
      True if successful, False if denomination not found
    """
    denom = self.get_by_value(value)
    if denom:
      denom.available_count += count
      self.db.commit()
      self.db.refresh(denom)
      return True
    return False
 
  def update_counts(self, changes: Dict[int, int]) -> bool:
    """
    Update multiple denomination counts in a single transaction.
   
    This is used when returning change to customer - decrements multiple
    denominations atomically.
   
    Args:
      changes: Dictionary of {denomination_value: count_to_subtract}
     
    Returns:
      True if all updates successful, False otherwise (rolls back)
    """
    try:
     # First check if all denominations have sufficient count
      for value, count in changes.items():
        denom = self.get_by_value(value)
        if not denom or denom.available_count < count:
          self.db.rollback()
          return False
     
     # If all checks pass, perform updates
      for value, count in changes.items():
        denom = self.get_by_value(value)
        denom.available_count -= count
     
      self.db.commit()
      return True
    except Exception:
      self.db.rollback()
      return False
 
  def check_availability(self, value: int, required_count: int) -> bool:
    """
    Check if sufficient count of a denomination is available.
   
    Args:
      value: Denomination value
      required_count: Required count
     
    Returns:
      True if sufficient count available, False otherwise
    """
    denom = self.get_by_value(value)
    return denom is not None and denom.available_count >= required_count
 
  def get_available_denominations(self) -> List[ShopDenomination]:
    """
    Get denominations that have count > 0.
   
    Returns:
      List of available denominations
    """
    return self.db.query(ShopDenomination).filter(
      ShopDenomination.available_count > 0
    ).order_by(desc(ShopDenomination.denomination_value)).all()