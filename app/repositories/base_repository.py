
"""Base Repository implementing Generic CRUD operations"""
from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
  """
  Generic Repository Pattern implementation.
 
  Provides common CRUD operations for any SQLAlchemy model.
  Benefits:
  - Single Responsibility: Data access logic in one place
  - DRY Principle: Reusable across all entities
  - Testability: Easy to mock in unit tests
  - Type Safety: Generic type hints
 
  Type Parameters:
    ModelType: The SQLAlchemy model class
  """
 
  def __init__(self, model: Type[ModelType], db: Session):
    """
    Initialize repository with model and database session.
   
    Args:
      model: SQLAlchemy model class
      db: Database session
    """
    self.model = model
    self.db = db
 
  def get_by_id(self, id: int) -> Optional[ModelType]:
    """
    Get a single record by primary key.
   
    Args:
      id: Primary key value
     
    Returns:
      Model instance or None if not found
    """
    return self.db.query(self.model).filter(self.model.id == id).first()
 
  def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
    """
    Get all records with pagination.
   
    Args:
      skip: Number of records to skip (offset)
      limit: Maximum number of records to return
     
    Returns:
      List of model instances
    """
    return self.db.query(self.model).offset(skip).limit(limit).all()
 
  def create(self, **kwargs) -> ModelType:
    """
    Create a new record.
   
    Args:
      **kwargs: Model field values
     
    Returns:
      Created model instance with populated ID
    """
    db_obj = self.model(**kwargs)
    self.db.add(db_obj)
    self.db.commit()
    self.db.refresh(db_obj)
    return db_obj
 
  def update(self, id: int, **kwargs) -> Optional[ModelType]:
    """
    Update an existing record.
   
    Args:
      id: Primary key of record to update
      **kwargs: Fields to update
     
    Returns:
      Updated model instance or None if not found
    """
    db_obj = self.get_by_id(id)
    if db_obj:
      for key, value in kwargs.items():
        if hasattr(db_obj, key):
          setattr(db_obj, key, value)
      self.db.commit()
      self.db.refresh(db_obj)
    return db_obj
 
  def delete(self, id: int) -> bool:
    """
    Delete a record.
   
    Args:
      id: Primary key of record to delete
     
    Returns:
      True if deleted, False if not found
    """
    db_obj = self.get_by_id(id)
    if db_obj:
      self.db.delete(db_obj)
      self.db.commit()
      return True
    return False
 
  def count(self) -> int:
    """
    Count total records.
   
    Returns:
      Total number of records
    """
    return self.db.query(self.model).count()
 
  def exists(self, id: int) -> bool:
    """
    Check if a record exists.
   
    Args:
      id: Primary key to check
     
    Returns:
      True if exists, False otherwise
    """
    return self.db.query(self.model).filter(self.model.id == id).first() is not None