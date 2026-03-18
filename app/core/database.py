
"""Database Connection and Session Management"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.config import settings
from app.models.base import Base

# Import all models to ensure they are registered with Base
from app.models.product import Product
from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.models.denomination import ShopDenomination, PurchaseDenomination

# Create SQLAlchemy engine
engine = create_engine(
  settings.database_url,
  connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
  echo=settings.debug, # Log SQL statements in debug mode
  pool_pre_ping=True # Verify connections before using them
)

# Create session factory
SessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine
)


def get_db() -> Generator[Session, None, None]:
  """
  Dependency function to get database session.
 
  Yields:
    Session: SQLAlchemy database session
   
  Usage:
    @app.get("/items")
    def read_items(db: Session = Depends(get_db)):
      return db.query(Item).all()
  """
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


def init_db() -> None:
  """
  Initialize database by creating all tables.
 
  This should be called on application startup.
  Creates all tables defined in models if they don't exist.
  """
  Base.metadata.create_all(bind=engine)


def drop_db() -> None:
  """
  Drop all database tables.
 
  WARNING: This will delete all data!
  Use only for testing or database reset.
  """
  Base.metadata.drop_all(bind=engine)