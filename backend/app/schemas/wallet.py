"""
Wallet and Transaction Schemas
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


# ==================== TRANSACTION SCHEMAS ====================

class TransactionBase(BaseModel):
    """Base transaction schema"""
    amount: int = Field(..., gt=0, description="Transaction amount in VND")
    type: str = Field(..., description="Transaction type: topup, usage, refund")
    description: Optional[str] = Field(None, description="Transaction description")
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        allowed_types = ['topup', 'usage', 'refund']
        if v not in allowed_types:
            raise ValueError(f"Type must be one of: {', '.join(allowed_types)}")
        return v


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction"""
    payment_method: Optional[str] = Field(None, description="Payment method: qr, bank_transfer, momo, vnpay")


class TransactionResponse(TransactionBase):
    """Schema for transaction response"""
    id: str = Field(..., alias="_id")
    user_id: str
    status: str = Field(..., description="Transaction status: pending, completed, failed, cancelled")
    payment_id: Optional[str] = None
    payment_method: Optional[str] = None
    payment_details: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TransactionListResponse(BaseModel):
    """Schema for transaction list response"""
    success: bool = True
    total: int
    transactions: List[TransactionResponse]


# ==================== WALLET SCHEMAS ====================

class WalletInfo(BaseModel):
    """Schema for wallet information"""
    user_id: str
    balance: int = Field(..., description="Current balance in VND")
    total_topup: int = Field(..., description="Total amount topped up")
    total_usage: int = Field(..., description="Total amount used")
    pending_transactions: int = Field(..., description="Number of pending transactions")
    recent_transactions: List[TransactionResponse] = Field(default_factory=list)


class WalletResponse(BaseModel):
    """Schema for wallet response"""
    success: bool = True
    wallet: WalletInfo


# ==================== TOP-UP SCHEMAS ====================

class TopUpRequest(BaseModel):
    """Schema for top-up request"""
    amount: int = Field(..., gt=0, le=100000000, description="Amount to top up (VND). Max: 100,000,000")
    payment_method: str = Field(..., description="Payment method: qr, bank_transfer, momo, vnpay")
    
    @field_validator('payment_method')
    @classmethod
    def validate_payment_method(cls, v):
        allowed_methods = ['qr', 'bank_transfer', 'momo', 'vnpay']
        if v not in allowed_methods:
            raise ValueError(f"Payment method must be one of: {', '.join(allowed_methods)}")
        return v
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        # Amount must be multiple of 10,000
        if v % 10000 != 0:
            raise ValueError("Amount must be multiple of 10,000 VND")
        
        # Minimum 10,000 VND
        if v < 10000:
            raise ValueError("Minimum top-up amount is 10,000 VND")
        
        return v


class TopUpResponse(BaseModel):
    """Schema for top-up response"""
    success: bool = True
    message: str = "Top-up request created successfully"
    transaction_id: str
    payment_id: str
    amount: int
    payment_method: str
    qr_code: Optional[str] = None  # Base64 encoded QR code image or URL
    payment_url: Optional[str] = None  # Payment gateway URL
    bank_info: Optional[dict] = None  # Bank transfer information
    expires_at: datetime  # Payment expiration time


class PaymentVerificationRequest(BaseModel):
    """Schema for payment verification (webhook)"""
    payment_id: str
    status: str  # success, failed
    transaction_code: Optional[str] = None
    payment_time: Optional[datetime] = None
    signature: Optional[str] = None  # Security signature from payment gateway


class PaymentVerificationResponse(BaseModel):
    """Schema for payment verification response"""
    success: bool
    message: str
    transaction_id: Optional[str] = None
    new_balance: Optional[int] = None


# ==================== STATISTICS SCHEMAS ====================

class WalletStatistics(BaseModel):
    """Schema for wallet statistics"""
    total_topup: int
    total_usage: int
    current_balance: int
    total_transactions: int
    successful_transactions: int
    pending_transactions: int
    failed_transactions: int
    this_month_topup: int
    this_month_usage: int
