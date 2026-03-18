
"""Custom Exceptions for the Billing System"""


class BillingSystemException(Exception):
  """Base exception for all billing system errors"""
  pass


class InsufficientStockError(BillingSystemException):
  """Raised when product stock is insufficient"""
  pass


class InsufficientChangeError(BillingSystemException):
  """Raised when shop cannot make exact change with available denominations"""
  pass


class ProductNotFoundError(BillingSystemException):
  """Raised when product is not found"""
  pass


class InvalidQuantityError(BillingSystemException):
  """Raised when quantity is invalid (negative or zero)"""
  pass


class InsufficientPaymentError(BillingSystemException):
  """Raised when customer payment is insufficient"""
  pass


class PurchaseNotFoundError(BillingSystemException):
  """Raised when purchase is not found"""
  pass