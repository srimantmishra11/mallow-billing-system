
"""Billing Service - Core business logic for billing operations"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from math import floor
from app.repositories.product_repository import ProductRepository
from app.repositories.purchase_repository import PurchaseRepository
from app.services.denomination_service import DenominationService
from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.models.denomination import PurchaseDenomination
from app.core.exceptions import (
  InsufficientStockError,
  ProductNotFoundError,
  InvalidQuantityError,
  InsufficientPaymentError
)


class BillingService:
  """
  Core billing service orchestrating the entire billing process.
 
  Responsibilities:
  - Validate products and stock availability
  - Calculate purchase prices, taxes, and totals
  - Calculate change denominations
  - Create purchase records
  - Update stock levels
  - Update denomination counts
 
  This service follows Service Layer Pattern - encapsulates business logic
  and orchestrates multiple repositories and services.
  """
 
  def __init__(self, db: Session):
    """
    Initialize billing service with database session.
   
    Args:
      db: SQLAlchemy database session
    """
    self.db = db
    self.product_repo = ProductRepository(db)
    self.purchase_repo = PurchaseRepository(db)
    self.denom_service = DenominationService(db)
 
  def create_bill(
    self,
    customer_email: str,
    items: List[Dict[str, Any]],
    cash_paid: float
  ) -> Purchase:
    """
    Create a complete bill with all calculations.
   
    This is the main orchestration method that:
    1. Validates all products and stock
    2. Calculates all prices and taxes
    3. Calculates change denominations
    4. Creates purchase record
    5. Updates stock levels
    6. Updates denomination counts
   
    Args:
      customer_email: Customer's email address
      items: List of dicts with 'product_id' and 'quantity'
        Example: [{'product_id': 'P101', 'quantity': 2}, ...]
      cash_paid: Amount paid by customer
   
    Returns:
      Purchase: Created purchase record with all details
   
    Raises:
      ProductNotFoundError: If product doesn't exist
      InsufficientStockError: If insufficient stock
      InvalidQuantityError: If quantity <= 0
      InsufficientPaymentError: If payment is insufficient
      InsufficientChangeError: If exact change cannot be made
    """
   # Step 1: Validate all items
    self._validate_items(items)
   
   # Step 2: Calculate bill items with prices and taxes
    bill_items = self._calculate_bill_items(items)
   
   # Step 3: Calculate totals
    totals = self._calculate_totals(bill_items)
   
   # Step 4: Validate payment
    if cash_paid < totals['rounded_amount']:
      raise InsufficientPaymentError(
        f"Insufficient payment. Required: ₹{totals['rounded_amount']}, "
        f"Paid: ₹{cash_paid}"
      )
   
   # Step 5: Calculate change denominations
    balance = cash_paid - totals['rounded_amount']
    denominations = {}
    if balance > 0:
      denominations = self.denom_service.calculate_change(balance)
   
   # Step 6: Create purchase record (transaction starts)
    try:
      purchase = self._create_purchase_record(
        customer_email=customer_email,
        totals=totals,
        cash_paid=cash_paid,
        balance=balance,
        bill_items=bill_items,
        denominations=denominations
      )
     
     # Step 7: Update stock levels
      self._update_stock(items)
     
     # Step 8: Update denomination counts
      if denominations:
        self.denom_service.update_denominations(denominations)
     
      self.db.commit()
      self.db.refresh(purchase)
     
      return purchase
     
    except Exception as e:
      self.db.rollback()
      raise e
 
  def _validate_items(self, items: List[Dict[str, Any]]) -> None:
    """
    Validate all items in the bill.
   
    Checks:
    - Product exists
    - Quantity is positive
    - Sufficient stock available
   
    Args:
      items: List of product items
   
    Raises:
      ProductNotFoundError: If product doesn't exist
      InvalidQuantityError: If quantity <= 0
      InsufficientStockError: If insufficient stock
    """
    for item in items:
      product_id = item.get('product_id')
      quantity = item.get('quantity', 0)
     
     # Validate quantity
      if quantity <= 0:
        raise InvalidQuantityError(
          f"Invalid quantity {quantity} for product {product_id}"
        )
     
     # Validate product exists
      product = self.product_repo.get_by_product_id(product_id)
      if not product:
        raise ProductNotFoundError(
          f"Product {product_id} not found"
        )
     
     # Validate stock availability
      if product.available_stock < quantity:
        raise InsufficientStockError(
          f"Insufficient stock for {product.name}. "
          f"Available: {product.available_stock}, Requested: {quantity}"
        )
 
  def _calculate_bill_items(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Calculate prices and taxes for all items.
   
    For each item calculates:
    - Purchase Price = Unit Price × Quantity
    - Tax Amount = Purchase Price × (Tax % / 100)
    - Total Price = Purchase Price + Tax Amount
   
    Args:
      items: List of product items with product_id and quantity
   
    Returns:
      List of dictionaries with all calculated fields
    """
    bill_items = []
   
    for item in items:
      product_id = item['product_id']
      quantity = item['quantity']
     
     # Get product details
      product = self.product_repo.get_by_product_id(product_id)
     
     # Calculate prices
      unit_price = product.price
      tax_percentage = product.tax_percentage
      purchase_price = unit_price * quantity
      tax_amount = purchase_price * (tax_percentage / 100)
      total_price = purchase_price + tax_amount
     
      bill_items.append({
        'product_id': product_id,
        'product_name': product.name,
        'quantity': quantity,
        'unit_price': unit_price,
        'tax_percentage': tax_percentage,
        'purchase_price': purchase_price,
        'tax_amount': tax_amount,
        'total_price': total_price
      })
   
    return bill_items
 
  def _calculate_totals(self, bill_items: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Calculate overall bill totals.
   
    Calculates:
    - Total Price Without Tax = Σ(Purchase Price)
    - Total Tax Payable = Σ(Tax Amount)
    - Net Price = Total + Tax
    - Rounded Amount = Floor(Net Price)
   
    Args:
      bill_items: List of calculated bill items
   
    Returns:
      Dictionary with total_amount, tax_amount, net_amount, rounded_amount
    """
    total_amount = sum(item['purchase_price'] for item in bill_items)
    tax_amount = sum(item['tax_amount'] for item in bill_items)
    net_amount = total_amount + tax_amount
    rounded_amount = floor(net_amount) # Round down
   
    return {
      'total_amount': total_amount,
      'tax_amount': tax_amount,
      'net_amount': net_amount,
      'rounded_amount': rounded_amount
    }
 
  def _create_purchase_record(
    self,
    customer_email: str,
    totals: Dict[str, float],
    cash_paid: float,
    balance: float,
    bill_items: List[Dict[str, Any]],
    denominations: Dict[int, int]
  ) -> Purchase:
    """
    Create Purchase record with items and denominations.
   
    Args:
      customer_email: Customer email
      totals: Calculated totals dictionary
      cash_paid: Amount paid by customer
      balance: Change to return
      bill_items: Calculated bill items
      denominations: Change denominations
   
    Returns:
      Created Purchase object
    """
   # Create Purchase
    purchase = Purchase(
      customer_email=customer_email,
      total_amount=totals['total_amount'],
      tax_amount=totals['tax_amount'],
      net_amount=totals['net_amount'],
      rounded_amount=totals['rounded_amount'],
      cash_paid=cash_paid,
      balance_returned=balance
    )
    self.db.add(purchase)
    self.db.flush() # Get purchase ID
   
   # Create Purchase Items
    for item in bill_items:
      purchase_item = PurchaseItem(
        purchase_id=purchase.id,
        product_id=item['product_id'],
        quantity=item['quantity'],
        unit_price=item['unit_price'],
        tax_percentage=item['tax_percentage'],
        purchase_price=item['purchase_price'],
        tax_amount=item['tax_amount'],
        total_price=item['total_price']
      )
      self.db.add(purchase_item)
   
   # Create Purchase Denominations
    for denom_value, count in denominations.items():
      purchase_denom = PurchaseDenomination(
        purchase_id=purchase.id,
        denomination_value=denom_value,
        count_returned=count
      )
      self.db.add(purchase_denom)
   
    return purchase
 
  def _update_stock(self, items: List[Dict[str, Any]]) -> None:
    """
    Decrease stock for all purchased products.
   
    Args:
      items: List of product items with product_id and quantity
    """
    for item in items:
      self.product_repo.decrease_stock(
        item['product_id'],
        item['quantity']
      )
 
  def get_bill_summary(self, purchase_id: int) -> Dict[str, Any]:
    """
    Get formatted bill summary for display.
   
    Args:
      purchase_id: Purchase ID
   
    Returns:
      Dictionary with bill details formatted for display
    """
    purchase = self.purchase_repo.get_with_details(purchase_id)
   
    if not purchase:
      return None
   
   # Format items
    items = []
    for item in purchase.items:
      items.append({
        'product_id': item.product_id,
        'product_name': item.product.name,
        'unit_price': item.unit_price,
        'quantity': item.quantity,
        'purchase_price': item.purchase_price,
        'tax_percentage': item.tax_percentage,
        'tax_amount': item.tax_amount,
        'total_price': item.total_price
      })
   
   # Format denominations
    denominations = []
    for denom in purchase.denominations:
      denominations.append({
        'value': denom.denomination_value,
        'count': denom.count_returned,
        'amount': denom.denomination_value * denom.count_returned
      })
   
    return {
      'purchase_id': purchase.id,
      'customer_email': purchase.customer_email,
      'purchase_date': purchase.purchase_date,
      'items': items,
      'total_amount': purchase.total_amount,
      'tax_amount': purchase.tax_amount,
      'net_amount': purchase.net_amount,
      'rounded_amount': purchase.rounded_amount,
      'cash_paid': purchase.cash_paid,
      'balance_returned': purchase.balance_returned,
      'denominations': denominations
    }