

"""Email Factory - Factory Pattern for creating email senders"""
from enum import Enum
from app.services.email_service import EmailSender, SMTPEmailSender, ConsoleEmailSender
from app.config import settings


class EmailProvider(Enum):
  """Enumeration of supported email providers"""
  SMTP = "smtp"
  CONSOLE = "console"
 # Future: SENDGRID = "sendgrid", AWS_SES = "aws_ses", etc.


class EmailFactory:
  """
  Factory for creating email sender instances.
 
  Design Pattern: Factory Pattern
  Benefits:
  - Centralized object creation
  - Easy to add new email providers
  - Configuration-driven selection
  - Testable (use console sender in tests)
 
  Example:
    sender = EmailFactory.create() # Uses config
    await sender.send_email(to, subject, html)
  """
 
  _providers = {
    EmailProvider.SMTP: SMTPEmailSender,
    EmailProvider.CONSOLE: ConsoleEmailSender,
  }
 
  @classmethod
  def create(cls, provider: EmailProvider = None) -> EmailSender:
    """
    Create email sender based on provider.
   
    Args:
      provider: Email provider enum. If None, uses settings.
   
    Returns:
      EmailSender instance
   
    Raises:
      ValueError: If provider is unknown
    """
    if provider is None:
     # Get from settings
      provider_str = settings.email_provider.lower()
      try:
        provider = EmailProvider(provider_str)
      except ValueError:
        raise ValueError(f"Unknown email provider in settings: {provider_str}")
   
    sender_class = cls._providers.get(provider)
    if not sender_class:
      raise ValueError(f"Unknown email provider: {provider}")
   
    return sender_class()
 
  @classmethod
  def register_provider(cls, provider: EmailProvider, sender_class: type) -> None:
    """
    Register a new email provider.
   
    Allows extending the factory without modifying its code.
   
    Args:
      provider: Provider enum value
      sender_class: Email sender class
    """
    cls._providers[provider] = sender_class