
"""Denomination Service - Manages shop denominations and change calculation"""
from typing import Dict, List
from sqlalchemy.orm import Session
from app.repositories.denomination_repository import DenominationRepository
from app.strategies.denomination_strategy import DenominationStrategy
from app.strategies.greedy_denomination import GreedyDenominationStrategy
from app.models.denomination import ShopDenomination


class DenominationService:
  """
  Service for denomination management using Strategy Pattern.
 
  Responsibilities:
  - Calculate change using configurable strategy
  - Update shop denomination counts
  - Query denomination availability
 
  Design Pattern: Strategy Pattern
  - Can switch denomination calculation algorithms at runtime
  - Default: Greedy algorithm (optimal for most currencies)
  """
 
  def __init__(
    self,
    db: Session,
    strategy: DenominationStrategy = None
  ):
    """
    Initialize denomination service.
   
    Args:
      db: Database session
      strategy: Denomination calculation strategy (defaults to Greedy)
    """
    self.db = db
    self.repo = DenominationRepository(db)
   # Default to greedy strategy if none provided
    self.strategy = strategy or GreedyDenominationStrategy()
 
  def set_strategy(self, strategy: DenominationStrategy) -> None:
    """
    Change the denomination calculation strategy at runtime.
   
    Args:
      strategy: New strategy to use
    """
    self.strategy = strategy
 
  def calculate_change(self, amount: float) -> Dict[int, int]:
    """
    Calculate change denominations using current strategy.
   
    Args:
      amount: Amount to return (float, will be converted to int)
   
    Returns:
      Dictionary mapping denomination to count to return
      Example: {500: 1, 50: 2, 20: 2, 2: 1, 1: 1}
   
    Raises:
      InsufficientChangeError: If exact change cannot be made
    """
   # Convert to integer (round down)
    amount_int = int(amount)
   
    if amount_int == 0:
      return {}
   
   # Get available denominations from database
    available = self.repo.get_all_as_dict()
   
   # Use strategy to calculate
    result = self.strategy.calculate_change(amount_int, available)
   
    return result
 
  def update_denominations(self, used_denominations: Dict[int, int]) -> bool:
    """
    Update shop denominations after returning change to customer.
   
    This decreases the available count for each denomination used.
   
    Args:
      used_denominations: Dictionary of {denomination: count_returned}
   
    Returns:
      True if successful, False otherwise
    """
    return self.repo.update_counts(used_denominations)
 
  def get_available_denominations(self) -> Dict[int, int]:
    """
    Get current denomination availability.
   
    Returns:
      Dictionary of {denomination: available_count}
    """
    return self.repo.get_all_as_dict()
 
  def get_all_denominations(self) -> List[ShopDenomination]:
    """
    Get all denomination records sorted by value (descending).
   
    Returns:
      List of ShopDenomination objects
    """
    return self.repo.get_all_sorted(descending=True)
 
  def replenish_denomination(self, value: int, count: int) -> bool:
    """
    Add more notes/coins of a specific denomination.
   
    Args:
      value: Denomination value
      count: Number to add
   
    Returns:
      True if successful, False if denomination not found
    """
    return self.repo.increase_count(value, count)
 
  def check_change_possible(self, amount: float) -> bool:
    """
    Check if exact change can be made for an amount.
   
    Args:
      amount: Amount to check
   
    Returns:
      True if change can be made, False otherwise
    """
    try:
      self.calculate_change(amount)
      return True
    except Exception:
      return False