"""FastAPI Main Application - Entry point for the billing system"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.api import products, billing, purchases
from app.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="A production-ready billing system with FastAPI, SQLAlchemy, and design patterns",
    version="1.0.0",
    debug=settings.debug
)

# CORS middleware (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Include API routers
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(billing.router, prefix="/api/billing", tags=["Billing"])
app.include_router(purchases.router, prefix="/api/purchases", tags=["Purchases"])


@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    print("Starting Billing System...")
    init_db()
    print("Database initialized")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Home page"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Billing System"}
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": "1.0.0"
    }


@app.get("/products", response_class=HTMLResponse)
async def products_page(request: Request):
    """Products management page"""
    return templates.TemplateResponse(
        "products/list.html",
        {"request": request, "title": "Products"}
    )


@app.get("/billing", response_class=HTMLResponse)
async def billing_page(request: Request):
    """Billing page"""
    return templates.TemplateResponse(
        "billing/create_bill.html",
        {"request": request, "title": "Create Bill"}
    )


@app.get("/billing/summary/{purchase_id}", response_class=HTMLResponse)
async def bill_summary_page(request: Request, purchase_id: int):
    """Bill summary page"""
    return templates.TemplateResponse(
        "billing/bill_summary.html",
        {
            "request": request,
            "title": f"Bill Summary #{purchase_id}",
            "purchase_id": purchase_id
        }
    )


@app.get("/purchases", response_class=HTMLResponse)
async def purchases_page(request: Request):
    """Purchase history page"""
    return templates.TemplateResponse(
        "purchases/history.html",
        {"request": request, "title": "Purchase History"}
    )


@app.get("/purchases/{purchase_id}", response_class=HTMLResponse)
async def purchase_detail_page(request: Request, purchase_id: int):
    """Purchase detail page"""
    return templates.TemplateResponse(
        "purchases/detail.html",
        {
            "request": request,
            "title": f"Purchase #{purchase_id}",
            "purchase_id": purchase_id
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )