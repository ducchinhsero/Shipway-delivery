"""
Custom exceptions for the application
"""
from typing import Any, Optional


class AppException(Exception):
    """
    Custom application exception
    
    Args:
        status_code: HTTP status code
        message: Error message
        detail: Additional error details
    """
    
    def __init__(
        self,
        status_code: int,
        message: str,
        detail: Optional[Any] = None
    ):
        self.status_code = status_code
        self.message = message
        self.detail = detail
        super().__init__(self.message)


class ValidationException(AppException):
    """Exception for validation errors"""
    
    def __init__(self, message: str, detail: Optional[Any] = None):
        super().__init__(status_code=400, message=message, detail=detail)


class NotFoundException(AppException):
    """Exception for not found errors"""
    
    def __init__(self, message: str = "Resource not found", detail: Optional[Any] = None):
        super().__init__(status_code=404, message=message, detail=detail)


class UnauthorizedException(AppException):
    """Exception for unauthorized access"""
    
    def __init__(self, message: str = "Unauthorized", detail: Optional[Any] = None):
        super().__init__(status_code=401, message=message, detail=detail)


class ForbiddenException(AppException):
    """Exception for forbidden access"""
    
    def __init__(self, message: str = "Forbidden", detail: Optional[Any] = None):
        super().__init__(status_code=403, message=message, detail=detail)


class ServerException(AppException):
    """Exception for internal server errors"""
    
    def __init__(self, message: str = "Internal server error", detail: Optional[Any] = None):
        super().__init__(status_code=500, message=message, detail=detail)
