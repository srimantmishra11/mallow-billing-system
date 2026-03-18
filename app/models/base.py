
"""Base Model and Mixins"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TimestampMixin:
  """Mixin to add created_at and updated_at timestamps to models"""
 
  created_at = Column(
    DateTime,
    default=datetime.utcnow,
    nullable=False,
    comment="Record creation timestamp"
  )
  updated_at = Column(
    DateTime,
    default=datetime.utcnow,
    onupdate=datetime.utcnow,
    nullable=False,
    comment="Record last update timestamp"
  )