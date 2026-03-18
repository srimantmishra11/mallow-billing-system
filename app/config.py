
"""Application Configuration using Pydantic Settings"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
	"""Application settings loaded from environment variables"""

	# Application
	app_name: str = "Billing System"
	debug: bool = True
	secret_key: str = "dev-secret-key"

	# Database
	database_url: str = "sqlite:///./billing.db"

	# Email Configuration
	email_provider: str = "console"
	smtp_host: str = "smtp.gmail.com"
	smtp_port: int = 587
	smtp_username: str = ""
	smtp_password: str = ""
	smtp_from_email: str = "billing@example.com"

	# Currency Denominations
	denominations: str = "500,50,20,10,5,2,1"

	@property
	def denomination_list(self) -> List[int]:
		"""Parse denominations from comma-separated string"""
		return [int(x.strip()) for x in self.denominations.split(",")]

	class Config:
		env_file = ".env"
		case_sensitive = False


# Global settings instance
settings = Settings()