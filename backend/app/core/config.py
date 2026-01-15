"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # App Info
    APP_NAME: str = "Shipway API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API Backend – Authentication / User Management / OTP Verification"
    
    # MongoDB - Support both naming conventions
    MONGO_URI: Optional[str] = None
    MONGODB_URL: Optional[str] = None
    DB_NAME: Optional[str] = None
    MONGODB_DB_NAME: Optional[str] = None
    
    # JWT - Support both naming conventions
    SECRET_KEY: Optional[str] = None
    JWT_SECRET: Optional[str] = None
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = None
    JWT_EXPIRE_MINUTES: Optional[int] = None
    
    # OTP
    OTP_EXPIRE_MINUTES: int = 5
    OTP_MAX_ATTEMPTS: int = 5
    
    # Twilio (Optional - for SMS)
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    
    # Environment
    NODE_ENV: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def get_mongodb_url(self) -> str:
        """Get MongoDB URL (support both MONGO_URI and MONGODB_URL)"""
        return self.MONGO_URI or self.MONGODB_URL or "mongodb://localhost:27017"
    
    def get_db_name(self) -> str:
        """Get database name (support both DB_NAME and MONGODB_DB_NAME)"""
        return self.DB_NAME or self.MONGODB_DB_NAME or "shipway"
    
    def get_jwt_secret(self) -> str:
        """Get JWT secret (support both SECRET_KEY and JWT_SECRET)"""
        secret = self.SECRET_KEY or self.JWT_SECRET
        if not secret:
            raise ValueError("SECRET_KEY or JWT_SECRET must be set in environment")
        return secret
    
    def get_token_expire_minutes(self) -> int:
        """Get token expiration time (support both naming conventions)"""
        return self.ACCESS_TOKEN_EXPIRE_MINUTES or self.JWT_EXPIRE_MINUTES or 1440


settings = Settings()
