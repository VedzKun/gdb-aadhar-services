"""
Aadhar Service - Configuration Settings

Environment-based configuration using pydantic-settings.

Author: GDB Architecture Team
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Aadhar Service Configuration
    """
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Service Configuration
    SERVICE_NAME: str = "GDB-Aadhar-Service"
    TITLE: str = "GDB Aadhar Verification Service"
    DESCRIPTION: str = "Third-party Simulation API for validating Aadhar numbers"
    PORT: int = 8005
    HOST: str = "0.0.0.0"
    
    # Inter-Service URLs (StandardizedPlural and LegacySingular)
    ACCOUNTS_SERVICE_URL: str = "http://localhost:8001"
    ACCOUNT_SERVICE_URL: str = "http://localhost:8001"
    
    TRANSACTIONS_SERVICE_URL: str = "http://localhost:8002"
    TRANSACTION_SERVICE_URL: str = "http://localhost:8002"
    
    USERS_SERVICE_URL: str = "http://localhost:8003"
    USER_SERVICE_URL: str = "http://localhost:8003"
    
    AUTH_SERVICE_URL: str = "http://localhost:8004"
    AADHAR_SERVICE_URL: str = "http://localhost:8005"
    COMPANY_SERVICE_URL: str = "http://localhost:8006"
    NOTIFICATION_SERVICE_URL: str = "http://localhost:8007"
    PAYMENT_GATEWAY_SERVICE_URL: str = "http://localhost:8008"

    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    CORS_ALLOWED_ORIGINS: list = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )


# Global settings instance
settings = Settings()

# Schema configuration for multi-tenant database
SCHEMA_NAME = "aadhar_service"

# Update search_path for PostgreSQL
async def set_schema_search_path(connection):
    """Set the search path to use the correct schema."""
    await connection.execute(f"SET search_path TO aadhar_service, public")
