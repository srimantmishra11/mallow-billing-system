
"""Billing API Endpoints - Create bills and view summaries"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from app.schemas.billing import BillingRequest, BillSummaryResponse, BillItemResponse, DenominationResponse
from app.services.billing_service import BillingService
from app.api.dependencies import get_billing_service
from app.factories.email_factory import EmailFactory
from app.utils.email_templates import generate_invoice_html
from app.core.exceptions import (
	InsufficientStockError,
	ProductNotFoundError,
	InvalidQuantityError,
	InsufficientPaymentError,
	InsufficientChangeError
)

router = APIRouter()


async def send_invoice_email(customer_email: str, bill_summary: dict):
	"""
	Background task to send invoice email asynchronously.

	This runs in the background without blocking the response.
	"""
	try:
		email_sender = EmailFactory.create()
		html_content = generate_invoice_html(bill_summary)
		await email_sender.send_email(
			to_email=customer_email,
			subject=f"Invoice #{bill_summary['purchase_id']} - Bill Receipt",
			html_content=html_content
		)
	except Exception as e:
		print(f"Failed to send invoice email: {str(e)}")


@router.post("/create", response_model=BillSummaryResponse, status_code=status.HTTP_201_CREATED)
async def create_bill(
	billing_data: BillingRequest,
	background_tasks: BackgroundTasks,
	service: BillingService = Depends(get_billing_service)
):
      """
      Create a new bill.

      This endpoint:
      1. Validates products and stock
      2. Calculates prices, taxes, and denominations
      3. Creates purchase record
      4. Updates stock and denominations
      5. Sends invoice email asynchronously (background)

      Raises:
          400: Invalid input (quantity, payment, etc.)
          404: Product not found
          409: Insufficient stock or change
      """
      try:
          # Convert items to list of dicts
          items = [item.model_dump() for item in billing_data.items]

          # Create bill
          purchase = service.create_bill(
              customer_email=billing_data.customer_email,
              items=items,
              cash_paid=billing_data.cash_paid
          )

          # Get bill summary
          bill_summary = service.get_bill_summary(purchase.id)

          # Send email asynchronously in background
          background_tasks.add_task(
              send_invoice_email,
              billing_data.customer_email,
              bill_summary
          )

          # Convert to response format
          response_items = [
              BillItemResponse(**item) for item in bill_summary['items']
          ]
          response_denoms = [
              DenominationResponse(**denom) for denom in bill_summary['denominations']
          ]

          return BillSummaryResponse(
              purchase_id=bill_summary['purchase_id'],
              customer_email=bill_summary['customer_email'],
              purchase_date=bill_summary['purchase_date'],
              items=response_items,
              total_amount=bill_summary['total_amount'],
              tax_amount=bill_summary['tax_amount'],
              net_amount=bill_summary['net_amount'],
              rounded_amount=bill_summary['rounded_amount'],
              cash_paid=bill_summary['cash_paid'],
              balance_returned=bill_summary['balance_returned'],
              denominations=response_denoms
          )

      except ProductNotFoundError as e:
          raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail=str(e)
          )
      except (InvalidQuantityError, InsufficientPaymentError) as e:
          raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST,
              detail=str(e)
          )
      except (InsufficientStockError, InsufficientChangeError) as e:
          raise HTTPException(
              status_code=status.HTTP_409_CONFLICT,
              detail=str(e)
          )
      except Exception as e:
          raise HTTPException(
              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
              detail=f"Error creating bill: {str(e)}"
          )

@router.get("/{purchase_id}", response_model=BillSummaryResponse)
async def get_bill_summary(
    purchase_id: int,
    service: BillingService = Depends(get_billing_service)
):
  """Get bill summary by purchase ID"""
  bill_summary = service.get_bill_summary(purchase_id)
 
  if not bill_summary:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Purchase {purchase_id} not found"
    )
 
 # Convert to response format
  response_items = [
    BillItemResponse(**item) for item in bill_summary['items']
  ]
  response_denoms = [
    DenominationResponse(**denom) for denom in bill_summary['denominations']
  ]
 
  return BillSummaryResponse(
    purchase_id=bill_summary['purchase_id'],
    customer_email=bill_summary['customer_email'],
    purchase_date=bill_summary['purchase_date'],
    items=response_items,
    total_amount=bill_summary['total_amount'],
    tax_amount=bill_summary['tax_amount'],
    net_amount=bill_summary['net_amount'],
    rounded_amount=bill_summary['rounded_amount'],
    cash_paid=bill_summary['cash_paid'],
    balance_returned=bill_summary['balance_returned'],
    denominations=response_denoms
  )