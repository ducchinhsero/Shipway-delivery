"""
OTP Service - Generate and send OTP via SMS
"""
import random
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from twilio.rest import Client as TwilioClient
from app.core.config import settings
from app.db import models


# Initialize Twilio client if configured
twilio_client: Optional[TwilioClient] = None
if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
    twilio_client = TwilioClient(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN
    )


def generate_otp() -> str:
    """
    Generate 6-digit OTP
    
    Returns:
        6-digit OTP string
    """
    return str(random.randint(100000, 999999))


async def send_sms(phone: str, otp: str) -> Dict[str, Any]:
    """
    Send OTP via SMS using Twilio
    
    Args:
        phone: Phone number
        otp: OTP code
        
    Returns:
        Result dictionary
    """
    if not twilio_client:
        print(f"[WARN] Twilio not configured. OTP for {phone}: {otp}")
        return {
            "success": True,
            "message": "OTP sent (mock)",
            "otp": otp if settings.NODE_ENV == "development" else None
        }
    
    try:
        message = twilio_client.messages.create(
            body=f"Mã OTP của bạn là: {otp}. Mã này có hiệu lực trong {settings.OTP_EXPIRE_MINUTES} phút.",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone
        )
        
        print(f"[OK] SMS sent to {phone}: {message.sid}")
        return {"success": True, "message": "OTP sent successfully"}
        
    except Exception as e:
        print(f"[ERROR] Error sending SMS: {str(e)}")
        raise Exception("Failed to send OTP via SMS")


async def create_and_send_otp(
    db: AsyncIOMotorDatabase,
    phone: str,
    purpose: str
) -> Dict[str, Any]:
    """
    Create and send OTP to phone number
    
    Args:
        db: Database instance
        phone: Phone number
        purpose: OTP purpose (register, reset-password, verify-phone)
        
    Returns:
        Result dictionary with success status and expiration time
    """
    # Generate OTP
    otp_code = generate_otp()
    
    # Calculate expiration time
    expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
    
    # Save OTP to database
    otp_data = {
        "phone": phone,
        "otp": otp_code,
        "purpose": purpose,
        "expires_at": expires_at
    }
    
    otp = await models.create_otp(db, otp_data)
    
    # Send OTP via SMS
    sms_result = await send_sms(phone, otp_code)
    
    print(f"[OTP] OTP created for {phone} ({purpose}): {otp_code}")
    
    result = {
        "success": True,
        "message": "OTP đã được gửi thành công",
        "expires_at": expires_at
    }
    
    # Include OTP in development mode for testing
    if settings.NODE_ENV == "development":
        result["otp"] = otp_code
    
    return result


async def verify_otp_code(
    db: AsyncIOMotorDatabase,
    phone: str,
    otp_code: str,
    purpose: str
) -> Dict[str, Any]:
    """
    Verify OTP code
    
    Args:
        db: Database instance
        phone: Phone number
        otp_code: OTP code to verify
        purpose: OTP purpose
        
    Returns:
        Result dictionary with verification status
    """
    # Find latest OTP
    otp = await models.find_latest_otp(db, phone, purpose)
    
    if not otp:
        return {
            "success": False,
            "message": "OTP không tồn tại hoặc đã được sử dụng"
        }
    
    # Check if expired
    if datetime.utcnow() > otp['expires_at']:
        await db.otps.delete_one({"_id": otp['_id']})
        return {
            "success": False,
            "message": "OTP đã hết hạn"
        }
    
    # Check attempts
    if otp['attempts'] >= settings.OTP_MAX_ATTEMPTS:
        await db.otps.delete_one({"_id": otp['_id']})
        return {
            "success": False,
            "message": "Đã vượt quá số lần thử. Vui lòng gửi lại OTP mới"
        }
    
    # Verify OTP
    if otp['otp'] != otp_code:
        # Increment attempts
        new_attempts = await models.increment_otp_attempts(db, otp['_id'])
        remaining = settings.OTP_MAX_ATTEMPTS - new_attempts
        
        return {
            "success": False,
            "message": f"OTP không đúng. Còn {remaining} lần thử",
            "remaining_attempts": remaining
        }
    
    # Mark as used
    await models.mark_otp_as_used(db, otp['_id'])
    
    print(f"[OK] OTP verified for {phone}")
    
    return {
        "success": True,
        "message": "OTP xác thực thành công"
    }
