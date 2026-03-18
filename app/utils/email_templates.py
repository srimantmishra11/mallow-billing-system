
"""Email Templates - HTML templates for emails"""
from typing import Dict, Any
from datetime import datetime


def generate_invoice_html(bill_summary: Dict[str, Any]) -> str:
  """
  Generate HTML invoice email content.
 
  Args:
    bill_summary: Bill summary dictionary from BillingService
 
  Returns:
    HTML string for email
  """
  items_html = ""
  for item in bill_summary['items']:
    items_html += f"""
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd;">{item['product_id']}</td>
      <td style="padding: 10px; border: 1px solid #ddd; text-align: right;">₹{item['unit_price']:.2f}</td>
      <td style="padding: 10px; border: 1px solid #ddd; text-align: center;">{item['quantity']}</td>
      <td style="padding: 10px; border: 1px solid #ddd; text-align: right;">₹{item['purchase_price']:.2f}</td>
      <td style="padding: 10px; border: 1px solid #ddd; text-align: right;">{item['tax_percentage']:.1f}%</td>
      <td style="padding: 10px; border: 1px solid #ddd; text-align: right;">₹{item['tax_amount']:.2f}</td>
      <td style="padding: 10px; border: 1px solid #ddd; text-align: right;"><strong>₹{item['total_price']:.2f}</strong></td>
    </tr>
    """
 
  denominations_html = ""
  if bill_summary['denominations']:
    for denom in bill_summary['denominations']:
      denominations_html += f"""
      <tr>
        <td style="padding: 8px; border: 1px solid #ddd;">₹{denom['value']}</td>
        <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">{denom['count']}</td>
        <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">₹{denom['amount']}</td>
      </tr>
      """
  else:
    denominations_html = "<tr><td colspan='3' style='padding: 10px; text-align: center;'>No change returned</td></tr>"
 
  html = f"""
  <!DOCTYPE html>
  <html>
  <head>
    <meta charset="UTF-8">
    <title>Invoice #{bill_summary['purchase_id']}</title>
  </head>
  <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
    <div style="background-color: #4CAF50; color: white; padding: 20px; text-align: center;">
      <h1>Invoice / Bill Receipt</h1>
      <p>Invoice #: {bill_summary['purchase_id']}</p>
      <p>Date: {bill_summary['purchase_date'].strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
   
    <div style="padding: 20px; background-color: #f9f9f9; margin-top: 20px;">
      <h2>Customer Details</h2>
      <p><strong>Email:</strong> {bill_summary['customer_email']}</p>
    </div>
   
    <div style="padding: 20px; margin-top: 20px;">
      <h2>Purchase Details</h2>
      <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
        <thead>
          <tr style="background-color: #4CAF50; color: white;">
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">Product ID</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: right;">Unit Price</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: center;">Qty</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: right;">Purchase Price</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: right;">Tax %</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: right;">Tax Amount</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: right;">Total</th>
          </tr>
        </thead>
        <tbody>
          {items_html}
        </tbody>
      </table>
    </div>
   
    <div style="padding: 20px; margin-top: 20px; background-color: #e8f4f8;">
      <h2>Bill Summary</h2>
      <table style="width: 100%; font-size: 16px;">
        <tr>
          <td style="padding: 8px;"><strong>Total Price Without Tax:</strong></td>
          <td style="padding: 8px; text-align: right;">₹{bill_summary['total_amount']:.2f}</td>
        </tr>
        <tr>
          <td style="padding: 8px;"><strong>Total Tax Payable:</strong></td>
          <td style="padding: 8px; text-align: right;">₹{bill_summary['tax_amount']:.2f}</td>
        </tr>
        <tr>
          <td style="padding: 8px;"><strong>Net Price:</strong></td>
          <td style="padding: 8px; text-align: right;">₹{bill_summary['net_amount']:.2f}</td>
        </tr>
        <tr style="background-color: #ffd700;">
          <td style="padding: 12px;"><strong>Rounded Net Price (Bill Amount):</strong></td>
          <td style="padding: 12px; text-align: right; font-size: 20px;"><strong>₹{bill_summary['rounded_amount']}</strong></td>
        </tr>
        <tr>
          <td style="padding: 8px;"><strong>Cash Paid by Customer:</strong></td>
          <td style="padding: 8px; text-align: right;">₹{bill_summary['cash_paid']:.2f}</td>
        </tr>
        <tr style="background-color: #90EE90;">
          <td style="padding: 12px;"><strong>Balance Returned:</strong></td>
          <td style="padding: 12px; text-align: right; font-size: 18px;"><strong>₹{bill_summary['balance_returned']:.2f}</strong></td>
        </tr>
      </table>
    </div>
   
    <div style="padding: 20px; margin-top: 20px;">
      <h2>Change Denomination Breakdown</h2>
      <table style="width: 50%; border-collapse: collapse; margin-top: 10px;">
        <thead>
          <tr style="background-color: #FF9800; color: white;">
            <th style="padding: 10px; border: 1px solid #ddd;">Denomination</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Count</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Amount</th>
          </tr>
        </thead>
        <tbody>
          {denominations_html}
        </tbody>
      </table>
    </div>
   
    <div style="padding: 20px; margin-top: 30px; text-align: center; background-color: #f0f0f0;">
      <p><strong>Thank you for your purchase!</strong></p>
      <p style="font-size: 12px; color: #666;">This is an automatically generated invoice.</p>
    </div>
  </body>
  </html>
  """
  return html