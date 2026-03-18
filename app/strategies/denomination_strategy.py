
"""Abstract Strategy for Denomination Calculation"""
from abc import ABC, abstractmethod
from typing import Dict


class DenominationStrategy(ABC):
  """
  Abstract base class for denomination calculation strategies.
 
  Implements Strategy Pattern - allows different algorithms for calculating
  change denominations to be used interchangeably.
 
  Benefits:
  - Open/Closed Principle: Add new algorithms without modifying existing code
  - Single Responsibility: Each strategy implements one algorithm
  - Testability: Each strategy can be tested independently
  - Flexibility: Switch algorithms at runtime
  """
 
  @abstractmethod
  def calculate_change(
    self,
    amount: int,
    available_denominations: Dict[int, int]
  ) -> Dict[int, int]:
    """
    Calculate how to return change using available denominations.
   
    Args:
      amount: Total amount to return (integer, e.g., 643)
      available_denominations: Dictionary mapping denomination to count available
        Example: {500: 10, 50: 20, 20: 30, 10: 50, 5: 50, 2: 100, 1: 200}
   
    Returns:
      Dictionary mapping denomination to count to return
      Example: {500: 1, 50: 2, 20: 2, 2: 1, 1: 1} for amount=643
   
    Raises:
      ValueError: If exact change cannot be made with available denominations
    """
    pass
 
  def validate_result(self, amount: int, result: Dict[int, int]) -> bool:
    """
    Validate that calculated denominations add up to exact amount.
   
    This is a utility method that can be used by concrete strategies.
   
    Args:
      amount: Expected total amount
      result: Calculated denomination breakdown
     
    Returns:
      True if result sums to amount, False otherwise
    """
    total = sum(denom * count for denom, count in result.items())
    return total == amount