
"""Greedy Algorithm Strategy for Denomination Calculation"""
from typing import Dict
from app.strategies.denomination_strategy import DenominationStrategy
from app.core.exceptions import InsufficientChangeError


class GreedyDenominationStrategy(DenominationStrategy):
  """
  Greedy algorithm for denomination calculation.
 
  Algorithm:
  1. Sort denominations in descending order (largest first)
  2. For each denomination:
   - Use as many as possible without exceeding remaining amount
   - Consider available count in shop
  3. If any amount remains, raise error (cannot make exact change)
 
  Time Complexity: O(n) where n is number of denominations
  Space Complexity: O(n)
 
  Optimality:
  Works optimally for most real-world currency systems (INR, USD, EUR)
  where denominations follow specific patterns (canonical coin systems).
 
  Example:
    amount = 643
    available = {500: 10, 50: 20, 20: 30, 10: 50, 5:50, 2: 100, 1: 200}
    result = {500: 1, 50: 2, 20: 2, 2: 1, 1: 1}
   
    Calculation:
    643 / 500 = 1 rem 143 → use 1x500
    143 / 50 = 2 rem 43  → use 2x50
    43 / 20  = 2 rem 3  → use 2x20
    3 / 10  = 0 rem 3  → use 0x10
    3 / 5   = 0 rem 3  → use 0x5
    3 / 2   = 1 rem 1  → use 1x2
    1 / 1   = 1 rem 0  → use 1x1
    Total: 500 + 100 + 40 + 2 + 1 = 643 ✓
  """
 
  def calculate_change(
    self,
    amount: int,
    available_denominations: Dict[int, int]
  ) -> Dict[int, int]:
    """
    Calculate change using greedy algorithm.
   
    Args:
      amount: Amount to return (integer)
      available_denominations: {denomination: available_count}
   
    Returns:
      {denomination: count_to_return}
   
    Raises:
      ValueError: If amount is negative
      InsufficientChangeError: If exact change cannot be made
    """
   # Validation
    if amount < 0:
      raise ValueError("Amount cannot be negative")
   
    if amount == 0:
      return {}
   
    result = {}
    remaining = amount
   
   # Sort denominations from largest to smallest
    sorted_denoms = sorted(available_denominations.keys(), reverse=True)
   
    for denom in sorted_denoms:
      if remaining == 0:
        break
     
      available_count = available_denominations[denom]
     
     # Calculate how many of this denomination we need
      count_needed = remaining // denom
     
     # Can't use more than what's available
      count_to_use = min(count_needed, available_count)
     
      if count_to_use > 0:
        result[denom] = count_to_use
        remaining -= denom * count_to_use
   
   # Verify exact change is possible
    if remaining > 0:
      raise InsufficientChangeError(
        f"Cannot make exact change for ₹{amount}. "
        f"Remaining: ₹{remaining}. "
        f"Available denominations are insufficient."
      )
   
   # Validate result
    if not self.validate_result(amount, result):
      raise ValueError("Internal error: calculated change is incorrect")
   
    return result