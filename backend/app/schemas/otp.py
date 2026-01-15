"""
Pydantic schemas for OTP-related requests and responses
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime
import re


# ==================== REQUEST SCHEMAS ====================

class SendOTPRequest(BaseModel):
    """Schema for sending OTP"""
    phone: str = Field(
        ...,
        example="+84123456789",
        description="Số điện thoại nhận OTP"
    )
    purpose: Literal["register", "reset-password", "verify-phone"] = Field(
        default="register",
        example="register",
        description="Mục đích gửi OTP"
    )
    
    @field_validator('phone')
    def validate_phone(cls, v):
        if not re.match(r'^[+]?[(]?[0-9]{1,4}[)]?[-\s.]?[(]?[0-9]{1,4}[)]?[-\s.]?[0-9]{1,9}$', v):
            raise ValueError('Số điện thoại không hợp lệ')
        return v
    
    class Config:
        json_schema_extra = {
            "description": "Request gửi mã OTP đến số điện thoại"
        }


class VerifyOTPRequest(BaseModel):
    """Schema for verifying OTP"""
    phone: str = Field(
        ...,
        example="+84123456789",
        description="Số điện thoại"
    )
    otp: str = Field(
        ...,
        min_length=6,
        max_length=6,
        example="123456",
        description="Mã OTP 6 chữ số"
    )
    purpose: Literal["register", "reset-password", "verify-phone"] = Field(
        default="register",
        example="register",
        description="Mục đích xác thực OTP"
    )
    
    @field_validator('phone')
    def validate_phone(cls, v):
        if not re.match(r'^[+]?[(]?[0-9]{1,4}[)]?[-\s.]?[(]?[0-9]{1,4}[)]?[-\s.]?[0-9]{1,9}$', v):
            raise ValueError('Số điện thoại không hợp lệ')
        return v
    
    @field_validator('otp')
    def validate_otp(cls, v):
        if not v.isdigit():
            raise ValueError('OTP phải là số')
        return v
    
    class Config:
        json_schema_extra = {
            "description": "Request xác thực mã OTP"
        }


class ResetPasswordRequest(BaseModel):
    """Schema for resetting password"""
    phone: str = Field(
        ...,
        example="+84123456789",
        description="Số điện thoại"
    )
    otp: str = Field(
        ...,
        min_length=6,
        max_length=6,
        example="123456",
        description="Mã OTP đã được gửi"
    )
    new_password: str = Field(
        ...,
        min_length=6,
        example="newpass123",
        description="Mật khẩu mới (tối thiểu 6 ký tự)"
    )
    
    @field_validator('phone')
    def validate_phone(cls, v):
        if not re.match(r'^[+]?[(]?[0-9]{1,4}[)]?[-\s.]?[(]?[0-9]{1,4}[)]?[-\s.]?[0-9]{1,9}$', v):
            raise ValueError('Số điện thoại không hợp lệ')
        return v
    
    @field_validator('otp')
    def validate_otp(cls, v):
        if not v.isdigit():
            raise ValueError('OTP phải là số')
        return v
    
    class Config:
        json_schema_extra = {
            "description": "Request đặt lại mật khẩu với OTP"
        }


# ==================== RESPONSE SCHEMAS ====================

class SendOTPResponse(BaseModel):
    """Schema for send OTP response"""
    success: bool = Field(default=True, example=True)
    message: str = Field(..., example="OTP đã được gửi thành công")
    expires_at: datetime = Field(
        ...,
        example="2024-01-15T10:30:00",
        description="Thời gian hết hạn của OTP"
    )
    otp: Optional[str] = Field(
        default=None,
        example="123456",
        description="Mã OTP (chỉ hiển thị trong development mode)"
    )
    
    class Config:
        json_schema_extra = {
            "description": "Response sau khi gửi OTP thành công"
        }


class VerifyOTPResponse(BaseModel):
    """Schema for verify OTP response"""
    success: bool = Field(..., example=True)
    message: str = Field(..., example="OTP xác thực thành công")
    remaining_attempts: Optional[int] = Field(
        default=None,
        example=3,
        description="Số lần thử còn lại (nếu OTP sai)"
    )
    
    class Config:
        json_schema_extra = {
            "description": "Response sau khi xác thực OTP"
        }


class ResetPasswordResponse(BaseModel):
    """Schema for reset password response"""
    success: bool = Field(default=True, example=True)
    message: str = Field(..., example="Đặt lại mật khẩu thành công")
    
    class Config:
        json_schema_extra = {
            "description": "Response sau khi đặt lại mật khẩu thành công"
        }
