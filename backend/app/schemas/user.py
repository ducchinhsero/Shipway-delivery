"""
Pydantic schemas for User-related requests and responses
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime
import re


# ==================== REQUEST SCHEMAS ====================

class UserRegisterRequest(BaseModel):
    """Schema for user registration"""
    phone: str = Field(
        ...,
        example="+84123456789",
        description="Số điện thoại của người dùng"
    )
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        example="Nguyễn Văn A",
        description="Tên đầy đủ của người dùng"
    )
    password: str = Field(
        ...,
        min_length=6,
        example="123456",
        description="Mật khẩu (tối thiểu 6 ký tự)"
    )
    otp: str = Field(
        ...,
        example="123456",
        description="Mã OTP đã được gửi đến số điện thoại"
    )
    role: Optional[Literal["user", "driver", "admin"]] = Field(
        default="user",
        example="user",
        description="Vai trò của người dùng"
    )
    email: Optional[str] = Field(
        default=None,
        example="user@example.com",
        description="Email (tùy chọn)"
    )
    
    @field_validator('phone')
    def validate_phone(cls, v):
        if not re.match(r'^[+]?[(]?[0-9]{1,4}[)]?[-\s.]?[(]?[0-9]{1,4}[)]?[-\s.]?[0-9]{1,9}$', v):
            raise ValueError('Số điện thoại không hợp lệ')
        return v
    
    @field_validator('email')
    def validate_email(cls, v):
        if v and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', v):
            raise ValueError('Email không hợp lệ')
        return v

    class Config:
        json_schema_extra = {
            "description": "Dữ liệu đăng ký tài khoản mới"
        }


class UserLoginRequest(BaseModel):
    """Schema for user login"""
    phone: str = Field(
        ...,
        example="+84123456789",
        description="Số điện thoại"
    )
    password: str = Field(
        ...,
        example="123456",
        description="Mật khẩu"
    )
    
    class Config:
        json_schema_extra = {
            "description": "Dữ liệu đăng nhập"
        }


class UserUpdateRequest(BaseModel):
    """Schema for updating user profile"""
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
        example="Nguyễn Văn B",
        description="Tên mới"
    )
    email: Optional[str] = Field(
        default=None,
        example="newemail@example.com",
        description="Email mới"
    )
    avatar: Optional[str] = Field(
        default=None,
        example="https://example.com/avatar.jpg",
        description="URL avatar"
    )
    
    @field_validator('email')
    def validate_email(cls, v):
        if v and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', v):
            raise ValueError('Email không hợp lệ')
        return v


# ==================== RESPONSE SCHEMAS ====================

class DriverInfo(BaseModel):
    """Driver-specific information"""
    license_number: Optional[str] = None
    vehicle_type: Optional[Literal["motorbike", "car", "truck", "van"]] = None
    vehicle_plate: Optional[str] = None
    is_verified: bool = False
    rating: float = 0.0
    total_trips: int = 0


class CompanyInfo(BaseModel):
    """Company-specific information"""
    company_name: Optional[str] = None
    tax_code: Optional[str] = None
    address: Optional[str] = None


class WalletInfo(BaseModel):
    """User wallet balance information"""
    balance: int = 0
    total_topup: int = 0
    total_usage: int = 0


class UserResponse(BaseModel):
    """Schema for user response"""
    id: str = Field(..., alias="_id", example="507f1f77bcf86cd799439011")
    phone: str = Field(..., example="+84123456789")
    name: str = Field(..., example="Nguyễn Văn A")
    role: str = Field(..., example="user")
    email: Optional[str] = None
    is_active: bool = True
    is_phone_verified: bool = False
    avatar: Optional[str] = None
    driver_info: Optional[DriverInfo] = None
    company_info: Optional[CompanyInfo] = None
    wallet_info: Optional[WalletInfo] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "description": "Thông tin người dùng"
        }


class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    success: bool = Field(default=True, example=True)
    message: str = Field(..., example="Đăng nhập thành công")
    token: str = Field(
        ...,
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTA3ZjFmNzdiY2Y4NmNkNzk5NDM5MDExIiwicm9sZSI6InVzZXIiLCJleHAiOjE3MDQ5NjcyMDB9.abc123",
        description="JWT token để xác thực các request sau này"
    )
    user: UserResponse
    
    class Config:
        json_schema_extra = {
            "description": "Response chứa JWT token và thông tin user"
        }


class UserProfileResponse(BaseModel):
    """Schema for user profile response"""
    success: bool = Field(default=True, example=True)
    user: UserResponse
    
    class Config:
        json_schema_extra = {
            "description": "Thông tin profile người dùng"
        }


class UpdateProfileResponse(BaseModel):
    """Schema for update profile response"""
    success: bool = Field(default=True, example=True)
    message: str = Field(..., example="Cập nhật thông tin thành công")
    user: UserResponse
    
    class Config:
        json_schema_extra = {
            "description": "Response sau khi cập nhật profile"
        }
