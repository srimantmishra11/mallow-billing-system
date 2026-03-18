
"""Email Service - Abstract email sender and implementations"""
from abc import ABC, abstractmethod
from typing import Optional
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings


class EmailSender(ABC):
  """
  Abstract base class for email senders.
 
  Implements Factory Pattern - allows different email providers
  to be used interchangeably.
  """
 
  @abstractmethod
  async def send_email(
    self,
    to_email: str,
    subject: str,
    html_content: str
  ) -> bool:
    """
    Send email.
   
    Args:
      to_email: Recipient email address
      subject: Email subject
      html_content: HTML body of email
   
    Returns:
      True if sent successfully, False otherwise
    """
    pass


class SMTPEmailSender(EmailSender):
  """
  SMTP email sender implementation.
 
  Uses aiosmtplib for async SMTP email sending.
  """
 
  async def send_email(
    self,
    to_email: str,
    subject: str,
    html_content: str
  ) -> bool:
    """Send email via SMTP"""
    try:
     # Create message
      message = MIMEMultipart("alternative")
      message["Subject"] = subject
      message["From"] = settings.smtp_from_email
      message["To"] = to_email
     
     # Add HTML content
      html_part = MIMEText(html_content, "html")
      message.attach(html_part)
     
     # Send via SMTP
      await aiosmtplib.send(
        message,
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_username,
        password=settings.smtp_password,
        use_tls=True
      )
     
      print(f"Email sent successfully to {to_email}")
      return True
     
    except Exception as e:
      print(f"Failed to send email to {to_email}: {str(e)}")
      return False


class ConsoleEmailSender(EmailSender):
  """
  Console email sender implementation for development.
 
  Prints email content to console instead of actually sending.
  """
 
  async def send_email(
    self,
    to_email: str,
    subject: str,
    html_content: str
  ) -> bool:
    """Print email to console"""
    print("=" * 80)
    print(" EMAIL (CONSOLE MODE - Development)")
    print("=" * 80)
    print(f"To: {to_email}")
    print(f"Subject: {subject}")
    print("-" * 80)
    print(html_content)
    print("=" * 80)
    return True