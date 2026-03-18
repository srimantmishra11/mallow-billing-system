
"""View Database Contents - Inspect all tables and data"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.database import SessionLocal, engine
from app.models.product import Product
from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.models.denomination import ShopDenomination, PurchaseDenomination
from sqlalchemy import inspect


def print_separator(title=""):
  """Print a formatted separator"""
  if title:
    print(f"\n{'='*80}")
    print(f" {title}")
    print('='*80)
  else:
    print('-'*80)


def view_all_tables():
  """Display all database tables"""
  inspector = inspect(engine)
  tables = inspector.get_table_names()
 
  print_separator("DATABASE STRUCTURE")
  print(f"Database: billing_system.db")
  print(f"Total Tables: {len(tables)}")
  print(f"\nTables:")
  for i, table in enumerate(tables, 1):
    print(f" {i}. {table}")


def view_products():
  """Display all products"""
  db = SessionLocal()
  try:
    products = db.query(Product).all()
   
    print_separator(f"PRODUCTS TABLE ({len(products)} records)")
    if products:
      print(f"{'ID':<5} {'Product ID':<12} {'Name':<30} {'Price':<10} {'Tax%':<6} {'Stock':<6}")
      print_separator()
      for p in products:
        print(f"{p.id:<5} {p.product_id:<12} {p.name:<30} ₹{p.price:<9.2f} {p.tax_percentage:<6.1f} {p.available_stock:<6}")
    else:
      print("No products found.")
  finally:
    db.close()


def view_shop_denominations():
  """Display shop denominations"""
  db = SessionLocal()
  try:
    denoms = db.query(ShopDenomination).order_by(ShopDenomination.denomination_value.desc()).all()
   
    print_separator(f"SHOP DENOMINATIONS ({len(denoms)} records)")
    if denoms:
      print(f"{'ID':<5} {'Value':<10} {'Available Count':<15} {'Total Amount':<15}")
      print_separator()
      total_cash = 0
      for d in denoms:
        amount = d.denomination_value * d.available_count
        total_cash += amount
        print(f"{d.id:<5} ₹{d.denomination_value:<9} {d.available_count:<15} ₹{amount:<14}")
      print_separator()
      print(f"Total Cash Available: ₹{total_cash}")
    else:
      print("No denominations found.")
  finally:
    db.close()


def view_purchases():
  """Display all purchases"""
  db = SessionLocal()
  try:
    purchases = db.query(Purchase).order_by(Purchase.id.desc()).all()
   
    print_separator(f"PURCHASES TABLE ({len(purchases)} records)")
    if purchases:
      print(f"{'ID':<5} {'Email':<30} {'Date':<20} {'Total':<12} {'Paid':<12} {'Change':<12}")
      print_separator()
      for p in purchases:
        date_str = p.purchase_date.strftime('%Y-%m-%d %H:%M:%S')
        print(f"{p.id:<5} {p.customer_email:<30} {date_str:<20} ₹{p.rounded_amount:<11.2f} ₹{p.cash_paid:<11.2f} ₹{p.balance_returned:<11.2f}")
    else:
      print("No purchases found.")
  finally:
    db.close()


def view_purchase_items():
  """Display all purchase items"""
  db = SessionLocal()
  try:
    items = db.query(PurchaseItem).all()
   
    print_separator(f"PURCHASE ITEMS TABLE ({len(items)} records)")
    if items:
      print(f"{'ID':<5} {'Purchase ID':<12} {'Product ID':<12} {'Qty':<5} {'Unit Price':<12} {'Total':<12}")
      print_separator()
      for item in items:
        print(f"{item.id:<5} {item.purchase_id:<12} {item.product_id:<12} {item.quantity:<5} ₹{item.unit_price:<11.2f} ₹{item.total_price:<11.2f}")
    else:
      print("No purchase items found.")
  finally:
    db.close()


def view_purchase_denominations():
  """Display purchase denominations"""
  db = SessionLocal()
  try:
    denoms = db.query(PurchaseDenomination).all()
   
    print_separator(f"PURCHASE DENOMINATIONS TABLE ({len(denoms)} records)")
    if denoms:
      print(f"{'ID':<5} {'Purchase ID':<12} {'Value':<10} {'Count':<10} {'Amount':<12}")
      print_separator()
      for d in denoms:
        amount = d.denomination_value * d.count_returned
        print(f"{d.id:<5} {d.purchase_id:<12} ₹{d.denomination_value:<9} {d.count_returned:<10} ₹{amount:<11}")
    else:
      print("No purchase denominations found.")
  finally:
    db.close()


def view_purchase_details(purchase_id: int):
  """Display detailed view of a specific purchase"""
  db = SessionLocal()
  try:
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
   
    if not purchase:
      print(f"\nPurchase #{purchase_id} not found!")
      return
   
    print_separator(f"PURCHASE DETAILS - #{purchase_id}")
    print(f"Customer Email: {purchase.customer_email}")
    print(f"Purchase Date: {purchase.purchase_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"")
    print(f"Subtotal:    ₹{purchase.total_amount:.2f}")
    print(f"Tax Amount:   ₹{purchase.tax_amount:.2f}")
    print(f"Net Amount:   ₹{purchase.net_amount:.2f}")
    print(f"Rounded Total: ₹{purchase.rounded_amount:.2f}")
    print(f"Cash Paid:   ₹{purchase.cash_paid:.2f}")
    print(f"Change:     ₹{purchase.balance_returned:.2f}")
   
   # Items
    print(f"\nItems:")
    print_separator()
    print(f"{'Product ID':<12} {'Product Name':<30} {'Qty':<5} {'Unit Price':<12} {'Tax%':<7} {'Total':<12}")
    print_separator()
    for item in purchase.items:
      print(f"{item.product_id:<12} {item.product.name:<30} {item.quantity:<5} ₹{item.unit_price:<11.2f} {item.tax_percentage:<6.1f}% ₹{item.total_price:<11.2f}")
   
   # Denominations
    if purchase.denominations:
      print(f"\nChange Breakdown:")
      print_separator()
      print(f"{'Denomination':<15} {'Count':<10} {'Amount':<12}")
      print_separator()
      for denom in purchase.denominations:
        amount = denom.denomination_value * denom.count_returned
        print(f"₹{denom.denomination_value:<14} {denom.count_returned:<10} ₹{amount:<11}")
   
  finally:
    db.close()


def main():
  """Main function"""
  print("\n" + "="*80)
  print(" BILLING SYSTEM - DATABASE VIEWER")
  print("="*80)
 
 # View all tables structure
  view_all_tables()
 
 # View all data
  view_products()
  view_shop_denominations()
  view_purchases()
  view_purchase_items()
  view_purchase_denominations()
 
 # If there are purchases, show details of the most recent one
  db = SessionLocal()
  try:
    latest_purchase = db.query(Purchase).order_by(Purchase.id.desc()).first()
    if latest_purchase:
      print("\n")
      view_purchase_details(latest_purchase.id)
  finally:
    db.close()
 
  print("\n" + "="*80)
  print(" END OF DATABASE CONTENTS")
  print("="*80 + "\n")


if __name__ == "__main__":
  main()